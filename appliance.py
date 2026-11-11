import tkinter as tk
from tkinter import messagebox

from database import save_appliance


# =========================
# TYPICAL APPLIANCE POWER
# =========================

APPLIANCE_POWER = {
    "Fan": 75,
    "LED Bulb": 9,
    "TV": 100,
    "Refrigerator": 150,
    "Laptop": 65,
    "Washing Machine": 500,
    "AC": 1500,
    "Iron Box": 1000,
    "Microwave Oven": 1200,
    "Water Heater": 2000
}


# =========================
# CALCULATE CONSUMPTION
# =========================

def calculate_appliance_consumption(wattage, hours):

    return (wattage * hours) / 1000


# =========================
# ADD APPLIANCE WINDOW
# =========================

def add_appliance_window(parent, refresh_function):

    window = tk.Toplevel(parent)

    window.title("Add Appliance")
    window.geometry("520x650")
    window.resizable(False, False)
    window.configure(bg="#F3F7FA")

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg="#102A43",
        height=110
    )

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="⚡ ADD APPLIANCE",
        font=("Segoe UI", 22, "bold"),
        bg="#102A43",
        fg="white"
    ).pack(pady=(25, 3))

    tk.Label(
        header,
        text="Select appliance and enter usage details",
        font=("Segoe UI", 10),
        bg="#102A43",
        fg="#D9EAF7"
    ).pack()

    # =========================
    # CARD
    # =========================

    card = tk.Frame(
        window,
        bg="white"
    )

    card.pack(
        padx=50,
        pady=20,
        fill="both",
        expand=True
    )

    # =========================
    # SELECT APPLIANCE
    # =========================

    tk.Label(
        card,
        text="Select Appliance",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#263238"
    ).pack(pady=(20, 5))

    appliance_var = tk.StringVar()

    appliance_list = list(APPLIANCE_POWER.keys()) + ["Other"]

    appliance_menu = tk.OptionMenu(
        card,
        appliance_var,
        *appliance_list
    )

    appliance_menu.config(
        font=("Segoe UI", 11),
        width=24
    )

    appliance_menu.pack()

    # =========================
    # CUSTOM NAME
    # =========================

    custom_name_label = tk.Label(
        card,
        text="Enter Appliance Name",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#263238"
    )

    custom_name_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=25
    )

    # =========================
    # POWER
    # =========================

    tk.Label(
        card,
        text="Power Rating",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#263238"
    ).pack(pady=(18, 5))

    power_label = tk.Label(
        card,
        text="Select an appliance",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#1976D2"
    )

    power_label.pack()

    custom_power_label = tk.Label(
        card,
        text="Enter Power Rating (W)",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg="#263238"
    )

    custom_power_entry = tk.Entry(
        card,
        font=("Segoe UI", 11),
        width=25
    )

    # =========================
    # UPDATE FIELDS
    # =========================

    def update_power(*args):

        appliance = appliance_var.get()

        if appliance == "Other":

            power_label.config(
                text="Enter your appliance power"
            )

            custom_name_label.pack(
                before=power_label,
                pady=(15, 5)
            )

            custom_name_entry.pack(
                before=power_label
            )

            custom_power_label.pack(
                pady=(12, 5)
            )

            custom_power_entry.pack()

        elif appliance:

            power = APPLIANCE_POWER[appliance]

            power_label.config(
                text=f"{power} W"
            )

            custom_name_label.pack_forget()
            custom_name_entry.pack_forget()
            custom_power_label.pack_forget()
            custom_power_entry.pack_forget()

    appliance_var.trace_add(
        "write",
        update_power
    )

    # =========================
    # USAGE HOURS
    # =========================

    tk.Label(
        card,
        text="Usage Hours per Day",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#263238"
    ).pack(pady=(18, 5))

    hours_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        width=25
    )

    hours_entry.pack()

    # =========================
    # SAVE
    # =========================

    def save():

        selected = appliance_var.get()

        if not selected:

            messagebox.showwarning(
                "Missing Information",
                "Please select an appliance."
            )

            return

        # =========================
        # CUSTOM APPLIANCE
        # =========================

        if selected == "Other":

            appliance = custom_name_entry.get().strip()

            if not appliance:

                messagebox.showwarning(
                    "Missing Name",
                    "Please enter the appliance name."
                )

                return

            try:

                wattage = float(
                    custom_power_entry.get()
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid Power",
                    "Please enter a valid power rating."
                )

                return

            if wattage <= 0:

                messagebox.showwarning(
                    "Invalid Power",
                    "Power rating must be greater than 0."
                )

                return

        # =========================
        # PREDEFINED APPLIANCE
        # =========================

        else:

            appliance = selected
            wattage = APPLIANCE_POWER[selected]

        # =========================
        # HOURS
        # =========================

        try:

            hours = float(
                hours_entry.get()
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Hours",
                "Please enter a valid number of hours."
            )

            return

        if hours <= 0:

            messagebox.showwarning(
                "Invalid Hours",
                "Usage hours must be greater than 0."
            )

            return

        if hours > 24:

            messagebox.showwarning(
                "Invalid Hours",
                "Usage hours cannot be more than 24."
            )

            return

        # =========================
        # CALCULATE
        # =========================

        units = calculate_appliance_consumption(
            wattage,
            hours
        )

        rate = 2.5

        cost = units * rate

        # =========================
        # SAVE
        # =========================

        save_appliance(
            appliance,
            wattage,
            hours,
            units,
            cost
        )

        messagebox.showinfo(
            "Appliance Added",
            f"{appliance} added successfully!\n\n"
            f"Power: {wattage:g} W\n"
            f"Usage: {hours:g} hours/day\n"
            f"Estimated consumption: {units:.2f} units/day\n"
            f"Estimated cost: ₹{cost:.2f}/day"
        )

        window.destroy()

        refresh_function()

    # =========================
    # SAVE BUTTON
    # =========================

    tk.Button(
        card,
        text="SAVE APPLIANCE",
        command=save,
        font=("Segoe UI", 11, "bold"),
        bg="#00897B",
        fg="white",
        relief="flat",
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=22)

    # =========================
    # NOTE
    # =========================

    tk.Label(
        card,
        text="Common appliances use typical power values.\n"
             "For Other, enter the appliance name and rated wattage.",
        font=("Segoe UI", 8, "italic"),
        bg="white",
        fg="#607D8B"
    ).pack()