"""
Files tab: drag-and-drop zone + scrollable file list.
"""

import customtkinter as ctk
from models import PDFFile, FileStatus, STATUS_LABELS, STATUS_COLORS, STATUS_ICONS


# ------------------------------------------------------------------ #
# Single file row
# ------------------------------------------------------------------ #

class FileRow(ctk.CTkFrame):
    def __init__(self, parent, pdf_file: PDFFile, on_remove, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        self._pdf_file = pdf_file
        self._on_remove = on_remove
        self._build()

    def _build(self):
        self.configure(fg_color=("gray92", "gray17"))
        self.grid_columnconfigure(1, weight=1)

        # PDF icon label
        icon_lbl = ctk.CTkLabel(
            self,
            text="📄",
            font=ctk.CTkFont(size=20),
            width=32,
        )
        icon_lbl.grid(row=0, column=0, rowspan=2, padx=(10, 6), pady=8)

        # Filename
        name_lbl = ctk.CTkLabel(
            self,
            text=self._pdf_file.filename,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        name_lbl.grid(row=0, column=1, sticky="w", pady=(8, 0))

        # Directory path (small, muted)
        path_lbl = ctk.CTkLabel(
            self,
            text=self._pdf_file.parent_dir,
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        path_lbl.grid(row=1, column=1, sticky="w", pady=(0, 8))

        # Status badge
        status = self._pdf_file.status
        light_col, dark_col = STATUS_COLORS.get(status, ("#6B7280", "#9CA3AF"))
        icon = STATUS_ICONS.get(status, "○")
        label_text = STATUS_LABELS.get(status, "")

        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.grid(row=0, column=2, rowspan=2, padx=8, pady=8)

        status_lbl = ctk.CTkLabel(
            status_frame,
            text=f"{icon}  {label_text}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=(light_col, dark_col),
        )
        status_lbl.pack()

        if self._pdf_file.error_message:
            err_lbl = ctk.CTkLabel(
                status_frame,
                text=self._pdf_file.error_message[:40],
                font=ctk.CTkFont(size=9),
                text_color=("gray50", "gray60"),
            )
            err_lbl.pack()

        # Remove button (only when pending)
        if self._pdf_file.status == FileStatus.PENDING:
            remove_btn = ctk.CTkButton(
                self,
                text="✕",
                width=28,
                height=28,
                corner_radius=14,
                fg_color="transparent",
                hover_color=("gray80", "gray30"),
                text_color=("gray50", "gray60"),
                command=lambda: self._on_remove(self._pdf_file.id),
            )
            remove_btn.grid(row=0, column=3, rowspan=2, padx=(0, 8))


# ------------------------------------------------------------------ #
# Drop zone (shown when no files are loaded)
# ------------------------------------------------------------------ #

class DropZone(ctk.CTkFrame):
    def __init__(self, parent, on_pick_files, on_pick_folder, **kwargs):
        super().__init__(parent, corner_radius=16, **kwargs)
        self._on_pick_files = on_pick_files
        self._on_pick_folder = on_pick_folder
        self._build()

    def _build(self):
        self.configure(
            fg_color=("gray94", "gray15"),
            border_width=2,
            border_color=("gray75", "gray35"),
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inner,
            text="📂",
            font=ctk.CTkFont(size=56),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            inner,
            text="PDFs oder Ordner hierher ziehen",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack()

        ctk.CTkLabel(
            inner,
            text="oder über die Schaltflächen auswählen",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        ).pack(pady=(2, 16))

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack()

        ctk.CTkButton(
            btn_frame,
            text="  Dateien wählen",
            image=None,
            width=160,
            height=38,
            corner_radius=10,
            command=self._on_pick_files,
        ).grid(row=0, column=0, padx=6)

        ctk.CTkButton(
            btn_frame,
            text="  Ordner wählen",
            width=160,
            height=38,
            corner_radius=10,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=self._on_pick_folder,
        ).grid(row=0, column=1, padx=6)

    def set_hover(self, active: bool):
        color = ("gray85", "gray22") if active else ("gray94", "gray15")
        self.configure(fg_color=color)


# ------------------------------------------------------------------ #
# Files tab frame
# ------------------------------------------------------------------ #

class FilesTab(ctk.CTkFrame):
    def __init__(self, parent, app_state, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._app = app_state
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Toolbar (shown when there are files)
        self._toolbar = ctk.CTkFrame(self, fg_color="transparent", height=44)
        self._toolbar.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 4))
        self._toolbar.grid_columnconfigure(0, weight=1)

        self._file_count_lbl = ctk.CTkLabel(
            self._toolbar,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self._file_count_lbl.grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(self._toolbar, fg_color="transparent")
        btn_frame.grid(row=0, column=1)

        ctk.CTkButton(
            btn_frame,
            text="+ Dateien",
            width=90,
            height=30,
            corner_radius=8,
            command=self._app.pick_files,
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="+ Ordner",
            width=90,
            height=30,
            corner_radius=8,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=self._app.pick_folder,
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            btn_frame,
            text="Leeren",
            width=72,
            height=30,
            corner_radius=8,
            fg_color="transparent",
            hover_color=("gray80", "gray30"),
            text_color=("gray30", "gray70"),
            command=self._app.clear_files,
        ).pack(side="left", padx=3)

        # Drop zone
        self._drop_zone = DropZone(
            self,
            on_pick_files=self._app.pick_files,
            on_pick_folder=self._app.pick_folder,
        )
        self._drop_zone.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))

        # Scrollable file list
        self._scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            label_text="",
        )
        self._scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self._scroll.grid_columnconfigure(0, weight=1)

        self._file_rows: dict = {}
        self._refresh()

    def _refresh(self):
        files = self._app.files
        if files:
            self._drop_zone.grid_remove()
            self._scroll.grid()
        else:
            self._scroll.grid_remove()
            self._drop_zone.grid()

        # Update count label
        n = len(files)
        if n == 0:
            self._file_count_lbl.configure(text="")
        elif n == 1:
            self._file_count_lbl.configure(text="1 Datei")
        else:
            self._file_count_lbl.configure(text=f"{n} Dateien")

        # Rebuild rows for changed files
        current_ids = {f.id for f in files}
        existing_ids = set(self._file_rows.keys())

        # Remove rows no longer present
        for fid in list(existing_ids - current_ids):
            self._file_rows[fid].destroy()
            del self._file_rows[fid]

        # Add or update rows
        for i, f in enumerate(files):
            if f.id in self._file_rows:
                # Destroy and recreate to reflect status change
                self._file_rows[f.id].destroy()
            row = FileRow(
                self._scroll,
                f,
                on_remove=self._app.remove_file,
            )
            row.grid(row=i, column=0, sticky="ew", pady=3)
            self._file_rows[f.id] = row

    def refresh(self):
        self._refresh()

    def set_drop_hover(self, active: bool):
        self._drop_zone.set_hover(active)
