"""
Persistent settings stored as JSON in the user's config directory.
"""

import json
import os
from pathlib import Path
from models import SavedPassword, SavedFolder, UndoEntry

APP_NAME = "MultiPDFDecrypter"
MAX_UNDO_ENTRIES = 50


def _config_path() -> Path:
    """Return the path to the settings JSON file, creating the directory if needed."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif os.uname().sysname == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))

    config_dir = base / APP_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "settings.json"


def _load_raw() -> dict:
    path = _config_path()
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_raw(data: dict) -> None:
    path = _config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class SettingsManager:
    def __init__(self):
        self._data = _load_raw()

    def _save(self):
        _save_raw(self._data)

    # ------------------------------------------------------------------ #
    # Passwords
    # ------------------------------------------------------------------ #

    def load_passwords(self) -> list:
        return [
            SavedPassword.from_dict(d)
            for d in self._data.get("passwords", [])
        ]

    def save_passwords(self, passwords: list) -> None:
        self._data["passwords"] = [p.to_dict() for p in passwords]
        self._save()

    # ------------------------------------------------------------------ #
    # Saved folders
    # ------------------------------------------------------------------ #

    def load_folders(self) -> list:
        return [
            SavedFolder.from_dict(d)
            for d in self._data.get("saved_folders", [])
        ]

    def save_folders(self, folders: list) -> None:
        self._data["saved_folders"] = [f.to_dict() for f in folders]
        self._save()

    # ------------------------------------------------------------------ #
    # Undo history
    # ------------------------------------------------------------------ #

    def load_undo_history(self) -> list:
        return [
            UndoEntry.from_dict(d)
            for d in self._data.get("undo_history", [])
        ]

    def save_undo_history(self, history: list) -> None:
        trimmed = history[:MAX_UNDO_ENTRIES]
        self._data["undo_history"] = [e.to_dict() for e in trimmed]
        self._save()

    # ------------------------------------------------------------------ #
    # Generic options
    # ------------------------------------------------------------------ #

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value
        self._save()

    # ------------------------------------------------------------------ #
    # Convenience helpers
    # ------------------------------------------------------------------ #

    @property
    def add_unlocked_prefix(self) -> bool:
        return self._data.get("add_unlocked_prefix", False)

    @add_unlocked_prefix.setter
    def add_unlocked_prefix(self, value: bool) -> None:
        self._data["add_unlocked_prefix"] = value
        self._save()

    @property
    def theme(self) -> str:
        return self._data.get("theme", "System")

    @theme.setter
    def theme(self, value: str) -> None:
        self._data["theme"] = value
        self._save()

    @property
    def window_geometry(self) -> str:
        return self._data.get("window_geometry", "1100x720")

    @window_geometry.setter
    def window_geometry(self, value: str) -> None:
        self._data["window_geometry"] = value
        self._save()
