import fitz
import json

def extract_paragraph_styles(pdf_path, output_json_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    styles = []

    # Iterate through each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]  # Extract text blocks

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        # Extract style information
                        style = {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "color": span["color"],
                            "alignment": span["alignment"],  # Bounding box (position)
                        }
                        styles.append(style)

    # Save the extracted styles to a JSON file
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(styles, json_file, indent=4, ensure_ascii=False)

    print(f"Paragraph styles extracted and saved to {output_json_path}")

# Example usage
pdf_path = "static/tmpheader.pdf"
output_json_path = "static/paragraph_styles.json"
extract_paragraph_styles(pdf_path, output_json_path)