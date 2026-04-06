"""
Main application window for Multi PDF Decrypter.
Composes all frames and holds shared application state.
"""

import os
import threading
import sys
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from models import (
    PDFFile,
    FileStatus,
    SavedPassword,
    SavedFolder,
    UndoEntry,
    FileOperation,
    OperationType,
)
from settings_manager import SettingsManager
from pdf_processor import (
    decrypt_pdf,
    move_to_locked_folder,
    undo_decrypt,
    undo_move_to_locked,
    scan_folder_for_encrypted_pdfs,
    ProcessStatus,
)
from frames.files_tab import FilesTab
from frames.password_panel import PasswordPanel
from frames.folders_tab import FoldersTab
from frames.history_tab import HistoryTab

# Try to import drag-and-drop support
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES

    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False


# ------------------------------------------------------------------ #
# App state (thin controller shared with frames)
# ------------------------------------------------------------------ #


class AppState:
    """Shared controller between the main window and child frames."""

    def __init__(self, settings: SettingsManager):
        self.settings = settings
        self.files: list[PDFFile] = []
        self._on_change_callbacks: list = []
        self._on_status_callbacks: list = []

    # --- Callbacks ---

    def on_change(self, cb):
        self._on_change_callbacks.append(cb)

    def on_status(self, cb):
        self._on_status_callbacks.append(cb)

    def _notify_change(self):
        for cb in self._on_change_callbacks:
            cb()

    def _notify_status(self, msg: str):
        for cb in self._on_status_callbacks:
            cb(msg)

    # --- File management ---

    def add_files(self, paths: list):
        added = 0
        for path in paths:
            p = Path(path)
            if p.suffix.lower() != ".pdf":
                continue
            if any(f.path == str(p) for f in self.files):
                continue
            # Skip files inside .pdf_backups or Locked
            parts = p.parts
            if ".pdf_backups" in parts or "Locked" in parts:
                continue
            if not p.exists():
                continue
            self.files.append(PDFFile(path=str(p)))
            added += 1
        if added:
            self._notify_change()
            self._notify_status(f"{len(self.files)} Datei(en) in der Liste")

    def add_folder(self, path: str):
        root = Path(path)
        paths = [str(p) for p in sorted(root.rglob("*.pdf"))]
        self.add_files(paths)

    def remove_file(self, file_id: str):
        self.files = [f for f in self.files if f.id != file_id]
        self._notify_change()

    def clear_files(self):
        self.files.clear()
        self._notify_change()
        self._notify_status("Liste geleert")

    # --- UI helpers (wired later to actual dialogs) ---

    def pick_files(self):
        paths = filedialog.askopenfilenames(
            title="PDFs auswählen",
            filetypes=[("PDF-Dateien", "*.pdf"), ("Alle Dateien", "*.*")],
        )
        if paths:
            self.add_files(list(paths))

    def pick_folder(self):
        path = filedialog.askdirectory(title="Ordner auswählen")
        if path:
            self.add_folder(path)

    def add_saved_folder(self):
        path = filedialog.askdirectory(title="Ordner speichern")
        if path:
            folders = self.settings.load_folders()
            if not any(f.path == path for f in folders):
                folders.append(SavedFolder(path=path))
                self.settings.save_folders(folders)
            self._notify_change()

    def delete_saved_folder(self, folder_id: str):
        folders = [f for f in self.settings.load_folders() if f.id != folder_id]
        self.settings.save_folders(folders)
        self._notify_change()

    def scan_folder(self, path: str):
        self._notify_status(f"Scanne {path} ...")
        found = scan_folder_for_encrypted_pdfs(path)
        self.add_files(found)
        self._notify_status(f"{len(found)} verschlüsselte PDF(s) gefunden")

    def scan_all_folders(self):
        for folder in self.settings.load_folders():
            self.scan_folder(folder.path)

    # --- Password management ---

    def add_password(self, password: str, label: str = ""):
        passwords = self.settings.load_passwords()
        passwords.append(SavedPassword(password=password, label=label))
        self.settings.save_passwords(passwords)

    def delete_password(self, pw_id: str):
        passwords = [p for p in self.settings.load_passwords() if p.id != pw_id]
        self.settings.save_passwords(passwords)

    # --- Undo ---

    def undo_entry(self, entry_id: str):
        history = self.settings.load_undo_history()
        entry = next((e for e in history if e.id == entry_id), None)
        if not entry:
            return

        for op in reversed(entry.operations):
            if op.op_type == OperationType.DECRYPT:
                undo_decrypt(op.original_path, op.result_path, op.backup_path)
            elif op.op_type == OperationType.MOVE_TO_LOCKED:
                undo_move_to_locked(op.original_path, op.result_path)

        history = [e for e in history if e.id != entry_id]
        self.settings.save_undo_history(history)
        self._notify_status("Vorgang rückgängig gemacht")
        self._notify_change()

    def clear_undo_history(self):
        self.settings.save_undo_history([])
        self._notify_change()


