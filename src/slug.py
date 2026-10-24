"""Normalize titles to ASCII slugs and expose the approved CLI."""

import argparse
import re
import unicodedata


def slugify(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("title must be a string")
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    result = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    if not result or len(result) > 64:
        raise ValueError("slug must contain 1 to 64 ASCII characters")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title")
    args = parser.parse_args()
    try:
        print(slugify(args.title))
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
