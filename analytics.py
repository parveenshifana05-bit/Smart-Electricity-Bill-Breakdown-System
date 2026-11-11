def calculate_analytics(data):

    total_units = data["units_consumed"].sum()

    average_usage = data["units_consumed"].mean()

    highest_usage = data["units_consumed"].max()

    lowest_usage = data["units_consumed"].min()

    print("\n--- Electricity Usage Analysis ---")
    print("Total Units:", total_units)
    print("Average Daily Usage:", round(average_usage, 2))
    print("Highest Daily Usage:", highest_usage)
    print("Lowest Daily Usage:", lowest_usage)

    return total_units, average_usage, highest_usage, lowest_usage