"""
Right panel: password management and options.
"""

import customtkinter as ctk
from models import SavedPassword


class PasswordRow(ctk.CTkFrame):
    def __init__(self, parent, pw: SavedPassword, on_delete, **kwargs):
        super().__init__(parent, corner_radius=8, **kwargs)
        self._pw = pw
        self._on_delete = on_delete
        self._visible = False
        self._build()

    def _build(self):
        self.configure(fg_color=("gray92", "gray17"))
        self.grid_columnconfigure(1, weight=1)

        # Lock icon
        ctk.CTkLabel(self, text="🔑", font=ctk.CTkFont(size=14), width=24).grid(
            row=0, column=0, padx=(8, 4), pady=6
        )

        # Label + masked password
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.grid(row=0, column=1, sticky="w", pady=4)
        info.grid_columnconfigure(0, weight=1)

        self._label_lbl = ctk.CTkLabel(
            info,
            text=self._pw.display_label(),
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        self._label_lbl.grid(row=0, column=0, sticky="w")

        self._pw_lbl = ctk.CTkLabel(
            info,
            text="•" * min(len(self._pw.password), 12),
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self._pw_lbl.grid(row=1, column=0, sticky="w")

        # Buttons frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=(4, 6), pady=4)

        self._eye_btn = ctk.CTkButton(
            btn_frame,
            text="👁",
            width=28,
            height=28,
            corner_radius=6,
            fg_color="transparent",
            hover_color=("gray80", "gray30"),
            command=self._toggle_visibility,
        )
        self._eye_btn.pack(side="left")

        ctk.CTkButton(
            btn_frame,
            text="✕",
            width=28,
            height=28,
            corner_radius=6,
            fg_color="transparent",
            hover_color=("#FEE2E2", "#7F1D1D"),
            text_color=("gray50", "gray60"),
            command=lambda: self._on_delete(self._pw.id),
        ).pack(side="left", padx=(2, 0))

    def _toggle_visibility(self):
        self._visible = not self._visible
        if self._visible:
            self._pw_lbl.configure(text=self._pw.password)
            self._eye_btn.configure(text="🙈")
        else:
            self._pw_lbl.configure(text="•" * min(len(self._pw.password), 12))
            self._eye_btn.configure(text="👁")


class PasswordPanel(ctk.CTkFrame):
    def __init__(self, parent, app_state, **kwargs):
        super().__init__(parent, corner_radius=0, **kwargs)
        self._app = app_state
        self._build()

    def _build(self):
        self.configure(fg_color=("gray96", "gray12"))
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # ---- Section: Passwörter ----
        ctk.CTkLabel(
            self,
            text="Passwörter",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 6))

        # Scrollable password list
        self._pw_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=180,
        )
        self._pw_scroll.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 6))
        self._pw_scroll.grid_columnconfigure(0, weight=1)
        self._pw_rows: dict = {}

        # ---- Add password form ----
        add_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray18"), corner_radius=10)
        add_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=4)
        add_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            add_frame,
            text="Neues Passwort",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 2))

        self._pw_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="Passwort eingeben...",
            show="•",
            height=34,
            corner_radius=8,
        )
        self._pw_entry.grid(row=1, column=0, sticky="ew", padx=(10, 4), pady=(0, 4))

        self._pw_show_btn = ctk.CTkButton(
            add_frame,
            text="👁",
            width=34,
            height=34,
            corner_radius=8,
            fg_color=("gray78", "gray28"),
            hover_color=("gray68", "gray38"),
            text_color=("gray10", "gray90"),
            command=self._toggle_pw_entry,
        )
        self._pw_show_btn.grid(row=1, column=1, padx=(0, 10), pady=(0, 4))

        ctk.CTkLabel(
            add_frame,
            text="Bezeichnung (optional)",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w",
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=10)

        self._label_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="z. B. Arbeit, Privat...",
            height=34,
            corner_radius=8,
        )
        self._label_entry.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 8)
        )

        ctk.CTkButton(
            add_frame,
            text="+ Passwort hinzufügen",
            height=36,
            corner_radius=8,
            command=self._add_password,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # ---- Divider ----
        ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray25")).grid(
            row=3, column=0, sticky="ew", padx=10, pady=8
        )

        # ---- Section: Optionen ----
        ctk.CTkLabel(
            self,
            text="Optionen",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=4, column=0, sticky="w", padx=14, pady=(0, 6))

        opt_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray18"), corner_radius=10)
        opt_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 12))
        opt_frame.grid_columnconfigure(0, weight=1)

        self._prefix_var = ctk.BooleanVar(value=self._app.settings.add_unlocked_prefix)
        self._prefix_cb = ctk.CTkCheckBox(
            opt_frame,
            text='"(Unlocked)" vor Dateinamen',
            variable=self._prefix_var,
            command=self._on_prefix_change,
            font=ctk.CTkFont(size=12),
            checkbox_width=18,
            checkbox_height=18,
        )
        self._prefix_cb.grid(row=0, column=0, sticky="w", padx=12, pady=10)

        ctk.CTkLabel(
            opt_frame,
            text='Schreibt "(Unlocked) " vor den\nDateinamen der entschlüsselten PDF.',
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            justify="left",
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

        self._refresh_passwords()

    # ------------------------------------------------------------------
    # Password list management
    # ------------------------------------------------------------------

    def _refresh_passwords(self):
        passwords = self._app.settings.load_passwords()

        current_ids = {p.id for p in passwords}
        for pid in list(self._pw_rows.keys()):
            if pid not in current_ids:
                self._pw_rows[pid].destroy()
                del self._pw_rows[pid]

        for i, pw in enumerate(passwords):
            if pw.id not in self._pw_rows:
                row = PasswordRow(
                    self._pw_scroll,
                    pw,
                    on_delete=self._delete_password,
                )
                row.grid(row=i, column=0, sticky="ew", pady=2)
                self._pw_rows[pw.id] = row

        if not passwords:
            if not hasattr(self, "_no_pw_lbl"):
                self._no_pw_lbl = ctk.CTkLabel(
                    self._pw_scroll,
                    text="Noch keine Passwörter gespeichert.",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray55", "gray55"),
                )
                self._no_pw_lbl.grid(row=0, column=0, pady=8)
        else:
            if hasattr(self, "_no_pw_lbl"):
                self._no_pw_lbl.destroy()
                del self._no_pw_lbl

    def _add_password(self):
        pw = self._pw_entry.get().strip()
        if not pw:
            self._pw_entry.configure(border_color="#DC2626")
            self.after(1200, lambda: self._pw_entry.configure(border_color=("gray65", "gray55")))
            return
        label = self._label_entry.get().strip()
        self._app.add_password(pw, label)
        self._pw_entry.delete(0, "end")
        self._label_entry.delete(0, "end")
        self._refresh_passwords()

    def _delete_password(self, pw_id: str):
        self._app.delete_password(pw_id)
        self._refresh_passwords()

    def _toggle_pw_entry(self):
        current = self._pw_entry.cget("show")
        if current == "•":
            self._pw_entry.configure(show="")
            self._pw_show_btn.configure(text="🙈")
        else:
            self._pw_entry.configure(show="•")
            self._pw_show_btn.configure(text="👁")

    def _on_prefix_change(self):
        self._app.settings.add_unlocked_prefix = self._prefix_var.get()

    def refresh(self):
        self._refresh_passwords()
        self._prefix_var.set(self._app.settings.add_unlocked_prefix)
