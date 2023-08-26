# acid: A robust python library for colour conversion.

A python library for colour conversion between colour models.

# Supported Colour Models

- RGB, RGBA, hex
- HSL
- HSV
- CMYK
- CIELAB
- CIEXYZ

# Example Usage

```py
from acid import Colour

white = Colour.from_rgb(255, 255, 255)
print(white.to_hex()) # #ffffff
print(white.to_hsl()) # (0, 0.0, 1.0)

hsv = Colour.from_hsv(184, 0.85, 1.0)
print(hsv.to_rgb()) # (38.25000000000001, 240.54999999999995, 255.0)

# round RGB values first
hsv.round()

print(hsv.to_rgb()) # (38, 241, 255)
```

# Todo

- [x] Finish CIELAB colour conversion
  - [x] Correctly implement to_lab
- [x] Finish CMYK colour conversion
- [ ] Publish to PyPI
