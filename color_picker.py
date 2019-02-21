from random import choice


class ColorChoice:

    def __init__(self, colors: list) -> None:
        self.colors: dict = [self.parse_color(value) for value in colors]
        self.orthogonal_colors: list = []

    @staticmethod
    def parse_color(color: str) -> tuple:
        color = color.replace("#", "")
        r, g, b = [int(color[i * 2:i * 2 + 2], base=16) for i in range(3)]
        return r, g, b

    @staticmethod
    def distance(a: tuple, b: tuple):
        return sum(abs(x - y) for x, y in zip(a, b))

    def get(self):
        if not self.orthogonal_colors:
            color = choice(list(self.colors))
        else:
            max_score, max_value = -1, None
            for value in self.colors:
                score = min(self.distance(value, taken_value) for taken_value in self.orthogonal_colors)
                if score > max_score:
                    max_score = score
                    max_value = value
            color = max_value

        self.orthogonal_colors.append(color)
        return color


if __name__ == '__main__':
    import settings

    color_picker = ColorChoice(list(settings.colors.values()))

    for i in range(10):
        print(color_picker.get())
