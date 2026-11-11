from csv_import import read_meter_data
from database import create_database, save_meter_data, save_bill
from bill_calculation import calculate_bill
from analytics import calculate_analytics
from dashboard import show_profile_page


# =========================
# CREATE DATABASE
# =========================

create_database()


# =========================
# READ METER DATA
# =========================

data = read_meter_data("meter_data.csv")


# =========================
# SAVE METER DATA
# =========================

save_meter_data(data)


# =========================
# ANALYZE USAGE
# =========================

total_units, average_usage, highest_usage, lowest_usage = calculate_analytics(data)


# =========================
# CALCULATE BILL
# =========================

bill = calculate_bill(total_units)


# =========================
# SAVE BILL
# =========================

bill_date = data["date"].max()

save_bill(
    bill_date,
    total_units,
    bill
)


# =========================
# DISPLAY BILL DETAILS
# =========================

print("\n--- Bill Details ---")
print("Total Units Consumed:", total_units)
print("Estimated Electricity Bill: ₹", bill)


# =========================
# OPEN USER PROFILE FIRST
# =========================

show_profile_page(
    total_units,
    average_usage,
    highest_usage,
    lowest_usage,
    bill
)