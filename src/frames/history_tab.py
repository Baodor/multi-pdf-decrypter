"""
History tab: shows undo-able operations.
"""

import customtkinter as ctk
from models import UndoEntry, OperationType


class HistoryRow(ctk.CTkFrame):
    def __init__(self, parent, entry: UndoEntry, on_undo, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        self._entry = entry
        self._on_undo = on_undo
        self._build()

    def _build(self):
        self.configure(fg_color=("gray92", "gray17"))
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="🕐", font=ctk.CTkFont(size=18), width=30).grid(
            row=0, column=0, padx=(10, 6), pady=8
        )

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            info,
            text=self._entry.description,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=self._entry.timestamp,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).pack(anchor="w")

        # Show operation summary
        decrypted = sum(
            1 for op in self._entry.operations
            if op.op_type == OperationType.DECRYPT
        )
        moved = sum(
            1 for op in self._entry.operations
            if op.op_type == OperationType.MOVE_TO_LOCKED
        )
        parts = []
        if decrypted:
            parts.append(f"{decrypted} entschlüsselt")
        if moved:
            parts.append(f"{moved} nach 'Locked' verschoben")
        if parts:
            ctk.CTkLabel(
                info,
                text="  ".join(parts),
                font=ctk.CTkFont(size=10),
                text_color=("gray55", "gray55"),
                anchor="w",
            ).pack(anchor="w")

        ctk.CTkButton(
            self,
            text="↩ Rückgängig",
            width=110,
            height=30,
            corner_radius=7,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=lambda: self._on_undo(self._entry.id),
        ).grid(row=0, column=2, padx=8, pady=8)


class HistoryTab(ctk.CTkFrame):
    def __init__(self, parent, app_state, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._app = app_state
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color="transparent", height=44)
        toolbar.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 4))
        toolbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            toolbar,
            text="Bisherige Vorgänge können hier rückgängig gemacht werden.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            toolbar,
            text="Verlauf löschen",
            width=110,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("#FEE2E2", "#7F1D1D"),
            text_color=("gray50", "gray60"),
            command=self._clear_history,
        ).grid(row=0, column=1)

        # Scrollable list
        self._scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self._scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self._scroll.grid_columnconfigure(0, weight=1)

        self._rows: dict = {}
        self._empty_lbl = None
        self.refresh()

    def refresh(self):
        history = self._app.settings.load_undo_history()

        current_ids = {e.id for e in history}
        for eid in list(self._rows.keys()):
            if eid not in current_ids:
                self._rows[eid].destroy()
                del self._rows[eid]

        for i, entry in enumerate(history):
            if entry.id not in self._rows:
                row = HistoryRow(
                    self._scroll,
                    entry,
                    on_undo=self._undo_entry,
                )
                row.grid(row=i, column=0, sticky="ew", pady=3)
                self._rows[entry.id] = row

        if not history:
            if self._empty_lbl is None:
                self._empty_lbl = ctk.CTkFrame(
                    self._scroll,
                    fg_color=("gray94", "gray15"),
                    corner_radius=12,
                )
                self._empty_lbl.grid(row=0, column=0, sticky="ew", pady=16, padx=8)
                self._empty_lbl.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(
                    self._empty_lbl,
                    text="↩",
                    font=ctk.CTkFont(size=40),
                ).grid(pady=(20, 4))

                ctk.CTkLabel(
                    self._empty_lbl,
                    text="Noch keine Vorgänge",
                    font=ctk.CTkFont(size=13, weight="bold"),
                ).grid(pady=(0, 4))

                ctk.CTkLabel(
                    self._empty_lbl,
                    text="Nach dem ersten Entschlüsseln erscheinen\ndie Vorgänge hier und können rückgängig\ngemacht werden.",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray50", "gray60"),
                    justify="center",
                ).grid(pady=(0, 20))
        else:
            if self._empty_lbl is not None:
                self._empty_lbl.destroy()
                self._empty_lbl = None

    def _undo_entry(self, entry_id: str):
        self._app.undo_entry(entry_id)
        self.refresh()

    def _clear_history(self):
        self._app.clear_undo_history()
        self.refresh()
