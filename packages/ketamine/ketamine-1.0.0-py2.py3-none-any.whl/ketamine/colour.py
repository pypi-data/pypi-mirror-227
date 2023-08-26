from dataclasses import dataclass
import math

from .cmyk import CMYKMixin
from .rgb import RGBMixin
from .hsv import HSVMixin
from .hsl import HSLMixin
from .hex import HexMixin
from .lab import LabMixin
from .xyz import XYZMixin


@dataclass
class Colour(CMYKMixin, RGBMixin, HSLMixin, HSVMixin, LabMixin, XYZMixin, HexMixin):
    """
    A class to easily convert between many kinds of colour models, including:

    - RGB, RGBA, hex
    - HSL
    - HSV
    - CMYK
    - CIELAB
    - CIEXYZ

    Internally it stores RGBA colour values as an intermediate between colour models.
    These values are accessable from properties .r, .g, .b and .a.

    Made by sertdfyguhi (https://github.com/sertdfyguhi).
    """

    r: int | float
    g: int | float
    b: int | float
    a: int | float = 255

    def floor(self) -> None:
        """
        Floors the internal RGBA colour values.

        Returns: None
        """
        self.r = math.floor(self.r)
        self.g = math.floor(self.g)
        self.b = math.floor(self.b)
        self.a = math.floor(self.a)

    def round(self) -> None:
        """
        Rounds the internal RGBA colour values.

        Returns: None
        """
        self.r = round(self.r)
        self.g = round(self.g)
        self.b = round(self.b)
        self.a = round(self.a)

    def ceil(self) -> None:
        """
        Ceils the internal RGBA colour values.

        Returns: None
        """
        self.r = math.ceil(self.r)
        self.g = math.ceil(self.g)
        self.b = math.ceil(self.b)
        self.a = math.ceil(self.a)
