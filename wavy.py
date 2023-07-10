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
        wonkyness: float = 4.0,
        points: int = 5,
        resolution: int = 100,
        format: str = "svg",
    ):
        self.set_width(width)
        self.set_height(height)
        self.set_color(color)
        self.set_start(start)
        self.set_wonkyness(wonkyness)
        self.set_points(points)
        self.set_resolution(resolution)
        self.set_format(format)
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

    def set_wonkyness(self, wonkyness: float) -> None:
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
        self.resolution = resolution

    def set_format(self, format: str) -> None:
        if format not in {"svg", "json"}:
            raise ValueError("Format must be svg or json")
        self.format = format

    def generate_x(self, x: float, available_width: float) -> float:
        return x + (random.random() - 0.5) / available_width

    def generate_y(self) -> float:
        return (random.random() - 0.5) * 0.05 * self.wonkyness + self.startY

    def generate_coords(self):
        coords = []
        for i in range(self.points):
            point1Y = max(0, min(1, self.generate_y()))
            point1X = self.generate_x(i / (self.points + 1), self.width / (self.points + 1))
            coords.append((point1X, point1Y))
        coords.append((1, self.startY))
        return generate_estimated_coords(*zip(*coords), n=self.resolution)

    def generate_svg_path(self, x_coords, y_coords) -> str:
        out = f"M 0 {y_coords[0]} "
        for x, y in zip(x_coords[1:], y_coords[1:]):
            out += f"L {x} {y} "
        out += "V 1 H 0 Z"
        return out

    def generate_wave(self):
        x_coords, y_coords = self.generate_coords()
        self.svg_path = self.generate_svg_path(x_coords, y_coords)
        if self.format == "json":
            return self.get_return_dict()
        return (
            self.base.replace("{width}", str(self.width))
            .replace("{height}", str(self.height))
            .replace("{color}", f"#{self.color}")
            .replace("{path}", self.svg_path)
        )

    def get_return_dict(self):
        d = {
            "path": self.svg_path,
            "color": f"#{self.color}",
            "width": self.width,
            "height": self.height,
            "wonkyness": self.wonkyness,
            "points": self.points,
            "resolution": self.resolution,
            "start": self.startY,
        }
        return d

    def interpolate_color(self, start_color: str, end_color: str, t: float) -> str:
        start_color_list = [int(start_color[i : i + 2], 16) for i in (0, 2, 4)]
        end_color_list = [int(end_color[i : i + 2], 16) for i in (0, 2, 4)]
        color = [
            round(start_color_list[i] + (end_color_list[i] - start_color_list[i]) * t)
            for i in range(3)
        ]
        return "".join(hex(i)[2:].zfill(2) for i in color)

    def generate_waves(
        self,
        layers: int = 6,
        start_color: str = "e7233a",
        end_color: str = "01051e",
        start_y: float = 0.2,
        end_y: float = 0.5,
    ):
        result = []
        for i in range(layers):
            color = self.interpolate_color(start_color, end_color, i / (layers - 1))
            self.set_color(color)
            self.set_start(start_y + (end_y - start_y) * i / (layers - 1))
            result.append(self.generate_wave())
        return result
