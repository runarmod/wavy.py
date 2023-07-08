import pathlib
import random
from b_spline import generate_estimated_coords


class Wavy:
    def __init__(
        self,
        width: int = 1920,
        height: int = 1080,
        color: str = "78fa67",
        start: float = 0.4,
        wonkyness: int = 4,
        points: int = 5,
        resolution: int = 100,
        only_include: set = None,
    ):
        self.set_width(width)
        self.set_height(height)
        self.set_color(color)
        self.set_start(start)
        self.set_wonkyness(wonkyness)
        self.set_points(points)
        self.set_resolution(resolution)
        self.only_include = set() if only_include is None else only_include
        self.base = pathlib.Path("base.svg").read_text()

    def set_width(self, width: int) -> None:
        if width <= 0:
            raise ValueError("Width must be positive")
        self.width = width

    def set_height(self, height: int) -> None:
        if height <= 0:
            raise ValueError("Height must be positive")
        self.height = height

    def set_color(self, color: str) -> None:
        if len(color) == 3:
            color = "".join(c * 2 for c in color)
        if len(color) != 6 or any(c not in "0123456789abcdef" for c in color):
            raise ValueError("Color must be in hex format without #")
        self.color = color

    def set_start(self, start: float) -> None:
        if start < 0 or start > 1:
            raise ValueError("Start must be between 0 and 1")
        self.startY = start

    def set_wonkyness(self, wonkyness: int) -> None:
        if wonkyness <= 0:
            raise ValueError("Wonkyness must be positive")
        self.wonkyness = wonkyness

    def set_points(self, points: int) -> None:
        if points <= 0:
            raise ValueError("Points must be positive")
        if points > self.width:
            raise ValueError("Points must be less than width")
        self.points = points

    def set_resolution(self, resolution: int) -> None:
        if resolution <= 0:
            raise ValueError("Resolution must be positive")
        if resolution > self.width:
            raise ValueError("Resolution must be less than width")
        self.resolution = resolution

    def generate_y(self) -> float:
        return (random.random() - 0.5) * 0.05 * self.wonkyness + self.startY

    def generate_coords(self) -> list[tuple[float, float]]:
        coords = []
        for i in range(self.points):
            point1Y = self.generate_y()
            coords.append((i / (self.points + 1), point1Y))
        coords.append((1, self.startY))
        return generate_estimated_coords(*zip(*coords), n=self.resolution)

    def generate_svg_path(self, x_coords: list[float], y_coords: list[float]) -> str:
        out = f"M 0 {y_coords[0]} "
        for x, y in zip(x_coords[1:], y_coords[1:]):
            out += f"L {x} {y} "
        out += "V 1 H 0 Z"
        return out

    def generate_wave(self) -> str:
        x_coords, y_coords = self.generate_coords()
        self.svg_path = self.generate_svg_path(x_coords, y_coords)
        if len(self.only_include) != 0:
            return self.get_return_dict()
        return (
            self.base.replace("{width}", str(self.width))
            .replace("{height}", str(self.height))
            .replace("{color}", f"#{self.color}")
            .replace("{path}", self.svg_path)
        )

    def get_return_dict(self):
        d = {}
        _all = "all" in self.only_include

        if _all or "path" in self.only_include:
            d["path"] = self.svg_path

        if _all or "color" in self.only_include:
            d["color"] = f"#{self.color}"

        if _all or "width" in self.only_include:
            d["width"] = self.width

        if _all or "height" in self.only_include:
            d["height"] = self.height

        if _all or "wonkyness" in self.only_include:
            d["wonkyness"] = self.wonkyness

        if _all or "points" in self.only_include:
            d["points"] = self.points

        if _all or "resolution" in self.only_include:
            d["resolution"] = self.resolution
        return d

    def interpolate_color(self, start_color: str, end_color: str, t: float) -> str:
        start_color = [int(start_color[i : i + 2], 16) for i in (0, 2, 4)]
        end_color = [int(end_color[i : i + 2], 16) for i in (0, 2, 4)]
        color = [round(start_color[i] + (end_color[i] - start_color[i]) * t) for i in range(3)]
        return "".join(hex(i)[2:].zfill(2) for i in color)

    def generate_waves(
        self,
        layers: int = 6,
        start_color: str = "e7233a",
        end_color: str = "01051e",
        start_y: float = 0.2,
        end_y: float = 0.5,
    ) -> list[str]:
        result = []
        for i in range(layers):
            color = self.interpolate_color(start_color, end_color, i / (layers - 1))
            self.set_color(color)
            self.set_start(start_y + (end_y - start_y) * i / (layers - 1))
            result.append(self.generate_wave())
        return result
