"""
ui.py - Graphical User Interface for HackHub Hackathon Management App.
Built strictly with standard library Python 3.10+ and tkinter/ttk.
Configured with ttk 'clam' theme at the top.
All colors and fonts are named constants with zero color literals elsewhere.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import webbrowser
from typing import Optional, List, Dict, Any

from store import (
    Store, Event, Team, Round, Panel, Criterion, User,
    STATUS_DRAFT, STATUS_REG_OPEN, STATUS_JUDGING, STATUS_COMPLETED,
    STATUS_ACTIVE, STATUS_QUALIFIED, STATUS_ELIMINATED, STATUS_DISQUALIFIED,
    EVENT_STATUSES
)

# =====================================================================
# NAMED CONSTANTS: COLORS & FONTS
# Zero color literals anywhere else in the application.
# =====================================================================
COLOR_WINDOW = "#0F0826"
COLOR_CARD = "#1B1540"
COLOR_BORDER = "#2E2663"
COLOR_PRIMARY = "#7957FF"
COLOR_PRIMARY_HOVER = "#9B76FF"
COLOR_SECONDARY = "#241C52"
COLOR_SECONDARY_HOVER = "#32276E"
COLOR_TITLE = "#FFFFFF"
COLOR_BODY = "#C7C2E1"
COLOR_MUTED = "#A39EBD"
COLOR_SUCCESS = "#34D399"
COLOR_WARNING = "#FBBF24"
COLOR_ERROR = "#F87171"
COLOR_GOLD = "#FBBF24"
COLOR_SILVER = "#C7C2E1"
COLOR_BRONZE = "#F97316"

FONT_FAMILY = "Helvetica"
FONT_HERO = (FONT_FAMILY, 22, "bold")
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 14, "bold")
FONT_SECTION = (FONT_FAMILY, 12, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_BODY_BOLD = (FONT_FAMILY, 11, "bold")
FONT_SMALL = (FONT_FAMILY, 9)
FONT_SMALL_BOLD = (FONT_FAMILY, 9, "bold")
FONT_PODIUM_NUM = (FONT_FAMILY, 24, "bold")
FONT_PODIUM_SCORE = (FONT_FAMILY, 13, "bold")


def configure_app_theme(root: tk.Tk) -> None:
    """Configures ttk 'clam' theme and all component styles using named constants."""
    style = ttk.Style(root)
    style.theme_use("clam")

    # Base Root / Frame
    root.configure(bg=COLOR_WINDOW)
    style.configure("TFrame", background=COLOR_WINDOW)
    style.configure("Card.TFrame", background=COLOR_CARD, relief="solid", borderwidth=1)
    style.configure("Border.TFrame", background=COLOR_BORDER)
    style.configure("Secondary.TFrame", background=COLOR_SECONDARY)

    # Labels
    style.configure("TLabel", background=COLOR_WINDOW, foreground=COLOR_BODY, font=FONT_BODY)
    style.configure("Card.TLabel", background=COLOR_CARD, foreground=COLOR_BODY, font=FONT_BODY)
    style.configure("CardMuted.TLabel", background=COLOR_CARD, foreground=COLOR_MUTED, font=FONT_SMALL)
    style.configure("Title.TLabel", background=COLOR_WINDOW, foreground=COLOR_TITLE, font=FONT_TITLE)
    style.configure("CardTitle.TLabel", background=COLOR_CARD, foreground=COLOR_TITLE, font=FONT_SUBTITLE)
    style.configure("Section.TLabel", background=COLOR_CARD, foreground=COLOR_TITLE, font=FONT_SECTION)
    style.configure("Hero.TLabel", background=COLOR_WINDOW, foreground=COLOR_TITLE, font=FONT_HERO)
    style.configure("Muted.TLabel", background=COLOR_WINDOW, foreground=COLOR_MUTED, font=FONT_SMALL)
    style.configure("Success.TLabel", background=COLOR_CARD, foreground=COLOR_SUCCESS, font=FONT_BODY_BOLD)
    style.configure("Warning.TLabel", background=COLOR_CARD, foreground=COLOR_WARNING, font=FONT_BODY_BOLD)
    style.configure("Error.TLabel", background=COLOR_CARD, foreground=COLOR_ERROR, font=FONT_BODY_BOLD)

    # Buttons
    style.configure(
        "Primary.TButton",
        background=COLOR_PRIMARY,
        foreground=COLOR_TITLE,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        focuscolor=COLOR_PRIMARY_HOVER,
        padding=[12, 6]
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLOR_PRIMARY_HOVER), ("disabled", COLOR_SECONDARY)],
        foreground=[("disabled", COLOR_MUTED)]
    )

    style.configure(
        "Secondary.TButton",
        background=COLOR_SECONDARY,
        foreground=COLOR_TITLE,
        font=FONT_BODY_BOLD,
        borderwidth=1,
        bordercolor=COLOR_BORDER,
        focuscolor=COLOR_SECONDARY_HOVER,
        padding=[10, 5]
    )
    style.map(
        "Secondary.TButton",
        background=[("active", COLOR_SECONDARY_HOVER), ("disabled", COLOR_CARD)],
        foreground=[("disabled", COLOR_MUTED)]
    )

    style.configure(
        "Danger.TButton",
        background=COLOR_ERROR,
        foreground=COLOR_TITLE,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=[10, 5]
    )
    style.map(
        "Danger.TButton",
        background=[("active", COLOR_WARNING), ("disabled", COLOR_SECONDARY)]
    )

    style.configure(
        "Success.TButton",
        background=COLOR_SUCCESS,
        foreground=COLOR_WINDOW,
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=[10, 5]
    )
    style.map(
        "Success.TButton",
        background=[("active", COLOR_BODY), ("disabled", COLOR_SECONDARY)]
    )

    # Entries & Comboboxes
    style.configure(
        "TEntry",
        fieldbackground=COLOR_CARD,
        foreground=COLOR_TITLE,
        insertcolor=COLOR_TITLE,
        bordercolor=COLOR_BORDER,
        lightcolor=COLOR_BORDER,
        darkcolor=COLOR_BORDER,
        padding=[6, 4]
    )
    style.configure(
        "TCombobox",
        fieldbackground=COLOR_CARD,
        background=COLOR_SECONDARY,
        foreground=COLOR_TITLE,
        arrowcolor=COLOR_TITLE,
        bordercolor=COLOR_BORDER,
        padding=[6, 4]
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", COLOR_CARD)],
        selectbackground=[("readonly", COLOR_PRIMARY)],
        selectforeground=[("readonly", COLOR_TITLE)]
    )

    # Checkbuttons
    style.configure(
        "TCheckbutton",
        background=COLOR_CARD,
        foreground=COLOR_BODY,
        font=FONT_BODY,
        focuscolor=COLOR_CARD
    )
    style.map(
        "TCheckbutton",
        background=[("active", COLOR_CARD)],
        foreground=[("active", COLOR_TITLE)]
    )

    # Notebook Tabs
    style.configure("TNotebook", background=COLOR_WINDOW, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=COLOR_SECONDARY,
        foreground=COLOR_MUTED,
        font=FONT_BODY_BOLD,
        padding=[16, 8],
        borderwidth=0
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_PRIMARY), ("active", COLOR_PRIMARY_HOVER)],
        foreground=[("selected", COLOR_TITLE), ("active", COLOR_TITLE)]
    )

    # Treeview (Data Tables)
    style.configure(
        "Treeview",
        background=COLOR_CARD,
        fieldbackground=COLOR_CARD,
        foreground=COLOR_BODY,
        font=FONT_BODY,
        rowheight=28,
        bordercolor=COLOR_BORDER,
        borderwidth=1
    )
    style.configure(
        "Treeview.Heading",
        background=COLOR_SECONDARY,
        foreground=COLOR_TITLE,
        font=FONT_BODY_BOLD,
        bordercolor=COLOR_BORDER,
        relief="flat",
        padding=[6, 6]
    )
    style.map(
        "Treeview.Heading",
        background=[("active", COLOR_SECONDARY_HOVER)],
        foreground=[("active", COLOR_TITLE)]
    )
    style.map(
        "Treeview",
        background=[("selected", COLOR_PRIMARY)],
        foreground=[("selected", COLOR_TITLE)]
    )


# =====================================================================
# REUSABLE CUSTOM WIDGETS
# =====================================================================
class Card(tk.Frame):
    """Clean bordered card container."""
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=COLOR_CARD,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            padx=14,
            pady=14,
            **kwargs
        )


class Badge(tk.Label):
    """Colored badge tag."""
    def __init__(self, parent, text: str, status_type: str = "default", **kwargs):
        bg_col = COLOR_SECONDARY
        fg_col = COLOR_BODY
        if status_type in [STATUS_REG_OPEN, "success", STATUS_QUALIFIED]:
            bg_col = COLOR_SECONDARY
            fg_col = COLOR_SUCCESS
        elif status_type in [STATUS_JUDGING, "warning"]:
            bg_col = COLOR_SECONDARY
            fg_col = COLOR_WARNING
        elif status_type in [STATUS_COMPLETED, "primary"]:
            bg_col = COLOR_PRIMARY
            fg_col = COLOR_TITLE
        elif status_type in [STATUS_DISQUALIFIED, STATUS_ELIMINATED, "error"]:
            bg_col = COLOR_SECONDARY
            fg_col = COLOR_ERROR

        super().__init__(
            parent,
            text=f"  {text}  ",
            bg=bg_col,
            fg=fg_col,
            font=FONT_SMALL_BOLD,
            relief="flat",
            padx=6,
            pady=2,
            **kwargs
        )


# =====================================================================
# MAIN APPLICATION CONTROLLER / NAVIGATOR
# =====================================================================
class HackHubApp(tk.Tk):
    def __init__(self, store: Store):
        super().__init__()
        self.store = store
        self.title("HackHub - Hackathon Management")
        self.minsize(960, 600)
        self.geometry("1100x720")
        self.configure(bg=COLOR_WINDOW)

        configure_app_theme(self)

        # Main window layout using grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top Navigation Bar
        self.top_bar = tk.Frame(self, bg=COLOR_SECONDARY, height=54, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        # Content Area (swapped frames)
        self.content_container = tk.Frame(self, bg=COLOR_WINDOW)
        self.content_container.grid(row=1, column=0, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)

        # Bottom Status Bar
        self.status_bar_frame = tk.Frame(self, bg=COLOR_CARD, height=26, highlightbackground=COLOR_BORDER, highlightthickness=1)
        self.status_bar_frame.grid(row=2, column=0, sticky="ew")
        self.status_bar_frame.grid_propagate(False)

        self.status_label = tk.Label(
            self.status_bar_frame,
            text="Ready",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=FONT_SMALL,
            anchor="w",
            padx=12
        )
        self.status_label.pack(side="left", fill="both", expand=True)

        self._active_screen: Optional[tk.Frame] = None
        self._current_event_id: Optional[str] = None
        self._build_top_bar()

        # Start at login screen
        self.navigate_to("LOGIN")

    def set_status(self, message: str, level: str = "info") -> None:
        prefix = "⚡ " if level == "info" else ("✓ " if level == "success" else "⚠ ")
        self.status_label.config(text=f"{prefix}{message}")

    def _build_top_bar(self) -> None:
        for widget in self.top_bar.winfo_children():
            widget.destroy()

        # Left branding + breadcrumb
        left_box = tk.Frame(self.top_bar, bg=COLOR_SECONDARY)
        left_box.pack(side="left", fill="y", padx=16)

        logo = tk.Label(
            left_box,
            text="⚡ HackHub",
            bg=COLOR_SECONDARY,
            fg=COLOR_TITLE,
            font=FONT_SUBTITLE,
            cursor="hand2"
        )
        logo.pack(side="left", pady=12)
        logo.bind("<Button-1>", lambda e: self.on_home_click())

        if self.store.current_user and self._current_event_id:
            event = self.store.get_event(self._current_event_id)
            ev_title = event.title if event else "Event"
            sep = tk.Label(left_box, text="  /  ", bg=COLOR_SECONDARY, fg=COLOR_MUTED, font=FONT_BODY)
            sep.pack(side="left")

            back_btn = ttk.Button(
                left_box,
                text="← My Events",
                style="Secondary.TButton",
                command=self.show_my_events
            )
            back_btn.pack(side="left", padx=4)

            crumb = tk.Label(
                left_box,
                text=f"  {ev_title}",
                bg=COLOR_SECONDARY,
                fg=COLOR_BODY,
                font=FONT_BODY_BOLD
            )
            crumb.pack(side="left")

        # Right user info & controls
        right_box = tk.Frame(self.top_bar, bg=COLOR_SECONDARY)
        right_box.pack(side="right", fill="y", padx=16)

        user = self.store.current_user
        if user:
            user_lbl = tk.Label(
                right_box,
                text=f"👤 {user.name} ({user.role})",
                bg=COLOR_SECONDARY,
                fg=COLOR_TITLE,
                font=FONT_BODY_BOLD
            )
            user_lbl.pack(side="left", padx=10, pady=12)

            logout_btn = ttk.Button(
                right_box,
                text="Log out",
                style="Secondary.TButton",
                command=self.on_logout
            )
            logout_btn.pack(side="left", padx=4)

    def on_home_click(self) -> None:
        if self.store.current_user:
            self.show_my_events()
        else:
            self.show_login()

    def on_logout(self) -> None:
        self.store.logout()
        self._current_event_id = None
        self.set_status("Logged out successfully.")
        self.show_login()

    def navigate_to(self, screen_name: str, event_id: Optional[str] = None, **kwargs) -> None:
        """Central navigator to switch between frames."""
        self._current_event_id = event_id
        self._build_top_bar()

        if self._active_screen:
            # Check if active screen has cleanup method
            if hasattr(self._active_screen, "cleanup"):
                self._active_screen.cleanup()
            self._active_screen.destroy()
            self._active_screen = None

        if screen_name == "LOGIN":
            self._active_screen = LoginScreen(self.content_container, self)
        elif screen_name == "MY_EVENTS":
            self._active_screen = MyEventsScreen(self.content_container, self)
        elif screen_name == "ORGANIZER":
            self._active_screen = OrganizerScreen(self.content_container, self, event_id)
        elif screen_name == "JUDGE":
            self._active_screen = JudgeScreen(self.content_container, self, event_id)
        elif screen_name == "VOLUNTEER":
            self._active_screen = VolunteerScreen(self.content_container, self, event_id)
        elif screen_name == "PARTICIPANT":
            self._active_screen = ParticipantScreen(self.content_container, self, event_id)
        elif screen_name == "LEADERBOARD":
            self._active_screen = LeaderboardScreen(self.content_container, self, event_id)

        if self._active_screen:
            self._active_screen.grid(row=0, column=0, sticky="nsew")

    def show_login(self) -> None:
        self.navigate_to("LOGIN")

    def show_my_events(self) -> None:
        self.navigate_to("MY_EVENTS")

    def open_event_for_user(self, event_id: str, role_override: Optional[str] = None) -> None:
        """Opens event screen according to user's role in this event."""
        user = self.store.current_user
        if not user:
            self.show_login()
            return

        role = role_override or self.store.get_user_role_in_event(event_id, user.id)
        if role == "ORGANIZER":
            self.navigate_to("ORGANIZER", event_id)
        elif role == "JUDGE":
            self.navigate_to("JUDGE", event_id)
        elif role == "VOLUNTEER":
            self.navigate_to("VOLUNTEER", event_id)
        else:
            self.navigate_to("PARTICIPANT", event_id)


