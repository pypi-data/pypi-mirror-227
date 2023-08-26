class HSVMixin:
    """Mixin to add HSV conversion functions."""

    def to_hsv(self) -> tuple[int | float]:
        """
        Converts the Colour object into HSV.

        Returns:
            tuple[int | float] consisting of:
                hue (0 - 360): in degrees
                saturation (0.0 - 1.0): as decimal percentage
                value (0.0 - 1.0): as decimal percentage
        """
        r, g, b = self.to_rgbd()

        M = max(r, g, b)
        m = min(r, g, b)
        d = M - m

        if d == 0:
            h = 0
        elif M == r:
            h = 60 * ((g - b) / d % 6)
        elif M == g:
            h = 60 * ((b - r) / d + 2)
        else:
            h = 60 * ((r - g) / d + 4)

        return (h, d / M, M)

    @classmethod
    def from_hsv(cls, h: int | float, s: int | float, v: int | float):
        """
        Creates a Colour object from a HSV colour.

        Args:
            h: int | float (0 - 360)
                Hue in degrees.
            s: int | float (0.0 - 1.0)
                Saturation as a decimal percentage.
            v: int | float (0.0 - 1.0)
                Value as a decimal percentage.

        Returns: Colour
        """
        c = v * s
        x = c * (1 - abs(h / 60 % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            rt, gt, bt = (c, x, 0)
        elif 60 <= h < 120:
            rt, gt, bt = (x, c, 0)
        elif 120 <= h < 180:
            rt, gt, bt = (0, c, x)
        elif 180 <= h < 240:
            rt, gt, bt = (0, x, c)
        elif 240 <= h < 300:
            rt, gt, bt = (x, 0, c)
        else:
            rt, gt, bt = (c, 0, x)

        return cls(
            (rt + m) * 255,
            (gt + m) * 255,
            (bt + m) * 255,
        )
