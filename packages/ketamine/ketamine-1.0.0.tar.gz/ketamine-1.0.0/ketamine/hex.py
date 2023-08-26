class HexMixin:
    """Mixin to add hex conversion functions."""

    def to_hex(self, with_hashtag: bool = True) -> str:
        """
        Converts the Colour object into a hex string.

        Args:
            with_hashtag: bool = True
                If true, returns hex string with a leading hashtag.

        Returns: string
        """
        hex_string = (
            f"{'#' if with_hashtag else ''}{self.r:02x}{self.g:02x}{self.b:02x}"
        )

        if self.a != 255:
            hex_string += f"{self.a:02x}"

        return hex_string

    @classmethod
    def from_hex(cls, hex_string: str):
        """
        Creates a Colour object from a hex string.

        Args:
            hex_string: string
                Hexadecimal colour string with or without leading hashtag.

        Returns: Colour
        """
        hex_string = hex_string.lstrip("#")
        if len(hex_string) == 3:
            hex_string = hex_string * 2

        return cls(
            int(hex_string[:2], 16),
            int(hex_string[2:4], 16),
            int(hex_string[4:6], 16),
            int(hex_string[6:8], 16) if len(hex_string) >= 8 else 255,
        )
