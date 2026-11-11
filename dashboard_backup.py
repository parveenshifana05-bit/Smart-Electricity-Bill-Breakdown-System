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
            room_no TEXT
        )
    """)

    connection.commit()
    connection.close()


# =========================
# USER PROFILE FIRST PAGE
# =========================

def show_profile_page(
    total_units,
    average_usage,
    highest_usage,
    lowest_usage,
    bill
):

    profile = tk.Tk()

    profile.title(
        "Smart Electricity Bill Breakdown System"
    )

    profile.geometry("600x500")
    profile.resizable(False, False)
    profile.configure(bg=LIGHT_BG)

    # HEADER
    header = tk.Frame(
        profile,
        bg=NAVY,
        height=120
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="⚡ SMART ELECTRICITY",
        font=("Segoe UI", 25, "bold"),
        bg=NAVY,
        fg=WHITE
    ).pack(pady=(25, 3))

    tk.Label(
        header,
        text="User Profile",
        font=("Segoe UI", 12),
        bg=NAVY,
        fg="#D9EAF7"
    ).pack()

    # PROFILE CARD
    card = tk.Frame(
        profile,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground="#D7E0E7"
    )

    card.pack(
        padx=70,
        pady=35,
        fill="both",
        expand=True
    )

    tk.Label(
        card,
        text="Enter Your Details",
        font=("Segoe UI", 18, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(25, 20))

    # NAME
    tk.Label(
        card,
        text="Name",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack()

    name_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        width=32
    )

    name_entry.pack(pady=7)

    # ROOM / HOUSE
    tk.Label(
        card,
        text="Room / House No.",
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=TEXT
    ).pack(pady=(12, 0))

    room_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        width=32
    )

    room_entry.pack(pady=7)

    # LOAD SAVED PROFILE
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

    # SAVE AND CONTINUE
    def save_and_continue():

        name = name_entry.get().strip()
        room = room_entry.get().strip()

        if not name or not room:

            messagebox.showwarning(
                "Missing Information",
                "Please enter both Name and Room / House No."
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

        profile.destroy()

        show_dashboard(
            total_units,
            average_usage,
            highest_usage,
            lowest_usage,
            bill
        )

    tk.Button(
        card,
        text="SAVE & CONTINUE  →",
        command=save_and_continue,
        font=("Segoe UI", 11, "bold"),
        bg=TEAL,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=WHITE,
        relief="flat",
        width=22,
        height=2,
        cursor="hand2"
    ).pack(pady=25)

    profile.mainloop()


# =========================
# DASHBOARD
# =========================

def show_dashboard(
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

    root.geometry("950x800")
    root.resizable(False, False)
    root.configure(bg=LIGHT_BG)

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        root,
        bg=NAVY,
        height=125
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="⚡ SMART ELECTRICITY",
        font=("Segoe UI", 26, "bold"),
        bg=NAVY,
        fg=WHITE
    ).pack(pady=(20, 2))

    tk.Label(
        header,
        text="Bill Breakdown & Energy Usage Dashboard",
        font=("Segoe UI", 13),
        bg=NAVY,
        fg="#D9EAF7"
    ).pack()

    # =========================
    # TITLE
    # =========================

    welcome = tk.Frame(
        root,
        bg=LIGHT_BG
    )

    welcome.pack(
        fill="x",
        padx=45,
        pady=(18, 5)
    )

    tk.Label(
        welcome,
        text="Electricity Overview",
        font=("Segoe UI", 18, "bold"),
        bg=LIGHT_BG,
        fg=TEXT
    ).pack(side="left")

    # =========================
    # SUMMARY CARDS
    # =========================

    cards = tk.Frame(
        root,
        bg=LIGHT_BG
    )

    cards.pack(pady=12)

    def create_card(
        title,
        value,
        subtitle,
        column,
        accent
    ):

        card = tk.Frame(
            cards,
            bg=WHITE,
            width=200,
            height=120,
            highlightthickness=1,
            highlightbackground="#D7E0E7"
        )

        card.grid(
            row=0,
            column=column,
            padx=7
        )

        card.grid_propagate(False)

        tk.Frame(
            card,
            bg=accent,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        content = tk.Frame(
            card,
            bg=WHITE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=12
        )

        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg=WHITE,
            fg=GREY
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        tk.Label(
            content,
            text=value,
            font=("Segoe UI", 22, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Label(
            content,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=GREY
        ).pack(
            anchor="w"
        )

    create_card(
        "TOTAL UNITS",
        str(total_units),
        "Units consumed",
        0,
        BLUE
    )

    create_card(
        "AVERAGE / DAY",
        f"{average_usage:.1f}",
        "Daily consumption",
        1,
        TEAL
    )

    create_card(
        "PEAK USAGE",
        str(highest_usage),
        "Highest daily units",
        2,
        ORANGE
    )

    create_card(
        "ESTIMATED BILL",
        f"₹{bill:.2f}",
        "Prototype calculation",
        3,
        GREEN
    )

    # =========================
    # USAGE SUMMARY
    # =========================

    summary = tk.Frame(
        root,
        bg=WHITE,
        highlightthickness=1,
        highlightbackground="#D7E0E7"
    )

    summary.pack(
        fill="x",
        padx=55,
        pady=10
    )

    tk.Label(
        summary,
        text="USAGE SUMMARY",
        font=("Segoe UI", 13, "bold"),
        bg=WHITE,
        fg=NAVY
    ).pack(
        anchor="w",
        padx=20,
        pady=(12, 5)
    )

    details = tk.Frame(
        summary,
        bg=WHITE
    )

    details.pack(
        fill="x",
        padx=20,
        pady=(0, 12)
    )

    tk.Label(
        details,
        text=f"Highest: {highest_usage} units",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="left",
        padx=(0, 40)
    )

    tk.Label(
        details,
        text=f"Lowest: {lowest_usage} units",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="left",
        padx=(0, 40)
    )

    tk.Label(
        details,
        text=f"Total: {total_units} units",
        font=("Segoe UI", 10),
        bg=WHITE,
        fg=TEXT
    ).pack(
        side="left"
    )

    # =========================
    # BILL BREAKDOWN
    # =========================

    def show_bill():

        (
            first_units,
            first_charge,
            second_units,
            second_charge,
            third_units,
            third_charge
        ) = get_bill_breakdown(total_units)

        window = tk.Toplevel(root)

        window.title("Electricity Bill")
        window.geometry("520x560")
        window.resizable(False, False)
        window.configure(bg=LIGHT_BG)

        header = tk.Frame(
            window,
            bg=NAVY,
            height=100
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="⚡ ELECTRICITY BILL",
            font=("Segoe UI", 22, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(pady=(22, 2))

        tk.Label(
            header,
            text="Smart Electricity Bill Breakdown",
            font=("Segoe UI", 10),
            bg=NAVY,
            fg="#D9EAF7"
        ).pack()

        tk.Label(
            window,
            text="TOTAL CONSUMPTION",
            font=("Segoe UI", 10, "bold"),
            bg=LIGHT_BG,
            fg=GREY
        ).pack(pady=(25, 2))

        tk.Label(
            window,
            text=f"{total_units} units",
            font=("Segoe UI", 24, "bold"),
            bg=LIGHT_BG,
            fg=TEXT
        ).pack()

        details = tk.Frame(
            window,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground="#D7E0E7"
        )

        details.pack(
            fill="x",
            padx=35,
            pady=20
        )

        tk.Label(
            details,
            text="BILL BREAKDOWN",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=NAVY
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(18, 12)
        )

        def add_row(
            row,
            slab,
            calculation,
            amount
        ):

            tk.Label(
                details,
                text=slab,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=TEXT
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=20,
                pady=7
            )

            tk.Label(
                details,
                text=calculation,
                font=("Segoe UI", 10),
                bg=WHITE,
                fg=GREY
            ).grid(
                row=row,
                column=1,
                sticky="e",
                padx=20,
                pady=7
            )

            tk.Label(
                details,
                text=f"₹{amount:.2f}",
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=TEXT
            ).grid(
                row=row,
                column=2,
                sticky="e",
                padx=20,
                pady=7
            )

        add_row(
            1,
            "Slab 1",
            f"{first_units} × ₹2.50",
            first_charge
        )

        add_row(
            2,
            "Slab 2",
            f"{second_units} × ₹4.00",
            second_charge
        )

        add_row(
            3,
            "Slab 3",
            f"{third_units} × ₹6.00",
            third_charge
        )

        tk.Frame(
            details,
            bg="#D7E0E7",
            height=1
        ).grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=20,
            pady=12
        )

        tk.Label(
            details,
            text="TOTAL BILL",
            font=("Segoe UI", 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=(3, 18)
        )

        tk.Label(
            details,
            text=f"₹{bill:.2f}",
            font=("Segoe UI", 18, "bold"),
            bg=WHITE,
            fg=GREEN
        ).grid(
            row=5,
            column=2,
            sticky="e",
            padx=20,
            pady=(3, 18)
        )

        tk.Label(
            window,
            text="Prototype tariff used for demonstration",
            font=("Segoe UI", 9, "italic"),
            bg=LIGHT_BG,
            fg=GREY
        ).pack(pady=(0, 12))

        tk.Button(
            window,
            text="Close",
            command=window.destroy,
            font=("Segoe UI", 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            relief="flat",
            width=14,
            height=2,
            cursor="hand2"
        ).pack()

    # =========================
    # USAGE ANALYSIS
    # =========================

    def show_usage():

        data = pd.read_csv(
            "meter_data.csv"
        )

        data["units_consumed"] = (
            data["current_reading"]
            - data["previous_reading"]
        )

        window = tk.Toplevel(root)

        window.title(
            "Electricity Usage Analysis"
        )

        window.geometry(
            "850x600"
        )

        window.configure(
            bg=LIGHT_BG
        )

        tk.Label(
            window,
            text="DAILY ELECTRICITY USAGE",
            font=("Segoe UI", 20, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(pady=15)

        figure = plt.Figure(
            figsize=(7.5, 4.5),
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
            master=window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    # =========================
    # APPLIANCE CONSUMPTION
    # =========================

    def show_appliances():

        window = tk.Toplevel(root)

        window.title(
            "Appliance Consumption"
        )

        window.geometry(
            "760x720"
        )

        window.resizable(
            False,
            False
        )

        window.configure(
            bg=LIGHT_BG
        )

        # =========================
        # HEADER
        # =========================

        header = tk.Frame(
            window,
            bg=NAVY,
            height=115
        )

        header.pack(fill="x")
        header.pack_propagate(False)

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
            fill="x"
        )

        table_card.configure(
            height=300
       ) 

        table_card.pack_propagate(False)

        table = tk.Frame(
            table_card,
            bg=WHITE
        )

        table.pack(
            padx=15,
            pady=15,
            fill="both",
            expand=True
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

            # Already sorted by units_consumed
            # from highest to lowest in database.py

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

            # =========================
            # BASIC ANALYSIS
            # =========================

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

            # =========================
            # WASTE DETECTION
            # =========================

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

            # =========================
            # HEADER
            # =========================

            analysis_header = tk.Frame(
                analysis,
                bg=NAVY,
                height=110
            )

            analysis_header.pack(
                fill="x"
            )

            analysis_header.pack_propagate(
                False
            )

            tk.Label(
                analysis_header,
                text="📊 APPLIANCE ANALYSIS",
                font=("Segoe UI", 22, "bold"),
                bg=NAVY,
                fg=WHITE
            ).pack(
                pady=(22, 4)
            )

            tk.Label(
                analysis_header,
                text="Consumption comparison and usage insights",
                font=("Segoe UI", 10),
                bg=NAVY,
                fg="#D9EAF7"
            ).pack()

            # =========================
            # SUMMARY
            # =========================

            cards = tk.Frame(
                analysis,
                bg=LIGHT_BG
            )

            cards.pack(
                pady=18
            )

            def create_analysis_card(
                title,
                value,
                subtitle,
                column
            ):

                card = tk.Frame(
                    cards,
                    bg=WHITE,
                    width=230,
                    height=105,
                    highlightthickness=1,
                    highlightbackground="#D7E0E7"
                )

                card.grid(
                    row=0,
                    column=column,
                    padx=7
                )

                card.grid_propagate(
                    False
                )

                tk.Label(
                    card,
                    text=title,
                    font=("Segoe UI", 10, "bold"),
                    bg=WHITE,
                    fg=GREY
                ).pack(
                    pady=(13, 3)
                )

                tk.Label(
                    card,
                    text=value,
                    font=("Segoe UI", 16, "bold"),
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

            create_analysis_card(
                "TOTAL CONSUMPTION",
                f"{total_consumption:.2f} units",
                "Estimated per day",
                0
            )

            create_analysis_card(
                "HIGHEST CONSUMER",
                highest[0],
                f"{highest[3]:.2f} units/day",
                1
            )

            create_analysis_card(
                "LOWEST CONSUMER",
                lowest[0],
                f"{lowest[3]:.2f} units/day",
                2
            )

            # =========================
            # COST
            # =========================

            tk.Label(
                analysis,
                text=f"Estimated total appliance cost: "
                     f"₹{total_cost:.2f} / day",
                font=("Segoe UI", 11, "bold"),
                bg=LIGHT_BG,
                fg=NAVY
            ).pack(
                pady=(0, 8)
            )

            # =========================
            # HIGH USAGE ALERT
            # =========================

            alert_card = tk.Frame(
                analysis,
                bg=WHITE,
                highlightthickness=1,
                highlightbackground="#D7E0E7"
            )

            alert_card.pack(
                fill="x",
                padx=35,
                pady=(0, 12)
            )

            if waste_alerts:

                tk.Label(
                    alert_card,
                    text="⚠ HIGH-USAGE ALERT",
                    font=("Segoe UI", 12, "bold"),
                    bg=WHITE,
                    fg="#C62828"
                ).pack(
                    anchor="w",
                    padx=18,
                    pady=(12, 5)
                )

                for alert in waste_alerts:

                    tk.Label(
                        alert_card,
                        text="• " + alert,
                        font=("Segoe UI", 10),
                        bg=WHITE,
                        fg=TEXT,
                        wraplength=720,
                        justify="left"
                    ).pack(
                        anchor="w",
                        padx=18,
                        pady=3
                    )

            else:

                tk.Label(
                    alert_card,
                    text="✓ No high-usage appliances detected",
                    font=("Segoe UI", 11, "bold"),
                    bg=WHITE,
                    fg="#2E7D32"
                ).pack(
                    padx=18,
                    pady=15
                )

            # =========================
            # ENERGY SAVING SUGGESTIONS
            # =========================

            suggestion_card = tk.Frame(
                analysis,
                bg=WHITE,
                highlightthickness=1,
                highlightbackground="#D7E0E7"
            )

            suggestion_card.pack(
                fill="x",
                padx=35,
                pady=(0, 12)
            )

            tk.Label(
                suggestion_card,
                text="💡 ENERGY-SAVING SUGGESTIONS",
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
                        wraplength=720,
                        justify="left"
                    ).pack(
                        anchor="w",
                        padx=18,
                        pady=3
                    )

            else:

                tk.Label(
                    suggestion_card,
                    text="✓ No specific energy-saving suggestions at this time.",
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

            figure = plt.Figure(
                figsize=(8, 2.8),
                dpi=100
            )

            axis = figure.add_subplot(111)

            names = [
                appliance[0]
                for appliance in appliances
            ]

            units = [
                appliance[3]
                for appliance in appliances
            ]

            axis.bar(
                names,
                units
            )

            axis.set_title(
                "Appliance Consumption Comparison"
            )

            axis.set_xlabel(
                "Appliance"
            )

            axis.set_ylabel(
                "Units per Day"
            )

            axis.tick_params(
                axis="x",
                rotation=30
            )

            figure.tight_layout()

            canvas = FigureCanvasTkAgg(
                figure,
                master=analysis
            )

            canvas.draw()

            canvas.get_tk_widget().pack(
                fill="x",
                padx=25,
                pady=8
            )

            # =========================
            # CLOSE
            # =========================

            tk.Button(
                analysis,
                text="Close",
                command=analysis.destroy,
                font=("Segoe UI", 10, "bold"),
                bg=NAVY,
                fg=WHITE,
                relief="flat",
                width=15,
                height=2,
                cursor="hand2"
            ).pack(
                pady=(0, 12)
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
            command=window.destroy,
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
    # DASHBOARD BUTTONS
    # =========================

    buttons = tk.Frame(
        root,
        bg=LIGHT_BG
    )

    buttons.pack(
        pady=10
    )

    def create_button(
        text,
        command,
        colour
    ):

        return tk.Button(
            buttons,
            text=text,
            command=command,
            width=18,
            height=2,
            font=("Segoe UI", 10, "bold"),
            bg=colour,
            fg=WHITE,
            activebackground=colour,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2"
        )

    # ROW 1

    create_button(
        "💰 Bill Breakdown",
        show_bill,
        BLUE
    ).grid(
        row=0,
        column=0,
        padx=6,
        pady=5
    )

    create_button(
        "📊 Usage Analysis",
        show_usage,
        TEAL
    ).grid(
        row=0,
        column=1,
        padx=6,
        pady=5
    )

    create_button(
        "💡 Energy Saving",
        energy_saving,
        GREEN
    ).grid(
        row=0,
        column=2,
        padx=6,
        pady=5
    )

    create_button(
        "👤 User Profile",
        user_profile,
        NAVY
    ).grid(
        row=0,
        column=3,
        padx=6,
        pady=5
    )

    # ROW 2

    create_button(
        "⚡ Appliance Consumption",
        show_appliances,
        ORANGE
    ).grid(
        row=1,
        column=1,
        columnspan=2,
        padx=6,
        pady=5
    )

    # GENERATE REPORT
    create_button(
        "📄 Generate Report",
        generate_report,
        NAVY
    ).grid(
        row=2,
        column=1,
        columnspan=2,
        padx=6,
        pady=5
    )

    # NOTIFICATIONS
    create_button(
        "🔔 Usage Alert",
        lambda: show_notification(
        average_usage,
        highest_usage
    ),
    ORANGE
    ).grid(
        row=3,
        column=1,
        columnspan=2,
        padx=6,
        pady=5
   )
    # =========================
    # EXIT
    # =========================

    tk.Button(
        root,
        text="Exit Application",
        command=root.destroy,
        font=("Segoe UI", 10),
        bg=LIGHT_BG,
        fg=GREY,
        relief="flat",
        cursor="hand2"
    ).pack(
        pady=5
    )

    # =========================
    # FOOTER
    # =========================

    tk.Label(
        root,
        text="Smart Energy Management  •  Python Desktop Application",
        font=("Segoe UI", 9),
        bg=LIGHT_BG,
        fg=GREY
    ).pack(
        side="bottom",
        pady=5
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