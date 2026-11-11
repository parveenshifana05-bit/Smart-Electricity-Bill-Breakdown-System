import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from bill_calculation import get_bill_breakdown
from database import ( get_appliances, delete_appliance,update_appliance) 
from appliance import add_appliance_window
from waste_detection import ( detect_appliance_waste ,get_highest_consumer, generate_suggestions)
from reports import generate_report
from notifications import show_notification

# =========================
# COLOURS
# =========================

NAVY = "#102A43"
BLUE = "#1976D2"
TEAL = "#00897B"
GREEN = "#2E7D32"
ORANGE = "#F57C00"
LIGHT_BG = "#F3F7FA"
WHITE = "#FFFFFF"
TEXT = "#263238"
GREY = "#607D8B"


# =========================
# CREATE USER PROFILE TABLE
# =========================

def create_profile_table():

    connection = sqlite3.connect("electricity.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            room_no TEXT,
            people INTEGER,
            household_type TEXT
        )
    """)

    # Add new columns to an existing database
    columns = [
        ("email", "TEXT"),
        ("people", "INTEGER"),
        ("household_type", "TEXT")
    ]

    for column, data_type in columns:

        try:
            cursor.execute(
                f"ALTER TABLE user_profile ADD COLUMN {column} {data_type}"
            )
        except sqlite3.OperationalError:
            pass

    connection.commit()
    connection.close()



# =========================
# USER PROFILE / ENERGY PROFILE
# =========================

def show_profile_page(
    total_units,
    average_usage,
    highest_usage,
    lowest_usage,
    bill
):

    root = tk.Tk()

    root.title(
        "Smart Electricity Bill Breakdown System"
    )

    root.state("zoomed")
    root.resizable(True, True)
    root.configure(bg="#F4F7FA")

    # =========================
    # PREMIUM COLOURS
    # =========================

    DARK_NAVY = "#0B1F33"
    NAVY = "#123A5A"
    TEAL = "#00A88F"
    TEAL_DARK = "#008F7A"
    WHITE = "#FFFFFF"
    TEXT = "#172B3A"
    GREY = "#718096"
    BORDER = "#D9E2EC"
    LIGHT_BG = "#F4F7FA"
    INPUT_BG = "#F8FAFC"

    # =========================
    # MAIN AREA
    # =========================

    main = tk.Frame(
        root,
        bg=LIGHT_BG
    )

    main.pack(
        fill="both",
        expand=True
    )

    # =========================
    # LEFT BRANDING PANEL
    # =========================

    left = tk.Frame(
        main,
        bg=DARK_NAVY,
        width=440
    )

    left.pack(
        side="left",
        fill="y"
    )

    left.pack_propagate(False)

    tk.Label(
        left,
        text="⚡",
        font=("Segoe UI", 48, "bold"),
        bg=DARK_NAVY,
        fg=TEAL
    ).pack(
        pady=(100, 10)
    )

    tk.Label(
        left,
        text="SMART\nELECTRICITY",
        font=("Segoe UI", 28, "bold"),
        bg=DARK_NAVY,
        fg=WHITE,
        justify="center"
    ).pack()

    tk.Label(
        left,
        text="SMART ENERGY MANAGEMENT SYSTEM",
        font=("Segoe UI", 10, "bold"),
        bg=DARK_NAVY,
        fg="#9FB3C8"
    ).pack(
        pady=(10, 50)
    )

    tk.Label(
        left,
        text=(
            "Monitor your electricity consumption,\n"
            "understand your usage patterns,\n"
            "and make smarter energy decisions."
        ),
        font=("Segoe UI", 12),
        bg=DARK_NAVY,
        fg="#D9E2EC",
        justify="center"
    ).pack()

    # =========================
    # FEATURES
    # =========================

    features = [
        "✓  Electricity monitoring",
        "✓  Bill estimation",
        "✓  Appliance analysis",
        "✓  Energy-saving insights"
    ]

    feature_box = tk.Frame(
        left,
        bg=DARK_NAVY
    )

    feature_box.pack(
        pady=50
    )

    for feature in features:

        tk.Label(
            feature_box,
            text=feature,
            font=("Segoe UI", 11),
            bg=DARK_NAVY,
            fg="#D9E2EC",
            anchor="w"
        ).pack(
            anchor="w",
            pady=8
        )

    # =========================
    # RIGHT AREA
    # =========================

    right = tk.Frame(
        main,
        bg=LIGHT_BG
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    # =========================
    # PROFILE CARD
    # =========================

    card = tk.Frame(
        right,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.place(
        relx=0.5,
        rely=0.48,
        anchor="center",
        width=650,
        height=690
    )

    # =========================
    # TITLE
    # =========================

    tk.Label(
        card,
        text="SET UP YOUR ENERGY PROFILE",
        font=("Segoe UI", 24, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        pady=(42, 6)
    )

    tk.Label(
        card,
        text=(
            "Tell us a little about your household "
            "to personalize your energy analysis."
        ),
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=GREY
    ).pack(
        pady=(0, 28)
    )

    # =========================
    # INPUT FUNCTION
    # =========================

    def create_input(label_text):

        tk.Label(
            card,
            text=label_text,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=65
        )

        box = tk.Frame(
            card,
            bg=INPUT_BG,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.pack(
            fill="x",
            padx=65,
            pady=(6, 17),
            ipady=2
        )

        entry = tk.Entry(
            box,
            font=("Segoe UI", 11),
            bg=INPUT_BG,
            fg=TEXT,
            relief="flat",
            bd=0
        )

        entry.pack(
            fill="x",
            padx=14,
            pady=9
        )

        return entry

    # =========================
    # NAME
    # =========================

    name_entry = create_input(
        "YOUR NAME"
    )

    # =========================
    # EMAIL
    # =========================

    email_entry = create_input(
        "EMAIL ID"
    )

    # =========================
    # ROOM / HOUSE
    # =========================

    room_entry = create_input(
        "ROOM / HOUSE NO."
    )

    # =========================
    # BOTTOM TWO FIELDS
    # =========================

    row = tk.Frame(
        card,
        bg=WHITE
    )

    row.pack(
        fill="x",
        padx=65
    )

    # NUMBER OF PEOPLE

    people_frame = tk.Frame(
        row,
        bg=WHITE
    )

    people_frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 8)
    )

    tk.Label(
        people_frame,
        text="NUMBER OF PEOPLE",
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    people_box = tk.Frame(
        people_frame,
        bg=INPUT_BG,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    people_box.pack(
        fill="x",
        pady=(6, 0),
        ipady=2
    )

    people_entry = tk.Entry(
        people_box,
        font=("Segoe UI", 11),
        bg=INPUT_BG,
        fg=TEXT,
        relief="flat",
        bd=0
    )

    people_entry.pack(
        fill="x",
        padx=12,
        pady=9
    )

    # HOUSEHOLD TYPE

    type_frame = tk.Frame(
        row,
        bg=WHITE
    )

    type_frame.pack(
        side="right",
        fill="x",
        expand=True,
        padx=(8, 0)
    )

    tk.Label(
        type_frame,
        text="HOUSEHOLD TYPE",
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    household_var = tk.StringVar(
        value="Apartment"
    )

    household_menu = tk.OptionMenu(
        type_frame,
        household_var,
        "House",
        "Apartment",
        "Hostel / PG"
    )

    household_menu.config(
        font=("Segoe UI", 10),
        bg=INPUT_BG,
        fg=TEXT,
        activebackground=INPUT_BG,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        cursor="hand2"
    )

    household_menu["menu"].config(
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=TEXT
    )

    household_menu.pack(
        fill="x",
        pady=(6, 0),
        ipady=5
    )

    # =========================
    # LOAD SAVED PROFILE
    # =========================

    connection = sqlite3.connect(
        "electricity.db"
    )

    cursor = connection.cursor()

    try:

        saved_profile = cursor.execute(
            """
            SELECT name,
                   email,
                   room_no,
                   people,
                   household_type
            FROM user_profile
            WHERE id = 1
            """
        ).fetchone()

    except sqlite3.OperationalError:

        saved_profile = None

    connection.close()

    if saved_profile:

        if saved_profile[0]:
            name_entry.insert(
                0,
                saved_profile[0]
            )

        if saved_profile[1]:
            email_entry.insert(
                0,
                saved_profile[1]
            )

        if saved_profile[2]:
            room_entry.insert(
                0,
                saved_profile[2]
            )

        if saved_profile[3]:
            people_entry.insert(
                0,
                str(saved_profile[3])
            )

        if saved_profile[4]:
            household_var.set(
                saved_profile[4]
            )

    # =========================
    # SAVE AND CONTINUE
    # =========================

    def save_and_continue():

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        room = room_entry.get().strip()
        people = people_entry.get().strip()
        household = household_var.get()

        if not name or not email or not room or not people:

            messagebox.showwarning(
                "Missing Information",
                "Please complete all profile details."
            )

            return

        if "@" not in email or "." not in email:

            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email ID."
            )

            return

        if not people.isdigit() or int(people) <= 0:

            messagebox.showwarning(
                "Invalid Number",
                "Please enter a valid number of people."
            )

            return

        connection = sqlite3.connect(
            "electricity.db"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO user_profile
            (
                id,
                name,
                email,
                room_no,
                people,
                household_type
            )
            VALUES (1, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                room,
                int(people),
                household
            )
        )

        connection.commit()
        connection.close()

        # Clear current page

        for widget in root.winfo_children():
            widget.destroy()

        # Open dashboard in same window

        show_dashboard(
            root,
            total_units,
            average_usage,
            highest_usage,
            lowest_usage,
            bill
        )

    # =========================
    # PREMIUM CONTINUE BUTTON
    # =========================

    continue_button = tk.Button(
        card,
        text="CONTINUE TO DASHBOARD   →",
        command=save_and_continue,
        font=("Segoe UI", 11, "bold"),
        bg=TEAL,
        fg=WHITE,
        activebackground=TEAL_DARK,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    continue_button.pack(
        fill="x",
        padx=65,
        pady=(28, 0),
        ipady=10
    )

    # =========================
    # BUTTON HOVER EFFECT
    # =========================

    def button_enter(event):

        continue_button.configure(
            bg=TEAL_DARK
        )

    def button_leave(event):

        continue_button.configure(
            bg=TEAL
        )

    continue_button.bind(
        "<Enter>",
        button_enter
    )

    continue_button.bind(
        "<Leave>",
        button_leave
    )

    # =========================
    # FOOTER
    # =========================

    tk.Label(
        right,
        text=(
            "Smart Energy Management  •  "
            "Python Desktop Application"
        ),
        font=("Segoe UI", 9),
        bg=LIGHT_BG,
        fg=GREY
    ).pack(
        side="bottom",
        pady=20
    )

    name_entry.focus()

    root.mainloop()

# =========================
# DASHBOARD
# =========================

def show_dashboard(
    root,
    total_units,
    average_usage,
    highest_usage,
    lowest_usage,
    bill
):


    root.title(
        "Smart Electricity Bill Breakdown System"
    )

    root.state("zoomed")
    root.resizable(True, True)
    root.configure(bg="#F4F7FA")

    # =========================
    # PREMIUM DASHBOARD
    # =========================

    DARK_NAVY = "#0B1F33"
    NAVY = "#123A5A"
    TEAL = "#00A88F"
    TEAL_DARK = "#008F7A"
    WHITE = "#FFFFFF"
    TEXT = "#172B3A"
    GREY = "#718096"
    LIGHT_BG = "#F4F7FA"
    BORDER = "#D9E2EC"
    SOFT_TEAL = "#E8F8F5"

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        root,
        bg=DARK_NAVY,
        height=105
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    # Brand
    brand_frame = tk.Frame(
        header,
        bg=DARK_NAVY
    )

    brand_frame.pack(
        side="left",
        padx=45
    )

    tk.Label(
        brand_frame,
        text="⚡",
        font=("Segoe UI", 27, "bold"),
        bg=DARK_NAVY,
        fg=TEAL
    ).pack(
        side="left",
        padx=(0, 12)
    )

    title_frame = tk.Frame(
        brand_frame,
        bg=DARK_NAVY
    )

    title_frame.pack(
        side="left"
    )

    tk.Label(
        title_frame,
        text="SMART ELECTRICITY",
        font=("Segoe UI", 20, "bold"),
        bg=DARK_NAVY,
        fg=WHITE
    ).pack(
        anchor="w"
    )

    tk.Label(
        title_frame,
        text="SMART ENERGY MANAGEMENT SYSTEM",
        font=("Segoe UI", 8, "bold"),
        bg=DARK_NAVY,
        fg="#9FB3C8"
    ).pack(
        anchor="w"
    )

    # Profile button in header
    profile_button = tk.Button(
        header,
        text="👤  Profile",
        command=lambda: user_profile(),
        font=("Segoe UI", 10, "bold"),
        bg="#173B57",
        fg=WHITE,
        activebackground="#204B6C",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=18,
        pady=8
    )

    profile_button.pack(
        side="right",
        padx=45
    )

    # =========================
    # MAIN CONTENT
    # =========================

    dashboard_content = tk.Frame(
        root,
        bg=LIGHT_BG
    )

    dashboard_content.pack(
        fill="both",
        expand=True,
        padx=45,
        pady=28
    )

    # =========================
    # WELCOME AREA
    # =========================

    welcome_frame = tk.Frame(
        dashboard_content,
        bg=LIGHT_BG
    )

    welcome_frame.pack(
        fill="x",
        pady=(0, 22)
    )

    tk.Label(
        welcome_frame,
        text="Electricity Overview",
        font=("Segoe UI", 23, "bold"),
        bg=LIGHT_BG,
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        welcome_frame,
        text="Monitor your consumption and manage your household energy.",
        font=("Segoe UI", 10),
        bg=LIGHT_BG,
        fg=GREY
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # =========================
    # SUMMARY CARDS
    # =========================

    summary_cards = tk.Frame(
        dashboard_content,
        bg=LIGHT_BG
    )

    summary_cards.pack(
        fill="x",
        pady=(0, 24)
    )

    def create_summary_card(
        title,
        value,
        subtitle,
        icon
    ):

        card = tk.Frame(
            summary_cards,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        inner = tk.Frame(
            card,
            bg=WHITE
        )

        inner.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=18
        )

        top = tk.Frame(
            inner,
            bg=WHITE
        )

        top.pack(
            fill="x"
        )

        tk.Label(
            top,
            text=icon,
            font=("Segoe UI", 18),
            bg=WHITE,
            fg=TEAL
        ).pack(
            side="left"
        )

        tk.Label(
            top,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=GREY
        ).pack(
            side="left",
            padx=10
        )

        tk.Label(
            inner,
            text=value,
            font=("Segoe UI", 23, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(10, 1)
        )

        tk.Label(
            inner,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=GREY
        ).pack(
            anchor="w"
        )

    create_summary_card(
        "TOTAL CONSUMPTION",
        f"{total_units} Units",
        "Total recorded consumption",
        "⚡"
    )

    create_summary_card(
        "AVERAGE / DAY",
        f"{average_usage:.1f}",
        "Units consumed per day",
        "◷"
    )

    create_summary_card(
        "PEAK USAGE",
        f"{highest_usage} Units",
        "Highest daily consumption",
        "↗"
    )

    create_summary_card(
        "ESTIMATED BILL",
        f"₹{bill:.2f}",
        "Prototype tariff calculation",
        "₹"
    )

    # =========================
    # USAGE STATUS
    # =========================

    status_card = tk.Frame(
        dashboard_content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    status_card.pack(
        fill="x",
        pady=(0, 24)
    )

    status_left = tk.Frame(
        status_card,
        bg=WHITE
    )

    status_left.pack(
        side="left",
        padx=22,
        pady=15
    )

    tk.Label(
        status_left,
        text="USAGE STATUS",
        font=("Segoe UI", 9, "bold"),
        bg=WHITE,
        fg=GREY
    ).pack(
        anchor="w"
    )

    if highest_usage > 12:

        status_text = "High usage detected"
        status_colour = "#C62828"

    elif average_usage > 8:

        status_text = "Usage needs attention"
        status_colour = "#F57C00"

    else:

        status_text = "Usage is within normal range"
        status_colour = TEAL

    tk.Label(
        status_left,
        text=status_text,
        font=("Segoe UI", 12, "bold"),
        bg=WHITE,
        fg=status_colour
    ).pack(
        anchor="w",
        pady=(3, 0)
    )

    tk.Label(
        status_card,
        text=(
            f"Highest: {highest_usage} units   •   "
            f"Lowest: {lowest_usage} units   •   "
            f"Total: {total_units} units"
        ),
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="right",
        padx=25
    )

    # =========================
    # QUICK ACTIONS
    # =========================

    tk.Label(
        dashboard_content,
        text="QUICK ACTIONS",
        font=("Segoe UI", 11, "bold"),
        bg=LIGHT_BG,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    action_grid = tk.Frame(
        dashboard_content,
        bg=LIGHT_BG
    )

    action_grid.pack(
        fill="both",
        expand=True
    )

    def create_action_card(
        parent,
        row,
        column,
        icon,
        title,
        description,
        command
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            height=125,
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2"
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=6,
            pady=6
        )

        card.grid_propagate(False)

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        parent.grid_rowconfigure(
            row,
            weight=1
        )

        content = tk.Frame(
            card,
            bg=WHITE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=12
        )

        icon_label = tk.Label(
            content,
            text=icon,
            font=("Segoe UI", 20),
            bg=WHITE,
            fg=TEAL
        )

        icon_label.pack(
            anchor="w"
        )

        title_label = tk.Label(
            content,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=TEXT
        )

        title_label.pack(
            anchor="w",
            pady=(5, 2)
        )

        description_label = tk.Label(
            content,
            text=description,
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=GREY
        )

        description_label.pack(
            anchor="w"
        )

        arrow_label = tk.Label(
            content,
            text="→",
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=TEAL
        )

        arrow_label.pack(
            anchor="e"
        )

        widgets = [
            card,
            content,
            icon_label,
            title_label,
            description_label,
            arrow_label
        ]

        def enter(event):

            for widget in widgets:

                widget.configure(
                    bg=SOFT_TEAL
                )

        def leave(event):

            for widget in widgets:

                widget.configure(
                    bg=WHITE
                )

        def click(event):

            command()

        for widget in widgets:

            widget.bind(
                "<Enter>",
                enter
            )

            widget.bind(
                "<Leave>",
                leave
            )

            widget.bind(
                "<Button-1>",
                click
            )

    create_action_card(
        action_grid,
        0,
        0,
        "₹",
        "Bill Breakdown",
        "View your estimated electricity bill",
        lambda:show_bill() 
    )

    create_action_card(
        action_grid,
        0,
        1,
        "◈",
        "Usage Analysis",
        "Explore your daily consumption pattern",
        lambda:show_usage()
    )

    create_action_card(
        action_grid,
        0,
        2,
        "⚡",
        "Appliance Consumption",
        "Analyse appliance-level electricity usage",
        lambda:show_appliances()
    )

    create_action_card(
        action_grid,
        1,
        0,
        "✦",
        "Energy Saving",
        "Get practical energy-saving suggestions",
        lambda:energy_saving()
    )

    create_action_card(
        action_grid,
        1,
        1,
        "📄",
        "Generate Report",
        "Create a detailed electricity report",
        generate_report
    )

    create_action_card(
        action_grid,
        1,
        2,
        "🔔",
        "Usage Alert",
        "Check your electricity usage status",
        lambda: show_notification(
            average_usage,
            highest_usage
        )
    )

    # =========================
    # FOOTER
    # =========================

    tk.Label(
        root,
        text="Smart Energy Management  •  Python Desktop Application",
        font=("Segoe UI", 8),
        bg=LIGHT_BG,
        fg=GREY
    ).pack(
        side="bottom",
        pady=8
    )

    # =========================
    # BILL BREAKDOWN
    # =========================
    def return_to_dashboard():

        for widget in root.winfo_children():
            widget.destroy()

        show_dashboard(
            root,
            total_units,
            average_usage,
            highest_usage,
            lowest_usage,
            bill
        )
    def show_bill():

        (
            first_units,
            first_charge,
            second_units,
            second_charge,
            third_units,
            third_charge
        ) = get_bill_breakdown(total_units)

        # Clear dashboard
        for widget in root.winfo_children():
            widget.destroy()

        root.configure(bg=LIGHT_BG)

        # =========================
        # HEADER
        # =========================

        header = tk.Frame(
            root,
            bg=DARK_NAVY,
            height=90
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(
            header,
            text="←  Back",
            command=lambda: return_to_dashboard(),
            font=("Segoe UI", 10, "bold"),
            bg="#173B57",
            fg=WHITE,
            activebackground="#204B6C",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            header,
            text="⚡  ELECTRICITY BILL",
            font=("Segoe UI", 21, "bold"),
            bg=DARK_NAVY,
            fg=WHITE
        ).pack(
            side="left",
            padx=25
        )

        # =========================
        # CONTENT
        # =========================

        content = tk.Frame(
            root,
            bg=LIGHT_BG
        )

        content.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=35
        )

        tk.Label(
            content,
            text="Your Estimated Electricity Bill",
            font=("Segoe UI", 24, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack()

        tk.Label(
            content,
            text="Understand exactly how your electricity bill is calculated.",
            font=("Segoe UI", 10),
            bg=LIGHT_BG,
            fg=GREY
        ).pack(
            pady=(5, 25)
        )

        # =========================
        # TOTAL BILL CARD
        # =========================

        total_card = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        total_card.pack(
            fill="x",
            pady=(0, 20)
        )

        tk.Label(
            total_card,
            text="TOTAL CONSUMPTION",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=GREY
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            total_card,
            text=f"{total_units} units",
            font=("Segoe UI", 26, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack()

        tk.Label(
            total_card,
            text=f"Estimated Bill: ₹{bill:.2f}",
            font=("Segoe UI", 18, "bold"),
            bg=WHITE,
            fg=TEAL
        ).pack(
            pady=(5, 20)
        )

        # =========================
        # SLAB EXPLANATION
        # =========================

        tk.Label(
            content,
            text="HOW YOUR BILL IS CALCULATED",
            font=("Segoe UI", 12, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        slab_card = tk.Frame(
            content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        slab_card.pack(
            fill="x"
        )

        def add_slab(
            title,
            explanation,
            calculation,
            amount,
            row
        ):

            tk.Label(
                slab_card,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg=WHITE,
                fg=NAVY
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=25,
                pady=14
            )

            tk.Label(
                slab_card,
                text=explanation,
                font=("Segoe UI", 10),
                bg=WHITE,
                fg=GREY
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=20,
                pady=14
            )

            tk.Label(
                slab_card,
                text=calculation,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=TEXT
            ).grid(
                row=row,
                column=2,
                sticky="e",
                padx=20,
                pady=14
            )

            tk.Label(
                slab_card,
                text=f"₹{amount:.2f}",
                font=("Segoe UI", 11, "bold"),
                bg=WHITE,
                fg=TEAL
            ).grid(
                row=row,
                column=3,
                sticky="e",
                padx=25,
                pady=14
            )

        add_slab(
            "First 100 units",
            "Slab 1",
            f"{first_units} × ₹2.50",
            first_charge,
            0
        )

        add_slab(
            "Next 100 units",
            "Slab 2",
            f"{second_units} × ₹4.00",
            second_charge,
            1
        )

        add_slab(
            "Above 200 units",
            "Slab 3",
            f"{third_units} × ₹6.00",
            third_charge,
            2
        )

        # =========================
        # TOTAL
        # =========================

        tk.Frame(
            slab_card,
            bg=BORDER,
            height=1
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=20
        )

        tk.Label(
            slab_card,
            text="TOTAL BILL",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="w",
            padx=25,
            pady=18
        )

        tk.Label(
            slab_card,
            text=f"₹{bill:.2f}",
            font=("Segoe UI", 18, "bold"),
            bg=WHITE,
            fg=TEAL
        ).grid(
            row=4,
            column=3,
            sticky="e",
            padx=25,
            pady=18
        )

        tk.Label(
            content,
            text="Prototype tariff used for demonstration",
            font=("Segoe UI", 9, "italic"),
            bg=LIGHT_BG,
            fg=GREY
        ).pack(
            pady=15
        )

    # =========================
    # USAGE ANALYSIS
    # =========================

    def show_usage():

        data = pd.read_csv("meter_data.csv")

        data["units_consumed"] = (
            data["current_reading"]
            - data["previous_reading"]
        )

        # Clear current page
        for widget in root.winfo_children():
            widget.destroy()

        root.configure(bg=LIGHT_BG)

        # =========================
        # HEADER
        # =========================

        header = tk.Frame(
            root,
            bg=DARK_NAVY,
            height=90
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(
            header,
            text="←  Back",
            command=return_to_dashboard,
            font=("Segoe UI", 10, "bold"),
            bg="#173B57",
            fg=WHITE,
            activebackground="#204B6C",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            header,
            text="📊  USAGE ANALYSIS",
            font=("Segoe UI", 21, "bold"),
            bg=DARK_NAVY,
            fg=WHITE
        ).pack(
            side="left",
            padx=25
        )

        # =========================
        # TITLE
        # =========================

        tk.Label(
            root,
            text="Daily Electricity Usage",
            font=("Segoe UI", 24, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack(
            pady=(30, 5)
        )

        tk.Label(
            root,
            text="Monitor how your electricity consumption changes each day.",
            font=("Segoe UI", 10),
            bg=LIGHT_BG,
            fg=GREY
        ).pack(
            pady=(0, 15)
        )

        # =========================
        # GRAPH
        # =========================

        graph_card = tk.Frame(
            root,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        graph_card.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=(5, 35)
        )

        figure = plt.Figure(
            figsize=(10, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        axis.plot(
            data["date"],
            data["units_consumed"],
            marker="o"
        )

        axis.set_xlabel(
            "Date"
        )

        axis.set_ylabel(
            "Units Consumed"
        )

        axis.set_title(
            "Daily Electricity Usage"
        )

        axis.tick_params(
            axis="x",
            rotation=45
        )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=graph_card
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

    # =========================
    # APPLIANCE CONSUMPTION
    # =========================

    def show_appliances():

        # Clear current dashboard
        for widget in root.winfo_children():
            widget.destroy()

        root.configure(
            bg=LIGHT_BG
        )

        # Use the main application window
        window = root

        # =========================
        # HEADER
        # =========================

        header = tk.Frame(
            window,
            bg=NAVY,
            height=90
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Button(
            header,
            text="←  Back",
            command=return_to_dashboard,
            font=("Segoe UI", 10, "bold"),
            bg="#173B57",
            fg=WHITE,
            activebackground="#204B6C",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(
            side="left",
            padx=30
        )

        tk.Label(
            header,
            text="⚡ APPLIANCE CONSUMPTION",
            font=("Segoe UI", 22, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(pady=(22, 4))

        tk.Label(
            header,
            text="Estimated electricity consumption by appliance",
            font=("Segoe UI", 10),
            bg=NAVY,
            fg="#D9EAF7"
        ).pack()

        # =========================
        # TABLE CARD
        # =========================

        table_card = tk.Frame(
            window,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#D7E0E7"
        )

        table_card.pack(
            padx=35,
            pady=18,
            fill="x",
        )

        table_card.configure(
            height=430
       ) 

        table_card.pack_propagate(False)

        # =========================
        # SCROLLABLE APPLIANCE TABLE
        # =========================

        table_area = tk.Frame(
            table_card,
            bg=WHITE
        )

        table_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        canvas = tk.Canvas(
            table_area,
            bg=WHITE,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            table_area,
            orient="vertical",
            command=canvas.yview
        )

        table = tk.Frame(
            canvas,
            bg=WHITE
        )

        table.grid_columnconfigure(
            0,
            weight=1
        )

        table.grid_columnconfigure(
            1,
            weight=1
        )

        table.grid_columnconfigure(
            2,
            weight=1
        )

        table.grid_columnconfigure(
            3,
            weight=1
        )

        table.grid_columnconfigure(
            4,
            weight=1
        )

        table_window = canvas.create_window(
            (0, 0),
            window=table,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        def resize_table(event):
            canvas.itemconfig(
                table_window,
                width=event.width
            )

        canvas.bind(
            "<Configure>",
            resize_table
        )

        def update_scroll(event=None):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        table.bind(
            "<Configure>",
            update_scroll
        )

        headings = [
            "Appliance",
            "Power (W)",
            "Hours",
            "Units",
            "Cost"
        ]

        widths = [
            20,
            14,
            14,
            14,
            14
        ]

        # =========================
        # TABLE HEADINGS
        # =========================

        for column, heading in enumerate(headings):

            tk.Label(
                table,
                text=heading,
                font=("Segoe UI", 10, "bold"),
                bg=NAVY,
                fg=WHITE,
                width=widths[column],
                height=2
            ).grid(
                row=0,
                column=column,
                padx=1,
                pady=1,
                sticky="nsew"
            )

        # =========================
        # LOAD APPLIANCES
        # =========================

        def load_appliances():

            for widget in table.winfo_children():

                if widget.grid_info().get("row") != 0:
                    widget.destroy()

            appliances = get_appliances()

            if not appliances:

                tk.Label(
                    table,
                    text="No appliances added yet.",
                    font=("Segoe UI", 11),
                    bg=WHITE,
                    fg=GREY
                ).grid(
                    row=1,
                    column=0,
                    columnspan=5,
                    pady=50
                )

                return

            for row_number, appliance in enumerate(
                appliances,
                start=1
            ):

                name = appliance[0]
                wattage = appliance[1]
                hours = appliance[2]
                units = appliance[3]
                cost = appliance[4]

                values = [
                    name,
                    f"{wattage:.0f}",
                    f"{hours:.1f}",
                    f"{units:.2f}",
                    f"₹{cost:.2f}"
                ]

                for column, value in enumerate(values):

                    tk.Label(
                        table,
                        text=value,
                        font=("Segoe UI", 10),
                        bg=WHITE,
                        fg=TEXT,
                        width=widths[column],
                        height=2
                    ).grid(
                        row=row_number,
                        column=column,
                        padx=1,
                        pady=1,
                        sticky="nsew"
                    )

            update_scroll()

        load_appliances()

        # =========================
        # ADD APPLIANCE
        # =========================

        def add_new_appliance():

            add_appliance_window(
                window,
                load_appliances
            )

        tk.Button(
            window,
            text="＋  Add Appliance",
            command=add_new_appliance,
            font=("Segoe UI", 11, "bold"),
            bg=TEAL,
            fg=WHITE,
            activebackground=TEAL,
            activeforeground=WHITE,
            relief="flat",
            width=20,
            height=2,
            cursor="hand2"
        ).pack(
            pady=(0, 8)
        )

        # =========================
        # APPLIANCE ANALYSIS
        # =========================

        def show_analysis():

            appliances = get_appliances()

            if not appliances:

                messagebox.showinfo(
                    "Appliance Analysis",
                    "No appliances have been added yet."
                )

                return

            highest = appliances[0]
            lowest = appliances[-1]

            total_consumption = sum(
                appliance[3]
                for appliance in appliances
            )

            total_cost = sum(
                appliance[4]
                for appliance in appliances
            )

            waste_alerts = detect_appliance_waste(
                appliances
            )

            suggestions = generate_suggestions(
                appliances
            )
            # =========================
            # ANALYSIS WINDOW
            # =========================

            analysis = tk.Toplevel(window)

            analysis.title(
                "Appliance Analysis"
            )

            analysis.geometry(
                "900x700"
            )

            analysis.resizable(
                False,
                False
            )

            analysis.configure(
                bg=LIGHT_BG
            )

            # Clear current appliance page
            for widget in window.winfo_children():
                widget.destroy()

            window.title(
                "Appliance Analysis"
            )

            window.state("zoomed")
            window.resizable(True, True)
            window.configure(
                bg=LIGHT_BG
            )

            # =========================
            # HEADER
            # =========================

            header = tk.Frame(
                window,
                bg=NAVY,
                height=120
            )

            header.pack(
                fill="x"
            )

            header.pack_propagate(False)

            tk.Button(
                header,
                text="←  Back",
                command=show_appliances,
                font=("Segoe UI", 10, "bold"),
                bg="#173B57",
                fg=WHITE,
                activebackground="#204B6C",
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=18,
                pady=8
            ).pack(
                side="left",
                padx=25,
                pady=35
            )

            tk.Label(
                header,
                text="📊  APPLIANCE ANALYSIS",
                font=("Segoe UI", 25, "bold"),
                bg=NAVY,
                fg=WHITE
            ).pack(
                pady=(25, 2)
            )

            tk.Label(
                header,
                text="Consumption comparison and usage insights",
                font=("Segoe UI", 10),
                bg=NAVY,
                fg="#D9EAF7"
            ).pack()

            # =========================
            # SUMMARY CARDS
            # =========================

            cards = tk.Frame(
                window,
                bg=LIGHT_BG
            )

            cards.pack(
                fill="x",
                padx=35,
                pady=20
            )

            def analysis_card(
                title,
                value,
                subtitle,
                column
            ):

                card = tk.Frame(
                    cards,
                    bg=WHITE,
                    height=110,
                    highlightthickness=1,
                    highlightbackground="#D7E0E7"
                )

                card.grid(
                    row=0,
                    column=column,
                    padx=6,
                    sticky="nsew"
                )

                cards.grid_columnconfigure(
                    column,
                    weight=1
                )

                card.grid_propagate(False)

                tk.Label(
                    card,
                    text=title,
                    font=("Segoe UI", 10, "bold"),
                    bg=WHITE,
                    fg=GREY
                ).pack(
                    pady=(15, 3)
                )

                tk.Label(
                    card,
                    text=value,
                    font=("Segoe UI", 17, "bold"),
                    bg=WHITE,
                    fg=TEXT
                ).pack()

                tk.Label(
                    card,
                    text=subtitle,
                    font=("Segoe UI", 9),
                    bg=WHITE,
                    fg=GREY
                ).pack()

            analysis_card(
                "TOTAL CONSUMPTION",
                f"{total_consumption:.2f} units",
                "Estimated appliance usage",
                0
            )

            analysis_card(
                "HIGHEST CONSUMER",
                highest[0],
                f"{highest[3]:.2f} units/day",
                1
            )

            analysis_card(
                "LOWEST CONSUMER",
                lowest[0],
                f"{lowest[3]:.2f} units/day",
                2
            )

            analysis_card(
                "ESTIMATED COST",
                f"₹{total_cost:.2f}",
                "Estimated appliance cost/day",
                3
            )

            # =========================
            # MAIN CONTENT
            # =========================

            content = tk.Frame(
                window,
                bg=LIGHT_BG
            )

            content.pack(
                fill="both",
                expand=True,
                padx=35
            )

            # =========================
            # HIGH USAGE
            # =========================

            alert_card = tk.Frame(
                content,
                bg=WHITE,
                highlightthickness=1,
                highlightbackground="#D7E0E7"
            )

            alert_card.pack(
                fill="x",
                pady=(0, 12)
            )

            tk.Label(
                alert_card,
                text="⚠  HIGH-USAGE ALERT",
                font=("Segoe UI", 12, "bold"),
                bg=WHITE,
                fg="#C62828"
            ).pack(
                anchor="w",
                padx=18,
                pady=(12, 5)
            )

            if waste_alerts:

                for alert in waste_alerts:

                    tk.Label(
                        alert_card,
                        text="• " + alert,
                        font=("Segoe UI", 10),
                        bg=WHITE,
                        fg=TEXT,
                        anchor="w"
                    ).pack(
                        anchor="w",
                        padx=18,
                        pady=3
                    )

            else:

                tk.Label(
                    alert_card,
                    text="✓ No high-usage appliances detected",
                    font=("Segoe UI", 10, "bold"),
                    bg=WHITE,
                    fg=GREEN
                ).pack(
                    anchor="w",
                    padx=18,
                    pady=(5, 15)
                )

            # =========================
            # SUGGESTIONS
            # =========================

            suggestion_card = tk.Frame(
                content,
                bg=WHITE,
                highlightthickness=1,
                highlightbackground="#D7E0E7"
            )

            suggestion_card.pack(
                fill="x",
                pady=(0, 12)
            )

            tk.Label(
                suggestion_card,
                text="💡  ENERGY-SAVING SUGGESTIONS",
                font=("Segoe UI", 12, "bold"),
                bg=WHITE,
                fg=GREEN
            ).pack(
                anchor="w",
                padx=18,
                pady=(12, 5)
            )

            if suggestions:

                for suggestion in suggestions:

                    tk.Label(
                        suggestion_card,
                        text="• " + suggestion,
                        font=("Segoe UI", 10),
                        bg=WHITE,
                        fg=TEXT,
                        anchor="w"
                    ).pack(
                        anchor="w",
                        padx=18,
                        pady=3
                    )

            else:

                tk.Label(
                    suggestion_card,
                    text="✓ No specific suggestions at this time.",
                    font=("Segoe UI", 10),
                    bg=WHITE,
                    fg=GREEN
                ).pack(
                    anchor="w",
                    padx=18,
                    pady=(5, 15)
                )

            # =========================
            # GRAPH
            # =========================

            graph_card = tk.Frame(
                window,
                bg=WHITE,
                highlightthickness=1,
                highlightbackground="#D7E0E7",
                height=300
            )

            graph_card.pack(
                fill="both",
                expand=True,
                padx=35,
                pady=(5, 12)
            )

            graph_card.pack_propagate(False)

            tk.Label(
                graph_card,
                text="APPLIANCE CONSUMPTION COMPARISON",
                font=("Segoe UI", 12, "bold"),
                bg=WHITE,
                fg=NAVY
            ).pack(
                anchor="w",
                padx=18,
                pady=(12, 5)
            )

            # Scrollable graph area
            graph_area = tk.Frame(
                graph_card,
                bg=WHITE
            )

            graph_area.pack(
                fill="both",
                expand=True,
                padx=10,
                pady=5
            )

            scroll_canvas = tk.Canvas(
                graph_area,
                bg=WHITE,
                highlightthickness=0
            )

            scrollbar = tk.Scrollbar(
                graph_area,
                orient="vertical",
                command=scroll_canvas.yview
            )

            scroll_frame = tk.Frame(
                scroll_canvas,
                bg=WHITE
            )

            scroll_frame.bind(
                "<Configure>",
                lambda e: scroll_canvas.configure(
                    scrollregion=scroll_canvas.bbox("all")
                )
            )

            window_id = scroll_canvas.create_window(
                (0, 0),
                window=scroll_frame,
                anchor="nw"
            )

            scroll_canvas.bind(
                "<Configure>",
                lambda e: scroll_canvas.itemconfig(
                    window_id,
                    width=e.width
                )
            )

            scroll_canvas.configure(
                yscrollcommand=scrollbar.set
            )

            scroll_canvas.pack(
                side="left",
                fill="both",
                expand=True
            )

            scrollbar.pack(
                side="right",
                fill="y"
            )

            # Sort highest consumption first
            sorted_appliances = sorted(
                appliances,
                key=lambda x: x[3],
                reverse=True
            )

            names = [
                appliance[0]
                for appliance in sorted_appliances
            ]

            units = [
                appliance[3]
                for appliance in sorted_appliances
            ]

            # Reverse so highest appears at the top
            names = names[::-1]
            units = units[::-1]

            # Figure height grows with appliances
            figure_height = max(
                3.2,
                len(names) * 0.45 + 1.2
            )

            figure = plt.Figure(
                figsize=(8, figure_height),
                dpi=100
            )

            axis = figure.add_subplot(111)

            axis.barh(
                names,
                units,
                height=0.28
            )

            axis.set_xlabel(
                "Units per Day",
                fontsize=9
            )

            axis.set_title(
                "Appliance Consumption",
                fontsize=12,
                fontweight="bold"
            )

            axis.grid(
                axis="x",
                linestyle="--",
                alpha=0.25
            )

            axis.set_axisbelow(True)

            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)
            axis.spines["left"].set_visible(False)

            axis.tick_params(
                axis="y",
                labelsize=9
            )

            axis.tick_params(
                axis="x",
                labelsize=8
            )

            # Show value at end of each thin bar
            if units:

                maximum = max(units)

                for index, value in enumerate(units):

                    axis.text(
                        value + maximum * 0.02,
                        index,
                        f"{value:.2f}",
                        va="center",
                        fontsize=8
                    )

                axis.set_xlim(
                    0,
                    maximum * 1.15
                )

            figure.subplots_adjust(
                left=0.25,
                right=0.95,
                top=0.88,
                bottom=0.15
            )

            graph_canvas = FigureCanvasTkAgg(
                figure,
                master=scroll_frame
            )

            graph_canvas.draw()

            graph_canvas.get_tk_widget().pack(
                fill="x",
                expand=False
            )

        # =========================
        # DELETE APPLIANCE
        # =========================

        def delete_selected_appliance():

            appliances = get_appliances()

            if not appliances:

                messagebox.showinfo(
                    "Delete Appliance",
                    "No appliances available to delete."
                )

                return

            delete_window = tk.Toplevel(window)

            delete_window.title(
                "Delete Appliance"
            )

            delete_window.geometry(
                "500x420"
            )

            delete_window.resizable(
                False,
                False
            )

            delete_window.configure(
                bg=LIGHT_BG
            )

            tk.Label(
                delete_window,
                text="🗑 DELETE APPLIANCE",
                font=("Segoe UI", 20, "bold"),
                bg=LIGHT_BG,
                fg=NAVY
            ).pack(
                pady=(25, 10)
            )

            tk.Label(
                delete_window,
                text="Select the appliance record to delete",
                font=("Segoe UI", 10),
                bg=LIGHT_BG,
                fg=GREY
            ).pack(
                pady=(0, 15)
            )

            appliance_var = tk.StringVar()

            options = []

            for appliance in appliances:

                name = appliance[0]
                hours = appliance[2]
                units = appliance[3]

                options.append(
                    f"{name} — {hours:.1f} hours/day — {units:.2f} units"
                )

            appliance_var.set(
                options[0]
            )

            menu = tk.OptionMenu(
                delete_window,
                appliance_var,
                *options
            )

            menu.config(
                font=("Segoe UI", 10),
                width=38
            )

            menu.pack(
                pady=10
            )

            def delete_record():

                selected = appliance_var.get()

                selected_index = options.index(
                    selected
                )

                appliance = appliances[
                    selected_index
                ]

                name = appliance[0]
                hours = appliance[2]

                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Delete {name} "
                    f"({hours:.1f} hours/day)?"
                )

                if not confirm:
                    return

                delete_appliance(
                    name,
                    hours
                )

                messagebox.showinfo(
                    "Deleted",
                    f"{name} deleted successfully."
                )

                delete_window.destroy()

                load_appliances()

            tk.Button(
                delete_window,
                text="DELETE SELECTED",
                command=delete_record,
                font=("Segoe UI", 10, "bold"),
                bg="#C62828",
                fg=WHITE,
                relief="flat",
                width=20,
                height=2,
                cursor="hand2"
            ).pack(
                pady=25
            )

            tk.Button(
                delete_window,
                text="Cancel",
                command=delete_window.destroy,
                font=("Segoe UI", 10),
                bg=NAVY,
                fg=WHITE,
                relief="flat",
                width=15,
                height=2,
                cursor="hand2"
            ).pack()

        # =========================
        # DELETE APPLIANCE BUTTON
        # =========================

        tk.Button(
            window,
            text="🗑  Delete Appliance",
            command=delete_selected_appliance,
            font=("Segoe UI", 11, "bold"),
            bg="#C62828",
            fg=WHITE,
            activebackground="#C62828",
            activeforeground=WHITE,
            relief="flat",
            width=20,
            height=2,
            cursor="hand2"
        ).pack(
            pady=(0, 8)
        )

        # =========================
        # VIEW ANALYSIS BUTTON
        # =========================

        tk.Button(
            window,
            text="📊  View Analysis",
            command=show_analysis,
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            width=20,
            height=2,
            cursor="hand2"
        ).pack(
            pady=(0, 8)
        )
        # =========================
        # CLOSE
        # =========================

        tk.Button(
            window,
            text="Close",
            command=return_to_dashboard,
            font=("Segoe UI", 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            relief="flat",
            width=15,
            height=2,
            cursor="hand2"
        ).pack(
            pady=(0, 15)
        )

    # =========================
    # ENERGY SAVING
    # =========================

    def energy_saving():

        if average_usage > 8:

            suggestion = (
                "ENERGY SAVING SUGGESTIONS\n\n"
                f"Average daily usage: "
                f"{average_usage:.1f} units\n\n"
                "• Switch off appliances when not required.\n"
                "• Avoid unnecessary standby power.\n"
                "• Use energy-efficient appliances.\n"
                "• Monitor high-usage days regularly."
            )

        else:

            suggestion = (
                "ENERGY SAVING SUGGESTIONS\n\n"
                f"Average daily usage: "
                f"{average_usage:.1f} units\n\n"
                "• Continue monitoring electricity usage.\n"
                "• Switch off unused appliances.\n"
                "• Avoid unnecessary standby power."
            )

        messagebox.showinfo(
            "Energy Saving",
            suggestion
        )

    # =========================
    # USER PROFILE
    # =========================

    def user_profile():

        window = tk.Toplevel(root)

        window.title(
            "User Profile"
        )

        window.geometry(
            "450x350"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            bg=LIGHT_BG
        )

        tk.Label(
            window,
            text="USER PROFILE",
            font=("Segoe UI", 20, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(
            pady=(25, 20)
        )

        tk.Label(
            window,
            text="Name",
            font=("Segoe UI", 11, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack()

        name_entry = tk.Entry(
            window,
            font=("Segoe UI", 12),
            width=30
        )

        name_entry.pack(
            pady=7
        )

        tk.Label(
            window,
            text="Room / House No.",
            font=("Segoe UI", 11, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack(
            pady=(10, 0)
        )

        room_entry = tk.Entry(
            window,
            font=("Segoe UI", 12),
            width=30
        )

        room_entry.pack(
            pady=7
        )

        connection = sqlite3.connect(
            "electricity.db"
        )

        cursor = connection.cursor()

        saved_profile = cursor.execute(
            """
            SELECT name, room_no
            FROM user_profile
            WHERE id = 1
            """
        ).fetchone()

        connection.close()

        if saved_profile:

            name_entry.insert(
                0,
                saved_profile[0]
            )

            room_entry.insert(
                0,
                saved_profile[1]
            )

        def save_profile():

            name = name_entry.get().strip()
            room = room_entry.get().strip()

            if not name or not room:

                messagebox.showwarning(
                    "Missing Information",
                    "Please enter both name and room/house number."
                )

                return

            connection = sqlite3.connect(
                "electricity.db"
            )

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT OR REPLACE INTO user_profile
                (id, name, room_no)
                VALUES (1, ?, ?)
                """,
                (name, room)
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Profile Saved",
                "User profile saved successfully."
            )

        tk.Button(
            window,
            text="Save Profile",
            command=save_profile,
            font=("Segoe UI", 11, "bold"),
            bg=TEAL,
            fg=WHITE,
            relief="flat",
            width=18,
            height=2,
            cursor="hand2"
        ).pack(
            pady=25
        )
    # =========================
    # GENERATE REPORT
    # =========================

    def generate_electricity_report():

        try:

            filename = generate_report(
                total_units,
                average_usage,
                highest_usage,
                lowest_usage,
                bill
            )

            messagebox.showinfo(
                "Report Generated",
                f"Electricity report generated successfully!\n\n"
                f"Saved as:\n{filename}"
            )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                f"Could not generate report.\n\n{error}"
            )

    # =========================
    # EXIT APPLICATION
    # =========================

    exit_button = tk.Button(
        root,
        text="Exit Application",
        command=root.destroy,
        font=("Segoe UI", 9, "bold"),
        bg=LIGHT_BG,
        fg=GREY,
        activebackground=LIGHT_BG,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        cursor="hand2"
    )

    exit_button.pack(
        pady=(0, 5)
    )

    # =========================
    # START DASHBOARD
    # =========================
    
    # =========================
    # AUTOMATIC USAGE ALERT
    # =========================

    if highest_usage > 12:

        messagebox.showwarning(
            "⚠ High Electricity Usage",
            f"High electricity usage detected!\n\n"
            f"Peak usage: {highest_usage} units/day\n"
            f"Average usage: {average_usage:.1f} units/day\n\n"
            "Please monitor your electricity consumption."
        )

    elif average_usage > 8:

        messagebox.showinfo(
            "Electricity Usage Notice",
            f"Average daily usage is "
            f"{average_usage:.1f} units.\n\n"
            "Consider reducing unnecessary electricity usage."
        )


    root.mainloop()

    

# =========================
# CREATE PROFILE TABLE
# =========================

create_profile_table()