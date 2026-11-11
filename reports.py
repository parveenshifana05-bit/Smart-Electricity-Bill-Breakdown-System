import os
import sqlite3
from tkinter import messagebox


def generate_report():

    connection = sqlite3.connect("electricity.db")
    cursor = connection.cursor()

    bill = cursor.execute("""
        SELECT total_units, amount
        FROM bills
        ORDER BY bill_id DESC
        LIMIT 1
    """).fetchone()

    appliances = cursor.execute("""
        SELECT name, wattage, usage_hours,
               units_consumed, estimated_cost
        FROM appliances
    """).fetchall()

    connection.close()

    if not bill:
        messagebox.showwarning(
            "Report",
            "No bill data available."
        )
        return

    total_units = bill[0]
    amount = bill[1]

    os.makedirs("Reports", exist_ok=True)

    filename = os.path.join(
        "Reports",
        "electricity_report.txt"
    )

    with open(filename, "w", encoding="utf-8") as file:

        file.write("=" * 50 + "\n")
        file.write("       SMART ELECTRICITY REPORT\n")
        file.write("=" * 50 + "\n\n")

        file.write("BILL DETAILS\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Units Consumed : {total_units}\n")
        file.write(f"Estimated Bill       : Rs.{amount:.2f}\n\n")

        file.write("APPLIANCE CONSUMPTION\n")
        file.write("-" * 50 + "\n")

        if appliances:

            for appliance in appliances:

                name, wattage, hours, units, cost = appliance

                file.write(
                    f"{name} | "
                    f"{wattage:.0f} W | "
                    f"{hours:.1f} hrs/day | "
                    f"{units:.2f} units/day | "
                    f"Rs.{cost:.2f}\n"
                )

        else:
            file.write("No appliance data available.\n")

        file.write("\n")
        file.write("ENERGY SAVING SUGGESTIONS\n")
        file.write("-" * 50 + "\n")
        file.write(
            "• Switch off appliances when not required.\n"
        )
        file.write(
            "• Avoid unnecessary standby power.\n"
        )
        file.write(
            "• Monitor high-consuming appliances.\n"
        )
        file.write(
            "• Prefer energy-efficient appliances.\n"
        )

        file.write("\n")
        file.write("=" * 50 + "\n")
        file.write("          End of Electricity Report\n")
        file.write("=" * 50 + "\n")

    messagebox.showinfo(
        "Report Generated",
        "Electricity report generated successfully!\n\n"
        "Check the 'Reports' folder."
    )