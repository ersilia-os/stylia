def mm_to_inch(x):
    return x * 0.0393701


def to_one_column(width):
    return width * 89 / 183  # Nature two:one column ratio


SUPPORT_TWO_COLUMN_LIMITS = {
    "paper": (mm_to_inch(183), mm_to_inch(275)),  # Nature
    "slide": (10, 5.625),  # Standard slide
    "widescreen": (13.3, 7.5),  # Widescreen
    "poster": (mm_to_inch(420), mm_to_inch(594)),  # A2
}
