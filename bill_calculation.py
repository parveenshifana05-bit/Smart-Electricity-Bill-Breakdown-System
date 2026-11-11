def calculate_bill(total_units):

    # Prototype tariff rates
    first_slab = min(total_units, 100)
    second_slab = min(max(total_units - 100, 0), 100)
    third_slab = max(total_units - 200, 0)

    first_charge = first_slab * 2.5
    second_charge = second_slab * 4
    third_charge = third_slab * 6

    total_bill = first_charge + second_charge + third_charge

    return total_bill


def get_bill_breakdown(total_units):

    first_slab = min(total_units, 100)
    second_slab = min(max(total_units - 100, 0), 100)
    third_slab = max(total_units - 200, 0)

    first_charge = first_slab * 2.5
    second_charge = second_slab * 4
    third_charge = third_slab * 6

    return (
        first_slab,
        first_charge,
        second_slab,
        second_charge,
        third_slab,
        third_charge
    )