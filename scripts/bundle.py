import argparse
import shutil
import zipfile
import tempfile
import re
from urllib.request import urlretrieve
from pathlib import Path


release_url = (
    "https://github.com/tailwindlabs/heroicons/archive/refs/tags/v{version}.zip"
)
release_name = "heroicons-{version}.zip"
version_match = r"(\d+\.\d+\.\d+)"
paint_match = r"(stroke|fill)=\".+?\"\s?"


parser = argparse.ArgumentParser(
    prog=__file__,
    description="Download and bundle the latest Heroicons release.",
)
parser.add_argument("version")
parser.add_argument("-o", "--out", default="src")
parser.add_argument("-i", "--icons", default="assets/icons")
parser.add_argument("--size", default=24)
parser.add_argument("-s", "--styles", default="solid,outline")

args = parser.parse_args()
args.icons_path = Path(args.icons)
args.out_path = Path(args.out)
args.style_path = args.out_path
args.index_path = args.out_path / "icon-index.txt"
args.size = int(args.size)

args.styles = args.styles.split(",")


icon_names = list()


# prepare output path
if args.icons_path.exists():
    shutil.rmtree(args.icons_path)
args.icons_path.mkdir(parents=True)


# download release if arg.version is not a path
if not Path(args.version).exists() and re.match(version_match, args.version):
    version_url = release_url.format(version=args.version)
    print(f"Downloading release {args.version} from {version_url}..")
    release_file, _ = urlretrieve(version_url)
elif Path(args.version).exists():
    release_file = Path(args.version)
    if m := re.search(version_match, args.version):
        args.version = m.group(1)
    else:
        print("No version information found in archive path.")
        exit(1)
else:
    print("Usage:   bundle.py <release_name>")
    print("Example: bundle.py 2.2.0")
    exit(1)


# unpack icon files (size 24)
with tempfile.TemporaryDirectory() as tempdir:
    with zipfile.ZipFile(release_file, "r") as zip_ref:
        zip_ref.extractall(
            tempdir,
            members=filter(
                lambda x: x.startswith(f"heroicons-{args.version}/src/{args.size}"),
                zip_ref.namelist(),
            ),
        )
    release_path = Path(tempdir) / f"heroicons-{args.version}/src/{args.size}"
    shutil.copytree(release_path, args.icons_path, dirs_exist_ok=True)


for style in args.styles:
    style_path = args.icons_path / style
    style_pramble = None

    symbol_data = ""

    for file in style_path.iterdir():
        icon_data = file.read_text(encoding="UTF-8").strip().split("\n")
        if not style_pramble:
            style_pramble = icon_data[0]
        icon_data = "".join(icon_data[1:-1]).strip()
        # remove fill / stroke from icons
        icon_data = re.sub(paint_match, "", icon_data)
        symbol_data += f'<symbol id="{file.stem}" viewBox="0 0 {args.size} {args.size}">{icon_data}</symbol>'

        icon_names.append(file.stem)

    if not style_pramble:
        style_pramble = '<svg xmlns="http://www.w3.org/2000/svg">'

    sprite_data = f'<?xml version="1.0" encoding="utf-8"?>{style_pramble}<defs>{symbol_data}</defs>'

    style_sprite_path = args.out_path / f"{style}.svg"
    style_sprite_path.write_text(sprite_data, encoding="UTF-8")

    print(f"Created `{style}` sprite at `{style_sprite_path!s}`")


icon_names = sorted(set(icon_names))
args.index_path.write_text("\n".join(icon_names), encoding="UTF-8")
print(f"Created index file at `{args.index_path!s}`")
