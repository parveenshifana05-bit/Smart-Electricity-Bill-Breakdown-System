import sqlite3


DB_NAME = "electricity.db"


# =========================
# CREATE DATABASE TABLES
# =========================
def create_database():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # 1. Users / household information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            room_no TEXT NOT NULL
        )
    """)

    # 2. Meter readings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meter_readings (
            reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            previous_reading REAL,
            current_reading REAL,
            units_consumed REAL
        )
    """)

    # 3. Tariff plans
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tariff_plans (
            tariff_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slab TEXT UNIQUE,
            units_from INTEGER,
            units_to INTEGER,
            rate REAL
        )
    """)

    # 4. Bills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_date TEXT,
            total_units REAL,
            amount REAL
        )
    """)

    # 5. User profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            room_no TEXT
        )
    """)

    # 6. Appliances
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appliances (
            appliance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            wattage REAL,
            usage_hours REAL,
            units_consumed REAL,
            estimated_cost REAL
        )
    """)

    # Insert prototype tariff values
    cursor.execute("""
        INSERT OR IGNORE INTO tariff_plans
        (slab, units_from, units_to, rate)
        VALUES ('Slab 1', 1, 100, 2.5)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO tariff_plans
        (slab, units_from, units_to, rate)
        VALUES ('Slab 2', 101, 200, 4.0)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO tariff_plans
        (slab, units_from, units_to, rate)
        VALUES ('Slab 3', 201, 999999, 6.0)
    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully.")


# =========================
# SAVE METER DATA
# =========================
def save_meter_data(data):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for _, row in data.iterrows():

        existing = cursor.execute(
            """
            SELECT 1
            FROM meter_readings
            WHERE date = ?
            """,
            (row["date"],)
        ).fetchone()

        if not existing:

            cursor.execute(
                """
                INSERT INTO meter_readings
                (
                    date,
                    previous_reading,
                    current_reading,
                    units_consumed
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    row["date"],
                    row["previous_reading"],
                    row["current_reading"],
                    row["units_consumed"]
                )
            )

    connection.commit()
    connection.close()


# =========================
# SAVE BILL
# =========================
def save_bill(bill_date, total_units, amount):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bills
        (bill_date, total_units, amount)
        VALUES (?, ?, ?)
        """,
        (bill_date, total_units, amount)
    )

    connection.commit()
    connection.close()


# =========================
# GET TARIFF PLANS
# =========================
def get_tariff_plans():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    plans = cursor.execute(
        """
        SELECT slab, units_from, units_to, rate
        FROM tariff_plans
        ORDER BY tariff_id
        """
    ).fetchall()

    connection.close()

    return plans


# =========================
# SAVE APPLIANCE
# =========================
def save_appliance(
    name,
    wattage,
    usage_hours,
    units_consumed,
    estimated_cost
):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO appliances
        (
            name,
            wattage,
            usage_hours,
            units_consumed,
            estimated_cost
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            wattage,
            usage_hours,
            units_consumed,
            estimated_cost
        )
    )

    connection.commit()
    connection.close()


# =========================
# GET APPLIANCES
# =========================
def get_appliances():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    appliances = cursor.execute(
        """
        SELECT name, wattage, usage_hours,
               units_consumed, estimated_cost
        FROM appliances
        ORDER BY units_consumed DESC
        """
    ).fetchall()

    connection.close()

    return appliances

# =========================
# DELETE APPLIANCE
# =========================


def delete_appliance(name, usage_hours):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM appliances
        WHERE appliance_id = (
            SELECT appliance_id
            FROM appliances
            WHERE name = ?
            AND usage_hours = ?
            ORDER BY appliance_id
            LIMIT 1
        )
        """,
        (name, usage_hours)
    )

    connection.commit()
    connection.close()

# =========================
# UPDATE APPLIANCE
# =========================

def update_appliance(name, old_hours, new_hours):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Get the appliance's power
    appliance = cursor.execute(
        """
        SELECT appliance_id, wattage
        FROM appliances
        WHERE name = ?
        AND usage_hours = ?
        ORDER BY appliance_id
        LIMIT 1
        """,
        (name, old_hours)
    ).fetchone()

    if appliance:

        appliance_id = appliance[0]
        wattage = appliance[1]

        # Recalculate consumption
        units = (wattage * new_hours) / 1000

        # Prototype tariff
        cost = units * 2.5

        cursor.execute(
            """
            UPDATE appliances
            SET usage_hours = ?,
                units_consumed = ?,
                estimated_cost = ?
            WHERE appliance_id = ?
            """,
            (
                new_hours,
                units,
                cost,
                appliance_id
            )
        )

    connection.commit()
    connection.close()