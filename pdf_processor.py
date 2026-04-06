"""
PDF processing: decrypt and move operations using pikepdf.
"""

import os
import shutil
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum

try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except ImportError:
    PIKEPDF_AVAILABLE = False


class ProcessStatus(Enum):
    SUCCESS = "success"
    NOT_ENCRYPTED = "not_encrypted"
    WRONG_PASSWORD = "wrong_password"
    ERROR = "error"


@dataclass
class ProcessResult:
    status: ProcessStatus
    original_path: str
    result_path: Optional[str] = None
    backup_path: Optional[str] = None
    error_message: Optional[str] = None


def is_pdf_encrypted(pdf_path: str) -> tuple[bool, bool]:
    """Returns (is_encrypted, needs_password).
    is_encrypted=True but needs_password=False means owner-password only."""
    if not PIKEPDF_AVAILABLE:
        return False, False
    try:
        with pikepdf.open(pdf_path) as pdf:
            return pdf.is_encrypted, False
    except pikepdf.PasswordError:
        return True, True
    except Exception:
        return False, False


def decrypt_pdf(
    pdf_path: str,
    passwords: list,
    add_prefix: bool = False,
) -> ProcessResult:
    """Attempt to decrypt a PDF with the supplied passwords.

    On success the original encrypted file is moved to a hidden
    '.pdf_backups' directory in the same folder, and the decrypted
    version is written to the original location (or with an
    '(Unlocked) ' prefix when add_prefix is True).
    """
    if not PIKEPDF_AVAILABLE:
        return ProcessResult(
            status=ProcessStatus.ERROR,
            original_path=pdf_path,
            error_message="pikepdf ist nicht installiert. Bitte 'pip install pikepdf' ausführen.",
        )

    path = Path(pdf_path)
    if not path.exists():
        return ProcessResult(
            status=ProcessStatus.ERROR,
            original_path=pdf_path,
            error_message="Datei nicht gefunden.",
        )

    # Check whether the file is encrypted
    try:
        pdf_no_pw = pikepdf.open(pdf_path)
        is_enc = pdf_no_pw.is_encrypted
        if not is_enc:
            pdf_no_pw.close()
            return ProcessResult(
                status=ProcessStatus.NOT_ENCRYPTED,
                original_path=pdf_path,
            )
        # Owner-password only – treat as success without a password
        unlocked_pdf = pdf_no_pw
        used_password = ""
    except pikepdf.PasswordError:
        unlocked_pdf = None
        used_password = None

        # Try each saved password
        for pw in passwords:
            try:
                unlocked_pdf = pikepdf.open(pdf_path, password=pw)
                used_password = pw
                break
            except pikepdf.PasswordError:
                continue
            except Exception as exc:
                return ProcessResult(
                    status=ProcessStatus.ERROR,
                    original_path=pdf_path,
                    error_message=str(exc),
                )

        if unlocked_pdf is None:
            return ProcessResult(
                status=ProcessStatus.WRONG_PASSWORD,
                original_path=pdf_path,
            )
    except Exception as exc:
        return ProcessResult(
            status=ProcessStatus.ERROR,
            original_path=pdf_path,
            error_message=str(exc),
        )

    # Determine output filename
    stem = path.stem
    output_name = f"(Unlocked) {path.name}" if add_prefix else path.name
    output_path = path.parent / output_name

    # Create hidden backup directory
    backup_dir = path.parent / ".pdf_backups"
    backup_path_obj = backup_dir / path.name

    try:
        backup_dir.mkdir(exist_ok=True)
        # Hide directory on Windows
        if os.name == "nt":
            import subprocess
            subprocess.run(
                ["attrib", "+H", str(backup_dir)],
                capture_output=True,
            )

        # Copy original to backup
        shutil.copy2(pdf_path, backup_path_obj)

        if output_path == path:
            # Overwrite in-place: write to temp then replace
            temp_path = path.parent / f"_tmp_{path.name}"
            unlocked_pdf.save(
                temp_path,
                encryption=False,
            )
            unlocked_pdf.close()
            os.replace(str(temp_path), str(output_path))
        else:
            # New filename (prefix mode) – write decrypted version,
            # then move the original to backups (it stays encrypted)
            unlocked_pdf.save(output_path, encryption=False)
            unlocked_pdf.close()

        return ProcessResult(
            status=ProcessStatus.SUCCESS,
            original_path=pdf_path,
            result_path=str(output_path),
            backup_path=str(backup_path_obj),
        )
    except Exception as exc:
        try:
            unlocked_pdf.close()
        except Exception:
            pass
        return ProcessResult(
            status=ProcessStatus.ERROR,
            original_path=pdf_path,
            error_message=str(exc),
        )


def move_to_locked_folder(pdf_path: str) -> Optional[str]:
    """Move a PDF that could not be decrypted into a 'Locked' subfolder.
    Returns the new path on success, None on failure."""
    path = Path(pdf_path)
    locked_dir = path.parent / "Locked"
    try:
        locked_dir.mkdir(exist_ok=True)
        dest = locked_dir / path.name
        # Resolve name conflicts
        counter = 1
        while dest.exists():
            dest = locked_dir / f"{path.stem}_{counter}{path.suffix}"
            counter += 1
        shutil.move(str(path), str(dest))
        return str(dest)
    except Exception:
        return None


def undo_decrypt(
    original_path: str,
    result_path: str,
    backup_path: Optional[str],
) -> bool:
    """Reverse a successful decrypt operation."""
    try:
        res = Path(result_path)
        orig = Path(original_path)

        # Delete the decrypted file
        if res.exists():
            res.unlink()

        # Restore backup to original location
        if backup_path:
            bak = Path(backup_path)
            if bak.exists():
                shutil.move(str(bak), str(orig))

        return True
    except Exception:
        return False


def undo_move_to_locked(original_path: str, result_path: str) -> bool:
    """Move a file back from the Locked folder to its original location."""
    try:
        src = Path(result_path)
        dst = Path(original_path)
        if src.exists():
            shutil.move(str(src), str(dst))
        return True
    except Exception:
        return False


def scan_folder_for_encrypted_pdfs(folder_path: str) -> list:
    """Recursively scan a folder and return paths of encrypted PDFs."""
    results = []
    try:
        root = Path(folder_path)
        for pdf in sorted(root.rglob("*.pdf")):
            # Skip the hidden backup and Locked directories
            parts = pdf.parts
            if ".pdf_backups" in parts or "Locked" in parts:
                continue
            enc, _ = is_pdf_encrypted(str(pdf))
            if enc:
                results.append(str(pdf))
    except Exception:
        pass
    return results
