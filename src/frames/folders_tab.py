"""
Saved folders tab: manage bookmark folders for batch scanning.
"""

import customtkinter as ctk
from models import SavedFolder


class FolderRow(ctk.CTkFrame):
    def __init__(self, parent, folder: SavedFolder, on_scan, on_delete, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        self._folder = folder
        self._on_scan = on_scan
        self._on_delete = on_delete
        self._build()

    def _build(self):
        self.configure(fg_color=("gray92", "gray17"))
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="📁", font=ctk.CTkFont(size=18), width=30).grid(
            row=0, column=0, padx=(10, 6), pady=8
        )

        # Show just the last two path components for readability
        from pathlib import Path
        p = Path(self._folder.path)
        parts = p.parts
        short = str(Path(*parts[-2:])) if len(parts) >= 2 else self._folder.path

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(
            info,
            text=short,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=self._folder.path,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).pack(anchor="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=(4, 8), pady=6)

        ctk.CTkButton(
            btn_frame,
            text="Scannen",
            width=76,
            height=28,
            corner_radius=7,
            command=lambda: self._on_scan(self._folder),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame,
            text="✕",
            width=28,
            height=28,
            corner_radius=7,
            fg_color="transparent",
            hover_color=("#FEE2E2", "#7F1D1D"),
            text_color=("gray50", "gray60"),
            command=lambda: self._on_delete(self._folder.id),
        ).pack(side="left")


class FoldersTab(ctk.CTkFrame):
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
            text="Gespeicherte Ordner werden nach verschlüsselten PDFs durchsucht.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.grid(row=0, column=1)

        ctk.CTkButton(
            btn_frame,
            text="+ Ordner",
            width=90,
            height=30,
            corner_radius=8,
            command=self._app.add_saved_folder,
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Alle scannen",
            width=100,
            height=30,
            corner_radius=8,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=self._app.scan_all_folders,
        ).pack(side="left", padx=3)

        # Scrollable folder list
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self._scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self._scroll.grid_columnconfigure(0, weight=1)

        self._folder_rows: dict = {}
        self._empty_lbl = None
        self.refresh()

    def refresh(self):
        folders = self._app.settings.load_folders()

        current_ids = {f.id for f in folders}
        for fid in list(self._folder_rows.keys()):
            if fid not in current_ids:
                self._folder_rows[fid].destroy()
                del self._folder_rows[fid]

        for i, folder in enumerate(folders):
            if folder.id not in self._folder_rows:
                row = FolderRow(
                    self._scroll,
                    folder,
                    on_scan=self._scan_single,
                    on_delete=self._delete_folder,
                )
                row.grid(row=i, column=0, sticky="ew", pady=3)
                self._folder_rows[folder.id] = row

        if not folders:
            if self._empty_lbl is None:
                self._empty_lbl = ctk.CTkFrame(
                    self._scroll, fg_color=("gray94", "gray15"), corner_radius=12
                )
                self._empty_lbl.grid(row=0, column=0, sticky="ew", pady=16, padx=8)
                self._empty_lbl.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(
                    self._empty_lbl,
                    text="📂",
                    font=ctk.CTkFont(size=40),
                ).grid(pady=(20, 4))

                ctk.CTkLabel(
                    self._empty_lbl,
                    text="Noch keine Ordner gespeichert",
                    font=ctk.CTkFont(size=13, weight="bold"),
                ).grid(pady=(0, 4))

                ctk.CTkLabel(
                    self._empty_lbl,
                    text='Klicke auf "+ Ordner", um einen Ordnerpfad zu speichern.\nBeim Klick auf "Scannen" werden alle verschlüsselten\nPDFs in diesem Ordner automatisch zur Liste hinzugefügt.',
                    font=ctk.CTkFont(size=11),
                    text_color=("gray50", "gray60"),
                    justify="center",
                ).grid(pady=(0, 20))
        else:
            if self._empty_lbl is not None:
                self._empty_lbl.destroy()
                self._empty_lbl = None

    def _scan_single(self, folder: SavedFolder):
        self._app.scan_folder(folder.path)

    def _delete_folder(self, folder_id: str):
        self._app.delete_saved_folder(folder_id)
        self.refresh()
