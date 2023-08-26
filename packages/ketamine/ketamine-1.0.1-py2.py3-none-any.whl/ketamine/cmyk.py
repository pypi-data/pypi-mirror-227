class CMYKMixin:
    """Mixin to add CMYK conversion functions."""

    def to_cmyk(self) -> tuple[int | float]:
        """
        Converts the Colour object into a CMYK colour.

        Returns: tuple[int | float (0.0 - 1.0)] consisting of CMYK values as a decimal percentage.
        """
        rt, gt, bt = self.to_rgbd()
        k = 1 - max(rt, gt, bt)
        c = (1 - rt - k) / (1 - k)
        m = (1 - gt - k) / (1 - k)
        y = (1 - bt - k) / (1 - k)

        return (c, m, y, k)

    @classmethod
    def from_cmyk(cls, c: int | float, m: int | float, y: int | float, k: int | float):
        """
        Creates a Colour object from a CMYK colour.

        Args:
            c: int | float (0.0 - 1.0)
                Cyan channel as a decimal percentage.
            m: int | float (0.0 - 1.0)
                Magenta channel as a decimal percentage.
            y: int | float (0.0 - 1.0)
                Yellow channel as a decimal percentage.
            k: int | float (0.0 - 1.0)
                Black key channel as a decimal percentage.

        Returns: Colour
        """
        return cls(
            255 * (1 - c) * (1 - k),
            255 * (1 - m) * (1 - k),
            255 * (1 - y) * (1 - k),
        )
