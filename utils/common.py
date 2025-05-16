#calculate no_of_leave based on condition
def point_down_round(value):
    whole = int(value)
    decimal = value - whole

    if decimal < 0.5:
        return whole
    elif 0.5 <= decimal or decimal <= 0.9:
        return whole + 0.5