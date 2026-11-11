import pandas as pd


def read_meter_data(filename):

    data = pd.read_csv(filename)

    # Check required columns
    required_columns = [
        "date",
        "previous_reading",
        "current_reading"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing column: {column}")

    # Convert readings to numbers
    data["previous_reading"] = pd.to_numeric(
        data["previous_reading"],
        errors="coerce"
    )

    data["current_reading"] = pd.to_numeric(
        data["current_reading"],
        errors="coerce"
    )

    # Remove invalid readings
    data = data.dropna(
        subset=["previous_reading", "current_reading"]
    )

    # Check current reading is not less than previous reading
    data = data[
        data["current_reading"] >= data["previous_reading"]
    ]

    # Calculate units consumed
    data["units_consumed"] = (
        data["current_reading"] - data["previous_reading"]
    )

    print("CSV data validated successfully.")
    print(data)

    return data