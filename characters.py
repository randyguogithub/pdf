from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def calculate_characters_per_page(font_size, left_margin=2*cm, right_margin=2*cm, top_margin=2*cm, bottom_margin=2*cm):
    # A4 page dimensions
    page_width, page_height = A4

    # Usable width and height
    usable_width = page_width - left_margin - right_margin
    usable_height = page_height - top_margin - bottom_margin

    # Character widths
    english_char_width = font_size * 0.5  # Approximate width of an English character
    chinese_char_width = font_size       # Chinese characters are square

    # Characters per line
    english_chars_per_line = int(usable_width / english_char_width)
    chinese_chars_per_line = int(usable_width / chinese_char_width)

    # Line height (leading)
    line_height = font_size * 1.2

    # Lines per page
    lines_per_page = int(usable_height / line_height)

    # Total characters per page
    total_english_chars = english_chars_per_line * lines_per_page
    total_chinese_chars = chinese_chars_per_line * lines_per_page

    return {
        "english_chars_per_line": english_chars_per_line,
        "chinese_chars_per_line": chinese_chars_per_line,
        "lines_per_page": lines_per_page,
        "total_english_chars": total_english_chars,
        "total_chinese_chars": total_chinese_chars
    }

# Example usage
font_size = 12
result = calculate_characters_per_page(font_size)
print(f"English characters per line: {result['english_chars_per_line']}")
print(f"Chinese characters per line: {result['chinese_chars_per_line']}")
print(f"Lines per page: {result['lines_per_page']}")
print(f"Total English characters per page: {result['total_english_chars']}")
print(f"Total Chinese characters per page: {result['total_chinese_chars']}")