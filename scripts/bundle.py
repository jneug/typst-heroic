from pathlib import Path

icon_path = Path("assets/icons/24")
icon_styles = ["solid", "outline"]
src_path = Path("src")


for style in icon_styles:
    style_path = icon_path / style
    style_pramble = None

    symbol_data = ""

    for file in style_path.iterdir():
        icon_data = file.read_text(encoding="UTF-8").strip().split("\n")
        if not style_pramble:
            style_pramble = icon_data[0]
        icon_data = "".join(icon_data[1:-1])
        symbol_data += (
            f'<symbol id="{file.stem}" viewBox="0 0 24 24">{icon_data.strip()}</symbol>'
        )

    if not style_pramble:
        style_pramble = '<svg xmlns="http://www.w3.org/2000/svg">'

    sprite_data = f'<?xml version="1.0" encoding="utf-8"?>{style_pramble}<defs>{symbol_data}</defs>'

    style_sprite_path = src_path / f"{style}.svg"
    style_sprite_path.write_text(sprite_data, encoding="UTF-8")

    print(f"Created {style} sprite at {style_sprite_path!s}")
