from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid


class FileStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DECRYPTED = "decrypted"
    WRONG_PASSWORD = "wrong_password"
    NOT_ENCRYPTED = "not_encrypted"
    ERROR = "error"


STATUS_LABELS = {
    FileStatus.PENDING: "Ausstehend",
    FileStatus.PROCESSING: "Verarbeite ...",
    FileStatus.DECRYPTED: "Entschlüsselt",
    FileStatus.WRONG_PASSWORD: "Kein passendes Passwort",
    FileStatus.NOT_ENCRYPTED: "Nicht verschlüsselt",
    FileStatus.ERROR: "Fehler",
}

# (light_color, dark_color)
STATUS_COLORS = {
    FileStatus.PENDING: ("#6B7280", "#9CA3AF"),
    FileStatus.PROCESSING: ("#2563EB", "#60A5FA"),
    FileStatus.DECRYPTED: ("#16A34A", "#4ADE80"),
    FileStatus.WRONG_PASSWORD: ("#EA580C", "#FB923C"),
    FileStatus.NOT_ENCRYPTED: ("#0891B2", "#22D3EE"),
    FileStatus.ERROR: ("#DC2626", "#F87171"),
}

STATUS_ICONS = {
    FileStatus.PENDING: "○",
    FileStatus.PROCESSING: "⟳",
    FileStatus.DECRYPTED: "✓",
    FileStatus.WRONG_PASSWORD: "🔒",
    FileStatus.NOT_ENCRYPTED: "ℹ",
    FileStatus.ERROR: "✕",
}


@dataclass
class PDFFile:
    path: str
    status: FileStatus = FileStatus.PENDING
    error_message: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def filename(self) -> str:
        from pathlib import Path
        return Path(self.path).name

    @property
    def parent_dir(self) -> str:
        from pathlib import Path
        return str(Path(self.path).parent)


@dataclass
class SavedPassword:
    password: str
    label: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def display_label(self) -> str:
        return self.label if self.label else self.password[:2] + "•••"

    def to_dict(self) -> dict:
        return {"id": self.id, "password": self.password, "label": self.label}

    @classmethod
    def from_dict(cls, data: dict) -> "SavedPassword":
        obj = cls(password=data["password"], label=data.get("label", ""))
        obj.id = data.get("id", str(uuid.uuid4()))
        return obj


@dataclass
class SavedFolder:
    path: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict:
        return {"id": self.id, "path": self.path}

    @classmethod
    def from_dict(cls, data: dict) -> "SavedFolder":
        obj = cls(path=data["path"])
        obj.id = data.get("id", str(uuid.uuid4()))
        return obj


class OperationType(Enum):
    DECRYPT = "decrypt"
    MOVE_TO_LOCKED = "move_to_locked"


@dataclass
class FileOperation:
    op_type: OperationType
    original_path: str
    result_path: str
    backup_path: Optional[str] = None


@dataclass
class UndoEntry:
    description: str
    operations: list
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "timestamp": self.timestamp,
            "operations": [
                {
                    "op_type": op.op_type.value,
                    "original_path": op.original_path,
                    "result_path": op.result_path,
                    "backup_path": op.backup_path,
                }
                for op in self.operations
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UndoEntry":
        ops = [
            FileOperation(
                op_type=OperationType(o["op_type"]),
                original_path=o["original_path"],
                result_path=o["result_path"],
                backup_path=o.get("backup_path"),
            )
            for o in data.get("operations", [])
        ]
        entry = cls(
            description=data["description"],
            operations=ops,
            id=data["id"],
            timestamp=data["timestamp"],
        )
        return entry
