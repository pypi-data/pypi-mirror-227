class HSLMixin:
    """Mixin to add HSL conversion functions."""

    def to_hsl(self) -> tuple[int | float]:
        """
        Converts the Colour object into HSL.

        Returns:
            tuple[int | float] consisting of:
                hue (0 - 360): in degrees
                saturation (0.0 - 1.0): as decimal percentage
                luminance (0.0 - 1.0): as decimal percentage
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

        l = (M + m) / 2
        s = 0 if d == 0 else d / (1 - abs(2 * l - 1))

        return (h, s, l)

    @classmethod
    def from_hsl(cls, h: int | float, s: int | float, l: int | float):
        """
        Creates a Colour object from a HSL colour.

        Args:
            h: int | float (0 - 360)
                Hue in degrees.
            s: int | float (0.0 - 1.0)
                Saturation as a decimal percentage.
            l: int | float (0.0 - 1.0)
                Luminance as a decimal percentage.

        Returns: Colour
        """
        d = s * (1 - abs(2 * l - 1))
        m = 255 * (l - d / 2)
        x = d * (1 - abs((h / 60) % 2 - 1))

        if 0 <= h < 60:
            r = 255 * d + m
            g = 255 * x + m
            b = m
        elif 60 <= h < 120:
            r = 255 * x + m
            g = 255 * d + m
            b = m
        elif 120 <= h < 180:
            r = m
            g = 255 * d + m
            b = 255 * x + m
        elif 180 <= h < 240:
            r = m
            g = 255 * x + m
            b = 255 * d + m
        elif 240 <= h < 300:
            r = 255 * x + m
            g = m
            b = 255 * d + m
        else:
            r = 255 * d + m
            g = m
            b = 255 * x + m

        return cls(r, g, b)
