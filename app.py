import streamlit as st
import fitz  # PyMuPDF for PDF processing

def extract_and_format_pdf(pdf_file, file_name):
    """
    Extracts text from PDF and reformats it into Markdown ATX with citations as H5 headers.
    """
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Start the formatted text with the H1 heading as the file name
    formatted_text = f"# {file_name}\n\n"

    # Extract text from each page and format
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        formatted_text += format_to_markdown(text)
    
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
        if line.startswith("ADHD - Research Chiro May Alleviate ADHD"):
            markdown_text += "## " + line + "\n\n"  # Section heading as H2
        elif line.startswith("Research Shows Chiropractic"):
            markdown_text += "## " + line + "\n\n"  # Section heading as H2
        elif line.startswith("The Latest Research"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.startswith("Previous Research"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.startswith("Case Studies"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.startswith("Theories on How Chiropractic"):
            markdown_text += "### " + line + "\n\n"  # Subheading as H3
        elif line.startswith("Help a Child in Your Life"):
            markdown_text += "## " + line + "\n\n"  # Section heading as H2
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
        st.text_area("", formatted_text, height=600)

if __name__ == "__main__":
    main()
