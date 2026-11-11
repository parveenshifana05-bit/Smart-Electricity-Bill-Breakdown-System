import tkinter as tk
from tkinter import messagebox


def show_notification(average_usage, highest_usage):

    if highest_usage > 12:

        messagebox.showwarning(
            "⚠ High Usage Alert",
            f"High electricity usage detected!\n\n"
            f"Peak usage: {highest_usage} units/day\n"
            f"Average usage: {average_usage:.1f} units/day\n\n"
            "Please monitor your electricity consumption."
        )

    elif average_usage > 8:

        messagebox.showinfo(
            "Electricity Usage Notice",
            f"Average daily usage is {average_usage:.1f} units.\n\n"
            "Consider reducing unnecessary electricity usage."
        )

    else:

        messagebox.showinfo(
            "Electricity Usage",
            "Electricity usage is within the normal range."
        )


def generate_notification(average_usage, highest_usage):

    if highest_usage > 12:
        return "⚠ High electricity usage detected."

    if average_usage > 8:
        return "Notice: Average daily consumption is relatively high."

    return "✓ Electricity usage is being monitored normally."