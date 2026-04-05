"""
Monk Scale → Colour Palette data.

Each tone has three lists:
  - flattering: colours that complement this skin tone
  - neutrals:   safe anchors (always allowed)
  - avoid:      colours that clash or wash out
"""

MONK_SCALE_PALETTES = {
    1: {  # Very Fair / Porcelain
        "flattering": ["soft pastels", "navy", "dusty rose", "lavender", "sage"],
        "flattering_hex": ["#f9c6d0", "#001f5b", "#c4a5a5", "#c2b0d4", "#b2c2b0"],
        "neutrals": ["ivory", "soft white", "light grey"],
        "neutrals_hex": ["#fffff0", "#f8f8f8", "#d3d3d3"],
        "avoid": ["neon yellow", "harsh orange"],
        "avoid_hex": ["#ffff00", "#ff6600"],
    },
    2: {  # Fair
        "flattering": ["jewel tones", "teal", "burgundy", "blush", "forest green"],
        "flattering_hex": ["#5b2d8e", "#008080", "#800020", "#ffb6c1", "#228b22"],
        "neutrals": ["off-white", "cream", "silver"],
        "neutrals_hex": ["#faf0e6", "#fffdd0", "#c0c0c0"],
        "avoid": ["washed-out pastels"],
        "avoid_hex": ["#e0e0e0"],
    },
    3: {  # Light-Medium
        "flattering": ["terracotta", "olive", "coral", "mustard", "rust"],
        "flattering_hex": ["#c66b3d", "#808000", "#ff6b6b", "#e1ad01", "#b7410e"],
        "neutrals": ["warm beige", "camel", "gold"],
        "neutrals_hex": ["#f5f0e8", "#c19a6b", "#ffd700"],
        "avoid": ["cool greys", "icy blues"],
        "avoid_hex": ["#808080", "#add8e6"],
    },
    4: {  # Medium / Warm Beige
        "flattering": ["earthy tones", "burnt orange", "warm brown", "cobalt"],
        "flattering_hex": ["#c4a882", "#cc5500", "#8b4513", "#0047ab"],
        "neutrals": ["tan", "warm white", "bronze"],
        "neutrals_hex": ["#d2b48c", "#fdf5e6", "#cd7f32"],
        "avoid": ["pastel pink", "neon"],
        "avoid_hex": ["#ffb6c1", "#39ff14"],
    },
    5: {  # Medium-Deep / Olive
        "flattering": ["emerald", "deep plum", "amber", "cobalt"],
        "flattering_hex": ["#50c878", "#673147", "#ffbf00", "#0047ab"],
        "neutrals": ["warm grey", "khaki", "gold"],
        "neutrals_hex": ["#a9a9a9", "#c3b091", "#ffd700"],
        "avoid": ["light beige"],
        "avoid_hex": ["#f5f5dc"],
    },
    6: {  # Deep / Brown
        "flattering": ["royal blue", "fuchsia", "bright white", "orange"],
        "flattering_hex": ["#4169e1", "#ff00ff", "#ffffff", "#ff8c00"],
        "neutrals": ["bright white", "charcoal", "black"],
        "neutrals_hex": ["#ffffff", "#36454f", "#000000"],
        "avoid": ["dusty muted tones"],
        "avoid_hex": ["#bcb4a4"],
    },
    7: {  # Very Deep / Ebony
        "flattering": ["electric blue", "hot pink", "white", "gold"],
        "flattering_hex": ["#7b00d4", "#ff69b4", "#ffffff", "#ffd700"],
        "neutrals": ["pure white", "jet black", "gold"],
        "neutrals_hex": ["#ffffff", "#000000", "#ffd700"],
        "avoid": ["dark browns"],
        "avoid_hex": ["#3d1c02"],
    },
}

# Colour wheel — complementary & analogous helpers (colour family strings)
COLOUR_WHEEL_GROUPS = [
    ["red", "crimson", "scarlet", "maroon", "wine", "ruby"],
    ["orange", "burnt orange", "rust", "terracotta", "coral", "peach", "amber"],
    ["yellow", "mustard", "gold", "lemon"],
    ["green", "olive", "sage", "forest green", "emerald", "khaki"],
    ["blue", "navy", "cobalt", "royal blue", "electric blue", "teal", "sky blue", "icy blue"],
    ["violet", "purple", "lavender", "plum", "deep plum", "lilac"],
    ["pink", "blush", "dusty rose", "hot pink", "fuchsia", "rose"],
]

NEUTRAL_COLOURS = [
    "white", "bright white", "pure white", "soft white", "ivory", "off-white", "cream",
    "black", "jet black", "charcoal",
    "grey", "light grey", "warm grey", "silver",
    "beige", "warm beige", "camel", "tan", "light beige",
]

NEUTRAL_HEX_RANGES = {
    # ranges: (R_min, R_max, G_min, G_max, B_min, B_max, max_saturation)
    "white_range": (220, 255, 220, 255, 220, 255),
    "black_range": (0, 35, 0, 35, 0, 35),
    "grey_range": None,  # handled by saturation check
}

# Occasions
OCCASIONS = ["casual", "formal", "party", "sport", "ethnic_festive"]

# Occasion → accepted formality levels
OCCASION_FORMALITY = {
    "casual": (1, 2),
    "sport": (1, 2),
    "ethnic_festive": (2, 4),
    "party": (3, 4),
    "formal": (4, 5),
}

# Style personas
STYLE_PERSONAS = [
    "Ethnic Traditional",
    "Minimalist",
    "Casual Chic",
    "Boho",
    "Streetwear",
    "Smart Formal",
]

# Persona → expected item types (strongest signals)
PERSONA_ITEM_TYPES = {
    "Ethnic Traditional": ["kurta", "churidar", "palazzos", "dupatta", "juttis", "salwar"],
    "Minimalist": ["shirt", "blouse", "trousers", "loafers", "flats", "belt"],
    "Casual Chic": ["blouse", "jeans", "t-shirt", "sneakers", "flats"],
    "Boho": ["printed top", "maxi skirt", "flowy dress", "boots", "scarf"],
    "Streetwear": ["hoodie", "joggers", "sneakers", "graphic tee", "cap"],
    "Smart Formal": ["blazer", "formal shirt", "trousers", "dress shoes", "heels"],
}

# Persona → expected formality range (min, max)
PERSONA_FORMALITY = {
    "Ethnic Traditional": (2, 4),
    "Minimalist": (2, 4),
    "Casual Chic": (2, 3),
    "Boho": (1, 3),
    "Streetwear": (1, 2),
    "Smart Formal": (4, 5),
}

# Pattern → visual weight
PATTERN_WEIGHT = {
    "solid": 1,
    "striped": 2,
    "checked": 2,
    "printed": 3,
    "embroidered": 3,
    "graphic": 3,
}