# ------------------------------------------------------------------ #
# Main window
# ------------------------------------------------------------------ #


def _make_app_class():
    """Return an App class that inherits from TkinterDnD.DnDWrapper if available."""
    if DND_AVAILABLE:

        class App(ctk.CTk, TkinterDnD.DnDWrapper):
            def __init__(self):
                super().__init__()
                self.TkdndVersion = TkinterDnD._require(self)

    else:

        class App(ctk.CTk):
            def __init__(self):
                super().__init__()

    return App


class MultiPDFDecrypterWindow:
    """Builds and manages the main application window."""

    ACCENT = "#2563EB"

    def __init__(self):
        self._settings = SettingsManager()

        # Apply saved theme
        ctk.set_appearance_mode(self._settings.theme)
        ctk.set_default_color_theme("blue")

        AppBase = _make_app_class()
        self._root = AppBase()
        self._root.title("Multi PDF Decrypter")
        self._root.geometry(self._settings.window_geometry)
        self._root.minsize(900, 600)

        # Save window geometry on close
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._state = AppState(self._settings)
        self._state.on_change(self._on_state_change)
        self._state.on_status(self._set_status)

        self._build_ui()
        self._register_dnd()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self):
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_content()
        self._build_bottom_bar()

    def _build_header(self):
        header = ctk.CTkFrame(
            self._root, height=60, corner_radius=0, fg_color=("gray88", "gray14")
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        # App icon + title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=18, pady=0, sticky="w")

        ctk.CTkLabel(
            title_frame,
            text="🔓",
            font=ctk.CTkFont(size=26),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            title_frame,
            text="Multi PDF Decrypter",
            font=ctk.CTkFont(size=17, weight="bold"),
        ).pack(side="left")

        # Theme toggle
        theme_frame = ctk.CTkFrame(header, fg_color="transparent")
        theme_frame.grid(row=0, column=2, padx=18, sticky="e")

        ctk.CTkLabel(
            theme_frame,
            text="Design:",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        ).pack(side="left", padx=(0, 6))

        self._theme_var = ctk.StringVar(value=self._settings.theme)
        theme_seg = ctk.CTkSegmentedButton(
            theme_frame,
            values=["Hell", "Dunkel", "System"],
            variable=self._theme_var,
            command=self._on_theme_change,
            width=200,
            height=30,
        )
        theme_seg.pack(side="left")

    def _build_content(self):
        content = ctk.CTkFrame(self._root, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Left: tabbed view
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(8, 4), pady=8)
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self._tabview = ctk.CTkTabview(left, anchor="nw")
        self._tabview.grid(row=0, column=0, sticky="nsew")
        self._tabview.grid_columnconfigure(0, weight=1)

        self._tabview.add("Dateien")
        self._tabview.add("Gespeicherte Ordner")
        self._tabview.add("Verlauf")

        for tab_name in ["Dateien", "Gespeicherte Ordner", "Verlauf"]:
            self._tabview.tab(tab_name).grid_rowconfigure(0, weight=1)
            self._tabview.tab(tab_name).grid_columnconfigure(0, weight=1)

        self._files_tab = FilesTab(
            self._tabview.tab("Dateien"),
            app_state=self._state,
        )
        self._files_tab.grid(row=0, column=0, sticky="nsew")

        self._folders_tab = FoldersTab(
            self._tabview.tab("Gespeicherte Ordner"),
            app_state=self._state,
        )
        self._folders_tab.grid(row=0, column=0, sticky="nsew")

        self._history_tab = HistoryTab(
            self._tabview.tab("Verlauf"),
            app_state=self._state,
        )
        self._history_tab.grid(row=0, column=0, sticky="nsew")

        # Right: password panel (fixed width)
        self._pw_panel = PasswordPanel(
            content,
            app_state=self._state,
        )
        self._pw_panel.grid(
            row=0, column=1, sticky="nsew", padx=(4, 8), pady=8
        )
        self._pw_panel.configure(width=310)
        content.grid_columnconfigure(1, minsize=310, weight=0)

    def _build_bottom_bar(self):
        bar = ctk.CTkFrame(
            self._root, height=64, corner_radius=0, fg_color=("gray88", "gray14")
        )
        bar.grid(row=2, column=0, sticky="ew")
        bar.grid_columnconfigure(2, weight=1)
        bar.grid_propagate(False)

        # Decrypt button
        self._decrypt_btn = ctk.CTkButton(
            bar,
            text="  🔓  Alle entschlüsseln",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=42,
            width=210,
            corner_radius=10,
            command=self._start_processing,
        )
        self._decrypt_btn.grid(row=0, column=0, padx=(16, 8), pady=11)

        # Undo last button
        self._undo_btn = ctk.CTkButton(
            bar,
            text="↩  Letzten rückgängig",
            height=42,
            width=190,
            corner_radius=10,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=self._undo_last,
        )
        self._undo_btn.grid(row=0, column=1, padx=4, pady=11)

        # Progress bar (hidden initially)
        self._progress_bar = ctk.CTkProgressBar(bar, width=180, height=8, mode="indeterminate")
        self._progress_bar.grid(row=0, column=2, padx=8, pady=11, sticky="w")
        self._progress_bar.grid_remove()

        # Status label
        self._status_lbl = ctk.CTkLabel(
            bar,
            text="Bereit",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
            anchor="e",
        )
        self._status_lbl.grid(row=0, column=3, padx=(8, 18), pady=11, sticky="e")

    # ------------------------------------------------------------------
    # Drag and drop
    # ------------------------------------------------------------------

    def _register_dnd(self):
        if not DND_AVAILABLE:
            return
        try:
            self._root.drop_target_register(DND_FILES)
            self._root.dnd_bind("<<Drop>>", self._on_drop)
            self._root.dnd_bind("<<DragEnter>>", self._on_drag_enter)
            self._root.dnd_bind("<<DragLeave>>", self._on_drag_leave)
        except Exception:
            pass

    def _on_drag_enter(self, event):
        self._files_tab.set_drop_hover(True)
        self._tabview.set(tab="Dateien")

    def _on_drag_leave(self, event):
        self._files_tab.set_drop_hover(False)

    def _on_drop(self, event):
        self._files_tab.set_drop_hover(False)
        paths = self._parse_dnd_data(event.data)
        for path in paths:
            p = Path(path)
            if p.is_dir():
                self._state.add_folder(str(p))
            elif p.suffix.lower() == ".pdf":
                self._state.add_files([str(p)])

    @staticmethod
    def _parse_dnd_data(data: str) -> list:
        """Parse tkdnd drop data into a list of file paths."""
        import re
        raw = re.findall(r"\{([^}]+)\}|(\S+)", data)
        paths = []
        for in_braces, bare in raw:
            path = in_braces or bare
            # Remove file:// URI prefix
            if path.startswith("file://"):
                path = path[7:]
                # Windows: file:///C:/... -> C:/...
                if len(path) > 2 and path[0] == "/" and path[2] == ":":
                    path = path[1:]
            paths.append(path)
        return paths

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    def _start_processing(self):
        pending = [f for f in self._state.files if f.status == FileStatus.PENDING]
        if not pending:
            self._set_status("Keine ausstehenden Dateien")
            return

        passwords = [p.password for p in self._settings.load_passwords()]
        if not passwords:
            self._set_status("Bitte zuerst mindestens ein Passwort hinzufügen")
            return

        self._decrypt_btn.configure(state="disabled", text="  ⟳  Verarbeite...")
        self._undo_btn.configure(state="disabled")
        self._progress_bar.grid()
        self._progress_bar.start()

        thread = threading.Thread(
            target=self._process_worker,
            args=(pending, passwords),
            daemon=True,
        )
        thread.start()

    def _process_worker(self, files: list, passwords: list):
        add_prefix = self._settings.add_unlocked_prefix
        operations: list[FileOperation] = []

        for pdf_file in files:
            # Mark as processing
            self._root.after(
                0,
                lambda fid=pdf_file.id: self._update_file_status(
                    fid, FileStatus.PROCESSING
                ),
            )

            result = decrypt_pdf(pdf_file.path, passwords, add_prefix)

            if result.status == ProcessStatus.SUCCESS:
                op = FileOperation(
                    op_type=OperationType.DECRYPT,
                    original_path=result.original_path,
                    result_path=result.result_path or result.original_path,
                    backup_path=result.backup_path,
                )
                operations.append(op)
                self._root.after(
                    0,
                    lambda fid=pdf_file.id: self._update_file_status(
                        fid, FileStatus.DECRYPTED
                    ),
                )
            elif result.status == ProcessStatus.NOT_ENCRYPTED:
                self._root.after(
                    0,
                    lambda fid=pdf_file.id: self._update_file_status(
                        fid, FileStatus.NOT_ENCRYPTED
                    ),
                )
            elif result.status == ProcessStatus.WRONG_PASSWORD:
                # Move to Locked folder
                moved_path = move_to_locked_folder(pdf_file.path)
                if moved_path:
                    op = FileOperation(
                        op_type=OperationType.MOVE_TO_LOCKED,
                        original_path=pdf_file.path,
                        result_path=moved_path,
                    )
                    operations.append(op)
                self._root.after(
                    0,
                    lambda fid=pdf_file.id: self._update_file_status(
                        fid, FileStatus.WRONG_PASSWORD
                    ),
                )
            else:
                err = result.error_message or "Unbekannter Fehler"
                self._root.after(
                    0,
                    lambda fid=pdf_file.id, e=err: self._update_file_status(
                        fid, FileStatus.ERROR, e
                    ),
                )

        # Save undo entry
        if operations:
            decrypted = sum(1 for o in operations if o.op_type == OperationType.DECRYPT)
            moved = sum(1 for o in operations if o.op_type == OperationType.MOVE_TO_LOCKED)
            parts = []
            if decrypted:
                parts.append(f"{decrypted} entschlüsselt")
            if moved:
                parts.append(f"{moved} nach 'Locked' verschoben")
            desc = ", ".join(parts)

            entry = UndoEntry(description=desc, operations=operations)
            history = self._settings.load_undo_history()
            history.insert(0, entry)
            self._settings.save_undo_history(history)

        self._root.after(0, self._processing_done)

    def _update_file_status(self, file_id: str, status: FileStatus, error: str = ""):
        for f in self._state.files:
            if f.id == file_id:
                f.status = status
                f.error_message = error
                break
        self._files_tab.refresh()

    def _processing_done(self):
        self._progress_bar.stop()
        self._progress_bar.grid_remove()
        self._decrypt_btn.configure(state="normal", text="  🔓  Alle entschlüsseln")
        self._undo_btn.configure(state="normal")

        total = len(self._state.files)
        done = sum(1 for f in self._state.files if f.status == FileStatus.DECRYPTED)
        locked = sum(1 for f in self._state.files if f.status == FileStatus.WRONG_PASSWORD)
        self._set_status(f"Fertig: {done} entschlüsselt, {locked} gesperrt, {total} gesamt")

        self._history_tab.refresh()

    # ------------------------------------------------------------------
    # Undo helpers
    # ------------------------------------------------------------------

    def _undo_last(self):
        history = self._settings.load_undo_history()
        if not history:
            self._set_status("Kein Vorgang zum Rückgängigmachen")
            return
        self._state.undo_entry(history[0].id)
        self._history_tab.refresh()
        # Reset all file statuses to pending so user can reprocess
        for f in self._state.files:
            f.status = FileStatus.PENDING
            f.error_message = ""
        self._files_tab.refresh()

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _on_state_change(self):
        self._files_tab.refresh()
        self._folders_tab.refresh()
        self._history_tab.refresh()
        self._pw_panel.refresh()

    def _set_status(self, msg: str):
        self._status_lbl.configure(text=msg)

    def _on_theme_change(self, value: str):
        mode_map = {"Hell": "Light", "Dunkel": "Dark", "System": "System"}
        mode = mode_map.get(value, "System")
        ctk.set_appearance_mode(mode)
        self._settings.theme = mode

    def _on_close(self):
        geo = self._root.geometry()
        self._settings.window_geometry = geo
        self._root.destroy()

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self):
        self._root.mainloop()