# =====================================================================
# SCREEN 1: LOGIN / REGISTER
# =====================================================================
class LoginScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp):
        super().__init__(parent, bg=COLOR_WINDOW)
        self.app = app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.is_register_mode = False
        self._build_ui()

    def _build_ui(self) -> None:
        for w in self.winfo_children():
            w.destroy()

        center_card = Card(self)
        center_card.place(relx=0.5, rely=0.5, anchor="center", width=480)

        # Header
        title_text = "Create an Account" if self.is_register_mode else "Welcome to HackHub"
        subtitle_text = "Register as a participant, judge, volunteer or organizer" if self.is_register_mode else "Sign in to manage and participate in hackathons"

        tk.Label(center_card, text=title_text, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_TITLE).pack(anchor="w", pady=(0, 4))
        tk.Label(center_card, text=subtitle_text, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(0, 16))

        # Fields
        if self.is_register_mode:
            tk.Label(center_card, text="Full Name", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
            self.name_entry = ttk.Entry(center_card)
            self.name_entry.pack(fill="x", pady=(0, 8))

            tk.Label(center_card, text="Desired Primary Role", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
            self.role_combo = ttk.Combobox(center_card, state="readonly", values=["PARTICIPANT", "ORGANIZER", "JUDGE", "VOLUNTEER"])
            self.role_combo.set("PARTICIPANT")
            self.role_combo.pack(fill="x", pady=(0, 8))

        tk.Label(center_card, text="Email Address", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.email_entry = ttk.Entry(center_card)
        self.email_entry.pack(fill="x", pady=(0, 8))

        tk.Label(center_card, text="Password", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.pwd_entry = ttk.Entry(center_card, show="*")
        self.pwd_entry.pack(fill="x", pady=(0, 16))

        # Submit on Enter key
        self.pwd_entry.bind("<Return>", lambda e: self.on_submit())
        self.email_entry.bind("<Return>", lambda e: self.on_submit())
        if self.is_register_mode:
            self.name_entry.bind("<Return>", lambda e: self.on_submit())

        # Submit Button
        btn_text = "Create Account" if self.is_register_mode else "Sign In"
        submit_btn = ttk.Button(center_card, text=btn_text, style="Primary.TButton", command=self.on_submit)
        submit_btn.pack(fill="x", pady=(4, 8))

        # Toggle Register / Login mode
        toggle_frame = tk.Frame(center_card, bg=COLOR_CARD)
        toggle_frame.pack(fill="x", pady=(4, 16))
        prompt_txt = "Already have an account?" if self.is_register_mode else "Don't have an account yet?"
        link_txt = "Sign In" if self.is_register_mode else "Register here"

        tk.Label(toggle_frame, text=prompt_txt, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(side="left")
        link_btn = tk.Label(toggle_frame, text=f" {link_txt}", bg=COLOR_CARD, fg=COLOR_PRIMARY, font=FONT_SMALL_BOLD, cursor="hand2")
        link_btn.pack(side="left")
        link_btn.bind("<Button-1>", lambda e: self.toggle_mode())

        # Demo Logins Section
        demo_box = tk.LabelFrame(
            center_card,
            text=" Quick Demo Logins (Click to autofill & login) ",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=FONT_SMALL_BOLD,
            padx=10,
            pady=8
        )
        demo_box.pack(fill="x", pady=(8, 0))

        demo_users = self.app.store.get_demo_users()
        for du in demo_users:
            btn = ttk.Button(
                demo_box,
                text=f"{du['role']}: {du['name']}",
                style="Secondary.TButton",
                command=lambda d=du: self.quick_demo_login(d)
            )
            btn.pack(fill="x", pady=2)

        # Set default focus
        if self.is_register_mode:
            self.name_entry.focus_set()
        else:
            self.email_entry.focus_set()

    def toggle_mode(self) -> None:
        self.is_register_mode = not self.is_register_mode
        self._build_ui()

    def quick_demo_login(self, demo: Dict[str, str]) -> None:
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, demo["email"])
        self.pwd_entry.delete(0, tk.END)
        self.pwd_entry.insert(0, demo["password"])
        self.on_submit()

    def on_submit(self) -> None:
        email = self.email_entry.get().strip()
        pwd = self.pwd_entry.get().strip()

        if self.is_register_mode:
            name = self.name_entry.get().strip()
            role = self.role_combo.get()
            success, msg, user = self.app.store.register(email, pwd, name, role)
            if success:
                self.app.set_status(f"Welcome, {user.name}!", "success")
                self.app.show_my_events()
            else:
                messagebox.showerror("Registration Error", msg)
        else:
            success, msg, user = self.app.store.authenticate(email, pwd)
            if success:
                self.app.set_status(f"Welcome back, {user.name}!", "success")
                self.app.show_my_events()
            else:
                messagebox.showerror("Login Failed", msg)


# =====================================================================
# SCREEN 2: MY EVENTS
# =====================================================================
class MyEventsScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp):
        super().__init__(parent, bg=COLOR_WINDOW)
        self.app = app
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        # Left Column: Event List
        left_frame = tk.Frame(self, bg=COLOR_WINDOW, padx=24, pady=20)
        left_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(left_frame, text="My Events", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_TITLE).pack(anchor="w", pady=(0, 4))
        tk.Label(
            left_frame,
            text="Select an event to access your role-based dashboard.",
            bg=COLOR_WINDOW,
            fg=COLOR_MUTED,
            font=FONT_BODY
        ).pack(anchor="w", pady=(0, 16))

        # Scrollable event cards container
        canvas = tk.Canvas(left_frame, bg=COLOR_WINDOW, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_WINDOW)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate user events
        user = self.app.store.current_user
        user_events = self.app.store.get_events_for_user(user.id if user else "")

        if not user_events:
            empty_card = Card(scrollable_frame)
            empty_card.pack(fill="x", pady=12)
            tk.Label(
                empty_card,
                text="No events yet",
                bg=COLOR_CARD,
                fg=COLOR_TITLE,
                font=FONT_SUBTITLE
            ).pack(anchor="w", pady=(0, 4))
            tk.Label(
                empty_card,
                text="Create a new event using the form on the right to get started!",
                bg=COLOR_CARD,
                fg=COLOR_MUTED,
                font=FONT_BODY
            ).pack(anchor="w")
        else:
            for event, role in user_events:
                self._create_event_card(scrollable_frame, event, role)

        # Right Column: Create Event Card
        right_frame = tk.Frame(self, bg=COLOR_WINDOW, padx=24, pady=20)
        right_frame.grid(row=0, column=1, sticky="nsew")

        create_card = Card(right_frame)
        create_card.pack(fill="x")

        tk.Label(create_card, text="Create New Hackathon", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(anchor="w", pady=(0, 4))
        tk.Label(create_card, text="You will be designated as the Organizer.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(0, 14))

        tk.Label(create_card, text="Event Title", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.new_title_entry = ttk.Entry(create_card)
        self.new_title_entry.pack(fill="x", pady=(0, 10))

        tk.Label(create_card, text="Description", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.new_desc_text = tk.Text(
            create_card,
            height=5,
            bg=COLOR_CARD,
            fg=COLOR_TITLE,
            insertbackground=COLOR_TITLE,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            font=FONT_BODY
        )
        self.new_desc_text.pack(fill="x", pady=(0, 16))

        create_btn = ttk.Button(
            create_card,
            text="+ Create Event",
            style="Primary.TButton",
            command=self.on_create_event
        )
        create_btn.pack(fill="x")

    def _create_event_card(self, parent: tk.Widget, event: Event, role: str) -> None:
        card = Card(parent)
        card.pack(fill="x", pady=8)

        # Header row: Title + Status + Role badge
        hdr = tk.Frame(card, bg=COLOR_CARD)
        hdr.pack(fill="x", pady=(0, 6))

        tk.Label(hdr, text=event.title, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(side="left")
        Badge(hdr, event.status, status_type=event.status).pack(side="right", padx=(6, 0))
        Badge(hdr, f"Role: {role}", status_type="default").pack(side="right")

        # Description
        desc_text = event.description if len(event.description) < 140 else event.description[:137] + "..."
        tk.Label(card, text=desc_text, bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY, wraplength=480, justify="left").pack(anchor="w", pady=(0, 10))

        # Metrics row
        metrics_frame = tk.Frame(card, bg=COLOR_CARD)
        metrics_frame.pack(fill="x", pady=(0, 12))

        teams_count = len(event.teams)
        rounds_count = len(event.rounds)
        judges_count = len(event.judge_ids)

        tk.Label(metrics_frame, text=f"👥 {teams_count} Teams   •   🎯 {rounds_count} Rounds   •   ⚖️ {judges_count} Judges", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL_BOLD).pack(side="left")

        # Actions row
        actions_frame = tk.Frame(card, bg=COLOR_CARD)
        actions_frame.pack(fill="x")

        # Primary action opens role-based screen
        role_label_action = {
            "ORGANIZER": "Open Organizer Console →",
            "JUDGE": "Open Judge Workspace →",
            "VOLUNTEER": "Open Volunteer Schedule →",
            "PARTICIPANT": "Open Team Page →"
        }.get(role, "Enter Event →")

        open_btn = ttk.Button(
            actions_frame,
            text=role_label_action,
            style="Primary.TButton",
            command=lambda eid=event.id, r=role: self.app.open_event_for_user(eid, r)
        )
        open_btn.pack(side="left", padx=(0, 8))

        # Leaderboard button (accessible to organizer anytime, and to everyone when completed)
        if role == "ORGANIZER" or event.status == STATUS_COMPLETED:
            lb_btn = ttk.Button(
                actions_frame,
                text="🏆 Leaderboard",
                style="Secondary.TButton",
                command=lambda eid=event.id: self.app.navigate_to("LEADERBOARD", eid)
            )
            lb_btn.pack(side="left")

        # Role switcher preview for organizers to easily inspect other perspectives
        if role == "ORGANIZER":
            preview_box = tk.Frame(actions_frame, bg=COLOR_CARD)
            preview_box.pack(side="right")
            tk.Label(preview_box, text="Preview as: ", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(side="left")

            preview_combo = ttk.Combobox(
                preview_box,
                state="readonly",
                values=["JUDGE", "VOLUNTEER", "PARTICIPANT"],
                width=12
            )
            preview_combo.set("JUDGE")
            preview_combo.pack(side="left", padx=4)

            go_preview_btn = ttk.Button(
                preview_box,
                text="Go",
                style="Secondary.TButton",
                command=lambda eid=event.id, cb=preview_combo: self.app.open_event_for_user(eid, cb.get())
            )
            go_preview_btn.pack(side="left")

    def on_create_event(self) -> None:
        title = self.new_title_entry.get().strip()
        desc = self.new_desc_text.get("1.0", tk.END).strip()
        user = self.app.store.current_user

        if not title:
            messagebox.showwarning("Validation Error", "Please enter an event title.")
            return

        success, msg, event = self.app.store.create_event(title, desc, user.id if user else "")
        if success:
            self.app.set_status(f"Created event '{title}'", "success")
            self.app.show_my_events()
        else:
            messagebox.showerror("Error", msg)


# =====================================================================
# SCREEN 3: ORGANIZER EVENT VIEW (NOTEBOOK WITH 6 TABS)
# =====================================================================
class OrganizerScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp, event_id: str):
        super().__init__(parent, bg=COLOR_WINDOW)
        self.app = app
        self.event_id = event_id
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        event = self.app.store.get_event(self.event_id)
        if not event:
            tk.Label(self, text="Event not found", bg=COLOR_WINDOW, fg=COLOR_ERROR, font=FONT_TITLE).pack(pady=40)
            return

        # Header banner
        header_frame = tk.Frame(self, bg=COLOR_CARD, padx=20, pady=14, highlightbackground=COLOR_BORDER, highlightthickness=1)
        header_frame.grid(row=0, column=0, sticky="ew")

        left_hdr = tk.Frame(header_frame, bg=COLOR_CARD)
        left_hdr.pack(side="left")

        tk.Label(left_hdr, text=event.title, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_TITLE).pack(side="left", padx=(0, 10))
        Badge(left_hdr, event.status, status_type=event.status).pack(side="left")

        right_hdr = tk.Frame(header_frame, bg=COLOR_CARD)
        right_hdr.pack(side="right")

        lb_btn = ttk.Button(
            right_hdr,
            text="🏆 Live Leaderboard",
            style="Primary.TButton",
            command=lambda: self.app.navigate_to("LEADERBOARD", self.event_id)
        )
        lb_btn.pack(side="right", padx=6)

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=16, pady=12)

        # Tabs
        self.tab_overview = OverviewTab(self.notebook, self)
        self.tab_teams = TeamsTab(self.notebook, self)
        self.tab_staff = StaffTab(self.notebook, self)
        self.tab_rounds = RoundsCriteriaTab(self.notebook, self)
        self.tab_panels = PanelsTab(self.notebook, self)
        self.tab_results = ResultsTab(self.notebook, self)

        self.notebook.add(self.tab_overview, text=" Overview ")
        self.notebook.add(self.tab_teams, text=" Teams ")
        self.notebook.add(self.tab_staff, text=" Judges & Volunteers ")
        self.notebook.add(self.tab_rounds, text=" Rounds & Criteria ")
        self.notebook.add(self.tab_panels, text=" Panels ")
        self.notebook.add(self.tab_results, text=" Results & Progression ")

    def refresh_all(self) -> None:
        self.app.navigate_to("ORGANIZER", self.event_id)


# --- TAB 1: OVERVIEW & STATUS STEPPER ---
class OverviewTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id
        self._build_ui()

    def _build_ui(self) -> None:
        event = self.app.store.get_event(self.event_id)
        if not event:
            return

        # Status Stepper Card
        stepper_card = Card(self)
        stepper_card.pack(fill="x", pady=(0, 20))

        tk.Label(stepper_card, text="Event Progression Stepper", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(anchor="w", pady=(0, 14))

        stepper_row = tk.Frame(stepper_card, bg=COLOR_CARD)
        stepper_row.pack(fill="x", pady=(0, 16))

        curr_idx = EVENT_STATUSES.index(event.status)

        for idx, st in enumerate(EVENT_STATUSES):
            step_box = tk.Frame(stepper_row, bg=COLOR_CARD)
            step_box.pack(side="left", expand=True)

            is_done = idx < curr_idx
            is_current = idx == curr_idx

            if is_done:
                circle_bg = COLOR_SUCCESS
                circle_fg = COLOR_WINDOW
                circle_text = "✓"
                label_fg = COLOR_SUCCESS
            elif is_current:
                circle_bg = COLOR_PRIMARY
                circle_fg = COLOR_TITLE
                circle_text = str(idx + 1)
                label_fg = COLOR_TITLE
            else:
                circle_bg = COLOR_SECONDARY
                circle_fg = COLOR_MUTED
                circle_text = str(idx + 1)
                label_fg = COLOR_MUTED

            circle = tk.Label(
                step_box,
                text=circle_text,
                bg=circle_bg,
                fg=circle_fg,
                font=FONT_BODY_BOLD,
                width=3,
                height=1,
                relief="flat"
            )
            circle.pack()

            tk.Label(
                step_box,
                text=st.replace("_", " "),
                bg=COLOR_CARD,
                fg=label_fg,
                font=FONT_SMALL_BOLD
            ).pack(pady=(4, 0))

            if idx < len(EVENT_STATUSES) - 1:
                line_col = COLOR_SUCCESS if is_done else COLOR_BORDER
                line = tk.Frame(stepper_row, bg=line_col, height=2)
                line.pack(side="left", fill="x", expand=True, pady=8)

        # Stepper Action Area
        action_row = tk.Frame(stepper_card, bg=COLOR_CARD)
        action_row.pack(fill="x", pady=(8, 0))

        if curr_idx < len(EVENT_STATUSES) - 1:
            next_status = EVENT_STATUSES[curr_idx + 1]
            btn_text = f"Advance to {next_status.replace('_', ' ')} →"
            advance_btn = ttk.Button(
                action_row,
                text=btn_text,
                style="Primary.TButton",
                command=lambda: self.on_advance_status(next_status)
            )
            advance_btn.pack(side="left")
            tk.Label(
                action_row,
                text=f"Note: Advancing status unlocks new stages and cannot be undone.",
                bg=COLOR_CARD,
                fg=COLOR_MUTED,
                font=FONT_SMALL
            ).pack(side="left", padx=12)
        else:
            tk.Label(
                action_row,
                text="🎉 Event has reached COMPLETED status. Scores and ranks are final.",
                bg=COLOR_CARD,
                fg=COLOR_SUCCESS,
                font=FONT_BODY_BOLD
            ).pack(side="left")

        # Metrics Summary Row
        metrics_grid = tk.Frame(self, bg=COLOR_WINDOW)
        metrics_grid.pack(fill="x", pady=(0, 20))
        for col in range(4):
            metrics_grid.grid_columnconfigure(col, weight=1, uniform="metric")

        teams = event.teams
        checked_in_count = sum(1 for t in teams if t.checked_in)
        active_teams = sum(1 for t in teams if not t.is_disqualified)

        self._create_metric_box(metrics_grid, 0, "Registered Teams", f"{len(teams)}", f"{active_teams} active, {checked_in_count} checked-in")
        self._create_metric_box(metrics_grid, 1, "Staff Assigned", f"{len(event.judge_ids) + len(event.volunteer_ids)}", f"{len(event.judge_ids)} judges, {len(event.volunteer_ids)} volunteers")
        self._create_metric_box(metrics_grid, 2, "Rounds Configured", f"{len(event.rounds)}", f"{len(event.panels)} panel(s) total")
        self._create_metric_box(metrics_grid, 3, "Scores Saved", f"{len(event.scores)}", "Across all active panels")

        # Description / Details Card
        info_card = Card(self)
        info_card.pack(fill="both", expand=True)
        tk.Label(info_card, text="Hackathon Details", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(anchor="w", pady=(0, 6))
        tk.Label(info_card, text=event.description, bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY, wraplength=700, justify="left").pack(anchor="w")

    def _create_metric_box(self, parent: tk.Widget, col: int, title: str, value: str, sub: str) -> None:
        c = Card(parent)
        c.grid(row=0, column=col, padx=6, sticky="nsew")
        tk.Label(c, text=title, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL_BOLD).pack(anchor="w")
        tk.Label(c, text=value, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_HERO).pack(anchor="w", pady=(4, 2))
        tk.Label(c, text=sub, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(anchor="w")

    def on_advance_status(self, next_status: str) -> None:
        confirm = messagebox.askyesno(
            "Confirm Status Advance",
            f"Are you sure you want to advance the event to '{next_status}'?\n\nThis will trigger the next stage of the hackathon."
        )
        if not confirm:
            return

        success, msg = self.app.store.advance_event_status(self.event_id)
        if success:
            self.app.set_status(msg, "success")
            self.screen.refresh_all()
        else:
            messagebox.showwarning("Cannot Advance Status", msg)


# --- TAB 2: TEAMS MANAGEMENT ---
class TeamsTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id
        self.sort_descending = False
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Filter Bar & Actions Top Row
        top_bar = tk.Frame(self, bg=COLOR_WINDOW)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(top_bar, text="Search / Filter:", bg=COLOR_WINDOW, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_table())
        search_entry = ttk.Entry(top_bar, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(0, 16))

        # Buttons
        self.disqualify_btn = ttk.Button(
            top_bar,
            text="⚠️ Disqualify Team",
            style="Danger.TButton",
            command=self.on_disqualify
        )
        self.disqualify_btn.pack(side="right", padx=4)

        self.reinstate_btn = ttk.Button(
            top_bar,
            text="✓ Reinstate Team",
            style="Success.TButton",
            command=self.on_reinstate
        )
        self.reinstate_btn.pack(side="right", padx=4)

        # Teams Treeview Table
        table_frame = tk.Frame(self, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("name", "project", "members", "checked_in", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("name", text="Team Name ↕", command=lambda: self.sort_column("name"))
        self.tree.heading("project", text="Project Title ↕", command=lambda: self.sort_column("project"))
        self.tree.heading("members", text="Members ↕", command=lambda: self.sort_column("members"))
        self.tree.heading("checked_in", text="Checked-In ↕", command=lambda: self.sort_column("checked_in"))
        self.tree.heading("status", text="Status ↕", command=lambda: self.sort_column("status"))

        self.tree.column("name", width=180, anchor="w")
        self.tree.column("project", width=220, anchor="w")
        self.tree.column("members", width=220, anchor="w")
        self.tree.column("checked_in", width=100, anchor="center")
        self.tree.column("status", width=140, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        self.tree.tag_configure("disqualified", foreground=COLOR_ERROR)
        self.tree.tag_configure("active", foreground=COLOR_BODY)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Bottom Detail Card for Selected Team
        self.detail_card = Card(self)
        self.detail_card.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        self.detail_label = tk.Label(
            self.detail_card,
            text="Select a team from the table to view details, inspect disqualification reasons, or change status.",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=FONT_BODY,
            wraplength=900,
            justify="left"
        )
        self.detail_label.pack(anchor="w")

        self.refresh_table()

    def refresh_table(self) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        teams = self.app.store.get_teams(self.event_id)
        query = self.search_var.get().lower().strip()

        for t in teams:
            members_str = ", ".join(t.members)
            checked_str = "Yes" if t.checked_in else "No"
            status_str = "DISQUALIFIED" if t.is_disqualified else "ACTIVE"

            # Filter check
            if query:
                haystack = f"{t.name} {t.project_title} {members_str} {status_str}".lower()
                if query not in haystack:
                    continue

            tag = "disqualified" if t.is_disqualified else "active"
            self.tree.insert(
                "",
                "end",
                iid=t.id,
                values=(t.name, t.project_title, members_str, checked_str, status_str),
                tags=(tag,)
            )

    def sort_column(self, col: str) -> None:
        self.sort_descending = not self.sort_descending
        teams = self.app.store.get_teams(self.event_id)

        key_func = {
            "name": lambda t: t.name.lower(),
            "project": lambda t: t.project_title.lower(),
            "members": lambda t: len(t.members),
            "checked_in": lambda t: 1 if t.checked_in else 0,
            "status": lambda t: 1 if t.is_disqualified else 0
        }.get(col, lambda t: t.name.lower())

        teams.sort(key=key_func, reverse=self.sort_descending)
        self.refresh_table()

    def on_row_select(self, event) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        tid = selected[0]
        team = self.app.store.get_team(self.event_id, tid)
        if not team:
            return

        detail_text = f"Team: {team.name}  |  Project: {team.project_title}\nRepo: {team.repo_url}\nDescription: {team.description}\nMembers: {', '.join(team.members)}"
        if team.is_disqualified:
            detail_text += f"\n\n🚨 DISQUALIFIED: {team.disqualification_reason}"
            self.detail_label.config(text=detail_text, fg=COLOR_ERROR)
            self.disqualify_btn.config(state="disabled")
            self.reinstate_btn.config(state="normal")
        else:
            self.detail_label.config(text=detail_text, fg=COLOR_BODY)
            self.disqualify_btn.config(state="normal")
            self.reinstate_btn.config(state="disabled")

    def on_disqualify(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Team", "Please select a team to disqualify.")
            return
        tid = selected[0]
        team = self.app.store.get_team(self.event_id, tid)
        if not team:
            return

        reason = simpledialog.askstring(
            "Disqualify Team",
            f"Enter mandatory disqualification reason for '{team.name}':",
            parent=self
        )
        if reason is None:
            return  # Cancelled

        if not reason.strip():
            messagebox.showwarning("Reason Required", "Disqualification requires a non-empty reason.")
            return

        success, msg = self.app.store.disqualify_team(self.event_id, tid, reason)
        if success:
            self.app.set_status(msg, "warning")
            self.refresh_table()
            self.tree.selection_set(tid)
            self.on_row_select(None)
        else:
            messagebox.showerror("Error", msg)

    def on_reinstate(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Team", "Please select a team to reinstate.")
            return
        tid = selected[0]
        team = self.app.store.get_team(self.event_id, tid)
        if not team:
            return

        confirm = messagebox.askyesno(
            "Reinstate Team",
            f"Are you sure you want to reinstate Team '{team.name}' to ACTIVE status?"
        )
        if not confirm:
            return

        success, msg = self.app.store.reinstate_team(self.event_id, tid)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_table()
            self.tree.selection_set(tid)
            self.on_row_select(None)
        else:
            messagebox.showerror("Error", msg)


# --- TAB 3: STAFF (JUDGES & VOLUNTEERS) ---
class StaffTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="staff")
        self.grid_columnconfigure(1, weight=1, uniform="staff")

        # Left Column: Judges
        judge_card = Card(self)
        judge_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        judge_card.grid_rowconfigure(2, weight=1)
        judge_card.grid_columnconfigure(0, weight=1)

        tk.Label(judge_card, text="Assigned Judges", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).grid(row=0, column=0, sticky="w", pady=(0, 4))
        tk.Label(judge_card, text="Judges score teams within their assigned panels.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Judges Table
        j_tree_frame = tk.Frame(judge_card, bg=COLOR_CARD)
        j_tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        j_tree_frame.grid_rowconfigure(0, weight=1)
        j_tree_frame.grid_columnconfigure(0, weight=1)

        self.j_tree = ttk.Treeview(j_tree_frame, columns=("name", "email"), show="headings", selectmode="browse")
        self.j_tree.heading("name", text="Name")
        self.j_tree.heading("email", text="Email")
        self.j_tree.column("name", width=150)
        self.j_tree.column("email", width=200)

        j_scroll = ttk.Scrollbar(j_tree_frame, orient="vertical", command=self.j_tree.yview)
        self.j_tree.configure(yscrollcommand=j_scroll.set)
        self.j_tree.grid(row=0, column=0, sticky="nsew")
        j_scroll.grid(row=0, column=1, sticky="ns")

        # Judge Actions
        j_act = tk.Frame(judge_card, bg=COLOR_CARD)
        j_act.grid(row=3, column=0, sticky="ew")

        tk.Label(j_act, text="Add by email:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_SMALL_BOLD).pack(anchor="w", pady=(4, 2))
        j_add_row = tk.Frame(j_act, bg=COLOR_CARD)
        j_add_row.pack(fill="x", pady=(0, 8))

        self.j_email_entry = ttk.Entry(j_add_row)
        self.j_email_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.j_email_entry.bind("<Return>", lambda e: self.on_add_judge())

        add_j_btn = ttk.Button(j_add_row, text="+ Add Judge", style="Primary.TButton", command=self.on_add_judge)
        add_j_btn.pack(side="right")

        rem_j_btn = ttk.Button(j_act, text="Remove Selected Judge", style="Secondary.TButton", command=self.on_remove_judge)
        rem_j_btn.pack(anchor="w")

        # Right Column: Volunteers
        vol_card = Card(self)
        vol_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        vol_card.grid_rowconfigure(2, weight=1)
        vol_card.grid_columnconfigure(0, weight=1)

        tk.Label(vol_card, text="Assigned Volunteers", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).grid(row=0, column=0, sticky="w", pady=(0, 4))
        tk.Label(vol_card, text="Volunteers check in teams and manage panel schedules.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Volunteers Table
        v_tree_frame = tk.Frame(vol_card, bg=COLOR_CARD)
        v_tree_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        v_tree_frame.grid_rowconfigure(0, weight=1)
        v_tree_frame.grid_columnconfigure(0, weight=1)

        self.v_tree = ttk.Treeview(v_tree_frame, columns=("name", "email"), show="headings", selectmode="browse")
        self.v_tree.heading("name", text="Name")
        self.v_tree.heading("email", text="Email")
        self.v_tree.column("name", width=150)
        self.v_tree.column("email", width=200)

        v_scroll = ttk.Scrollbar(v_tree_frame, orient="vertical", command=self.v_tree.yview)
        self.v_tree.configure(yscrollcommand=v_scroll.set)
        self.v_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")

        # Volunteer Actions
        v_act = tk.Frame(vol_card, bg=COLOR_CARD)
        v_act.grid(row=3, column=0, sticky="ew")

        tk.Label(v_act, text="Add by email:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_SMALL_BOLD).pack(anchor="w", pady=(4, 2))
        v_add_row = tk.Frame(v_act, bg=COLOR_CARD)
        v_add_row.pack(fill="x", pady=(0, 8))

        self.v_email_entry = ttk.Entry(v_add_row)
        self.v_email_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.v_email_entry.bind("<Return>", lambda e: self.on_add_volunteer())

        add_v_btn = ttk.Button(v_add_row, text="+ Add Volunteer", style="Primary.TButton", command=self.on_add_volunteer)
        add_v_btn.pack(side="right")

        rem_v_btn = ttk.Button(v_act, text="Remove Selected Volunteer", style="Secondary.TButton", command=self.on_remove_volunteer)
        rem_v_btn.pack(anchor="w")

        self.refresh_staff()

    def refresh_staff(self) -> None:
        # Refresh judges
        for r in self.j_tree.get_children():
            self.j_tree.delete(r)
        judges = self.app.store.get_judges(self.event_id)
        for j in judges:
            self.j_tree.insert("", "end", iid=j.id, values=(j.name, j.email))

        # Refresh volunteers
        for r in self.v_tree.get_children():
            self.v_tree.delete(r)
        volunteers = self.app.store.get_volunteers(self.event_id)
        for v in volunteers:
            self.v_tree.insert("", "end", iid=v.id, values=(v.name, v.email))

    def on_add_judge(self) -> None:
        email = self.j_email_entry.get().strip()
        if not email:
            messagebox.showwarning("Validation", "Please enter judge's email address.")
            return
        success, msg = self.app.store.add_judge_by_email(self.event_id, email)
        if success:
            self.app.set_status(msg, "success")
            self.j_email_entry.delete(0, tk.END)
            self.refresh_staff()
        else:
            messagebox.showwarning("Notice", msg)

    def on_remove_judge(self) -> None:
        sel = self.j_tree.selection()
        if not sel:
            messagebox.showinfo("Select Judge", "Please select a judge to remove.")
            return
        jid = sel[0]
        confirm = messagebox.askyesno("Confirm Removal", "Remove this judge from the event?")
        if not confirm:
            return
        success, msg = self.app.store.remove_judge(self.event_id, jid)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_staff()
        else:
            messagebox.showerror("Error", msg)

    def on_add_volunteer(self) -> None:
        email = self.v_email_entry.get().strip()
        if not email:
            messagebox.showwarning("Validation", "Please enter volunteer's email address.")
            return
        success, msg = self.app.store.add_volunteer_by_email(self.event_id, email)
        if success:
            self.app.set_status(msg, "success")
            self.v_email_entry.delete(0, tk.END)
            self.refresh_staff()
        else:
            messagebox.showwarning("Notice", msg)

    def on_remove_volunteer(self) -> None:
        sel = self.v_tree.selection()
        if not sel:
            messagebox.showinfo("Select Volunteer", "Please select a volunteer to remove.")
            return
        vid = sel[0]
        confirm = messagebox.askyesno("Confirm Removal", "Remove this volunteer from the event?")
        if not confirm:
            return
        success, msg = self.app.store.remove_volunteer(self.event_id, vid)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_staff()
        else:
            messagebox.showerror("Error", msg)


# --- TAB 4: ROUNDS AND CRITERIA ---
class RoundsCriteriaTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id

        # Local working criteria list for editing
        self.criteria_entries: List[Dict[str, Any]] = []
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top Bar: Round Selector + Add/Delete Round
        top_bar = tk.Frame(self, bg=COLOR_WINDOW)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        tk.Label(top_bar, text="Select Round:", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 8))

        self.round_combo = ttk.Combobox(top_bar, state="readonly", width=30)
        self.round_combo.pack(side="left", padx=(0, 12))
        self.round_combo.bind("<<ComboboxSelected>>", lambda e: self.on_round_selected())

        add_rnd_btn = ttk.Button(top_bar, text="+ Add Round", style="Primary.TButton", command=self.on_add_round)
        add_rnd_btn.pack(side="left", padx=4)

        del_rnd_btn = ttk.Button(top_bar, text="Delete Round", style="Secondary.TButton", command=self.on_delete_round)
        del_rnd_btn.pack(side="left", padx=4)

        # Main Criteria Card
        self.crit_card = Card(self)
        self.crit_card.grid(row=1, column=0, sticky="nsew")
        self.crit_card.grid_rowconfigure(1, weight=1)
        self.crit_card.grid_columnconfigure(0, weight=1)

        crit_hdr = tk.Frame(self.crit_card, bg=COLOR_CARD)
        crit_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        tk.Label(crit_hdr, text="Evaluation Criteria (Total Weight MUST equal 100%)", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(side="left")

        # Live Weight Counter Label
        self.weight_label = tk.Label(crit_hdr, text="Total weight: 0 / 100", bg=COLOR_CARD, fg=COLOR_ERROR, font=FONT_BODY_BOLD)
        self.weight_label.pack(side="right")

        # Scrollable Frame for Criteria Rows
        canvas = tk.Canvas(self.crit_card, bg=COLOR_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.crit_card, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas, bg=COLOR_CARD)

        self.rows_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Bottom Actions Bar
        bot_bar = tk.Frame(self.crit_card, bg=COLOR_CARD)
        bot_bar.grid(row=2, column=0, sticky="ew", pady=(12, 0))

        add_crit_btn = ttk.Button(bot_bar, text="+ Add Criterion", style="Secondary.TButton", command=self.add_criterion_row)
        add_crit_btn.pack(side="left", padx=(0, 10))

        self.save_btn = ttk.Button(bot_bar, text="Save Criteria", style="Primary.TButton", command=self.on_save_criteria)
        self.save_btn.pack(side="right")

        self.refresh_rounds_dropdown()

    def get_selected_round_id(self) -> Optional[str]:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            return None
        sel_idx = self.round_combo.current()
        if 0 <= sel_idx < len(event.rounds):
            return event.rounds[sel_idx].id
        return event.rounds[0].id

    def refresh_rounds_dropdown(self) -> None:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            self.round_combo["values"] = []
            return
        vals = [f"Round {r.round_number}: {r.name}" for r in event.rounds]
        self.round_combo["values"] = vals
        self.round_combo.current(0)
        self.on_round_selected()

    def on_round_selected(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        round_obj = self.app.store.get_round(self.event_id, round_id)
        if not round_obj:
            return

        # Clear existing row widgets
        for w in self.rows_frame.winfo_children():
            w.destroy()
        self.criteria_entries.clear()

        # Render Header row
        header_row = tk.Frame(self.rows_frame, bg=COLOR_SECONDARY, padx=8, pady=6)
        header_row.pack(fill="x", pady=(0, 6))
        tk.Label(header_row, text="Criterion Name", bg=COLOR_SECONDARY, fg=COLOR_TITLE, font=FONT_BODY_BOLD, width=30, anchor="w").pack(side="left")
        tk.Label(header_row, text="Max Score (pts)", bg=COLOR_SECONDARY, fg=COLOR_TITLE, font=FONT_BODY_BOLD, width=15, anchor="center").pack(side="left", padx=8)
        tk.Label(header_row, text="Weight (%)", bg=COLOR_SECONDARY, fg=COLOR_TITLE, font=FONT_BODY_BOLD, width=15, anchor="center").pack(side="left", padx=8)
        tk.Label(header_row, text="Actions", bg=COLOR_SECONDARY, fg=COLOR_TITLE, font=FONT_BODY_BOLD, width=10, anchor="center").pack(side="right")

        for crit in round_obj.criteria:
            self.add_criterion_row(crit.name, crit.max_score, crit.weight, crit.id)

        self.update_live_weight()

    def add_criterion_row(
        self,
        name: str = "New Criterion",
        max_score: float = 10.0,
        weight: float = 20.0,
        crit_id: Optional[str] = None
    ) -> None:
        row = tk.Frame(self.rows_frame, bg=COLOR_CARD, padx=8, pady=4)
        row.pack(fill="x", pady=2)

        name_var = tk.StringVar(value=name)
        max_var = tk.StringVar(value=str(int(max_score) if max_score.is_integer() else max_score))
        weight_var = tk.StringVar(value=str(int(weight) if weight.is_integer() else weight))

        # Real-time weight tracking
        weight_var.trace_add("write", lambda *args: self.update_live_weight())

        name_ent = ttk.Entry(row, textvariable=name_var, width=32)
        name_ent.pack(side="left")

        max_ent = ttk.Entry(row, textvariable=max_var, width=16, justify="center")
        max_ent.pack(side="left", padx=12)

        weight_ent = ttk.Entry(row, textvariable=weight_var, width=16, justify="center")
        weight_ent.pack(side="left", padx=12)

        entry_data = {
            "id": crit_id,
            "row": row,
            "name_var": name_var,
            "max_var": max_var,
            "weight_var": weight_var
        }
        self.criteria_entries.append(entry_data)

        del_btn = ttk.Button(
            row,
            text="✕ Remove",
            style="Danger.TButton",
            command=lambda ed=entry_data: self.remove_criterion_row(ed)
        )
        del_btn.pack(side="right")

        self.update_live_weight()

    def remove_criterion_row(self, entry_data: Dict[str, Any]) -> None:
        if len(self.criteria_entries) <= 1:
            messagebox.showwarning("Notice", "A round must have at least one evaluation criterion.")
            return

        entry_data["row"].destroy()
        self.criteria_entries.remove(entry_data)
        self.update_live_weight()

    def update_live_weight(self) -> None:
        total = 0.0
        for ed in self.criteria_entries:
            try:
                val = float(ed["weight_var"].get().strip())
                total += val
            except ValueError:
                pass

        if abs(total - 100.0) < 0.001:
            self.weight_label.config(text=f"Total weight: {total:.1f} / 100%  [Valid ✓]", fg=COLOR_SUCCESS)
            self.save_btn.config(state="normal")
        else:
            self.weight_label.config(text=f"Total weight: {total:.1f} / 100%  [Must equal 100%]", fg=COLOR_ERROR)
            self.save_btn.config(state="disabled")

    def on_add_round(self) -> None:
        round_name = simpledialog.askstring("Add Round", "Enter round name (e.g. Semi-Finals):", parent=self)
        if round_name is None:
            return
        success, msg, _ = self.app.store.add_round(self.event_id, round_name)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_rounds_dropdown()
            # Select new round
            event = self.app.store.get_event(self.event_id)
            if event and event.rounds:
                self.round_combo.current(len(event.rounds) - 1)
                self.on_round_selected()
        else:
            messagebox.showwarning("Notice", msg)

    def on_delete_round(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this round and its panel assignments?")
        if not confirm:
            return
        success, msg = self.app.store.delete_round(self.event_id, round_id)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_rounds_dropdown()
        else:
            messagebox.showwarning("Notice", msg)

    def on_save_criteria(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return

        payload = []
        for ed in self.criteria_entries:
            name = ed["name_var"].get().strip()
            try:
                max_score = float(ed["max_var"].get().strip())
                weight = float(ed["weight_var"].get().strip())
            except ValueError:
                messagebox.showerror("Validation Error", "All scores and weights must be valid numbers.")
                return

            payload.append({
                "id": ed["id"],
                "name": name,
                "max_score": max_score,
                "weight": weight
            })

        success, msg = self.app.store.save_round_criteria(self.event_id, round_id, payload)
        if success:
            self.app.set_status(msg, "success")
            messagebox.showinfo("Saved", "Criteria successfully updated and saved!")
        else:
            messagebox.showerror("Cannot Save Criteria", msg)


# --- TAB 5: PANELS ---
class PanelsTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id
        self.selected_panel_id: Optional[str] = None
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)

        # Top Bar: Round selector + Actions
        top_bar = tk.Frame(self, bg=COLOR_WINDOW)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        tk.Label(top_bar, text="Select Round:", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 8))
        self.round_combo = ttk.Combobox(top_bar, state="readonly", width=30)
        self.round_combo.pack(side="left", padx=(0, 14))
        self.round_combo.bind("<<ComboboxSelected>>", lambda e: self.on_round_changed())

        create_pnl_btn = ttk.Button(top_bar, text="+ Create Panel", style="Primary.TButton", command=self.on_create_panel)
        create_pnl_btn.pack(side="left", padx=4)

        auto_bal_btn = ttk.Button(top_bar, text="⚡ Auto-balance Teams", style="Secondary.TButton", command=self.on_auto_balance)
        auto_bal_btn.pack(side="left", padx=4)

        del_pnl_btn = ttk.Button(top_bar, text="Delete Panel", style="Danger.TButton", command=self.on_delete_panel)
        del_pnl_btn.pack(side="left", padx=4)

        # Left Column: Panels List
        left_card = Card(self)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_card.grid_rowconfigure(1, weight=1)
        left_card.grid_columnconfigure(0, weight=1)

        tk.Label(left_card, text="Round Panels", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.panel_listbox = tk.Listbox(
            left_card,
            bg=COLOR_SECONDARY,
            fg=COLOR_TITLE,
            selectbackground=COLOR_PRIMARY,
            selectforeground=COLOR_TITLE,
            font=FONT_BODY,
            highlightthickness=0,
            borderwidth=1,
            relief="solid"
        )
        self.panel_listbox.grid(row=1, column=0, sticky="nsew")
        self.panel_listbox.bind("<<ListboxSelect>>", self.on_panel_select)

        # Right Column: Panel Details (Assigned Judges & Teams)
        self.detail_card = Card(self)
        self.detail_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        self.detail_card.grid_rowconfigure(2, weight=1)
        self.detail_card.grid_rowconfigure(5, weight=1)
        self.detail_card.grid_columnconfigure(0, weight=1)

        self.panel_title_lbl = tk.Label(self.detail_card, text="Select a panel", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE)
        self.panel_title_lbl.grid(row=0, column=0, sticky="w", pady=(0, 6))

        # Judges Section
        tk.Label(self.detail_card, text="Assigned Judges:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).grid(row=1, column=0, sticky="w", pady=(4, 2))
        self.judges_tree = ttk.Treeview(self.detail_card, columns=("name", "email"), show="headings", height=4)
        self.judges_tree.heading("name", text="Name")
        self.judges_tree.heading("email", text="Email")
        self.judges_tree.grid(row=2, column=0, sticky="nsew", pady=(0, 4))

        j_act = tk.Frame(self.detail_card, bg=COLOR_CARD)
        j_act.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        self.avail_judge_combo = ttk.Combobox(j_act, state="readonly", width=24)
        self.avail_judge_combo.pack(side="left", padx=(0, 6))

        assign_j_btn = ttk.Button(j_act, text="+ Assign Judge", style="Secondary.TButton", command=self.on_assign_judge)
        assign_j_btn.pack(side="left", padx=4)

        rem_j_btn = ttk.Button(j_act, text="Remove Judge", style="Secondary.TButton", command=self.on_remove_judge)
        rem_j_btn.pack(side="right")

        # Teams Section
        tk.Label(self.detail_card, text="Assigned Teams:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).grid(row=4, column=0, sticky="w", pady=(4, 2))
        self.teams_tree = ttk.Treeview(self.detail_card, columns=("name", "project"), show="headings", height=5)
        self.teams_tree.heading("name", text="Team Name")
        self.teams_tree.heading("project", text="Project Title")
        self.teams_tree.grid(row=5, column=0, sticky="nsew", pady=(0, 4))

        t_act = tk.Frame(self.detail_card, bg=COLOR_CARD)
        t_act.grid(row=6, column=0, sticky="ew")

        self.avail_team_combo = ttk.Combobox(t_act, state="readonly", width=24)
        self.avail_team_combo.pack(side="left", padx=(0, 6))

        assign_t_btn = ttk.Button(t_act, text="+ Assign Team", style="Secondary.TButton", command=self.on_assign_team)
        assign_t_btn.pack(side="left", padx=4)

        rem_t_btn = ttk.Button(t_act, text="Remove Team", style="Secondary.TButton", command=self.on_remove_team)
        rem_t_btn.pack(side="right")

        self.refresh_rounds()

    def get_selected_round_id(self) -> Optional[str]:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            return None
        sel_idx = self.round_combo.current()
        if 0 <= sel_idx < len(event.rounds):
            return event.rounds[sel_idx].id
        return event.rounds[0].id

    def refresh_rounds(self) -> None:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            return
        vals = [f"Round {r.round_number}: {r.name}" for r in event.rounds]
        self.round_combo["values"] = vals
        self.round_combo.current(0)
        self.on_round_changed()

    def on_round_changed(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        self.refresh_panels_list()

    def refresh_panels_list(self) -> None:
        self.panel_listbox.delete(0, tk.END)
        round_id = self.get_selected_round_id()
        panels = self.app.store.get_panels(self.event_id, round_id)

        self._current_panels = panels
        for p in panels:
            self.panel_listbox.insert(tk.END, f"  {p.name}  ({len(p.judge_ids)} judges, {len(p.team_ids)} teams)")

        if panels:
            self.panel_listbox.selection_set(0)
            self.on_panel_select(None)
        else:
            self.selected_panel_id = None
            self.panel_title_lbl.config(text="No panels in this round. Click '+ Create Panel'.")
            for r in self.judges_tree.get_children():
                self.judges_tree.delete(r)
            for r in self.teams_tree.get_children():
                self.teams_tree.delete(r)

    def on_panel_select(self, event) -> None:
        sel = self.panel_listbox.curselection()
        if not sel or not hasattr(self, "_current_panels") or sel[0] >= len(self._current_panels):
            return
        panel = self._current_panels[sel[0]]
        self.selected_panel_id = panel.id
        self.panel_title_lbl.config(text=f"Panel: {panel.name}")

        # Refresh Judges
        for r in self.judges_tree.get_children():
            self.judges_tree.delete(r)
        for jid in panel.judge_ids:
            user = self.app.store.users.get(jid)
            if user:
                self.judges_tree.insert("", "end", iid=user.id, values=(user.name, user.email))

        # Refresh Teams
        for r in self.teams_tree.get_children():
            self.teams_tree.delete(r)
        for tid in panel.team_ids:
            team = self.app.store.get_team(self.event_id, tid)
            if team:
                self.teams_tree.insert("", "end", iid=team.id, values=(team.name, team.project_title))

        # Update combo options
        event = self.app.store.get_event(self.event_id)
        if event:
            all_judges = self.app.store.get_judges(self.event_id)
            unassigned_j = [j for j in all_judges if j.id not in panel.judge_ids]
            self._unassigned_judges = unassigned_j
            self.avail_judge_combo["values"] = [f"{j.name} ({j.email})" for j in unassigned_j]
            if unassigned_j:
                self.avail_judge_combo.current(0)
            else:
                self.avail_judge_combo.set("")

            all_teams = self.app.store.get_teams(self.event_id)
            unassigned_t = [t for t in all_teams if t.id not in panel.team_ids and not t.is_disqualified]
            self._unassigned_teams = unassigned_t
            self.avail_team_combo["values"] = [t.name for t in unassigned_t]
            if unassigned_t:
                self.avail_team_combo.current(0)
            else:
                self.avail_team_combo.set("")

    def on_create_panel(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return

        name = simpledialog.askstring("New Panel", "Enter panel name (e.g. Panel A - Software):", parent=self)
        if name is None:
            return

        success, msg, _ = self.app.store.create_panel(self.event_id, round_id, name)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()
        else:
            messagebox.showwarning("Notice", msg)

    def on_delete_panel(self) -> None:
        if not self.selected_panel_id:
            messagebox.showinfo("Select Panel", "Please select a panel to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Delete this panel?")
        if not confirm:
            return

        success, msg = self.app.store.delete_panel(self.event_id, self.selected_panel_id)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()
        else:
            messagebox.showerror("Error", msg)

    def on_auto_balance(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return

        confirm = messagebox.askyesno(
            "Auto-balance Teams",
            "This will distribute all eligible teams evenly across the panels in this round. Continue?"
        )
        if not confirm:
            return

        success, msg = self.app.store.auto_balance_teams(self.event_id, round_id)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()
        else:
            messagebox.showwarning("Notice", msg)

    def on_assign_judge(self) -> None:
        if not self.selected_panel_id or not hasattr(self, "_unassigned_judges"):
            return
        idx = self.avail_judge_combo.current()
        if idx < 0 or idx >= len(self._unassigned_judges):
            return
        judge = self._unassigned_judges[idx]
        success, msg = self.app.store.assign_judge_to_panel(self.event_id, self.selected_panel_id, judge.id)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()

    def on_remove_judge(self) -> None:
        if not self.selected_panel_id:
            return
        sel = self.judges_tree.selection()
        if not sel:
            messagebox.showinfo("Select Judge", "Please select a judge to remove from this panel.")
            return
        jid = sel[0]
        success, msg = self.app.store.remove_judge_from_panel(self.event_id, self.selected_panel_id, jid)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()

    def on_assign_team(self) -> None:
        if not self.selected_panel_id or not hasattr(self, "_unassigned_teams"):
            return
        idx = self.avail_team_combo.current()
        if idx < 0 or idx >= len(self._unassigned_teams):
            return
        team = self._unassigned_teams[idx]
        success, msg = self.app.store.assign_team_to_panel(self.event_id, self.selected_panel_id, team.id)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()

    def on_remove_team(self) -> None:
        if not self.selected_panel_id:
            return
        sel = self.teams_tree.selection()
        if not sel:
            messagebox.showinfo("Select Team", "Please select a team to remove from this panel.")
            return
        tid = sel[0]
        success, msg = self.app.store.remove_team_from_panel(self.event_id, self.selected_panel_id, tid)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_panels_list()


# --- TAB 6: RESULTS & PROGRESSION ---
class ResultsTab(tk.Frame):
    def __init__(self, parent: tk.Widget, organizer_screen: OrganizerScreen):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.screen = organizer_screen
        self.app = organizer_screen.app
        self.event_id = organizer_screen.event_id
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top Bar: Round & Panel selectors
        top_bar = tk.Frame(self, bg=COLOR_WINDOW)
        top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(top_bar, text="Round:", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 6))
        self.round_combo = ttk.Combobox(top_bar, state="readonly", width=22)
        self.round_combo.pack(side="left", padx=(0, 12))
        self.round_combo.bind("<<ComboboxSelected>>", lambda e: self.on_round_changed())

        tk.Label(top_bar, text="Panel:", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 6))
        self.panel_combo = ttk.Combobox(top_bar, state="readonly", width=24)
        self.panel_combo.pack(side="left", padx=(0, 16))
        self.panel_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_results_table())

        refresh_btn = ttk.Button(top_bar, text="⟳ Refresh", style="Secondary.TButton", command=self.refresh_results_table)
        refresh_btn.pack(side="left")

        # Progression Actions Bar
        actions_bar = Card(self)
        actions_bar.grid(row=1, column=0, sticky="ew", pady=(0, 12))

        close_btn = ttk.Button(actions_bar, text="🔒 Close Round", style="Primary.TButton", command=self.on_close_round)
        close_btn.pack(side="left", padx=(0, 16))

        tk.Label(actions_bar, text="Advance top N per panel:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 6))
        self.n_spin = ttk.Spinbox(actions_bar, from_=1, to=10, width=4)
        self.n_spin.set("2")
        self.n_spin.pack(side="left", padx=(0, 6))

        adv_btn = ttk.Button(actions_bar, text="Advance Top N →", style="Secondary.TButton", command=self.on_advance_top_n)
        adv_btn.pack(side="left", padx=(0, 16))

        # Manual Qualify / Eliminate toggles
        qual_btn = ttk.Button(actions_bar, text="✓ Qualify Selected", style="Success.TButton", command=lambda: self.set_selected_status(STATUS_QUALIFIED))
        qual_btn.pack(side="left", padx=4)

        elim_btn = ttk.Button(actions_bar, text="✕ Eliminate Selected", style="Danger.TButton", command=lambda: self.set_selected_status(STATUS_ELIMINATED))
        elim_btn.pack(side="left", padx=4)

        # Ranked Table
        table_frame = tk.Frame(self, bg=COLOR_CARD, highlightbackground=COLOR_BORDER, highlightthickness=1)
        table_frame.grid(row=2, column=0, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        cols = ("rank", "name", "project", "avg_score", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("rank", text="Rank")
        self.tree.heading("name", text="Team Name")
        self.tree.heading("project", text="Project Title")
        self.tree.heading("avg_score", text="Weighted Avg Score")
        self.tree.heading("status", text="Round Status")

        self.tree.column("rank", width=80, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("project", width=280, anchor="w")
        self.tree.column("avg_score", width=160, anchor="center")
        self.tree.column("status", width=140, anchor="center")

        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.tree.tag_configure("disqualified", foreground=COLOR_ERROR)
        self.tree.tag_configure("qualified", foreground=COLOR_SUCCESS)
        self.tree.tag_configure("eliminated", foreground=COLOR_MUTED)

        self.refresh_rounds()

    def get_selected_round_id(self) -> Optional[str]:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            return None
        idx = self.round_combo.current()
        if 0 <= idx < len(event.rounds):
            return event.rounds[idx].id
        return event.rounds[0].id

    def refresh_rounds(self) -> None:
        event = self.app.store.get_event(self.event_id)
        if not event or not event.rounds:
            return
        self.round_combo["values"] = [f"Round {r.round_number}: {r.name}" for r in event.rounds]
        self.round_combo.current(0)
        self.on_round_changed()

    def on_round_changed(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        panels = self.app.store.get_panels(self.event_id, round_id)
        self._current_panels = panels
        self.panel_combo["values"] = [p.name for p in panels]
        if panels:
            self.panel_combo.current(0)
        else:
            self.panel_combo.set("")
        self.refresh_results_table()

    def refresh_results_table(self) -> None:
        for r in self.tree.get_children():
            self.tree.delete(r)

        round_id = self.get_selected_round_id()
        if not round_id or not hasattr(self, "_current_panels"):
            return

        panel_idx = self.panel_combo.current()
        if panel_idx < 0 or panel_idx >= len(self._current_panels):
            return
        panel = self._current_panels[panel_idx]

        ranked = self.app.store.get_panel_ranked_teams(self.event_id, round_id, panel.id)

        for item in ranked:
            t = item["team"]
            rank_str = f"#{item['rank']}"
            score_str = f"{item['average_score']:.2f} / 100"
            status_str = "DISQUALIFIED" if t.is_disqualified else item["round_status"]

            tag = "disqualified" if t.is_disqualified else ("qualified" if item["round_status"] == STATUS_QUALIFIED else "eliminated")

            self.tree.insert(
                "",
                "end",
                iid=t.id,
                values=(rank_str, t.name, t.project_title, score_str, status_str),
                tags=(tag,)
            )

    def on_close_round(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return

        success, msg, missing = self.app.store.close_round(self.event_id, round_id)
        if success:
            self.app.set_status(msg, "success")
            messagebox.showinfo("Round Closed", msg)
        else:
            # Show friendly dialog with list of missing scores
            missing_text = "\n".join(f"• {m}" for m in missing[:8])
            if len(missing) > 8:
                missing_text += f"\n...and {len(missing) - 8} more."

            messagebox.showerror(
                "Cannot Close Round (Missing Scores)",
                f"{msg}\n\nPlease ensure all judges submit scores for their assigned teams:\n\n{missing_text}"
            )

    def on_advance_top_n(self) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        try:
            n = int(self.n_spin.get())
        except ValueError:
            messagebox.showwarning("Validation", "Please enter a valid integer for N.")
            return

        confirm = messagebox.askyesno(
            "Confirm Advancement",
            f"Advance the top {n} teams from EACH panel in this round to QUALIFIED status?"
        )
        if not confirm:
            return

        success, msg = self.app.store.advance_top_n_per_panel(self.event_id, round_id, n)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_results_table()
        else:
            messagebox.showwarning("Notice", msg)

    def set_selected_status(self, status: str) -> None:
        round_id = self.get_selected_round_id()
        if not round_id:
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Team", "Please select a team in the table first.")
            return
        tid = sel[0]
        success, msg = self.app.store.set_team_round_status(self.event_id, round_id, tid, status)
        if success:
            self.app.set_status(msg, "success")
            self.refresh_results_table()


# =====================================================================
# SCREEN 4: JUDGE WORKSPACE
# =====================================================================
class JudgeScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp, event_id: str):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.app = app
        self.event_id = event_id
        self.selected_team_id: Optional[str] = None
        self.score_inputs: Dict[str, Dict[str, Any]] = {}
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=260)
        self.grid_columnconfigure(1, weight=3)

        event = self.app.store.get_event(self.event_id)
        user = self.app.store.current_user
        if not event or not user:
            return

        # Top Header Banner
        header = Card(self)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        tk.Label(header, text=f"Judge Workspace: {event.title}", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_TITLE).pack(side="left")
        Badge(header, "Judge Portal", status_type="default").pack(side="left", padx=10)

        # Closed round alert banner (shown if closed)
        self.closed_banner = tk.Label(
            header,
            text=" 🔒 This round has been closed. Scores are read-only. ",
            bg=COLOR_SECONDARY,
            fg=COLOR_WARNING,
            font=FONT_BODY_BOLD
        )

        # Left Column: Assigned Teams List
        left_card = Card(self)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_card.grid_rowconfigure(1, weight=1)
        left_card.grid_columnconfigure(0, weight=1)

        tk.Label(left_card, text="Your Assigned Teams", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.team_listbox = tk.Listbox(
            left_card,
            bg=COLOR_SECONDARY,
            fg=COLOR_TITLE,
            selectbackground=COLOR_PRIMARY,
            selectforeground=COLOR_TITLE,
            font=FONT_BODY,
            highlightthickness=0,
            borderwidth=1,
            relief="solid"
        )
        self.team_listbox.grid(row=1, column=0, sticky="nsew")
        self.team_listbox.bind("<<ListboxSelect>>", self.on_team_select)

        # Right Column: Evaluation & Scoring Card
        self.eval_card = Card(self)
        self.eval_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        self.eval_card.grid_rowconfigure(2, weight=1)
        self.eval_card.grid_columnconfigure(0, weight=1)

        # Team Title & Details
        self.team_header_lbl = tk.Label(self.eval_card, text="Select a team to begin scoring", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE)
        self.team_header_lbl.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.team_sub_lbl = tk.Label(self.eval_card, text="", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_BODY)
        self.team_sub_lbl.grid(row=1, column=0, sticky="w", pady=(0, 12))

        # Scrollable Criteria Form Container
        canvas = tk.Canvas(self.eval_card, bg=COLOR_CARD, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.eval_card, orient="vertical", command=canvas.yview)
        self.crit_form_frame = tk.Frame(canvas, bg=COLOR_CARD)

        self.crit_form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=self.crit_form_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        # Bottom Live Weighted Score & Save Bar
        bot_bar = tk.Frame(self.eval_card, bg=COLOR_CARD)
        bot_bar.grid(row=3, column=0, sticky="ew", pady=(14, 0))

        self.weighted_total_lbl = tk.Label(
            bot_bar,
            text="Weighted Total: 0.00 / 100",
            bg=COLOR_CARD,
            fg=COLOR_SUCCESS,
            font=FONT_SUBTITLE
        )
        self.weighted_total_lbl.pack(side="left")

        self.saved_timestamp_lbl = tk.Label(
            bot_bar,
            text="",
            bg=COLOR_CARD,
            fg=COLOR_MUTED,
            font=FONT_SMALL
        )
        self.saved_timestamp_lbl.pack(side="left", padx=16)

        self.save_btn = ttk.Button(
            bot_bar,
            text="Save Scores",
            style="Primary.TButton",
            command=self.save_all_scores
        )
        self.save_btn.pack(side="right")

        self.load_judge_data()

    def load_judge_data(self) -> None:
        event = self.app.store.get_event(self.event_id)
        user = self.app.store.current_user
        if not event or not user or not event.rounds:
            return

        # Active round is the first non-closed round or the last round
        self.active_round = next((r for r in event.rounds if not r.is_closed), event.rounds[-1])

        # If round closed, show banner
        if self.active_round.is_closed:
            self.closed_banner.pack(side="right")
            self.save_btn.config(state="disabled")
        else:
            self.closed_banner.pack_forget()

        # Get panel and teams for this judge
        self.panel, self.teams = self.app.store.get_judge_panel_and_teams(
            self.event_id,
            self.active_round.id,
            user.id
        )

        self.team_listbox.delete(0, tk.END)
        if not self.teams:
            self.team_listbox.insert(tk.END, "No teams assigned")
            self.team_header_lbl.config(text="No teams currently assigned to your panel.")
            return

        for t in self.teams:
            self.team_listbox.insert(tk.END, f"  {t.name}")

        self.team_listbox.selection_set(0)
        self.on_team_select(None)

    def on_team_select(self, event) -> None:
        sel = self.team_listbox.curselection()
        if not sel or sel[0] >= len(self.teams):
            return

        team = self.teams[sel[0]]
        self.selected_team_id = team.id
        self.team_header_lbl.config(text=f"Evaluating: {team.name}")
        self.team_sub_lbl.config(text=f"Project: {team.project_title}  |  Repo: {team.repo_url}")

        # Rebuild Criteria Form
        for w in self.crit_form_frame.winfo_children():
            w.destroy()
        self.score_inputs.clear()

        user = self.app.store.current_user
        existing_scores = self.app.store.get_team_scores_by_judge(
            self.event_id,
            self.active_round.id,
            user.id,
            team.id
        )

        is_readonly = self.active_round.is_closed

        for crit in self.active_round.criteria:
            crit_box = Card(self.crit_form_frame)
            crit_box.pack(fill="x", pady=6)

            # Read-only criterion name and info
            hdr = tk.Frame(crit_box, bg=COLOR_CARD)
            hdr.pack(fill="x", pady=(0, 6))

            tk.Label(hdr, text=crit.name, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left")
            tk.Label(hdr, text=f"Max: {crit.max_score} pts  •  Weight: {crit.weight}%", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(side="right")

            inputs_row = tk.Frame(crit_box, bg=COLOR_CARD)
            inputs_row.pack(fill="x")

            # Score entry
            tk.Label(inputs_row, text="Score:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_SMALL_BOLD).pack(side="left", padx=(0, 4))
            score_var = tk.StringVar()
            saved_val = existing_scores.get(crit.id, {}).get("value", "")
            if saved_val != "":
                score_var.set(str(int(saved_val) if float(saved_val).is_integer() else saved_val))

            score_ent = ttk.Entry(inputs_row, textvariable=score_var, width=8, justify="center")
            if is_readonly:
                score_ent.config(state="disabled")
            score_ent.pack(side="left", padx=(0, 16))

            # Comment entry
            tk.Label(inputs_row, text="Feedback / Comments:", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_SMALL_BOLD).pack(side="left", padx=(0, 4))
            comment_var = tk.StringVar()
            saved_comment = existing_scores.get(crit.id, {}).get("comment", "")
            comment_var.set(saved_comment)

            comment_ent = ttk.Entry(inputs_row, textvariable=comment_var)
            if is_readonly:
                comment_ent.config(state="disabled")
            comment_ent.pack(side="left", fill="x", expand=True)

            # Live calculation on KeyRelease
            score_var.trace_add("write", lambda *args: self.calculate_live_total())

            # Save on leaving field (FocusOut)
            if not is_readonly:
                score_ent.bind("<FocusOut>", lambda e, c=crit: self.auto_save_criterion(c.id))
                comment_ent.bind("<FocusOut>", lambda e, c=crit: self.auto_save_criterion(c.id))

            self.score_inputs[crit.id] = {
                "crit": crit,
                "score_var": score_var,
                "comment_var": comment_var
            }

        self.calculate_live_total()

    def calculate_live_total(self) -> None:
        total = 0.0
        for crit_id, item in self.score_inputs.items():
            crit = item["crit"]
            val_str = item["score_var"].get().strip()
            try:
                val = float(val_str)
                if 0 <= val <= crit.max_score and crit.max_score > 0:
                    total += (val / crit.max_score) * crit.weight
            except ValueError:
                pass

        self.weighted_total_lbl.config(text=f"Weighted Total: {total:.2f} / 100")

    def auto_save_criterion(self, criterion_id: str) -> None:
        if self.active_round.is_closed or not self.selected_team_id:
            return

        item = self.score_inputs.get(criterion_id)
        if not item:
            return

        val_str = item["score_var"].get().strip()
        comment = item["comment_var"].get().strip()

        if not val_str:
            return

        try:
            val = float(val_str)
        except ValueError:
            return

        user = self.app.store.current_user
        success, msg, timestamp = self.app.store.save_score(
            self.event_id,
            self.active_round.id,
            self.panel.id if self.panel else "",
            user.id,
            self.selected_team_id,
            criterion_id,
            val,
            comment
        )
        if success:
            self.saved_timestamp_lbl.config(text=f"✓ Saved at {timestamp}", fg=COLOR_SUCCESS)

    def save_all_scores(self) -> None:
        if self.active_round.is_closed or not self.selected_team_id:
            return

        last_time = ""
        for crit_id in self.score_inputs:
            self.auto_save_criterion(crit_id)

        user = self.app.store.current_user
        scores = self.app.store.get_team_scores_by_judge(
            self.event_id,
            self.active_round.id,
            user.id,
            self.selected_team_id
        )
        if scores:
            last_time = datetime.now().strftime("%H:%M:%S")
            self.saved_timestamp_lbl.config(text=f"✓ All saved at {last_time}", fg=COLOR_SUCCESS)
            self.app.set_status(f"Scores saved for team at {last_time}", "success")


# =====================================================================
# SCREEN 5: VOLUNTEER SCHEDULE
# =====================================================================
class VolunteerScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp, event_id: str):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.app = app
        self.event_id = event_id
        self._build_ui()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        event = self.app.store.get_event(self.event_id)
        if not event:
            return

        # Header Banner
        header = Card(self)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        tk.Label(header, text=f"Volunteer Schedule: {event.title}", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_TITLE).pack(side="left")
        Badge(header, "Volunteer Portal", status_type="default").pack(side="left", padx=10)
        tk.Label(header, text="Check in teams upon arrival. Note: Scores are strictly confidential and hidden.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(side="right")

        # Scrollable Panels and Teams View
        canvas = tk.Canvas(self, bg=COLOR_WINDOW, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_WINDOW)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        panels = event.panels
        if not panels:
            empty_card = Card(scrollable_frame)
            empty_card.pack(fill="x", pady=20)
            tk.Label(empty_card, text="No panels configured yet for this event.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_BODY).pack()
            return

        for panel in panels:
            round_obj = next((r for r in event.rounds if r.id == panel.round_id), None)
            round_name = round_obj.name if round_obj else "Round"

            p_card = Card(scrollable_frame)
            p_card.pack(fill="x", pady=8)

            hdr = tk.Frame(p_card, bg=COLOR_CARD)
            hdr.pack(fill="x", pady=(0, 8))

            tk.Label(hdr, text=f"📍 {panel.name} ({round_name})", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(side="left")

            judges = [self.app.store.users[jid].name for jid in panel.judge_ids if jid in self.app.store.users]
            judges_str = f"Judges: {', '.join(judges)}" if judges else "No judges assigned"
            tk.Label(hdr, text=judges_str, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL).pack(side="right")

            if not panel.team_ids:
                tk.Label(p_card, text="No teams currently assigned to this panel.", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_BODY).pack(anchor="w", pady=4)
                continue

            for tid in panel.team_ids:
                team = self.app.store.get_team(self.event_id, tid)
                if not team:
                    continue

                t_row = tk.Frame(p_card, bg=COLOR_SECONDARY, padx=12, pady=8)
                t_row.pack(fill="x", pady=4)

                # Check-in Checkbox
                chk_var = tk.BooleanVar(value=team.checked_in)
                chk = ttk.Checkbutton(
                    t_row,
                    text="Checked In",
                    variable=chk_var,
                    command=lambda t=team, v=chk_var: self.toggle_checkin(t, v)
                )
                chk.pack(side="left", padx=(0, 14))

                # Team info
                tk.Label(t_row, text=team.name, bg=COLOR_SECONDARY, fg=COLOR_TITLE, font=FONT_BODY_BOLD).pack(side="left", padx=(0, 8))
                tk.Label(t_row, text=f"— {team.project_title} ({', '.join(team.members)})", bg=COLOR_SECONDARY, fg=COLOR_BODY, font=FONT_BODY).pack(side="left")

                if team.is_disqualified:
                    Badge(t_row, "DISQUALIFIED", status_type="error").pack(side="right")

    def toggle_checkin(self, team: Team, var: tk.BooleanVar) -> None:
        new_val = var.get()
        success, msg = self.app.store.set_team_checked_in(self.event_id, team.id, new_val)
        if success:
            self.app.set_status(msg, "success")


# =====================================================================
# SCREEN 6: PARTICIPANT TEAM PAGE
# =====================================================================
class ParticipantScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp, event_id: str):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=20)
        self.app = app
        self.event_id = event_id
        self._build_ui()

    def _build_ui(self) -> None:
        for w in self.winfo_children():
            w.destroy()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        event = self.app.store.get_event(self.event_id)
        user = self.app.store.current_user
        if not event or not user:
            return

        team = self.app.store.get_team_for_user(self.event_id, user.id)

        center_card = Card(self)
        center_card.place(relx=0.5, rely=0.5, anchor="center", width=620)

        # Header
        title_text = "Your Team Registration" if team else "Register Your Hackathon Team"
        tk.Label(center_card, text=title_text, bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_TITLE).pack(anchor="w", pady=(0, 4))

        is_locked = event.status in [STATUS_JUDGING, STATUS_COMPLETED]
        if is_locked:
            tk.Label(
                center_card,
                text="🔒 Judging has started or completed. Team details are locked.",
                bg=COLOR_CARD,
                fg=COLOR_WARNING,
                font=FONT_SMALL_BOLD
            ).pack(anchor="w", pady=(0, 10))
        else:
            tk.Label(
                center_card,
                text=f"Event: {event.title} (Registration Open)",
                bg=COLOR_CARD,
                fg=COLOR_MUTED,
                font=FONT_SMALL
            ).pack(anchor="w", pady=(0, 10))

        if team and team.is_disqualified:
            disq_box = Card(center_card)
            disq_box.pack(fill="x", pady=(0, 10))
            tk.Label(disq_box, text="🚨 TEAM DISQUALIFIED", bg=COLOR_CARD, fg=COLOR_ERROR, font=FONT_BODY_BOLD).pack(anchor="w")
            tk.Label(disq_box, text=f"Reason: {team.disqualification_reason}", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_SMALL).pack(anchor="w")

        # Form Fields
        tk.Label(center_card, text="Team Name", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.name_entry = ttk.Entry(center_card)
        if team:
            self.name_entry.insert(0, team.name)
        if is_locked:
            self.name_entry.config(state="disabled")
        self.name_entry.pack(fill="x", pady=(0, 8))

        tk.Label(center_card, text="Member Names (comma separated)", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.members_entry = ttk.Entry(center_card)
        if team:
            self.members_entry.insert(0, ", ".join(team.members))
        else:
            self.members_entry.insert(0, user.name)
        if is_locked:
            self.members_entry.config(state="disabled")
        self.members_entry.pack(fill="x", pady=(0, 8))

        tk.Label(center_card, text="Project Title", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.proj_entry = ttk.Entry(center_card)
        if team:
            self.proj_entry.insert(0, team.project_title)
        if is_locked:
            self.proj_entry.config(state="disabled")
        self.proj_entry.pack(fill="x", pady=(0, 8))

        tk.Label(center_card, text="Project Description", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        self.desc_text = tk.Text(
            center_card,
            height=4,
            bg=COLOR_CARD,
            fg=COLOR_TITLE,
            insertbackground=COLOR_TITLE,
            highlightbackground=COLOR_BORDER,
            highlightthickness=1,
            font=FONT_BODY
        )
        if team:
            self.desc_text.insert("1.0", team.description)
        if is_locked:
            self.desc_text.config(state="disabled")
        self.desc_text.pack(fill="x", pady=(0, 8))

        # Repo URL with "Open link" button
        tk.Label(center_card, text="Repository URL (must start with http:// or https://)", bg=COLOR_CARD, fg=COLOR_BODY, font=FONT_BODY_BOLD).pack(anchor="w", pady=(4, 2))
        repo_row = tk.Frame(center_card, bg=COLOR_CARD)
        repo_row.pack(fill="x", pady=(0, 16))

        self.repo_entry = ttk.Entry(repo_row)
        if team:
            self.repo_entry.insert(0, team.repo_url)
        else:
            self.repo_entry.insert(0, "https://github.com/")
        if is_locked:
            self.repo_entry.config(state="disabled")
        self.repo_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        open_link_btn = ttk.Button(repo_row, text="Open link ↗", style="Secondary.TButton", command=self.on_open_link)
        open_link_btn.pack(side="right")

        # Submit / Save button
        if not is_locked:
            btn_txt = "Save Changes" if team else "Submit Team Registration"
            submit_btn = ttk.Button(
                center_card,
                text=btn_txt,
                style="Primary.TButton",
                command=lambda t=team: self.on_save_team(t)
            )
            submit_btn.pack(fill="x")

    def on_open_link(self) -> None:
        url = self.repo_entry.get().strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            messagebox.showwarning("Invalid Link", "Repository URL must begin with http:// or https://")
            return
        webbrowser.open(url)
        self.app.set_status(f"Opening browser link: {url}", "info")

    def on_save_team(self, existing_team: Optional[Team]) -> None:
        name = self.name_entry.get().strip()
        members_raw = self.members_entry.get().split(",")
        members = [m.strip() for m in members_raw if m.strip()]
        proj = self.proj_entry.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        repo = self.repo_entry.get().strip()
        user = self.app.store.current_user

        if existing_team:
            success, msg = self.app.store.update_team(self.event_id, existing_team.id, name, members, proj, desc, repo)
        else:
            success, msg, new_t = self.app.store.register_team(self.event_id, user.id, name, members, proj, desc, repo)

        if success:
            self.app.set_status(msg, "success")
            messagebox.showinfo("Success", msg)
            self._build_ui()
        else:
            messagebox.showerror("Error", msg)


# =====================================================================
# SCREEN 7: LEADERBOARD & ANALYTICS
# =====================================================================
class LeaderboardScreen(tk.Frame):
    def __init__(self, parent: tk.Widget, app: HackHubApp, event_id: str):
        super().__init__(parent, bg=COLOR_WINDOW, padx=20, pady=16)
        self.app = app
        self.event_id = event_id
        self.after_id: Optional[str] = None
        self._build_ui()
        self.refresh_leaderboard()
        self.schedule_auto_refresh()

    def cleanup(self) -> None:
        """Stops recurring auto-refresh timer when navigating away."""
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def schedule_auto_refresh(self) -> None:
        self.after_id = self.after(10000, self.auto_refresh)

    def auto_refresh(self) -> None:
        self.refresh_leaderboard()
        self.app.set_status(f"Leaderboard auto-refreshed at {datetime.now().strftime('%H:%M:%S')}", "info")
        self.schedule_auto_refresh()

    def _build_ui(self) -> None:
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        event = self.app.store.get_event(self.event_id)
        if not event:
            return

        # Header Row
        header_row = tk.Frame(self, bg=COLOR_WINDOW)
        header_row.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(header_row, text=f"🏆 Live Leaderboard: {event.title}", bg=COLOR_WINDOW, fg=COLOR_TITLE, font=FONT_HERO).pack(side="left")
        Badge(header_row, event.status, status_type=event.status).pack(side="left", padx=10)

        self.last_refreshed_lbl = tk.Label(header_row, text="", bg=COLOR_WINDOW, fg=COLOR_MUTED, font=FONT_SMALL)
        self.last_refreshed_lbl.pack(side="right", padx=(8, 0))

        refresh_btn = ttk.Button(header_row, text="⟳ Refresh Now", style="Secondary.TButton", command=self.refresh_leaderboard)
        refresh_btn.pack(side="right")

        # Summary Metrics Row
        self.summary_row = tk.Frame(self, bg=COLOR_WINDOW)
        self.summary_row.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        for col in range(6):
            self.summary_row.grid_columnconfigure(col, weight=1, uniform="stat")

        # Middle Content: Left Podium Canvas & Right Bar Chart Canvas
        mid_grid = tk.Frame(self, bg=COLOR_WINDOW)
        mid_grid.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
        mid_grid.grid_rowconfigure(0, weight=1)
        mid_grid.grid_columnconfigure(0, weight=1, uniform="vis")
        mid_grid.grid_columnconfigure(1, weight=1, uniform="vis")

        # Podium Card & Canvas
        podium_card = Card(mid_grid)
        podium_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(podium_card, text="🏅 Top 3 Podium", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(anchor="w", pady=(0, 6))

        self.podium_canvas = tk.Canvas(podium_card, bg=COLOR_CARD, highlightthickness=0, height=220)
        self.podium_canvas.pack(fill="both", expand=True)

        # Bar Chart Card & Canvas
        chart_card = Card(mid_grid)
        chart_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(chart_card, text="📊 Score Comparison (Top Teams)", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).pack(anchor="w", pady=(0, 6))

        self.chart_canvas = tk.Canvas(chart_card, bg=COLOR_CARD, highlightthickness=0, height=220)
        self.chart_canvas.pack(fill="both", expand=True)

        # Bottom Ranked Table Card
        table_card = Card(self)
        table_card.grid(row=3, column=0, sticky="nsew")
        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        tk.Label(table_card, text="Full Standings (Tie-break: Earlier Registration Wins)", bg=COLOR_CARD, fg=COLOR_TITLE, font=FONT_SUBTITLE).grid(row=0, column=0, sticky="w", pady=(0, 8))

        cols = ("rank", "name", "project", "score", "status")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", height=5)
        self.tree.heading("rank", text="Rank")
        self.tree.heading("name", text="Team Name")
        self.tree.heading("project", text="Project Title")
        self.tree.heading("score", text="Overall Score")
        self.tree.heading("status", text="Status")

        self.tree.column("rank", width=80, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("project", width=320, anchor="w")
        self.tree.column("score", width=160, anchor="center")
        self.tree.column("status", width=140, anchor="center")

        scroll_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.grid(row=1, column=0, sticky="nsew")
        scroll_y.grid(row=1, column=1, sticky="ns")

        self.tree.tag_configure("disqualified", foreground=COLOR_ERROR)
        self.tree.tag_configure("winner", foreground=COLOR_GOLD)
        self.tree.tag_configure("active", foreground=COLOR_BODY)

    def refresh_leaderboard(self) -> None:
        data = self.app.store.get_leaderboard_data(self.event_id)
        stats = data["stats"]
        podium = data["podium"]
        ranked = data["ranked_teams"]
        chart_data = data["chart_data"]

        self.last_refreshed_lbl.config(text=f"Updated: {datetime.now().strftime('%H:%M:%S')}")

        # Re-render Summary Metrics Row
        for w in self.summary_row.winfo_children():
            w.destroy()

        self._render_metric_box(0, "Total Teams", str(stats["total_teams"]))
        self._render_metric_box(1, "Rounds", str(stats["total_rounds"]))
        self._render_metric_box(2, "Disqualified", str(stats["disqualified_count"]), is_warn=stats["disqualified_count"] > 0)
        self._render_metric_box(3, "Current Winner", stats["winner"])
        self._render_metric_box(4, "Highest Score", f"{stats['highest_score']:.1f}")
        self._render_metric_box(5, "Average Score", f"{stats['avg_score']:.1f}")

        # Render Canvas Podium
        self._draw_podium(podium)

        # Render Canvas Bar Chart
        self._draw_chart(chart_data)

        # Render Table
        for r in self.tree.get_children():
            self.tree.delete(r)

        for item in ranked:
            t = item["team"]
            rank_str = f"#{item['rank']}"
            score_str = f"{item['overall_score']:.2f} / 100"
            status_str = "DISQUALIFIED" if t.is_disqualified else "ACTIVE"

            tag = "disqualified" if t.is_disqualified else ("winner" if item["rank"] == 1 else "active")
            self.tree.insert(
                "",
                "end",
                iid=t.id,
                values=(rank_str, t.name, t.project_title, score_str, status_str),
                tags=(tag,)
            )

    def _render_metric_box(self, col: int, label: str, value: str, is_warn: bool = False) -> None:
        c = Card(self.summary_row)
        c.grid(row=0, column=col, padx=4, sticky="nsew")
        tk.Label(c, text=label, bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SMALL_BOLD).pack(anchor="w")
        fg_col = COLOR_ERROR if is_warn else COLOR_TITLE
        tk.Label(c, text=value, bg=COLOR_CARD, fg=fg_col, font=FONT_SECTION).pack(anchor="w", pady=(2, 0))

    def _draw_podium(self, podium: List[Dict[str, Any]]) -> None:
        canvas = self.podium_canvas
        canvas.delete("all")
        w = canvas.winfo_width() or 460
        h = canvas.winfo_height() or 220

        base_y = h - 20
        col_w = min(110, w // 4)
        center_x = w // 2

        # Order: 2nd (left), 1st (center), 3rd (right)
        configs = [
            {"idx": 1, "x": center_x - col_w - 14, "height": 110, "color": COLOR_SILVER, "rank": "2nd"},
            {"idx": 0, "x": center_x, "height": 150, "color": COLOR_GOLD, "rank": "1st"},
            {"idx": 2, "x": center_x + col_w + 14, "height": 80, "color": COLOR_BRONZE, "rank": "3rd"},
        ]

        for cfg in configs:
            pos = cfg["idx"]
            x = cfg["x"]
            p_h = cfg["height"]
            color = cfg["color"]
            rank_str = cfg["rank"]

            # Draw block
            x1 = x - (col_w // 2)
            x2 = x + (col_w // 2)
            y1 = base_y - p_h
            y2 = base_y

            canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_SECONDARY, outline=color, width=2)

            # Block rank number
            canvas.create_text(x, y1 + 30, text=rank_str, fill=color, font=FONT_PODIUM_NUM)

            if pos < len(podium):
                item = podium[pos]
                name = item["team"].name
                score = item["overall_score"]

                # Score text inside block
                canvas.create_text(x, y1 + 65, text=f"{score:.1f} pts", fill=COLOR_TITLE, font=FONT_PODIUM_SCORE)

                # Team name above block
                canvas.create_text(x, y1 - 16, text=name, fill=COLOR_TITLE, font=FONT_BODY_BOLD)
            else:
                canvas.create_text(x, y1 - 14, text="Empty", fill=COLOR_MUTED, font=FONT_SMALL)

    def _draw_chart(self, chart_data: List[Dict[str, Any]]) -> None:
        canvas = self.chart_canvas
        canvas.delete("all")
        w = canvas.winfo_width() or 460
        h = canvas.winfo_height() or 220

        if not chart_data:
            canvas.create_text(w // 2, h // 2, text="No scores recorded yet", fill=COLOR_MUTED, font=FONT_BODY)
            return

        left_margin = 120
        right_margin = 70
        bar_area_w = max(100, w - left_margin - right_margin)
        n = len(chart_data)
        bar_h = max(14, min(24, (h - 30) // n))

        start_y = 15

        for i, item in enumerate(chart_data):
            y = start_y + (i * (bar_h + 8))
            name = item["name"]
            score = item["score"]
            is_disq = item["disqualified"]

            # Team label
            label_text = name if len(name) <= 15 else name[:13] + ".."
            canvas.create_text(left_margin - 8, y + (bar_h // 2), text=label_text, fill=COLOR_TITLE, font=FONT_SMALL_BOLD, anchor="e")

            # Bar
            ratio = min(1.0, max(0.0, score / 100.0))
            bar_w = ratio * bar_area_w

            bar_color = COLOR_ERROR if is_disq else COLOR_PRIMARY
            canvas.create_rectangle(
                left_margin,
                y,
                left_margin + bar_w,
                y + bar_h,
                fill=bar_color,
                outline=COLOR_BORDER,
                width=1
            )

            # Score text
            score_txt = "DISQ" if is_disq else f"{score:.1f}"
            canvas.create_text(
                left_margin + bar_w + 8,
                y + (bar_h // 2),
                text=score_txt,
                fill=COLOR_BODY,
                font=FONT_SMALL_BOLD,
                anchor="w"
            )
