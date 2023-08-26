class RGBMixin:
    """Mixin to add RGB / RGBA conversion functions."""

    def to_rgb(self) -> tuple[int | float]:
        """
        Converts the Colour object into RGB.

        Returns:
            tuple[int | float (0 - 255)] consisting of RGB values.
        """
        return (self.r, self.g, self.b)

    def to_rgba(self) -> tuple[int | float]:
        """
        Converts the Colour object into RGBA.

        Returns:
            tuple[int | float (0 - 255)] consisting of RGBA values.
        """
        return (self.r, self.g, self.b, self.a)

    def to_rgbd(self) -> tuple[int | float]:
        """
        Converts the Colour object into decimal RGB.

        Returns:
            tuple[int | float (0.0 - 1.0)] consisting of decimal RGB values.
        """
        return (self.r / 255, self.g / 255, self.b / 255)

    def to_rgbad(self) -> tuple[int | float]:
        """
        Converts the Colour object into decimal RGBA.

        Returns:
            tuple[int | float (0.0 - 1.0)] consisting of decimal RGBA values.
        """
        return (self.r / 255, self.g / 255, self.b / 255, self.a / 255)

    @classmethod
    def from_rgb(
        cls, r: int | float, g: int | float, b: int | float, a: int | float = 255
    ):
        """
        Creates a Colour object from an 8-bit RGBA colour.

        Args:
            r: int | float (0 - 255)
                Red channel value.
            g: int | float (0 - 255)
                Green channel value.
            b: int | float (0 - 255)
                Blue channel value.
            a: int | float (0 - 255) = 255
                Alpha channel value.

        Returns: Colour
        """
        return cls(r, g, b, a)

    @classmethod
    def from_rgbd(
        cls, r: int | float, g: int | float, b: int | float, a: int | float = 1
    ):
        """
        Creates a Colour object from a decimal RGBA colour (0.0 - 1.0).

        Args:
            r: int | float (0.0 - 1.0)
                Normalized red channel value.
            g: int | float (0.0 - 1.0)
                Normalized green channel value.
            b: int | float (0.0 - 1.0)
                Normalized blue channel value.
            a: int | float (0.0 - 1.0) = 1
                Normalized alpha channel value.

        Returns: Colour
        """
        return cls(r * 255, g * 255, b * 255, a * 255)
