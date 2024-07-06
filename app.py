import streamlit as st
import re
from docx import Document

# Custom CSS to set a white background, place the image at the top, ensure black font color, and style buttons
def set_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;  /* Set font color to black */
        }
        .main {
            background: white;  /* White background */
            padding: 10px;
            border-radius: 10px;
            margin: 20px;
            color: black;
        }
        .top-menu {
            background: rgba(255, 255, 255, 0.8);  /* White background with opacity */
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            color: black;
            display: flex;
            justify-content: space-around;  /* Evenly space out the menu items */
        }
        .menu-item {
            margin: 0 15px;
            font-weight: bold;
            cursor: pointer;
            color: black;  /* Set font color to black */
        }
        .menu-item:hover {
            text-decoration: underline;
        }
        .upload-btn {
            margin-top: 20px;
            color: black;
        }
        .top-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
            margin-bottom: 20px;
        }
        body, p, div, h1, h2, h3, h4, h5, h6, span, li, a {
            color: black;  /* Set font color to black */
        }
        .stTextArea textarea {
            background-color: #98FB98 !important;  /* Set text area background color to green */
            color: black;
        }
        .custom-div {
            background-color: #98FB98;  /* Set background color of custom div to green */
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: black;
        }
        /* Style for buttons */
        .stButton>button {
            background-color: white;  /* Button background color */
            color: black;  /* Button text color */
            border: 2px solid black;  /* Button border */
            border-radius: 10px;  /* Rounded corners */
            padding: 10px 20px;  /* Padding */
            font-weight: bold;  /* Bold text */
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #f0f0f0;  /* Lighter background on hover */
        }
        /* Style for file uploader */
        .stFileUploader>label {
            background-color: white;  /* File uploader background color */
            color: black;  /* File uploader text color */
            border: 2px solid black;  /* File uploader border */
            border-radius: 10px;  /* Rounded corners */
            padding: 10px 20px;  /* Padding */
            font-weight: bold;  /* Bold text */
            cursor: pointer;
        }
        .stFileUploader>label:hover {
            background-color: #f0f0f0;  /* Lighter background on hover */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Read the content of a .docx file
def read_docx(file):
    doc = Document(file)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

# Tokenize text into words
def tokenize_text(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)

# Highlight differences between contract and template
def highlight_differences(contract_text, template_text):
    contract_words = tokenize_text(contract_text)
    template_words = tokenize_text(template_text)

    highlighted_text = ""
    contract_tokens = re.findall(r'\b\w+\b', contract_text)

    for token in contract_tokens:
        if token.lower() not in template_words:
            highlighted_text += f'<span style="background-color: #FF6347; color: black;">{token}</span> '
        else:
            highlighted_text += token + ' '

    return highlighted_text

# Extract clauses from the text
def extract_clauses(text):
    clauses = {
        "agreement": "",
        "party": "",
        "confidentiality": "",
        "termination": "",
        "liability": "",
        "payment": "",
        "governing law": "",
        "dispute resolution": ""
    }
    current_clause = None
    for line in text.split('\n'):
        for clause in clauses.keys():
            if re.search(rf'\b{clause}\b', line, re.IGNORECASE):
                current_clause = clause
                break
        if current_clause:
            clauses[current_clause] += line + '\n'
    return clauses

# Main function to handle navigation and rendering
def main():
    set_custom_css()
    
    st.title("BUSINESS CONTRACT VALIDATION - To classify content within the Contract Clauses & to determine deviations from Template & highlight them")
    
    st.markdown('<div class="top-menu">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Home"):
            st.session_state.page = 'home'
    with col2:
        if st.button("Highlighted Deviations"):
            st.session_state.page = 'highlighted_deviations'
    with col3:
        if st.button("Extracted Clauses"):
            st.session_state.page = 'extracted_clauses'
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<img class="top-image" src="https://i.pinimg.com/originals/bf/9e/cd/bf9ecdb5d13c6f816e89753c55e4e6da.gif" alt="top image">', unsafe_allow_html=True)

    # Initialize session state variables
    if 'contract_text' not in st.session_state:
        st.session_state.contract_text = None
    if 'template_text' not in st.session_state:
        st.session_state.template_text = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Instructions on how to use the application and the animated GIF
    st.markdown('## How to Use')
    st.markdown('1. Upload your contract document using the "Upload your document" button.')
    st.markdown('2. Upload the template document using the "Upload the template" button.')
    st.markdown('3. Choose between "Highlight Text" to see deviations or "Extract Clauses" in the top menu to view specific sections.')
    
    # Home page for uploading documents
    if st.session_state.page == 'home':
        st.write("Upload your document and the template to highlight deviations  and view different clauses.")

        # File uploaders
        contract_file = st.file_uploader("Upload your document", type=["txt", "docx"], key="contract")
        template_file = st.file_uploader("Upload the template", type=["txt", "docx"], key="template")

        if contract_file and template_file:
            # Read the content of the uploaded files
            if contract_file.name.endswith(".txt"):
                st.session_state.contract_text = contract_file.read().decode("utf-8")
            else:
                st.session_state.contract_text = read_docx(contract_file)

            if template_file.name.endswith(".txt"):
                st.session_state.template_text = template_file.read().decode("utf-8")
            else:
                st.session_state.template_text = read_docx(template_file)
            

        
        # Place the image below the upload buttons
        st.image("https://i.pinimg.com/564x/6d/02/4e/6d024e072be5b902b2594f14119e2bcb.jpg", use_column_width=True, caption="Project Name")

    # Options page after submitting documents
    

    # Highlighted deviations page
    if st.session_state.page == 'highlighted_deviations' and st.session_state.contract_text and st.session_state.template_text:
        st.subheader("Original Document")
        st.text_area("Original Document Text", st.session_state.contract_text, height=300, key="original_doc")

        st.subheader("Template")
        st.text_area("Template Text", st.session_state.template_text, height=300, key="template_doc")

        highlighted_text = highlight_differences(st.session_state.contract_text, st.session_state.template_text)

        st.subheader("Highlighted Deviations")
        st.markdown(highlighted_text, unsafe_allow_html=True)

    # Extracted clauses page
    if st.session_state.page == 'extracted_clauses' and st.session_state.contract_text:
        st.subheader("Extracted Clauses from Contract")
        clauses = extract_clauses(st.session_state.contract_text)
        for i, (clause, text) in enumerate(clauses.items()):
            st.markdown(f"**{clause.capitalize()} Clause:**")
            st.text_area("", text, height=150, key=f"{clause}_{i}")

if __name__ == "__main__":
    main()
