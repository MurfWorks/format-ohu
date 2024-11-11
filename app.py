import streamlit as st
import fitz  # PyMuPDF for PDF processing
import re

def extract_columns_from_page(page):
    """
    Extracts text from a page in left-to-right column order and removes unnecessary lines.
    """
    blocks = page.get_text("blocks")  # Get text blocks with spatial information
    blocks.sort(key=lambda b: (b[1], b[0]))  # Sort by y (top-to-bottom), then x (left-to-right)
    
    left_column, middle_column, right_column = "", "", ""
    page_width = page.rect.width
    
    for block in blocks:
        x0, x1 = block[:2]
        text = block[4].strip()
        
        # Remove unwanted lines
        if "OPTIMAL HEALTH UNIVERSITY" in text or "●" in text:
            continue
        
        if x0 < page_width / 3:
            left_column += text + "\n\n"
        elif x0 < 2 * page_width / 3:
            middle_column += text + "\n\n"
        else:
            right_column += text + "\n\n"
    
    combined_text = left_column + middle_column + right_column  # Combine columns in reading order
    return fix_hyphenated_words(combined_text)  # Fix hyphenated line breaks

def fix_hyphenated_words(text):
    """
    Fixes hyphenated words that are split across lines, joining them into a single word.
    """
    # Regular expression to find hyphenated words at the end of a line
    text = re.sub(r"(\b\w+)-\s+(\w+\b)", r"\1\2", text)
    return text

def extract_and_format_pdf(pdf_file, file_name):
    """
    Extracts text from a multi-column PDF and reformats it to Markdown ATX with preserved structure.
    """
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    formatted_text = f"# {file_name}\n\n"  # Start with the file name as the H1 heading

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = extract_columns_from_page(page)
        formatted_text += format_to_markdown(page_text)
    
    return formatted_text

def format_to_markdown(text):
    """
    Converts text to Markdown ATX format with H2 for section headings,
    H3 for subheadings, and citations as H5 headers.
    """
    lines = text.splitlines()
    markdown_text = ""
    
    for line in lines:
        line = line.strip()

        # Detect and format heading levels based on structure or keywords
        if re.match(r"^#\d+:", line):  # Lines starting with # followed by number
            markdown_text += "## " + line + "\n\n"  # Format as H2
        elif line.startswith("Top 10 Ways Chiropractic"):
            markdown_text += "## " + line + "\n\n"  # Main section heading as H2
        elif line.startswith("Chiropractic") and not line.startswith("#"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.endswith(")") and not line.startswith("#####"):
            markdown_text += "##### " + line + "\n\n"  # Format citation as H5
        else:
            markdown_text += line + " "
    
    return markdown_text

def main():
    st.title("PDF to Markdown ATX Formatter")
    st.markdown("Upload a PDF file to convert its text content to Markdown ATX format with citations as H5 headers.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        file_name = uploaded_file.name.split(".")[0]  # Use the filename without the extension as H1 heading
        with st.spinner('Extracting and formatting text...'):
            formatted_text = extract_and_format_pdf(uploaded_file, file_name)
        
        st.markdown("### Formatted Markdown ATX Text")
        text_area = st.text_area("", formatted_text, height=600)

        # "Copy Text" button
        if st.button("Copy Text"):
            # JavaScript to copy text to clipboard
            st.write(
                f'<script>navigator.clipboard.writeText(`{formatted_text}`)</script>',
                unsafe_allow_html=True
            )
            st.success("Text copied to clipboard!")

if __name__ == "__main__":
    main()
