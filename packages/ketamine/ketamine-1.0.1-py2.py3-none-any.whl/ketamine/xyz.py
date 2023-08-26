# standard d65
xn = 95.0489
yn = 100
zn = 108.8840


def normalize_XYZ(x: int | float, y: int | float, z: int | float) -> tuple[int | float]:
    """
    Normalizes XYZ colour values using CIE standard illuminant D65 as white achromatic reference illuminant.

    Args:
        x: int | float
            X value.
        y: int | float
            Y value.
        z: int | float
            Z value.

    Returns: tuple[int | float] consisting of normalized XYZ colour values.
    """
    return (x / xn, y / yn, z / zn)


class XYZMixin:
    """Mixin to add CIEXYZ conversion functions."""

    def to_xyz(self, normalize: bool = True) -> tuple[int | float]:
        """
        Converts the Colour object into XYZ. Assumes Colour object is in the sRGB colour space.
        Uses CIE standard illuminant D65 as white reference.

        Args:
            normalize: bool = True
                If true, normalizes XYZ colour values before returning.

        Returns: tuple[int | float] consisting of XYZ values.
        """
        # linearize sRGB data
        rgb = self.to_rgbd()
        rt, gt, bt = (
            c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb
        )

        # transformation matrix
        x = 0.4124564 * rt + 0.3575761 * gt + 0.1804375 * bt
        y = 0.2126729 * rt + 0.7151522 * gt + 0.0721750 * bt
        z = 0.0193339 * rt + 0.1191920 * gt + 0.9503041 * bt

        if normalize:
            return (x, y, z)
        else:
            return (x * xn, y * yn, z * zn)

    @classmethod
    def from_xyz(cls, x: int | float, y: int | float, z: int | float):
        """
        Creates a Colour object from a XYZ colour.
        Uses CIE standard illuminant D65 as white reference.

        Args:
            x: int | float (0.0 - 1.0)
                Normalized X value.
            y: int | float (0.0 - 1.0)
                Normalized Y value.
            z: int | float (0.0 - 1.0)
                Normalized Z value.

        Returns: Colour
        """
        # transformation matrix
        rgbt = (
            3.2404542 * x + -1.5371385 * y + -0.4985314 * z,
            -0.9692660 * x + 1.8760108 * y + 0.0415560 * z,
            0.0556434 * x + -0.2040259 * y + 1.0572252 * z,
        )

        # apply gamma
        r, g, b = (
            c * 12.92 if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
            for c in rgbt
        )

        return cls(r * 255, g * 255, b * 255)
