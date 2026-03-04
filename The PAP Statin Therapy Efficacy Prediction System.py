"""
PAP Statin Therapy Efficacy Prediction System  v2.0
Redesigned UI – horizontal tab navigation, two-panel layout
matching the clean/minimal reference style
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# ══════════════════════════════════════════════════════════════
# 0.  Global Theme
# ══════════════════════════════════════════════════════════════
C = {
    "hdr_bg":   "#1B2A3B",   # top header
    "tab_bg":   "#1F3347",   # tab bar
    "tab_sel":  "#2E86C1",   # selected tab
    "tab_hov":  "#2A4A6B",   # hover tab
    "page_bg":  "#F4F6F9",   # page background
    "panel_bg": "#FFFFFF",   # panel/card background
    "border":   "#DDE2EA",   # card border
    "input_bg": "#F8FAFC",   # input field bg
    "txt_dark": "#1B2631",   # primary text
    "txt_mid":  "#5D6D7E",   # secondary text
    "txt_light":"#95A5A6",   # hint text
    "accent":   "#2E86C1",   # blue accent
    "green":    "#27AE60",   # success
    "red":      "#E74C3C",   # danger
    "orange":   "#E67E22",   # warning
    "yellow":   "#F1C40F",   # yellow
    "purple":   "#8E44AD",   # purple
    "cyan":     "#1ABC9C",   # teal
    "hdr2":     "#1A5276",   # dark blue
}

FN   = ("Segoe UI", 10)
FN9  = ("Segoe UI", 9)
FB   = ("Segoe UI", 10, "bold")
FH   = ("Segoe UI", 12, "bold")
FT   = ("Segoe UI", 16, "bold")
FMN  = ("Consolas", 9)


# ══════════════════════════════════════════════════════════════
# 1.  Login Window
# ══════════════════════════════════════════════════════════════
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAP Statin Therapy Efficacy Prediction System")
        self.resizable(False, False)
        self.configure(bg="#F0F4F8")
        w, h = 420, 540
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self._build()

    def _build(self):
        # thin top accent bar
        tk.Frame(self, bg=C["accent"], height=4).pack(fill=tk.X)

        card = tk.Frame(self, bg=C["panel_bg"],
                        highlightthickness=1,
                        highlightbackground=C["border"])
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=470)

        # ── icon area ──
        top = tk.Frame(card, bg=C["hdr_bg"], height=130)
        top.pack(fill=tk.X)
        top.pack_propagate(False)

        # pill icon (canvas)
        cv = tk.Canvas(top, width=48, height=48,
                       bg=C["hdr_bg"], highlightthickness=0)
        cv.place(relx=0.5, rely=0.30, anchor="center")
        # draw a simple pill shape
        cv.create_oval(4, 4, 44, 44, fill=C["accent"], outline="white", width=2)
        cv.create_text(24, 24, text="💊", font=("Segoe UI", 18))

        tk.Label(top, text="PAP Statin Therapy Efficacy",
                 font=("Segoe UI", 12, "bold"),
                 bg=C["hdr_bg"], fg="white").place(relx=0.5, rely=0.62, anchor="center")
        tk.Label(top, text="Prediction System",
                 font=("Segoe UI", 10),
                 bg=C["hdr_bg"], fg="#85C1E9").place(relx=0.5, rely=0.80, anchor="center")

        # ── form ──
        form = tk.Frame(card, bg=C["panel_bg"])
        form.pack(padx=36, pady=24, fill=tk.X)

        for label, attr, show in [
            ("Username", "user_entry", ""),
            ("Password", "pwd_entry",  "●"),
        ]:
            tk.Label(form, text=label, font=FB,
                     bg=C["panel_bg"], fg=C["txt_mid"]).pack(anchor="w", pady=(10, 3))
            e = tk.Entry(form, font=FN, relief="solid", bd=1,
                         bg=C["input_bg"], fg=C["txt_dark"],
                         highlightthickness=2,
                         highlightcolor=C["accent"],
                         highlightbackground=C["border"],
                         insertbackground=C["accent"],
                         show=show)
            e.pack(fill=tk.X, ipady=7)
            setattr(self, attr, e)

        self.err_lbl = tk.Label(form, text="", font=FN9,
                                bg=C["panel_bg"], fg=C["red"])
        self.err_lbl.pack(anchor="w", pady=(6, 0))

        btn = tk.Button(form, text="Login to System",
                        font=("Segoe UI", 11, "bold"),
                        bg=C["accent"], fg="white",
                        relief="flat", cursor="hand2",
                        activebackground=C["hdr2"],
                        activeforeground="white",
                        command=self._login)
        btn.pack(fill=tk.X, ipady=10, pady=(14, 0))

        tk.Label(card, text="Default username and password are both:  1",
                 font=FN9, bg=C["panel_bg"], fg=C["txt_light"]).pack(pady=8)

        self.pwd_entry.bind("<Return>", lambda _: self._login())

    def _login(self):
        if self.user_entry.get().strip() == "1" and self.pwd_entry.get().strip() == "1":
            self.destroy()
            MainApp().mainloop()
        else:
            self.err_lbl.config(text="⚠  Incorrect username or password")


# ══════════════════════════════════════════════════════════════
# 2.  Main Application
# ══════════════════════════════════════════════════════════════
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAP Statin Therapy Efficacy Prediction System  v2.0")
        self.state("zoomed")
        self.configure(bg=C["page_bg"])
        self._stored: dict = {}
        self._running = False
        self._init_vars()
        self._style()
        self._build()

    # ── Tk variables ──────────────────────────────────────────
    def _init_vars(self):
        self.v_train   = tk.StringVar()
        self.v_test    = tk.StringVar()
        self.v_outdir  = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "PAP_outputs"))
        self.v_label   = tk.StringVar(value="Label")
        self.v_fmt     = tk.StringVar(value="pdf")
        self.v_dpi     = tk.IntVar(value=1200)

        self.v_lasso   = tk.BooleanVar(value=True)
        self.v_rfe     = tk.BooleanVar(value=True)
        self.v_rf_fs   = tk.BooleanVar(value=True)
        self.v_xgb_fs  = tk.BooleanVar(value=True)
        self.v_mi      = tk.BooleanVar(value=True)
        self.v_kbest   = tk.BooleanVar(value=True)
        self.v_patience= tk.IntVar(value=15)
        self.v_minimp  = tk.DoubleVar(value=0.001)
        self.v_cvfolds = tk.IntVar(value=5)

        self.mv = {k: tk.BooleanVar(value=True) for k in [
            "Logistic Regression","Decision Tree","Random Forest","Extra Trees",
            "XGBoost","LightGBM","CatBoost","AdaBoost","SVM","KNN","Naive Bayes"]}
        self.v_stack   = tk.BooleanVar(value=True)
        self.v_maxstd  = tk.DoubleVar(value=0.08)
        self.v_minauc  = tk.DoubleVar(value=0.83)
        self.v_thr     = tk.DoubleVar(value=0.5)
        self.v_cw      = tk.StringVar(value="balanced")
        self.v_shap_m  = tk.StringVar(value="Logistic Regression")
        self.v_prog    = tk.DoubleVar(value=0)
        self.v_status  = tk.StringVar(value="Ready — please load data first")

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TProgressbar", troughcolor="#E0E6EF",
                     background=C["accent"], thickness=8)
        s.configure("Treeview", font=FN, rowheight=28,
                     background=C["panel_bg"],
                     foreground=C["txt_dark"],
                     fieldbackground=C["panel_bg"])
        s.configure("Treeview.Heading", font=FB,
                     background=C["hdr_bg"], foreground="white")
        s.map("Treeview",
              background=[("selected", C["accent"])],
              foreground=[("selected", "white")])

    # ── Layout ────────────────────────────────────────────────
    def _build(self):
        self._mk_header()
        self._mk_tabbar()
        self._mk_pages()
        self._mk_statusbar()
        self._show("data")

    # ── Top header ────────────────────────────────────────────
    def _mk_header(self):
        h = tk.Frame(self, bg=C["hdr_bg"], height=50)
        h.pack(fill=tk.X)
        h.pack_propagate(False)
        # pill icon
        cv = tk.Canvas(h, width=28, height=28,
                       bg=C["hdr_bg"], highlightthickness=0)
        cv.place(x=16, rely=0.5, anchor="w")
        cv.create_oval(2, 2, 26, 26, fill=C["accent"], outline="white", width=1)
        cv.create_text(14, 14, text="💊", font=("Segoe UI", 12))
        tk.Label(h, text="PAP Statin Therapy Efficacy Prediction System",
                 font=("Segoe UI", 14, "bold"),
                 bg=C["hdr_bg"], fg="white").place(x=52, rely=0.5, anchor="w")
        tk.Label(h, text="v2.0",
                 font=FN9, bg=C["hdr_bg"], fg="#85C1E9").place(relx=1, x=-14, rely=0.5, anchor="e")

    # ── Horizontal tab bar ────────────────────────────────────
    def _mk_tabbar(self):
        bar = tk.Frame(self, bg=C["tab_bg"], height=40)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)
        self._tabs: dict[str, tk.Button] = {}
        items = [
            ("data",   "📂  Data Input"),
            ("feat",   "🔍  Feature Selection"),
            ("model",  "🤖  Model Config"),
            ("run",    "▶  Run Analysis"),
            ("result", "📊  Results"),
            ("shap",   "💡  SHAP"),
            ("about",  "ℹ  About"),
        ]
        for key, label in items:
            b = tk.Button(bar, text=label,
                          font=("Segoe UI", 10),
                          bg=C["tab_bg"], fg="#B8C9D9",
                          relief="flat", cursor="hand2",
                          padx=14, pady=0,
                          activebackground=C["tab_sel"],
                          activeforeground="white",
                          command=lambda k=key: self._show(k))
            b.pack(side=tk.LEFT, fill=tk.Y, padx=1)
            b.bind("<Enter>", lambda e, b=b: b.config(bg=C["tab_hov"])
                   if b.cget("bg") != C["tab_sel"] else None)
            b.bind("<Leave>", lambda e, b=b: b.config(bg=C["tab_bg"])
                   if b.cget("bg") == C["tab_hov"] else None)
            self._tabs[key] = b

    def _show(self, key):
        if key not in self._pages:
            return
        for pg in self._pages.values():
            pg.pack_forget()
        self._pages[key].pack(fill=tk.BOTH, expand=True)
        for k, b in self._tabs.items():
            b.config(bg=C["tab_sel"] if k == key else C["tab_bg"],
                     fg="white" if k == key else "#B8C9D9")

    # ── Pages container ───────────────────────────────────────
    def _mk_pages(self):
        self._pages: dict[str, tk.Frame] = {}
        for key, fn in [
            ("data",   self._pg_data),
            ("feat",   self._pg_feat),
            ("model",  self._pg_model),
            ("run",    self._pg_run),
            ("result", self._pg_result),
            ("shap",   self._pg_shap),
            ("about",  self._pg_about),
        ]:
            pg = tk.Frame(self, bg=C["page_bg"])
            fn(pg)
            self._pages[key] = pg

    # ── Status bar ────────────────────────────────────────────
    def _mk_statusbar(self):
        bar = tk.Frame(self, bg=C["hdr_bg"], height=26)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self.v_status,
                 font=FN9, bg=C["hdr_bg"], fg="#85C1E9").pack(side=tk.LEFT, padx=12)
        pb = ttk.Progressbar(bar, variable=self.v_prog,
                              maximum=100, length=200)
        pb.pack(side=tk.RIGHT, padx=12, pady=4)
        tk.Label(bar, text="PAP Statin Therapy Efficacy Prediction System  |  v2.0",
                 font=FN9, bg=C["hdr_bg"], fg="#4A6A80").pack(side=tk.RIGHT, padx=(0, 220))

    # ══════════════════════════════════════════════════════════
    # ── UI helpers ───────────────────────────────────────────
    # ══════════════════════════════════════════════════════════
    def _panel(self, parent, title="", expand=False, color=None):
        """White panel card with optional header"""
        outer = tk.Frame(parent, bg=C["panel_bg"],
                         highlightthickness=1,
                         highlightbackground=C["border"])
        if expand:
            outer.pack(fill=tk.BOTH, expand=True, pady=4)
        else:
            outer.pack(fill=tk.X, pady=4)
        if title:
            hdr = tk.Frame(outer, bg=color or C["hdr_bg"], height=32)
            hdr.pack(fill=tk.X)
            hdr.pack_propagate(False)
            tk.Label(hdr, text=f"  {title}",
                     font=FB, bg=color or C["hdr_bg"],
                     fg="white").pack(side=tk.LEFT, pady=4)
        inner = tk.Frame(outer, bg=C["panel_bg"])
        if expand:
            inner.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        else:
            inner.pack(fill=tk.X, padx=14, pady=10)
        return inner

    def _two_col(self, parent, pad=8):
        row = tk.Frame(parent, bg=C["page_bg"])
        row.pack(fill=tk.BOTH, expand=True, padx=pad, pady=4)
        L = tk.Frame(row, bg=C["page_bg"])
        L.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        R = tk.Frame(row, bg=C["page_bg"])
        R.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(4, 0))
        return L, R

    def _label(self, parent, text, font=None, fg=None, **kw):
        return tk.Label(parent, text=text,
                        font=font or FN, fg=fg or C["txt_dark"],
                        bg=C["panel_bg"], **kw)

    def _field_label(self, parent, text):
        tk.Label(parent, text=text, font=FB,
                 bg=C["panel_bg"], fg=C["txt_mid"]).pack(anchor="w", pady=(8, 2))

    def _entry(self, parent, var, width=28):
        e = tk.Entry(parent, textvariable=var, font=FN,
                     relief="solid", bd=1,
                     bg=C["input_bg"], fg=C["txt_dark"],
                     highlightthickness=2,
                     highlightcolor=C["accent"],
                     highlightbackground=C["border"],
                     insertbackground=C["accent"],
                     width=width)
        e.pack(anchor="w", ipady=5, pady=(0, 6))
        return e

    def _file_row(self, parent, label, var, ftypes):
        self._field_label(parent, label)
        row = tk.Frame(parent, bg=C["panel_bg"])
        row.pack(fill=tk.X, pady=(0, 6))
        e = tk.Entry(row, textvariable=var, font=FN,
                     relief="solid", bd=1,
                     bg=C["input_bg"], fg=C["txt_dark"],
                     highlightthickness=2,
                     highlightcolor=C["accent"],
                     highlightbackground=C["border"])
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        tk.Button(row, text="  Browse  ",
                  font=FN9, bg=C["accent"], fg="white",
                  relief="flat", cursor="hand2",
                  activebackground=C["hdr2"],
                  command=lambda: var.set(
                      filedialog.askopenfilename(filetypes=ftypes) or var.get()
                  )).pack(side=tk.LEFT, padx=(5, 0), ipady=5)

    def _dir_row(self, parent, label, var):
        self._field_label(parent, label)
        row = tk.Frame(parent, bg=C["panel_bg"])
        row.pack(fill=tk.X, pady=(0, 6))
        e = tk.Entry(row, textvariable=var, font=FN,
                     relief="solid", bd=1,
                     bg=C["input_bg"], fg=C["txt_dark"],
                     highlightthickness=2,
                     highlightcolor=C["accent"],
                     highlightbackground=C["border"])
        e.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        tk.Button(row, text="  Browse  ",
                  font=FN9, bg=C["txt_mid"], fg="white",
                  relief="flat", cursor="hand2",
                  command=lambda: var.set(
                      filedialog.askdirectory() or var.get()
                  )).pack(side=tk.LEFT, padx=(5, 0), ipady=5)

    def _spinbox(self, parent, var, from_, to, inc=1, width=10):
        sb = tk.Spinbox(parent, from_=from_, to=to, increment=inc,
                        textvariable=var, width=width, font=FN,
                        relief="solid", bd=1,
                        bg=C["input_bg"], fg=C["txt_dark"])
        sb.pack(anchor="w", ipady=4, pady=(0, 6))
        return sb

    def _check(self, parent, var, text, color=None):
        color = color or C["accent"]
        tk.Checkbutton(parent, variable=var, text=text,
                       font=FN, bg=C["panel_bg"], fg=C["txt_dark"],
                       activebackground=C["panel_bg"],
                       selectcolor=color, pady=3).pack(anchor="w")

    def _radio_row(self, parent, var, values):
        row = tk.Frame(parent, bg=C["panel_bg"])
        row.pack(anchor="w", pady=(0, 6))
        for v in values:
            tk.Radiobutton(row, text=v, variable=var, value=v,
                           font=FN, bg=C["panel_bg"], fg=C["txt_dark"],
                           activebackground=C["panel_bg"],
                           selectcolor=C["accent"]).pack(side=tk.LEFT, padx=(0, 12))

    def _btn(self, parent, text, cmd, bg=None, fg="white", side=None, **kw):
        bg = bg or C["accent"]
        b = tk.Button(parent, text=text, font=FB,
                      bg=bg, fg=fg, relief="flat",
                      cursor="hand2", padx=14, pady=6,
                      activebackground=C["hdr2"],
                      activeforeground="white",
                      command=cmd, **kw)
        b.bind("<Enter>", lambda e: b.config(bg=C["hdr2"]))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        if side:
            b.pack(side=side, padx=3)
        else:
            b.pack(padx=3)
        return b

    def _hint(self, parent, text):
        tk.Label(parent, text=text, font=FN9,
                 bg=C["panel_bg"], fg=C["txt_light"],
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 4))

    def _sep(self, parent):
        tk.Frame(parent, bg=C["border"], height=1).pack(fill=tk.X, pady=6)

    def _status_badge(self, parent, textvariable, ok_text="✓ Complete"):
        """Small green badge used in reference style"""
        lbl = tk.Label(parent, text="", font=FN9,
                       bg=C["panel_bg"], fg=C["green"])
        lbl.pack(side=tk.RIGHT, padx=8)
        return lbl

    # ══════════════════════════════════════════════════════════
    # Page: Data Input
    # ══════════════════════════════════════════════════════════
    def _pg_data(self, pg):
        L, R = self._two_col(pg, pad=12)

        # ── Left: file inputs ──
        c1_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c1_outer.pack(fill=tk.X, pady=4)
        hrow = tk.Frame(c1_outer, bg=C["panel_bg"])
        hrow.pack(fill=tk.X, padx=14, pady=(10, 0))
        tk.Label(hrow, text="📂  Data Input", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(side=tk.LEFT)
        self._train_badge = tk.Label(hrow, text="", font=FN9,
                                     bg=C["panel_bg"], fg=C["green"])
        self._train_badge.pack(side=tk.RIGHT)
        c1 = tk.Frame(c1_outer, bg=C["panel_bg"])
        c1.pack(fill=tk.X, padx=14, pady=(4, 12))

        self._file_row(c1, "Training Dataset (.xlsx / .xls)", self.v_train,
                       [("Excel files", "*.xlsx *.xls")])
        self.v_train.trace_add("write", lambda *_: self._train_badge.config(text="✓ Loaded"))
        self._hint(c1, "One sample per row, one feature per column, includes label column")
        btn_row1 = tk.Frame(c1, bg=C["panel_bg"])
        btn_row1.pack(anchor="w")
        self._btn(btn_row1, "Preview",
                  lambda: self._preview(self.v_train),
                  bg=C["txt_mid"], side=tk.LEFT)

        tk.Frame(c1, bg=C["border"], height=1).pack(fill=tk.X, pady=10)

        hrow2 = tk.Frame(c1, bg=C["panel_bg"])
        hrow2.pack(fill=tk.X)
        tk.Label(hrow2, text="Test Dataset (.xlsx / .xls)", font=FB,
                 bg=C["panel_bg"], fg=C["txt_mid"]).pack(side=tk.LEFT)
        self._test_badge = tk.Label(hrow2, text="", font=FN9,
                                    bg=C["panel_bg"], fg=C["green"])
        self._test_badge.pack(side=tk.RIGHT)
        self.v_test.trace_add("write", lambda *_: self._test_badge.config(text="✓ Loaded"))

        row_te = tk.Frame(c1, bg=C["panel_bg"])
        row_te.pack(fill=tk.X, pady=(3, 6))
        e_te = tk.Entry(row_te, textvariable=self.v_test, font=FN,
                        relief="solid", bd=1, bg=C["input_bg"], fg=C["txt_dark"],
                        highlightthickness=2, highlightcolor=C["accent"],
                        highlightbackground=C["border"])
        e_te.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        tk.Button(row_te, text="  Browse  ", font=FN9,
                  bg=C["accent"], fg="white", relief="flat", cursor="hand2",
                  activebackground=C["hdr2"],
                  command=lambda: self.v_test.set(
                      filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")]) or self.v_test.get()
                  )).pack(side=tk.LEFT, padx=(5, 0), ipady=5)
        self._hint(c1, "Same feature columns as training set, includes label column")
        btn_row2 = tk.Frame(c1, bg=C["panel_bg"])
        btn_row2.pack(anchor="w")
        self._btn(btn_row2, "Preview",
                  lambda: self._preview(self.v_test),
                  bg=C["txt_mid"], side=tk.LEFT)

        # ── Data Summary panel (like reference) ──
        sum_outer = tk.Frame(L, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        sum_outer.pack(fill=tk.X, pady=4)
        tk.Label(sum_outer, text="📋  Data Summary", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        sum_inner = tk.Frame(sum_outer, bg="#F8FAFC",
                             highlightthickness=1, highlightbackground=C["border"])
        sum_inner.pack(fill=tk.X, padx=14, pady=(0, 12))
        self._sum_rows: dict = {}
        for key, label in [("Label Column", "Label Column:"),
                            ("Training Samples", "Training Samples:"),
                            ("Test Samples", "Test Samples:"),
                            ("Features", "Features:"),
                            ("Status", "Status:")]:
            row = tk.Frame(sum_inner, bg="#F8FAFC")
            row.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(row, text=label, font=FN, bg="#F8FAFC",
                     fg=C["txt_mid"], width=18, anchor="w").pack(side=tk.LEFT)
            lbl = tk.Label(row, text="—", font=FN,
                           bg="#F8FAFC", fg=C["txt_dark"])
            lbl.pack(side=tk.LEFT)
            self._sum_rows[key] = lbl
        tk.Button(sum_outer, text="Load & Validate Data",
                  font=FB, bg=C["green"], fg="white",
                  relief="flat", cursor="hand2", padx=14, pady=6,
                  activebackground="#1E8449",
                  command=self._load_preview_data).pack(anchor="w", padx=14, pady=(0, 12))

        # ── Right: configuration ──
        c3_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c3_outer.pack(fill=tk.X, pady=4)
        tk.Label(c3_outer, text="⚙  Analysis Configuration", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c3 = tk.Frame(c3_outer, bg=C["panel_bg"])
        c3.pack(fill=tk.X, padx=14, pady=(0, 12))

        self._field_label(c3, "Label Column Name")
        self._entry(c3, self.v_label, width=22)
        self._hint(c3, "Target column in Excel  (e.g. Label, Y, Diagnosis) — 0=control, 1=case")

        self._dir_row(c3, "Output File Path:", self.v_outdir)
        self._hint(c3, "Destination for charts (PDF/PNG/SVG) and Excel reports")

        self._sep(c3)

        self._field_label(c3, "Figure Format")
        self._radio_row(c3, self.v_fmt, ["pdf", "png", "svg"])

        self._field_label(c3, "Figure DPI (Resolution)")
        self._spinbox(c3, self.v_dpi, 72, 2400, 100)

        # format notes
        c4_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c4_outer.pack(fill=tk.X, pady=4)
        tk.Label(c4_outer, text="📖  Data Format Requirements", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c4 = tk.Frame(c4_outer, bg=C["panel_bg"])
        c4.pack(fill=tk.X, padx=14, pady=(0, 12))
        for txt in [
            "•  Format: Excel (.xlsx / .xls), rows = samples, columns = features",
            "•  Must include a binary label column  (0 = control,  1 = case)",
            "•  Feature columns must be numeric; missing values handled automatically",
            "•  Recommended: training set ≥ 50 rows,  test set ≥ 20 rows",
            "•  Training and test sets must share identical feature column names",
        ]:
            tk.Label(c4, text=txt, font=FN, bg=C["panel_bg"],
                     fg=C["txt_mid"], anchor="w").pack(anchor="w", pady=2)

    def _load_preview_data(self):
        try:
            import pandas as pd
            tr = self.v_train.get(); te = self.v_test.get()
            lbl = self.v_label.get()
            if not tr or not te:
                messagebox.showwarning("Warning", "Please select both training and test files first.")
                return
            df_tr = pd.read_excel(tr)
            df_te = pd.read_excel(te)
            n_feat = df_tr.shape[1] - 1
            self._sum_rows["Label Column"].config(text=lbl)
            self._sum_rows["Training Samples"].config(
                text=f"{len(df_tr)}  (pos={int(df_tr[lbl].sum())}, neg={int((df_tr[lbl]==0).sum())})")
            self._sum_rows["Test Samples"].config(text=str(len(df_te)))
            self._sum_rows["Features"].config(text=str(n_feat))
            self._sum_rows["Status"].config(text="✓ All files loaded", fg=C["green"])
        except Exception as e:
            self._sum_rows["Status"].config(text=f"✗ Error: {e}", fg=C["red"])

    # ══════════════════════════════════════════════════════════
    # Page: Feature Selection
    # ══════════════════════════════════════════════════════════
    def _pg_feat(self, pg):
        L, R = self._two_col(pg, pad=12)

        # Left: method checkboxes
        c1_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c1_outer.pack(fill=tk.BOTH, expand=True, pady=4)
        tk.Label(c1_outer, text="🔍  Feature Selection Methods",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c1 = tk.Frame(c1_outer, bg=C["panel_bg"])
        c1.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        methods = [
            (self.v_lasso,  "Lasso  (L1 Regularization)",
             "Shrinks unimportant feature coefficients to zero; retains non-zero features", C["red"]),
            (self.v_rfe,    "RFE  (Recursive Feature Elimination)",
             "Iteratively removes least important features based on logistic regression weights", C["accent"]),
            (self.v_rf_fs,  "Random Forest Importance",
             "Ranks features by mean impurity decrease (Gini) across all trees", C["green"]),
            (self.v_xgb_fs, "XGBoost Importance",
             "Measures feature contribution via gain, coverage, and frequency", C["orange"]),
            (self.v_mi,     "Mutual Information",
             "Quantifies non-linear statistical dependence between features and label", C["purple"]),
            (self.v_kbest,  "SelectKBest  (ANOVA F-test)",
             "Ranks features by univariate ANOVA F-statistic; fast and straightforward", C["cyan"]),
        ]
        for var, name, desc, col in methods:
            row = tk.Frame(c1, bg="#F8FAFC",
                           highlightbackground=C["border"], highlightthickness=1)
            row.pack(fill=tk.X, pady=3)
            tk.Frame(row, bg=col, width=4).pack(side=tk.LEFT, fill=tk.Y)
            inner = tk.Frame(row, bg="#F8FAFC")
            inner.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=7)
            tk.Checkbutton(inner, variable=var, text=name,
                           font=FB, bg="#F8FAFC", fg=C["txt_dark"],
                           activebackground="#F8FAFC",
                           selectcolor=col).pack(anchor="w")
            tk.Label(inner, text=desc, font=FN9,
                     bg="#F8FAFC", fg=C["txt_light"]).pack(anchor="w")

        btn_row = tk.Frame(c1, bg=C["panel_bg"])
        btn_row.pack(fill=tk.X, pady=(8, 0))
        self._btn(btn_row, "Select All",
                  lambda: [v.set(True) for v in [self.v_lasso,self.v_rfe,self.v_rf_fs,self.v_xgb_fs,self.v_mi,self.v_kbest]],
                  bg=C["green"], side=tk.LEFT)
        self._btn(btn_row, "Clear All",
                  lambda: [v.set(False) for v in [self.v_lasso,self.v_rfe,self.v_rf_fs,self.v_xgb_fs,self.v_mi,self.v_kbest]],
                  bg=C["txt_mid"], side=tk.LEFT)

        # Right: parameters
        c2_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c2_outer.pack(fill=tk.X, pady=4)
        tk.Label(c2_outer, text="⚙  Algorithm Parameters",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c2 = tk.Frame(c2_outer, bg=C["panel_bg"])
        c2.pack(fill=tk.X, padx=14, pady=(0, 12))

        for label, var, fr, to, inc, tip in [
            ("CV Folds",        self.v_cvfolds, 3, 20, 1,
             "Number of folds for cross-validation; 5–10 recommended"),
            ("Early Stopping Patience", self.v_patience, 5, 80, 5,
             "Stop search when AUC has not improved for N consecutive steps"),
            ("Min AUC Improvement", self.v_minimp, 0.0001, 0.05, 0.001,
             "Minimum AUC gain required to count as a meaningful improvement"),
        ]:
            self._field_label(c2, label)
            self._spinbox(c2, var, fr, to, inc)
            self._hint(c2, tip)

        c3_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c3_outer.pack(fill=tk.X, pady=4)
        tk.Label(c3_outer, text="📖  Selection Strategy",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c3 = tk.Frame(c3_outer, bg=C["panel_bg"])
        c3.pack(fill=tk.X, padx=14, pady=(0, 12))
        tk.Label(c3, text=(
            "All selected methods run automatically. Performance is\n"
            "evaluated via cross-validated AUC on the training set.\n"
            "The method achieving the highest CV AUC supplies the\n"
            "final feature subset for downstream modelling.\n\n"
            "  Lasso          :  Natural selection (non-zero coefficients)\n"
            "  Other 5 methods:  Incremental search with early stopping"
        ), font=FN, bg=C["panel_bg"], fg=C["txt_mid"], justify="left").pack(anchor="w")

    # ══════════════════════════════════════════════════════════
    # Page: Model Config
    # ══════════════════════════════════════════════════════════
    def _pg_model(self, pg):
        L, R = self._two_col(pg, pad=12)

        # Left: base classifiers
        c1_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c1_outer.pack(fill=tk.BOTH, expand=True, pady=4)
        tk.Label(c1_outer, text="🤖  Base Classifiers",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c1 = tk.Frame(c1_outer, bg=C["panel_bg"])
        c1.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))

        meta = {
            "Logistic Regression": ("Linear model; highly interpretable",       C["accent"]),
            "Decision Tree":       ("Tree model; intuitive splits",             C["orange"]),
            "Random Forest":       ("Bagging ensemble; stable performance",     C["green"]),
            "Extra Trees":         ("Extremely randomised trees",               C["green"]),
            "XGBoost":             ("Gradient boosting; high accuracy",         C["yellow"]),
            "LightGBM":            ("Histogram boosting; fast training",        C["yellow"]),
            "CatBoost":            ("Boosting with categorical support",        C["red"]),
            "AdaBoost":            ("Adaptive boosting",                        C["orange"]),
            "SVM":                 ("Support Vector Machine; kernel trick",     C["purple"]),
            "KNN":                 ("K-Nearest Neighbours; non-parametric",     C["cyan"]),
            "Naive Bayes":         ("Naïve Bayes; extremely fast",              C["txt_light"]),
        }
        cols_frame = tk.Frame(c1, bg=C["panel_bg"])
        cols_frame.pack(fill=tk.X)
        ca = tk.Frame(cols_frame, bg=C["panel_bg"])
        ca.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))
        cb = tk.Frame(cols_frame, bg=C["panel_bg"])
        cb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for i, (name, var) in enumerate(self.mv.items()):
            col_parent = ca if i < 6 else cb
            desc, col = meta[name]
            row = tk.Frame(col_parent, bg="#F8FAFC",
                           highlightbackground=C["border"], highlightthickness=1)
            row.pack(fill=tk.X, pady=2)
            tk.Frame(row, bg=col, width=4).pack(side=tk.LEFT, fill=tk.Y)
            inner = tk.Frame(row, bg="#F8FAFC")
            inner.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, pady=5)
            tk.Checkbutton(inner, variable=var, text=name,
                           font=FB, bg="#F8FAFC", fg=C["txt_dark"],
                           activebackground="#F8FAFC",
                           selectcolor=col).pack(anchor="w")
            tk.Label(inner, text=desc, font=FN9,
                     bg="#F8FAFC", fg=C["txt_light"]).pack(anchor="w")

        btn_row = tk.Frame(c1, bg=C["panel_bg"])
        btn_row.pack(fill=tk.X, pady=(8, 0))
        self._btn(btn_row, "Select All",
                  lambda: [v.set(True)  for v in self.mv.values()],
                  bg=C["green"], side=tk.LEFT)
        self._btn(btn_row, "Clear All",
                  lambda: [v.set(False) for v in self.mv.values()],
                  bg=C["txt_mid"], side=tk.LEFT)

        # Right: Stacking config
        c2_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c2_outer.pack(fill=tk.X, pady=4)
        tk.Label(c2_outer, text="🔗  Stacking Ensemble Configuration",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c2 = tk.Frame(c2_outer, bg=C["panel_bg"])
        c2.pack(fill=tk.X, padx=14, pady=(0, 12))

        tk.Checkbutton(c2, variable=self.v_stack,
                       text="  Enable Stacking Ensemble",
                       font=("Segoe UI", 11, "bold"),
                       bg=C["panel_bg"], fg=C["txt_dark"],
                       activebackground=C["panel_bg"],
                       selectcolor=C["green"]).pack(anchor="w", pady=(0, 10))
        self._sep(c2)

        for label, var, fr, to, inc, tip in [
            ("Max CV Std Dev (base learner)", self.v_maxstd, 0.01, 0.30, 0.01,
             "Exclude learners whose CV std exceeds this threshold (unstable)"),
            ("Min CV AUC (base learner)",     self.v_minauc, 0.50, 0.99, 0.01,
             "Exclude learners whose CV AUC falls below this threshold (weak)"),
            ("Classification Threshold",      self.v_thr,   0.10, 0.90, 0.05,
             "Probability ≥ threshold → positive class prediction (default 0.5)"),
        ]:
            self._field_label(c2, label)
            self._spinbox(c2, var, fr, to, inc)
            self._hint(c2, tip)

        self._field_label(c2, "Class Weight")
        self._radio_row(c2, self.v_cw, ["balanced", "none"])

        c3_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c3_outer.pack(fill=tk.X, pady=4)
        tk.Label(c3_outer, text="📖  Stacking Principle",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c3 = tk.Frame(c3_outer, bg=C["panel_bg"])
        c3.pack(fill=tk.X, padx=14, pady=(0, 12))
        tk.Label(c3, text=(
            "Stage 1 — Base Learners\n"
            "  Each classifier generates out-of-fold predicted probabilities\n"
            "  on the training set via cross-validation.\n\n"
            "Stage 2 — Meta Learner\n"
            "  A logistic regression learns to optimally combine the\n"
            "  outputs of all base learners.\n\n"
            "Dynamic Filtering\n"
            "  Only learners with low CV variance and adequate AUC\n"
            "  are admitted to the ensemble."
        ), font=FN, bg=C["panel_bg"], fg=C["txt_mid"], justify="left").pack(anchor="w")

    # ══════════════════════════════════════════════════════════
    # Page: Run Analysis
    # ══════════════════════════════════════════════════════════
    def _pg_run(self, pg):
        # top control strip
        ctrl = tk.Frame(pg, bg=C["page_bg"])
        ctrl.pack(fill=tk.X, padx=12, pady=(8, 0))

        ctrl_card = tk.Frame(ctrl, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        ctrl_card.pack(fill=tk.X)
        inner_ctrl = tk.Frame(ctrl_card, bg=C["panel_bg"])
        inner_ctrl.pack(padx=14, pady=10, anchor="w", side=tk.LEFT)

        self.run_btn = self._btn(inner_ctrl, "  ▶  Start Analysis  ",
                                 self._start, bg=C["green"], side=tk.LEFT)
        self.stop_btn = tk.Button(inner_ctrl, text="  ⏹  Stop  ",
                                  font=FB, bg=C["red"], fg="white",
                                  relief="flat", cursor="hand2", state=tk.DISABLED,
                                  command=self._stop)
        self.stop_btn.pack(side=tk.LEFT, padx=4, ipady=6)
        self._btn(inner_ctrl, "Clear Log",
                  lambda: self.log_box.delete("1.0", tk.END),
                  bg=C["txt_mid"], side=tk.LEFT)

        right_ctrl = tk.Frame(ctrl_card, bg=C["panel_bg"])
        right_ctrl.pack(side=tk.RIGHT, padx=14, pady=10)
        self._btn(right_ctrl, "📂  Open Output Directory",
                  self._open_outdir, bg=C["accent"], side=tk.RIGHT)

        # progress card
        prog_card = tk.Frame(pg, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        prog_card.pack(fill=tk.X, padx=12, pady=4)
        prog_inner = tk.Frame(prog_card, bg=C["panel_bg"])
        prog_inner.pack(fill=tk.X, padx=14, pady=10)

        tk.Label(prog_inner, text="Analysis Progress:", font=FB,
                 bg=C["panel_bg"], fg=C["txt_mid"]).pack(anchor="w")
        pb_row = tk.Frame(prog_inner, bg=C["panel_bg"])
        pb_row.pack(fill=tk.X, pady=(4, 6))
        self._pb = ttk.Progressbar(pb_row, variable=self.v_prog,
                                   maximum=100)
        self._pb.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._pct_lbl = tk.Label(pb_row, text="0%", font=FN9,
                                 bg=C["panel_bg"], fg=C["accent"], width=6)
        self._pct_lbl.pack(side=tk.LEFT, padx=6)
        self.v_prog.trace_add("write", lambda *_: self._pct_lbl.config(
            text=f"{int(self.v_prog.get())}%"))

        # stage dots
        stage_row = tk.Frame(prog_inner, bg=C["panel_bg"])
        stage_row.pack(fill=tk.X)
        self._stage_dots: dict[str, tk.Label] = {}
        stages = ["Data Load", "Imputation", "Feature Sel.",
                  "Base Models", "Stacking", "Visualise", "SHAP"]
        for i, s in enumerate(stages):
            sf = tk.Frame(stage_row, bg=C["panel_bg"])
            sf.pack(side=tk.LEFT, expand=True)
            dot = tk.Label(sf, text="○", font=("Segoe UI", 14),
                           bg=C["panel_bg"], fg=C["border"])
            dot.pack()
            tk.Label(sf, text=s, font=FN9,
                     bg=C["panel_bg"], fg=C["txt_light"]).pack()
            self._stage_dots[s] = dot
            if i < len(stages) - 1:
                tk.Label(stage_row, text="─", font=FN,
                         bg=C["panel_bg"], fg=C["border"]).pack(side=tk.LEFT)

        # completion badge
        self._done_lbl = tk.Label(prog_inner, text="", font=FN,
                                  bg=C["panel_bg"], fg=C["green"])
        self._done_lbl.pack(anchor="w", pady=(4, 0))

        # log
        log_wrap = tk.Frame(pg, bg=C["page_bg"])
        log_wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        log_outer = tk.Frame(log_wrap, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        log_outer.pack(fill=tk.BOTH, expand=True)
        tk.Label(log_outer, text="  📄  Live Run Log", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=4, pady=(8, 0))
        log_inner = tk.Frame(log_outer, bg=C["panel_bg"])
        log_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
        self.log_box = scrolledtext.ScrolledText(
            log_inner, font=FMN, height=16,
            bg="#0D1520", fg="#A8D8EA",
            insertbackground="white", relief="flat", wrap=tk.WORD)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        for tag, fg in [("info","#5DADE2"),("ok","#2ECC71"),
                        ("warn","#F39C12"),("err","#E74C3C"),("sec","#F8C471")]:
            self.log_box.tag_config(tag, foreground=fg)
        self._log("System ready — load data first, then click  ▶ Start Analysis", "info")

    # ══════════════════════════════════════════════════════════
    # Page: Results
    # ══════════════════════════════════════════════════════════
    def _pg_result(self, pg):
        ctrl = tk.Frame(pg, bg=C["page_bg"])
        ctrl.pack(fill=tk.X, padx=12, pady=(8, 0))
        ctrl_card = tk.Frame(ctrl, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        ctrl_card.pack(fill=tk.X)
        inner = tk.Frame(ctrl_card, bg=C["panel_bg"])
        inner.pack(padx=12, pady=8, anchor="w", side=tk.LEFT)
        self._btn(inner, "🔄  Refresh Results", self._refresh_results, side=tk.LEFT)
        self._btn(inner, "📂  Open Output Directory", self._open_outdir,
                  bg=C["txt_mid"], side=tk.LEFT)

        wrap = tk.Frame(pg, bg=C["page_bg"])
        wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        # results header
        res_hdr = tk.Frame(wrap, bg=C["panel_bg"],
                           highlightthickness=1, highlightbackground=C["border"])
        res_hdr.pack(fill=tk.X, pady=(0, 4))
        hdr_inner = tk.Frame(res_hdr, bg=C["panel_bg"])
        hdr_inner.pack(fill=tk.X, padx=14, pady=8)
        tk.Label(hdr_inner, text="📈  Run Analysis & Results", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(side=tk.LEFT)

        # metric summary strip (like reference cards)
        self._metric_strip = tk.Frame(wrap, bg=C["page_bg"])
        self._metric_strip.pack(fill=tk.X, pady=(0, 4))
        self._metric_cards: dict = {}
        for title in ["Best Model", "Best CV AUC", "Best Test AUC", "Best F1"]:
            mc = tk.Frame(self._metric_strip, bg=C["panel_bg"],
                          highlightthickness=1, highlightbackground=C["border"])
            mc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)
            tk.Label(mc, text=title, font=FN9,
                     bg=C["panel_bg"], fg=C["txt_mid"]).pack(pady=(8, 0))
            val_lbl = tk.Label(mc, text="—", font=("Segoe UI", 16, "bold"),
                               bg=C["panel_bg"], fg=C["accent"])
            val_lbl.pack(pady=(0, 8))
            self._metric_cards[title] = val_lbl

        # table
        tbl_outer = tk.Frame(wrap, bg=C["panel_bg"],
                             highlightthickness=1, highlightbackground=C["border"])
        tbl_outer.pack(fill=tk.BOTH, expand=True)
        tk.Label(tbl_outer, text="  Top Results Preview", font=FB,
                 bg=C["panel_bg"], fg=C["txt_mid"]).pack(anchor="w", padx=4, pady=(6, 2))
        cols = ["Model", "CV AUC", "CV Std", "Test AUC", "Precision", "Recall", "F1"]
        self.result_tv = ttk.Treeview(tbl_outer, columns=cols, show="headings", height=14)
        for col in cols:
            self.result_tv.heading(col, text=col)
            w = 220 if col == "Model" else 90
            self.result_tv.column(col, width=w, anchor="center" if col != "Model" else "w")
        ysb = ttk.Scrollbar(tbl_outer, orient="vertical", command=self.result_tv.yview)
        self.result_tv.configure(yscrollcommand=ysb.set)
        self.result_tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_tv.tag_configure("stk", background="#FADBD8", foreground="#C0392B")
        self.result_tv.tag_configure("odd", background=C["panel_bg"])
        self.result_tv.tag_configure("evn", background="#EBF5FB")
        tk.Label(wrap, text="💡  Stacking Ensemble rows are highlighted in red  |  Full Excel report saved to output directory",
                 font=FN9, bg=C["page_bg"], fg=C["txt_light"]).pack(pady=4)

    # ══════════════════════════════════════════════════════════
    # Page: SHAP
    # ══════════════════════════════════════════════════════════
    def _pg_shap(self, pg):
        L, R = self._two_col(pg, pad=12)

        c1_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c1_outer.pack(fill=tk.X, pady=4)
        tk.Label(c1_outer, text="💡  SHAP Interpretability Analysis",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c1 = tk.Frame(c1_outer, bg=C["panel_bg"])
        c1.pack(fill=tk.X, padx=14, pady=(0, 12))

        tk.Label(c1, text="Select target model  (complete full analysis first):",
                 font=FB, bg=C["panel_bg"], fg=C["txt_mid"]).pack(anchor="w", pady=(0, 6))
        for m in ["Logistic Regression","Random Forest","XGBoost","LightGBM","CatBoost","Extra Trees"]:
            tk.Radiobutton(c1, variable=self.v_shap_m, value=m, text=m,
                           font=FN, bg=C["panel_bg"], fg=C["txt_dark"],
                           activebackground=C["panel_bg"],
                           selectcolor=C["accent"]).pack(anchor="w", pady=2)
        self._btn(c1, "  💡  Run SHAP Analysis  ",
                  self._run_shap_standalone, bg=C["purple"])

        c2_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c2_outer.pack(fill=tk.X, pady=4)
        tk.Label(c2_outer, text="📊  Output Charts",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c2 = tk.Frame(c2_outer, bg=C["panel_bg"])
        c2.pack(fill=tk.X, padx=14, pady=(0, 12))
        for title, desc in [
            ("Feature Importance Bar Chart", "Ranked mean(|SHAP value|) — global view"),
            ("Summary Beeswarm Plot",        "Full magnitude and directional breakdown"),
            ("Top-3 Dependence Plots",       "Feature value vs SHAP value relationships"),
        ]:
            f = tk.Frame(c2, bg=C["panel_bg"])
            f.pack(fill=tk.X, pady=4)
            tk.Label(f, text="  ●  " + title, font=FB,
                     bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w")
            tk.Label(f, text="      " + desc, font=FN9,
                     bg=C["panel_bg"], fg=C["txt_light"]).pack(anchor="w")

        # Right: principle + log
        c3_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c3_outer.pack(fill=tk.X, pady=4)
        tk.Label(c3_outer, text="📖  SHAP Overview",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c3 = tk.Frame(c3_outer, bg=C["panel_bg"])
        c3.pack(fill=tk.X, padx=14, pady=(0, 12))
        tk.Label(c3, text=(
            "SHAP (SHapley Additive exPlanations)\n"
            "provides instance-level feature attribution grounded in game theory.\n\n"
            "Key advantages:\n"
            "  • Global interpretability: identifies most predictive features\n"
            "  • Local interpretability: explains individual predictions\n"
            "  • Directionality: positive SHAP increases, negative decreases risk\n"
            "  • Consistency: satisfies fair allocation axioms from game theory\n\n"
            "Explainer selection:\n"
            "  • Linear models   → LinearExplainer  (fast)\n"
            "  • Tree models     → TreeExplainer    (exact & efficient)\n"
            "  • General models  → KernelExplainer"
        ), font=FN, bg=C["panel_bg"], fg=C["txt_mid"], justify="left").pack(anchor="w")

        c4_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c4_outer.pack(fill=tk.BOTH, expand=True, pady=4)
        tk.Label(c4_outer, text="  📄  SHAP Run Log", font=FH,
                 bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=4, pady=(8, 0))
        c4 = tk.Frame(c4_outer, bg=C["panel_bg"])
        c4.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
        self.shap_log = scrolledtext.ScrolledText(
            c4, font=FMN, height=12,
            bg="#0D1520", fg="#A8D8EA",
            relief="flat", wrap=tk.WORD)
        self.shap_log.pack(fill=tk.BOTH, expand=True)
        for tag, fg in [("ok","#2ECC71"),("err","#E74C3C"),("info","#5DADE2")]:
            self.shap_log.tag_config(tag, foreground=fg)

    # ══════════════════════════════════════════════════════════
    # Page: About
    # ══════════════════════════════════════════════════════════
    def _pg_about(self, pg):
        L, R = self._two_col(pg, pad=12)

        c1_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c1_outer.pack(fill=tk.X, pady=4)
        tk.Label(c1_outer, text="🏥  System Overview",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c1 = tk.Frame(c1_outer, bg=C["panel_bg"])
        c1.pack(fill=tk.X, padx=14, pady=(0, 12))
        tk.Label(c1, text=(
            "This platform is specifically designed for clinical prediction\n"
            "research in Pulmonary Alveolar Proteinosis (PAP), providing\n"
            "a complete, automated machine learning workflow.\n\n"
            "Stage 1 — Adaptive Feature Selection\n"
            "  6 selectable methods; automatic early stopping;\n"
            "  outputs per-method AUC comparison and the optimal\n"
            "  feature subset for downstream modelling.\n\n"
            "Stage 2 — Stacking Ensemble Modelling\n"
            "  11 base classifiers are trained and evaluated; unstable\n"
            "  or low-performing learners are filtered out dynamically.\n"
            "  A logistic regression meta-learner integrates predictions.\n"
            "  SHAP interpretability and full PDF/PNG/SVG charts output."
        ), font=FN, bg=C["panel_bg"], fg=C["txt_mid"], justify="left").pack(anchor="w")

        c2_outer = tk.Frame(L, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c2_outer.pack(fill=tk.X, pady=4)
        tk.Label(c2_outer, text="🚀  Quick Start Guide",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c2 = tk.Frame(c2_outer, bg=C["panel_bg"])
        c2.pack(fill=tk.X, padx=14, pady=(0, 12))
        steps = [
            ("1", "Data Input",        "Load training and test Excel files; configure label column"),
            ("2", "Feature Selection", "Choose methods; configure early stopping and CV folds"),
            ("3", "Model Config",      "Select classifiers; configure Stacking strategy"),
            ("4", "Run Analysis",      "Click  ▶ Start Analysis  and monitor live log"),
            ("5", "Results",           "Click  Refresh Results  to view performance comparison table"),
            ("6", "SHAP",              "Select target model and generate interpretability report"),
        ]
        for num, title, desc in steps:
            row = tk.Frame(c2, bg=C["panel_bg"])
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=f" {num} ", font=FB,
                     bg=C["accent"], fg="white", padx=6, pady=3).pack(side=tk.LEFT)
            inner = tk.Frame(row, bg=C["panel_bg"])
            inner.pack(side=tk.LEFT, padx=10)
            tk.Label(inner, text=title, font=FB,
                     bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w")
            tk.Label(inner, text=desc, font=FN9,
                     bg=C["panel_bg"], fg=C["txt_light"]).pack(anchor="w")

        # Right: FAQ + system info
        c3_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c3_outer.pack(fill=tk.X, pady=4)
        tk.Label(c3_outer, text="❓  Frequently Asked Questions",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c3 = tk.Frame(c3_outer, bg=C["panel_bg"])
        c3.pack(fill=tk.X, padx=14, pady=(0, 12))
        faqs = [
            ("How should I prepare the input data?",
             "Excel format; one sample per row, one feature per column; binary label (0/1); missing values are imputed automatically"),
            ("How do I speed up the analysis?",
             "Reduce the number of feature selection methods, increase patience value, or use fewer base classifiers"),
            ("What if SHAP analysis fails?",
             "Ensure full analysis is complete first; linear models are fastest; tree models use the exact TreeExplainer"),
            ("Why was a model excluded from Stacking?",
             "The model's CV std or CV AUC failed the thresholds set on the Model Config page; adjust those thresholds to include it"),
        ]
        for q, a in faqs:
            box = tk.Frame(c3, bg="#EBF5FB",
                           highlightbackground=C["border"], highlightthickness=1)
            box.pack(fill=tk.X, pady=4)
            tk.Label(box, text=f"  Q  {q}", font=FB,
                     bg=C["accent"], fg="white", padx=8, pady=4).pack(fill=tk.X, anchor="w")
            tk.Label(box, text=f"  A  {a}", font=FN,
                     bg="#EBF5FB", fg=C["txt_mid"],
                     justify="left", padx=12, pady=5, wraplength=300).pack(anchor="w")

        c4_outer = tk.Frame(R, bg=C["panel_bg"],
                            highlightthickness=1, highlightbackground=C["border"])
        c4_outer.pack(fill=tk.X, pady=4)
        tk.Label(c4_outer, text="📋  System Information",
                 font=FH, bg=C["panel_bg"], fg=C["txt_dark"]).pack(anchor="w", padx=14, pady=(10, 4))
        c4 = tk.Frame(c4_outer, bg=C["panel_bg"])
        c4.pack(fill=tk.X, padx=14, pady=(0, 12))
        for k, v in [
            ("System",      "PAP Statin Therapy Efficacy Prediction System"),
            ("Version",     "v2.0"),
            ("Year",        "2025"),
            ("Algorithms",  "Lasso / RFE / RF / XGBoost / MI / SelectKBest / Stacking / SHAP"),
            ("Dependencies","scikit-learn  xgboost  lightgbm  catboost  shap  pandas  matplotlib"),
        ]:
            row = tk.Frame(c4, bg=C["panel_bg"])
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=k + ":", font=FB,
                     bg=C["panel_bg"], fg=C["txt_mid"],
                     width=12, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=v, font=FN,
                     bg=C["panel_bg"], fg=C["txt_dark"],
                     wraplength=280, justify="left").pack(side=tk.LEFT)

    # ══════════════════════════════════════════════════════════
    # Analysis logic  (unchanged from original)
    # ══════════════════════════════════════════════════════════
    def _start(self):
        if self._running: return
        if not self.v_train.get() or not self.v_test.get():
            messagebox.showerror("Error", "Please load training and test datasets first!")
            return
        if not any(v.get() for v in self.mv.values()):
            messagebox.showerror("Error", "Please select at least one classifier!")
            return
        if not any([self.v_lasso.get(),self.v_rfe.get(),self.v_rf_fs.get(),
                    self.v_xgb_fs.get(),self.v_mi.get(),self.v_kbest.get()]):
            messagebox.showerror("Error", "Please select at least one feature selection method!")
            return
        self._running = True
        self.run_btn.config(state=tk.DISABLED, bg=C["txt_light"])
        self.stop_btn.config(state=tk.NORMAL)
        self.v_prog.set(0)
        self._done_lbl.config(text="")
        self._reset_dots()
        self._log("", "")
        self._log("═" * 60, "sec")
        self._log("  PAP Statin Therapy Efficacy Prediction System  v2.0", "sec")
        self._log("═" * 60, "sec")
        threading.Thread(target=self._thread_entry, daemon=True).start()

    def _stop(self):
        self._running = False
        self.v_status.set("⚠ Stopped by user")
        self._log("\n⚠  Analysis stopped by user.", "warn")
        self.run_btn.config(state=tk.NORMAL, bg=C["green"])
        self.stop_btn.config(state=tk.DISABLED)

    def _thread_entry(self):
        try:
            self._full_analysis()
        except Exception:
            import traceback
            self._log(f"\n❌ Runtime error:\n{traceback.format_exc()}", "err")
            self.v_status.set("❌ Error")
        finally:
            self._running = False
            self.after(0, lambda: self.run_btn.config(state=tk.NORMAL, bg=C["green"]))
            self.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))

    def _full_analysis(self):
        import numpy as np, pandas as pd

        self._dot("Data Load", "run")
        self._log("\n[1/7]  Loading data...", "info")
        self.v_status.set("Loading data...")
        try:
            tr_df = pd.read_excel(self.v_train.get())
            te_df = pd.read_excel(self.v_test.get())
            lbl   = self.v_label.get()
            X_tr, y_tr = tr_df.drop(lbl, axis=1), tr_df[lbl]
            X_te, y_te = te_df.drop(lbl, axis=1), te_df[lbl]
            self._log(f"  ✓ Training set {tr_df.shape}  |  Test set {te_df.shape}", "ok")
            self._log(f"  ✓ Positive cases (train): {int(y_tr.sum())}  Negative: {int((y_tr==0).sum())}", "ok")
        except Exception as e:
            self._log(f"  ❌ Load failed: {e}", "err")
            self._dot("Data Load", "err"); return
        self._dot("Data Load", "ok"); self.v_prog.set(10)
        if not self._running: return

        self._dot("Imputation", "run")
        self._log("\n[2/7]  Missing value imputation...", "info")
        self.v_status.set("Imputing missing values...")
        X_tr, X_te = self._impute(X_tr, X_te, y_tr, y_te)
        self._log(f"  ✓ Valid features: {X_tr.shape[1]}", "ok")
        self._dot("Imputation", "ok"); self.v_prog.set(18)
        if not self._running: return

        self._dot("Feature Sel.", "run")
        self._log("\n[3/7]  Adaptive feature selection...", "info")
        self.v_status.set("Selecting features...")
        feats = self._feature_selection(X_tr, y_tr)
        if not feats:
            self._log("  ❌ Feature selection failed", "err")
            self._dot("Feature Sel.", "err"); return
        self._log(f"  ★ Final features ({len(feats)}): {feats}", "ok")
        self._dot("Feature Sel.", "ok"); self.v_prog.set(38)
        if not self._running: return

        self._dot("Base Models", "run")
        self._log("\n[4/7]  Training base classifiers...", "info")
        self.v_status.set("Training base classifiers...")
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_tr_sc = sc.fit_transform(X_tr[feats])
        X_te_sc = sc.transform(X_te[feats])
        self._stored = {"Xtr": X_tr_sc, "Xte": X_te_sc, "ytr": y_tr,
                        "yte": y_te, "feats": feats, "scaler": sc,
                        "X_tr_raw": X_tr[feats], "X_te_raw": X_te[feats]}
        base_r = self._train_base(X_tr_sc, X_te_sc, y_tr, y_te)
        self._stored["base"] = base_r
        self._dot("Base Models", "ok"); self.v_prog.set(65)
        if not self._running: return

        if self.v_stack.get() and len(base_r) >= 2:
            self._dot("Stacking", "run")
            self._log("\n[5/7]  Building Stacking ensemble...", "info")
            self.v_status.set("Stacking ensemble...")
            stk_r = self._stacking(X_tr_sc, X_te_sc, y_tr, y_te, base_r)
            self._stored["stacking"] = stk_r
            self._dot("Stacking", "ok")
        self.v_prog.set(80)
        if not self._running: return

        self._dot("Visualise", "run")
        self._log("\n[6/7]  Generating visualisations...", "info")
        self.v_status.set("Generating charts...")
        out = self.v_outdir.get(); os.makedirs(out, exist_ok=True)
        self._visualize(out)
        self._dot("Visualise", "ok"); self.v_prog.set(90)
        if not self._running: return

        self._dot("SHAP", "run")
        self._log("\n[7/7]  SHAP interpretability analysis...", "info")
        self.v_status.set("SHAP analysis...")
        self._run_shap(out, "Logistic Regression")
        self._dot("SHAP", "ok"); self.v_prog.set(100)

        self.v_status.set("✅  Analysis complete!")
        self.after(0, lambda: self._done_lbl.config(text="✓ Analysis completed successfully!"))
        self._log("\n" + "═" * 60, "sec")
        self._log("  ✅  Complete!  Output directory: " + out, "ok")
        self._log("═" * 60, "sec")
        self.after(100, lambda: messagebox.showinfo("Complete",
            f"Analysis complete!\nResults saved to:\n{out}"))

    def _impute(self, X_tr, X_te, y_tr, y_te):
        import pandas as pd
        Xtr, Xte = X_tr.copy(), X_te.copy()
        for c in Xtr.columns:
            Xtr[c] = pd.to_numeric(Xtr[c], errors="coerce")
            Xte[c] = pd.to_numeric(Xte[c], errors="coerce")
        valid = [c for c in Xtr.columns if Xtr[c].notna().any()]
        Xtr, Xte = Xtr[valid], Xte[valid]
        for c in valid:
            means = Xtr.groupby(y_tr)[c].mean()
            for lab in means.index:
                Xtr.loc[y_tr == lab, c] = Xtr.loc[y_tr == lab, c].fillna(means[lab])
                mask = y_te == lab
                if mask.any():
                    Xte.loc[mask, c] = Xte.loc[mask, c].fillna(means[lab])
            Xte[c] = Xte[c].fillna(Xtr[c].mean())
        return Xtr, Xte

    def _feature_selection(self, X_tr, y_tr):
        import numpy as np, pandas as pd
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_score, StratifiedKFold
        from sklearn.feature_selection import RFE, SelectKBest, f_classif, mutual_info_classif
        from sklearn.ensemble import RandomForestClassifier
        from xgboost import XGBClassifier

        cv_k = self.v_cvfolds.get()
        pat  = self.v_patience.get()
        mni  = self.v_minimp.get()
        Xdf  = X_tr.copy().fillna(X_tr.mean())

        def cv_auc(feats):
            Xs = StandardScaler().fit_transform(Xdf[feats])
            lr = LogisticRegression(random_state=42, max_iter=1000)
            return cross_val_score(lr, Xs, y_tr, cv=cv_k,
                                   scoring="roc_auc", n_jobs=-1).mean()

        def incr(ranked):
            best_a, best_n, cnt = 0, 1, 0
            hist = []
            for n in range(1, len(ranked) + 1):
                if not self._running: break
                a = cv_auc(ranked[:n])
                hist.append((n, a, list(ranked[:n])))
                self._log(f"    N={n:2d}: AUC={a:.4f}", "info")
                if a - best_a > mni:
                    best_a, best_n, cnt = a, n, 0
                else:
                    cnt += 1
                if cnt >= pat: break
            if not hist: return None
            return hist[best_n - 1]

        results = []

        if self.v_lasso.get():
            self._log("  → Lasso...", "info")
            try:
                cv_s = StratifiedKFold(n_splits=cv_k, shuffle=True, random_state=42)
                Xs   = StandardScaler().fit_transform(Xdf)
                best_C, best_a = 1.0, 0
                for lam in np.logspace(-3, 1, 100):
                    C_ = 1.0 / lam
                    aucs = []
                    for tr, va in cv_s.split(Xs, y_tr):
                        m = LogisticRegression(penalty="l1", solver="liblinear",
                                               C=C_, random_state=42, max_iter=1000)
                        m.fit(Xs[tr], y_tr.iloc[tr])
                        from sklearn.metrics import roc_auc_score
                        aucs.append(roc_auc_score(y_tr.iloc[va],
                                                   m.predict_proba(Xs[va])[:, 1]))
                    if np.mean(aucs) > best_a:
                        best_a, best_C = np.mean(aucs), C_
                m = LogisticRegression(penalty="l1", solver="liblinear",
                                       C=best_C, random_state=42, max_iter=1000)
                m.fit(Xs, y_tr)
                nz = pd.Series(m.coef_[0], index=Xdf.columns)
                nz = nz[nz != 0].abs().sort_values(ascending=False).index.tolist()
                if nz:
                    results.append(("Lasso", nz, best_a))
                    self._log(f"  ✓ Lasso: {len(nz)} features, AUC={best_a:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ Lasso failed: {e}", "warn")

        if self.v_rfe.get() and self._running:
            self._log("  → RFE...", "info")
            try:
                Xs = StandardScaler().fit_transform(Xdf)
                est = LogisticRegression(penalty="l2", solver="liblinear",
                                          random_state=42, max_iter=1000)
                rfe = RFE(est, n_features_to_select=1, step=1)
                rfe.fit(Xs, y_tr)
                ranked = [X_tr.columns[i] for i in np.argsort(rfe.ranking_)]
                res = incr(ranked)
                if res:
                    results.append(("RFE", res[2], res[1]))
                    self._log(f"  ✓ RFE: {len(res[2])} features, AUC={res[1]:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ RFE failed: {e}", "warn")

        if self.v_rf_fs.get() and self._running:
            self._log("  → Random Forest...", "info")
            try:
                rf = RandomForestClassifier(n_estimators=100, max_depth=10,
                                             min_samples_split=5,
                                             random_state=42, n_jobs=-1)
                rf.fit(Xdf, y_tr)
                ranked = pd.Series(rf.feature_importances_,
                                   index=Xdf.columns).sort_values(ascending=False).index.tolist()
                res = incr(ranked)
                if res:
                    results.append(("RF", res[2], res[1]))
                    self._log(f"  ✓ RF: {len(res[2])} features, AUC={res[1]:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ RF failed: {e}", "warn")

        if self.v_xgb_fs.get() and self._running:
            self._log("  → XGBoost...", "info")
            try:
                xgb = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1,
                                     random_state=42, eval_metric="logloss", n_jobs=-1)
                xgb.fit(Xdf, y_tr)
                ranked = pd.Series(xgb.feature_importances_,
                                   index=Xdf.columns).sort_values(ascending=False).index.tolist()
                res = incr(ranked)
                if res:
                    results.append(("XGB", res[2], res[1]))
                    self._log(f"  ✓ XGB: {len(res[2])} features, AUC={res[1]:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ XGB failed: {e}", "warn")

        if self.v_mi.get() and self._running:
            self._log("  → Mutual Information...", "info")
            try:
                mi = mutual_info_classif(Xdf, y_tr, random_state=42)
                ranked = pd.Series(mi, index=Xdf.columns).sort_values(ascending=False).index.tolist()
                res = incr(ranked)
                if res:
                    results.append(("MI", res[2], res[1]))
                    self._log(f"  ✓ MI: {len(res[2])} features, AUC={res[1]:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ MI failed: {e}", "warn")

        if self.v_kbest.get() and self._running:
            self._log("  → SelectKBest...", "info")
            try:
                sel = SelectKBest(score_func=f_classif, k="all")
                sel.fit(Xdf, y_tr)
                ranked = pd.Series(sel.scores_,
                                   index=Xdf.columns).sort_values(ascending=False).index.tolist()
                res = incr(ranked)
                if res:
                    results.append(("KBest", res[2], res[1]))
                    self._log(f"  ✓ KBest: {len(res[2])} features, AUC={res[1]:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ KBest failed: {e}", "warn")

        if not results:
            return X_tr.columns.tolist()[:min(10, X_tr.shape[1])]
        best = max(results, key=lambda x: x[2])
        self._log(f"\n  ★ Best method: {best[0]}  AUC={best[2]:.4f}", "sec")
        return best[1]

    def _train_base(self, Xtr, Xte, ytr, yte):
        import numpy as np
        from sklearn.model_selection import cross_val_score, StratifiedKFold
        from sklearn.metrics import (roc_auc_score, accuracy_score,
                                     precision_score, recall_score, f1_score,
                                     confusion_matrix, roc_curve, det_curve,
                                     precision_recall_curve, average_precision_score)
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
        from sklearn.svm import SVC
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.naive_bayes import GaussianNB
        from xgboost import XGBClassifier
        from lightgbm import LGBMClassifier
        from catboost import CatBoostClassifier

        cw  = self.v_cw.get() if self.v_cw.get() != "none" else None
        cv  = StratifiedKFold(n_splits=self.v_cvfolds.get(), shuffle=True, random_state=42)
        thr = self.v_thr.get()

        all_m = {
            "Logistic Regression": LogisticRegression(
                penalty="l2", solver="liblinear", C=1.0,
                max_iter=2000, random_state=42, class_weight=cw),
            "Decision Tree": DecisionTreeClassifier(
                max_depth=3, min_samples_split=15, min_samples_leaf=8,
                random_state=42, class_weight=cw),
            "Random Forest": RandomForestClassifier(
                n_estimators=100, max_depth=3, min_samples_split=15,
                min_samples_leaf=8, max_features="sqrt",
                random_state=42, class_weight=cw, n_jobs=-1),
            "Extra Trees": ExtraTreesClassifier(
                n_estimators=100, max_depth=3, min_samples_split=15,
                min_samples_leaf=8, max_features="sqrt",
                random_state=42, class_weight=cw, n_jobs=-1),
            "XGBoost": XGBClassifier(
                n_estimators=80, max_depth=2, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
                reg_alpha=0.1, reg_lambda=1.0, scale_pos_weight=2,
                random_state=42, eval_metric="logloss", n_jobs=-1),
            "LightGBM": LGBMClassifier(
                n_estimators=80, max_depth=2, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, min_child_samples=15,
                reg_alpha=0.1, reg_lambda=1.0,
                random_state=42, class_weight=cw, n_jobs=-1, verbose=-1),
            "CatBoost": CatBoostClassifier(
                iterations=80, depth=2, learning_rate=0.05,
                l2_leaf_reg=5.0, random_state=42, verbose=False),
            "AdaBoost": AdaBoostClassifier(
                n_estimators=80, learning_rate=0.05,
                algorithm="SAMME", random_state=42),
            "SVM": SVC(kernel="rbf", C=1.0, probability=True,
                       random_state=42, class_weight=cw),
            "KNN": KNeighborsClassifier(n_neighbors=7),
            "Naive Bayes": GaussianNB(),
        }
        sel_m = {n: m for n, m in all_m.items()
                 if self.mv.get(n, tk.BooleanVar(value=False)).get()}
        results = {}
        total = len(sel_m)

        for i, (name, model) in enumerate(sel_m.items()):
            if not self._running: break
            self.v_prog.set(38 + i / total * 27)
            self.v_status.set(f"Training: {name}")
            self._log(f"\n  [{name}]", "info")
            try:
                sc_arr = cross_val_score(model, Xtr, ytr, cv=cv,
                                         scoring="roc_auc", n_jobs=-1)
                cv_m, cv_s = sc_arr.mean(), sc_arr.std()
                model.fit(Xtr, ytr)
                p_te = model.predict_proba(Xte)[:, 1]
                p_tr = model.predict_proba(Xtr)[:, 1]
                y_pd = (p_te >= thr).astype(int)
                fpr, tpr, _     = roc_curve(yte, p_te)
                fpr_d, fnr_d, _ = det_curve(yte, p_te)
                pc, rc, _       = precision_recall_curve(yte, p_te)
                results[name] = {
                    "model":  model,
                    "tr_auc": roc_auc_score(ytr, p_tr),
                    "te_auc": roc_auc_score(yte, p_te),
                    "cv_m": cv_m, "cv_s": cv_s,
                    "acc":  accuracy_score(yte, y_pd),
                    "prec": precision_score(yte, y_pd, zero_division=0),
                    "rec":  recall_score(yte, y_pd, zero_division=0),
                    "f1":   f1_score(yte, y_pd, zero_division=0),
                    "ap":   average_precision_score(yte, p_te),
                    "fpr": fpr, "tpr": tpr,
                    "fpr_d": fpr_d, "fnr_d": fnr_d,
                    "pc": pc, "rc": rc,
                    "cm":   confusion_matrix(yte, y_pd),
                }
                self._log(f"  ✓ CV={cv_m:.4f}±{cv_s:.4f}  Test={results[name]['te_auc']:.4f}  F1={results[name]['f1']:.4f}", "ok")
            except Exception as e:
                self._log(f"  ⚠ Failed: {e}", "warn")
        return results

    def _stacking(self, Xtr, Xte, ytr, yte, base_r):
        from sklearn.ensemble import StackingClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_score, StratifiedKFold
        from sklearn.metrics import (roc_auc_score, accuracy_score,
                                     precision_score, recall_score, f1_score,
                                     confusion_matrix, roc_curve, det_curve,
                                     precision_recall_curve, average_precision_score)

        mx_s = self.v_maxstd.get(); mn_a = self.v_minauc.get()
        thr  = self.v_thr.get();    cv_k = self.v_cvfolds.get()
        cw   = self.v_cw.get() if self.v_cw.get() != "none" else None
        elig = {n: r for n, r in base_r.items()
                if r["cv_s"] <= mx_s and r["cv_m"] >= mn_a}
        self._log(f"  Eligible base learners: {len(elig)}/{len(base_r)}", "info")
        if len(elig) < 2: elig = base_r

        _cv  = StratifiedKFold(cv_k, shuffle=True, random_state=42)
        ests = [(n, r["model"]) for n, r in sorted(elig.items(), key=lambda x: -x[1]["cv_m"])]
        meta = LogisticRegression(penalty="l2", solver="liblinear", C=1.0,
                                  max_iter=2000, random_state=42, class_weight=cw)
        stk  = StackingClassifier(estimators=ests, final_estimator=meta,
                                   cv=_cv, stack_method="predict_proba",
                                   passthrough=False, n_jobs=-1)
        sc_a = cross_val_score(stk, Xtr, ytr, cv=_cv, scoring="roc_auc", n_jobs=-1)
        cv_m, cv_s = sc_a.mean(), sc_a.std()
        stk.fit(Xtr, ytr)
        p_te = stk.predict_proba(Xte)[:, 1]
        p_tr = stk.predict_proba(Xtr)[:, 1]
        y_pd = (p_te >= thr).astype(int)
        fpr, tpr, _     = roc_curve(yte, p_te)
        fpr_d, fnr_d, _ = det_curve(yte, p_te)
        pc, rc, _       = precision_recall_curve(yte, p_te)
        self._log(f"  ✓ Stacking CV={cv_m:.4f}±{cv_s:.4f}  Test={roc_auc_score(yte, p_te):.4f}", "ok")
        return {
            "model": stk,
            "tr_auc": roc_auc_score(ytr, p_tr), "te_auc": roc_auc_score(yte, p_te),
            "cv_m": cv_m, "cv_s": cv_s,
            "acc":  accuracy_score(yte, y_pd),
            "prec": precision_score(yte, y_pd, zero_division=0),
            "rec":  recall_score(yte, y_pd, zero_division=0),
            "f1":   f1_score(yte, y_pd, zero_division=0),
            "ap":   average_precision_score(yte, p_te),
            "fpr": fpr, "tpr": tpr,
            "fpr_d": fpr_d, "fnr_d": fnr_d,
            "pc": pc, "rc": rc,
            "cm":   confusion_matrix(yte, y_pd),
        }

    def _visualize(self, out):
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np, pandas as pd

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["axes.grid"]   = False
        fmt = self.v_fmt.get(); dpi = self.v_dpi.get()

        base  = self._stored.get("base", {})
        stk   = self._stored.get("stacking")
        all_r = dict(base)
        if stk: all_r["Stacking Ensemble"] = stk

        COLORS = ['#0072B2','#D55E00','#009E73','#CC79A7','#56B4E9',
                  '#E69F00','#000000','#8B008B','#2E8B57','#FF6347','#4682B4','#E74C3C']

        # ROC
        fig, ax = plt.subplots(figsize=(8, 7))
        for idx, (name, r) in enumerate(all_r.items()):
            is_s = name == "Stacking Ensemble"
            ax.plot(r["fpr"], r["tpr"],
                    lw=2.2 if is_s else 1.2, ls="-",
                    color=COLORS[idx % len(COLORS)],
                    alpha=1.0 if is_s else 0.85,
                    label=f"{name}  (AUC = {r['te_auc']:.3f})",
                    zorder=10 if is_s else 3)
        ax.plot([0,1],[0,1],"k--",lw=0.8,alpha=0.4)
        ax.set_xlabel("False Positive Rate", fontsize=13, fontweight="bold")
        ax.set_ylabel("True Positive Rate",  fontsize=13, fontweight="bold")
        ax.set_title("ROC Curves — Test Set", fontsize=14, fontweight="bold", pad=10)
        ax.legend(loc="lower right", fontsize=8, frameon=True, framealpha=0.9)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(f"{out}/roc_test.{fmt}", dpi=dpi, bbox_inches="tight")
        plt.close(fig); self._log("  ✓ ROC curve saved", "ok")

        # PR
        fig, ax = plt.subplots(figsize=(8, 7))
        for idx, (name, r) in enumerate(all_r.items()):
            is_s = name == "Stacking Ensemble"
            ax.plot(r["rc"], r["pc"],
                    lw=2.2 if is_s else 1.2, ls="-",
                    color=COLORS[idx % len(COLORS)],
                    alpha=1.0 if is_s else 0.85,
                    label=f"{name}  (AP = {r['ap']:.3f})",
                    zorder=10 if is_s else 3)
        ax.set_xlabel("Recall",    fontsize=13, fontweight="bold")
        ax.set_ylabel("Precision", fontsize=13, fontweight="bold")
        ax.set_title("Precision-Recall Curves — Test Set", fontsize=14, fontweight="bold", pad=10)
        ax.legend(loc="lower left", fontsize=8, frameon=True, framealpha=0.9)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(f"{out}/pr_curves.{fmt}", dpi=dpi, bbox_inches="tight")
        plt.close(fig); self._log("  ✓ PR curve saved", "ok")

        # Confusion matrices
        nc = 4; nr = (len(all_r)+nc-1)//nc
        fig, axes = plt.subplots(nr, nc, figsize=(20, 5*nr))
        axes = np.array(axes).flatten()
        for idx, (name, r) in enumerate(all_r.items()):
            is_s = name == "Stacking Ensemble"
            sns.heatmap(r["cm"], annot=True, fmt="d", cmap="Blues",
                        xticklabels=["Neg","Pos"], yticklabels=["Neg","Pos"],
                        ax=axes[idx], cbar=False, annot_kws={"size":11},
                        linewidths=0.5, linecolor="white")
            axes[idx].set_title(f"{name}\nAUC={r['cv_m']:.3f}",
                                fontsize=9, fontweight="bold",
                                color="red" if is_s else "black")
        for ax in axes[len(all_r):]: ax.set_visible(False)
        fig.suptitle("Confusion Matrices — Test Set", fontsize=14, fontweight="bold")
        fig.tight_layout()
        fig.savefig(f"{out}/confusion_matrices.{fmt}", dpi=dpi, bbox_inches="tight")
        plt.close(fig); self._log("  ✓ Confusion matrices saved", "ok")

        # Excel
        cv_col = f"{self.v_cvfolds.get()}-Fold CV AUC"
        rows = [{"Model": n, cv_col: round(r["cv_m"],4), "CV Std": round(r["cv_s"],4),
                 "Test AUC": round(r["te_auc"],4), "Precision": round(r["prec"],4),
                 "Recall": round(r["rec"],4), "F1": round(r["f1"],4)}
                for n, r in all_r.items()]
        df = pd.DataFrame(rows).sort_values(cv_col, ascending=False)
        df.to_excel(f"{out}/model_comparison.xlsx", index=False)
        self._stored["df"] = df
        self._log("  ✓ Model comparison Excel saved", "ok")

    def _run_shap(self, out, model_name="Logistic Regression", log_w=None):
        def _l(msg, tag="info"):
            if log_w:
                self.after(0, lambda m=msg, t=tag: (
                    log_w.insert(tk.END, m+"\n", t), log_w.see(tk.END)))
            else:
                self._log(msg, tag)
        try:
            import shap, numpy as np
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt

            base   = self._stored.get("base", {})
            feats  = self._stored.get("feats", [])
            Xtr_sc = self._stored.get("Xtr")
            Xte_sc = self._stored.get("Xte")
            if Xtr_sc is None or model_name not in base:
                _l(f"  ⚠  Model [{model_name}] not ready. Complete full analysis first.", "err")
                return
            model = base[model_name]["model"]
            X_all = np.vstack([Xtr_sc, Xte_sc])
            fmt   = self.v_fmt.get(); dpi = self.v_dpi.get()
            safe  = model_name.replace(" ","_")

            _l(f"  Building SHAP Explainer [{model_name}]...", "info")
            explainer  = shap.LinearExplainer(model, Xtr_sc)
            shap_vals  = explainer.shap_values(X_all)
            mean_abs   = np.abs(shap_vals).mean(axis=0)
            sidx       = np.argsort(mean_abs)

            fig, ax = plt.subplots(figsize=(10, max(6, len(feats)*0.5)))
            ax.barh(range(len(feats)), mean_abs[sidx], color="#0072B2", alpha=0.85)
            ax.set_yticks(range(len(feats)))
            ax.set_yticklabels([feats[i] for i in sidx])
            ax.set_xlabel("mean(|SHAP value|)", fontsize=12, fontweight="bold")
            ax.set_title(f"SHAP Feature Importance — {model_name}", fontsize=14, fontweight="bold")
            ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
            fig.tight_layout()
            fig.savefig(f"{out}/shap_importance_{safe}.{fmt}", dpi=dpi, bbox_inches="tight")
            plt.close(fig); _l("  ✓ Feature importance chart saved", "ok")

            fig = plt.figure(figsize=(10, max(6, len(feats)*0.5)))
            shap.summary_plot(shap_vals, X_all, feature_names=feats, show=False)
            plt.title(f"SHAP Summary — {model_name}", fontsize=14, fontweight="bold", pad=20)
            plt.tight_layout()
            fig.savefig(f"{out}/shap_summary_{safe}.{fmt}", dpi=dpi, bbox_inches="tight")
            plt.close(fig); _l("  ✓ Summary beeswarm plot saved", "ok")

            top3 = np.argsort(mean_abs)[::-1][:min(3, len(feats))]
            fig, axes = plt.subplots(1, len(top3), figsize=(6*len(top3), 6))
            if len(top3) == 1: axes = [axes]
            for pi, fi in enumerate(top3):
                shap.dependence_plot(fi, shap_vals, X_all, feature_names=feats,
                                     ax=axes[pi], show=False)
                axes[pi].set_title(f"Top {pi+1}: {feats[fi]}", fontsize=11)
            fig.suptitle("SHAP Dependence Plots — Top 3 Features",
                         fontsize=14, fontweight="bold")
            fig.tight_layout()
            fig.savefig(f"{out}/shap_dependence_{safe}.{fmt}", dpi=dpi, bbox_inches="tight")
            plt.close(fig); _l("  ✓ Dependence plots saved", "ok")
            _l(f"  ★ SHAP complete — output: {out}", "ok")
        except Exception as e:
            import traceback
            _l(f"  ⚠  SHAP failed: {e}", "err")

    def _run_shap_standalone(self):
        if not self._stored.get("base"):
            messagebox.showwarning("Note", "Please complete the full analysis first!")
            return
        model_name = self.v_shap_m.get()
        self.shap_log.insert(tk.END, f"\nRunning SHAP analysis  [{model_name}]...\n", "info")
        out = self.v_outdir.get(); os.makedirs(out, exist_ok=True)
        threading.Thread(target=self._run_shap, args=(out, model_name, self.shap_log),
                         daemon=True).start()

    def _refresh_results(self):
        base = self._stored.get("base", {})
        stk  = self._stored.get("stacking")
        all_r = dict(base)
        if stk: all_r["Stacking Ensemble"] = stk
        if not all_r:
            messagebox.showinfo("Note", "No results yet — run the analysis first.")
            return
        for row in self.result_tv.get_children():
            self.result_tv.delete(row)
        sorted_r = sorted(all_r.items(), key=lambda x: -x[1]["cv_m"])
        for i, (name, r) in enumerate(sorted_r):
            tag = "stk" if name == "Stacking Ensemble" else ("evn" if i%2==0 else "odd")
            self.result_tv.insert("", tk.END, values=(
                name, f"{r['cv_m']:.4f}", f"{r['cv_s']:.4f}",
                f"{r['te_auc']:.4f}", f"{r['prec']:.4f}",
                f"{r['rec']:.4f}",    f"{r['f1']:.4f}",
            ), tags=(tag,))
        # update metric cards
        best_name, best_r = sorted_r[0]
        self._metric_cards["Best Model"].config(text=best_name.split()[0])
        self._metric_cards["Best CV AUC"].config(text=f"{best_r['cv_m']:.4f}")
        best_te = max(all_r.items(), key=lambda x: x[1]["te_auc"])
        self._metric_cards["Best Test AUC"].config(text=f"{best_te[1]['te_auc']:.4f}")
        best_f1 = max(all_r.items(), key=lambda x: x[1]["f1"])
        self._metric_cards["Best F1"].config(text=f"{best_f1[1]['f1']:.4f}")
        messagebox.showinfo("Done", f"Loaded {len(all_r)} model results")

    def _preview(self, var):
        path = var.get()
        if not path:
            messagebox.showinfo("Note", "Please select a file first"); return
        try:
            import pandas as pd
            df_full = pd.read_excel(path); df_prev = df_full.head(10)
            win = tk.Toplevel(self)
            win.title(f"Preview — {os.path.basename(path)}")
            win.geometry("900x420"); win.configure(bg=C["page_bg"])
            tk.Label(win, text=f"File: {path}   Shape: {df_full.shape}",
                     font=FN, bg=C["page_bg"], fg=C["txt_mid"]).pack(pady=6)
            wrap = tk.Frame(win, bg=C["page_bg"])
            wrap.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
            cols = list(df_prev.columns)
            tv = ttk.Treeview(wrap, columns=cols, show="headings")
            for c in cols:
                tv.heading(c, text=c)
                tv.column(c, width=max(80, len(str(c))*9), anchor="center")
            for _, row in df_prev.iterrows():
                tv.insert("", tk.END, values=list(row))
            xsb = ttk.Scrollbar(wrap, orient="horizontal", command=tv.xview)
            ysb = ttk.Scrollbar(wrap, orient="vertical",   command=tv.yview)
            tv.configure(xscrollcommand=xsb.set, yscrollcommand=ysb.set)
            tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            ysb.pack(side=tk.RIGHT, fill=tk.Y)
            xsb.pack(side=tk.BOTTOM, fill=tk.X)
        except Exception as e:
            messagebox.showerror("Preview failed", str(e))

    def _open_outdir(self):
        out = self.v_outdir.get()
        if not os.path.exists(out):
            messagebox.showinfo("Note", f"Directory not created yet:\n{out}"); return
        import subprocess
        if sys.platform == "win32":     os.startfile(out)
        elif sys.platform == "darwin":  subprocess.Popen(["open", out])
        else:                           subprocess.Popen(["xdg-open", out])

    def _reset_dots(self):
        for d in self._stage_dots.values():
            d.config(text="○", fg=C["border"])

    def _dot(self, name, state):
        d = self._stage_dots.get(name)
        if not d: return
        cfg = {"run":("◉",C["yellow"]), "ok":("●",C["green"]), "err":("✕",C["red"])}
        t, fg = cfg.get(state, ("○", C["border"]))
        self.after(0, lambda: d.config(text=t, fg=fg))

    def _log(self, msg, tag=""):
        def _do():
            self.log_box.insert(tk.END, msg+"\n", tag)
            self.log_box.see(tk.END)
        self.after(0, _do)


# ══════════════════════════════════════════════════════════════
# 3.  Scrollable Frame
# ══════════════════════════════════════════════════════════════
class _ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=C["page_bg"], **kw)
        self.canvas = tk.Canvas(self, bg=C["page_bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.inner = tk.Frame(self.canvas, bg=C["page_bg"])
        self._win  = self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", lambda _: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(
            self._win, width=e.width))
        self.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))


# ══════════════════════════════════════════════════════════════
# 4.  Entry point
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    LoginWindow().mainloop()