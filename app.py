import streamlit as st
import fitz  # PyMuPDF for PDF processing

def extract_columns_from_page(page):
    """
    Extracts text from a page in left-to-right column order.
    """
    blocks = page.get_text("blocks")  # Get text blocks with spatial information
    # Sort blocks by x-coordinate, which roughly corresponds to column position
    blocks.sort(key=lambda b: (b[1], b[0]))  # Sort by y (top-to-bottom), then x (left-to-right)
    
    # Group text by columns: left, middle, right
    left_column, middle_column, right_column = "", "", ""
    page_width = page.rect.width
    
    for block in blocks:
        x0, x1 = block[:2]
        text = block[4].strip()
        
        # Define approximate column areas
        if x0 < page_width / 3:
            left_column += text + "\n\n"
        elif x0 < 2 * page_width / 3:
            middle_column += text + "\n\n"
        else:
            right_column += text + "\n\n"
    
    return left_column + middle_column + right_column  # Combine columns in reading order

def extract_and_format_pdf(pdf_file, file_name):
    """
    Extracts text from a multi-column PDF and reformats it to Markdown ATX with preserved structure.
    """
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Start the formatted text with the H1 heading as the file name
    formatted_text = f"# {file_name}\n\n"

    # Extract and format each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        page_text = extract_columns_from_page(page)
        formatted_text += format_to_markdown(page_text)
    
    return formatted_text

def format_to_markdown(text):
    """
    Converts text from PDF to Markdown ATX format with H2 for section headings,
    H3 for subheadings, and citations as H5 headers.
    """
    lines = text.splitlines()
    markdown_text = ""
    
    for line in lines:
        line = line.strip()
        
        # Detect heading levels and format accordingly
        if line.startswith("Top 10 Ways Chiropractic"):
            markdown_text += "## " + line + "\n\n"  # Section heading as H2
        elif line.startswith("#") and len(line) <= 4:  # Detect top-level numbered headings
            markdown_text += "## " + line + "\n\n"  # Section heading as H2
        elif line.startswith("Chiropractic") and not line.startswith("#"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.endswith(")"):
            # Format citation as H5 in parentheses
            markdown_text += "##### " + line + "\n\n"
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

