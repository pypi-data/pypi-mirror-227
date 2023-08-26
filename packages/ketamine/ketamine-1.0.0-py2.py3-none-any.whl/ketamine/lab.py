import math

# constants
d = 6 / 29
d1 = d**3
d2 = 2 * d**2

p = 4 / 29


def f(t):
    return math.cbrt(t) if t > d1 else t / d2 + p


def inv_f(t):
    return t**3 if t > d else d2 * (t - p)


class LabMixin:
    """Mixin to add CIELAB conversion functions."""

    def to_lab(self) -> tuple[int | float]:
        """
        Converts the Colour object into Lab.

        Returns: tuple[int | float] consisting of Lab colour values.
        """
        x, y, z = self.to_xyz(normalize=True)
        yt = f(y)

        L = 116 * yt - 16
        a = 500 * (f(x) - yt)
        b = 200 * (yt - f(z))

        return (L, a, b)

    @classmethod
    def from_lab(cls, l: int | float, a: int | float, b: int | float):
        """
        Creates a Colour object from a Lab colour.

        Args:
            l: int | float
                L value.
            a: int | float
                a value.
            b: int | float
                b value.

        Returns: Colour
        """
        lp = (l + 16) / 116

        return cls.from_xyz(
            inv_f(lp + a / 500),
            inv_f(lp),
            inv_f(lp - b / 200),
        )
