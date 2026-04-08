"""
PayWithEase - Payment App UI
A Python Tkinter application replicating the PayWithEase payment interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading


# ─── Color Palette ────────────────────────────────────────────────────────────
BG_DARK       = "#0a1628"
BG_CARD       = "#0d2044"
BLUE_PRIMARY  = "#1565C0"
BLUE_ACCENT   = "#2196F3"
BLUE_LIGHT    = "#64B5F6"
GREEN_SUCCESS  = "#43A047"
GREEN_LIGHT    = "#81C784"
GOLD          = "#FFD700"
WHITE         = "#FFFFFF"
LIGHT_GRAY    = "#B0BEC5"
TEXT_MUTED    = "#78909C"
CARD_BORDER   = "#1E3A5F"


# ─── Animated Button ──────────────────────────────────────────────────────────
class AnimatedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=220, height=48,
                 bg=GREEN_SUCCESS, fg=WHITE, font=("Georgia", 13, "bold"),
                 radius=24, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0, **kwargs)
        self.text = text
        self.command = command
        self.btn_bg = bg
        self.btn_fg = fg
        self.btn_font = font
        self.radius = radius
        self.w = width
        self.h = height
        self._draw(bg)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        pts = [x1+r, y1,  x2-r, y1,
               x2,   y1,  x2,   y1+r,
               x2,   y2-r, x2,  y2,
               x2-r, y2,  x1+r, y2,
               x1,   y2,  x1,   y2-r,
               x1,   y1+r, x1,  y1]
        return self.create_polygon(pts, smooth=True, **kw)

    def _draw(self, color):
        self.delete("all")
        self._round_rect(2, 2, self.w-2, self.h-2, self.radius,
                         fill=color, outline=WHITE, width=1)
        self.create_text(self.w//2, self.h//2, text=self.text,
                         fill=self.btn_fg, font=self.btn_font)

    def _on_enter(self, _):
        self._draw(self._lighten(self.btn_bg))

    def _on_leave(self, _):
        self._draw(self.btn_bg)

    def _on_click(self, _):
        self._draw(self._darken(self.btn_bg))
        self.after(120, lambda: self._draw(self.btn_bg))
        if self.command:
            self.after(120, self.command)

    @staticmethod
    def _lighten(hex_color):
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r, g, b = min(255, r+30), min(255, g+30), min(255, b+30)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _darken(hex_color):
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f"#{r:02x}{g:02x}{b:02x}"


# ─── Success Screen ───────────────────────────────────────────────────────────
class SuccessScreen(tk.Frame):
    def __init__(self, parent, amount, recipient, on_done):
        super().__init__(parent, bg=BG_DARK)
        self._build(amount, recipient, on_done)

    def _build(self, amount, recipient, on_done):
        # Checkmark circle
        canvas = tk.Canvas(self, width=100, height=100, bg=BG_DARK, highlightthickness=0)
        canvas.pack(pady=(40, 10))
        canvas.create_oval(5, 5, 95, 95, fill=GREEN_SUCCESS, outline=GREEN_LIGHT, width=3)
        canvas.create_text(50, 50, text="✓", fill=WHITE, font=("Georgia", 36, "bold"))

        tk.Label(self, text="Payment Successful!", bg=BG_DARK,
                 fg=WHITE, font=("Georgia", 20, "bold")).pack(pady=(10, 4))

        tk.Label(self, text=f"₹{amount} sent to {recipient}", bg=BG_DARK,
                 fg=BLUE_LIGHT, font=("Georgia", 13)).pack()

        tk.Label(self, text="Transaction ID: PWE" + str(int(time.time())),
                 bg=BG_DARK, fg=TEXT_MUTED, font=("Courier", 10)).pack(pady=(8, 24))

        # Info row
        row = tk.Frame(self, bg=BG_CARD)
        row.pack(fill="x", padx=30, pady=8)
        for icon, label in [("⚡", "Quick & Easy"), ("🔒", "100% Secure"), ("↔", "Instant")]:
            col = tk.Frame(row, bg=BG_CARD)
            col.pack(side="left", expand=True, pady=12)
            tk.Label(col, text=icon, bg=BG_CARD, fg=GOLD, font=("Arial", 16)).pack()
            tk.Label(col, text=label, bg=BG_CARD, fg=LIGHT_GRAY,
                     font=("Georgia", 9)).pack()

        AnimatedButton(self, "Done ✔", command=on_done,
                       bg=BLUE_PRIMARY, width=200, height=44).pack(pady=30)


# ─── Main App ─────────────────────────────────────────────────────────────────
class PayWithEaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PayWithEase")
        self.geometry("400x700")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self._show_main()

    # ── Header ────────────────────────────────────────────────────────────────
    def _header(self, parent):
        hdr = tk.Frame(parent, bg=BLUE_PRIMARY, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="PayWith", bg=BLUE_PRIMARY,
                 fg=WHITE, font=("Georgia", 20, "bold")).pack(side="left", padx=(20, 0), pady=12)
        tk.Label(hdr, text="Ease", bg=BLUE_PRIMARY,
                 fg=GOLD, font=("Georgia", 20, "bold italic")).pack(side="left")
        tk.Label(hdr, text="📶", bg=BLUE_PRIMARY,
                 fg=WHITE, font=("Arial", 14)).pack(side="right", padx=20)

    # ── Balance Card ─────────────────────────────────────────────────────────
    def _balance_card(self, parent):
        card = tk.Frame(parent, bg=BG_CARD, relief="flat")
        card.pack(fill="x", padx=20, pady=(14, 8))
        tk.Label(card, text="Available Balance", bg=BG_CARD,
                 fg=TEXT_MUTED, font=("Georgia", 10)).pack(pady=(14, 2))
        tk.Label(card, text="₹ 24,850.00", bg=BG_CARD,
                 fg=WHITE, font=("Georgia", 28, "bold")).pack()
        tk.Label(card, text="🟢  Active  •  HDFC ••••4521", bg=BG_CARD,
                 fg=GREEN_LIGHT, font=("Georgia", 10)).pack(pady=(4, 14))

    # ── Quick Actions ─────────────────────────────────────────────────────────
    def _quick_actions(self, parent):
        lbl = tk.Label(parent, text="Quick Actions", bg=BG_DARK,
                       fg=LIGHT_GRAY, font=("Georgia", 11, "bold"))
        lbl.pack(anchor="w", padx=24, pady=(4, 6))
        row = tk.Frame(parent, bg=BG_DARK)
        row.pack(fill="x", padx=20)
        actions = [("💳", "Pay"), ("📤", "Send"), ("📥", "Request"), ("📜", "History")]
        for icon, name in actions:
            btn_frame = tk.Frame(row, bg=BG_CARD, cursor="hand2")
            btn_frame.pack(side="left", expand=True, fill="x", padx=4, pady=2)
            tk.Label(btn_frame, text=icon, bg=BG_CARD,
                     font=("Arial", 18)).pack(pady=(12, 2))
            tk.Label(btn_frame, text=name, bg=BG_CARD, fg=LIGHT_GRAY,
                     font=("Georgia", 9)).pack(pady=(0, 10))

    # ── Pay Form ──────────────────────────────────────────────────────────────
    def _pay_form(self, parent):
        form = tk.Frame(parent, bg=BG_CARD)
        form.pack(fill="x", padx=20, pady=(14, 0))

        tk.Label(form, text="New Payment", bg=BG_CARD,
                 fg=WHITE, font=("Georgia", 14, "bold")).pack(anchor="w", padx=16, pady=(14, 10))

        self._field(form, "👤  Recipient (UPI / Phone)")
        self.recipient_var = tk.StringVar(value="")
        self._entry(form, self.recipient_var, "e.g. name@upi or 9876543210")

        self._field(form, "₹  Amount")
        self.amount_var = tk.StringVar(value="")
        self._entry(form, self.amount_var, "0.00")

        self._field(form, "📝  Note (optional)")
        self.note_var = tk.StringVar(value="")
        self._entry(form, self.note_var, "What's this for?")

        self._pay_btn = AnimatedButton(form, "Pay Now  →", command=self._process_payment,
                                       bg=GREEN_SUCCESS, width=340, height=50)
        self._pay_btn.pack(pady=(16, 20))

    def _field(self, parent, text):
        tk.Label(parent, text=text, bg=BG_CARD,
                 fg=BLUE_LIGHT, font=("Georgia", 10)).pack(anchor="w", padx=16, pady=(8, 2))

    def _entry(self, parent, var, placeholder):
        e = tk.Entry(parent, textvariable=var, bg="#112240", fg=WHITE,
                     insertbackground=WHITE, relief="flat",
                     font=("Georgia", 12), bd=0)
        e.pack(fill="x", padx=16, ipady=8)
        if not var.get():
            e.insert(0, placeholder)
            e.config(fg=TEXT_MUTED)
            def on_focus_in(ev, entry=e, ph=placeholder, v=var):
                if entry.get() == ph:
                    entry.delete(0, "end")
                    entry.config(fg=WHITE)
            def on_focus_out(ev, entry=e, ph=placeholder, v=var):
                if not entry.get():
                    entry.insert(0, ph)
                    entry.config(fg=TEXT_MUTED)
            e.bind("<FocusIn>", on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
        # Separator line
        sep = tk.Frame(parent, bg=CARD_BORDER, height=1)
        sep.pack(fill="x", padx=16)

    # ── Recent Transactions ───────────────────────────────────────────────────
    def _recent(self, parent):
        tk.Label(parent, text="Recent", bg=BG_DARK,
                 fg=LIGHT_GRAY, font=("Georgia", 11, "bold")).pack(anchor="w", padx=24, pady=(14, 6))
        txns = [
            ("🛒", "Amazon",       "-₹1,299", "Today",      "red"),
            ("🍕", "Zomato",       "-₹340",   "Yesterday",  "red"),
            ("💸", "Rahul Kumar",  "+₹5,000", "2 days ago", "green"),
            ("⚡", "BSES Rajdhani", "-₹820",  "3 days ago", "red"),
        ]
        for icon, name, amt, date, color in txns:
            row = tk.Frame(parent, bg=BG_CARD)
            row.pack(fill="x", padx=20, pady=2)
            tk.Label(row, text=icon, bg=BG_CARD,
                     font=("Arial", 16)).pack(side="left", padx=(12, 8), pady=10)
            info = tk.Frame(row, bg=BG_CARD)
            info.pack(side="left", expand=True, fill="x")
            tk.Label(info, text=name, bg=BG_CARD, fg=WHITE,
                     font=("Georgia", 11)).pack(anchor="w")
            tk.Label(info, text=date, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Georgia", 9)).pack(anchor="w")
            fg = GREEN_LIGHT if color == "green" else "#EF9A9A"
            tk.Label(row, text=amt, bg=BG_CARD, fg=fg,
                     font=("Georgia", 12, "bold")).pack(side="right", padx=16)

    # ── Footer ────────────────────────────────────────────────────────────────
    def _footer(self, parent):
        ft = tk.Frame(parent, bg="#060f1f", height=38)
        ft.pack(fill="x", side="bottom")
        ft.pack_propagate(False)
        tk.Label(ft, text="Pay Anytime, Anywhere  •  Fast, Simple & Secure",
                 bg="#060f1f", fg=TEXT_MUTED, font=("Georgia", 9)).pack(pady=10)

    # ── Main Screen ───────────────────────────────────────────────────────────
    def _show_main(self):
        for w in self.winfo_children():
            w.destroy()

        canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._header(scroll_frame)
        self._balance_card(scroll_frame)
        self._quick_actions(scroll_frame)
        self._pay_form(scroll_frame)
        self._recent(scroll_frame)
        self._footer(scroll_frame)

        # Mouse wheel scroll
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ── Payment Processing ────────────────────────────────────────────────────
    def _process_payment(self):
        placeholders = {"e.g. name@upi or 9876543210", "0.00", "What's this for?", ""}
        recipient = self.recipient_var.get().strip()
        amount    = self.amount_var.get().strip()

        if recipient in placeholders or not recipient:
            messagebox.showwarning("Missing Info", "Please enter a recipient.", parent=self)
            return
        if amount in placeholders or not amount:
            messagebox.showwarning("Missing Info", "Please enter an amount.", parent=self)
            return
        try:
            amt_float = float(amount.replace(",", ""))
            if amt_float <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter a valid positive amount.", parent=self)
            return

        # Show processing overlay
        self._show_processing(amount, recipient)

    def _show_processing(self, amount, recipient):
        for w in self.winfo_children():
            w.destroy()
        self.configure(bg=BG_DARK)

        frame = tk.Frame(self, bg=BG_DARK)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Processing Payment…", bg=BG_DARK,
                 fg=WHITE, font=("Georgia", 16, "bold")).pack(pady=(120, 20))

        # Spinner (dots)
        spinner_lbl = tk.Label(frame, text="●  ●  ●", bg=BG_DARK,
                                fg=BLUE_ACCENT, font=("Arial", 24))
        spinner_lbl.pack()
        dots = ["●  ○  ○", "○  ●  ○", "○  ○  ●", "○  ●  ○"]
        self._dot_idx = 0

        def animate():
            spinner_lbl.config(text=dots[self._dot_idx % len(dots)])
            self._dot_idx += 1
            if self._dot_idx <= 12:
                self.after(250, animate)
            else:
                self._show_success(amount, recipient)
        animate()

    def _show_success(self, amount, recipient):
        for w in self.winfo_children():
            w.destroy()
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(expand=True, fill="both")
        SuccessScreen(container, amount, recipient,
                      on_done=self._show_main).pack(expand=True, fill="both")


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PayWithEaseApp()
    app.mainloop()
