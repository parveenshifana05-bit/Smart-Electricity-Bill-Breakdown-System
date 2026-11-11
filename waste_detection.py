# =========================
# WASTE / HIGH-USAGE DETECTION
# =========================

def detect_waste(appliances):

    alerts = []

    for appliance in appliances:

        name = appliance[0]
        hours = appliance[2]
        units = appliance[3]

        # High usage condition
        if hours > 8:

            alerts.append(
                f"{name} is being used for "
                f"{hours:.1f} hours/day "
                f"({units:.2f} units/day)."
            )

    return alerts

# =========================
# ENERGY SAVING SUGGESTIONS
# =========================

def generate_suggestions(appliances):

    suggestions = []

    for appliance in appliances:

        name = appliance[0]
        hours = appliance[2]
        units = appliance[3]

        if hours > 8:

            if name.lower() == "refrigerator":

                suggestions.append(
                    f"{name}: Check temperature settings, "
                    f"door-opening frequency and energy efficiency."
                )

            elif name.lower() in ["fan", "tv", "laptop"]:

                suggestions.append(
                    f"{name}: Reduce unnecessary usage "
                    f"and switch it off when not required."
                )

            elif name.lower() == "ac":

                suggestions.append(
                    f"{name}: Reduce unnecessary operating time "
                    f"and use an energy-efficient temperature setting."
                )

            else:

                suggestions.append(
                    f"{name}: Consider reducing usage time "
                    f"when the appliance is not required."
                )

    return suggestions

def detect_appliance_waste(appliances):

    warnings = []

    for appliance in appliances:

        name = appliance[0]
        hours = appliance[2]
        units = appliance[3]

        if hours >= 8:
            warnings.append(
                f"{name}: high usage of {hours:g} hours/day "
                f"({units:.2f} units/day)"
            )

    return warnings


def get_highest_consumer(appliances):

    if not appliances:
        return None 

    return max(
        appliances,
        key=lambda appliance: appliance[3]
    )