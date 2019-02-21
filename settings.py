TRIANGLE_SIZE = 0.1
GRID_WIDTH = 27
SIZE = 26
GRID_SIZE_X, GRID_SIZE_Y = SIZE, SIZE

LOOP_DELAY = 16


class ManagementMessage:
    PING = 0


class Action:
    SUCK = "suck"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    NOOP = "noop"

    COST_MAP = {
        SUCK: 2,
        LEFT: 1,
        RIGHT: 1,
        UP: 1,
        DOWN: 1,
        NOOP: 0,
    }


class Shape:
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


# test_color = colorsys.hsv_to_rgb(359,100,100)
colors = {
    "aqua": "#00ffff",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "blue": "#0000ff",
    "brown": "#a52a2a",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkviolet": "#9400d3",
    "fuchsia": "#ff00ff",
    "gold": "#ffd700",
    "green": "#008000",
    "indigo": "#4b0082",
    "khaki": "#f0e68c",
    "lightblue": "#add8e6",
    "lightcyan": "#e0ffff",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "navy": "#000080",
    "olive": "#808000",
    "orange": "#ffa500",
    "pink": "#ffc0cb",
    "purple": "#800080",
    "violet": "#800080",
    "red": "#ff0000",
    "silver": "#c0c0c0",
    "yellow": "#ffff00",
}
