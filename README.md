# Business Contract Validation

## Project Overview

The Business Contract Validation project is designed to facilitate the validation of business contracts by identifying deviations from predefined templates and extracting specific clauses for analysis. This Streamlit-based application aims to streamline the process of contract analysis and ensure compliance with established templates.

## Objectives

- **Automated Validation:** Automatically compare contract documents with templates to highlight differences.
- **Clause Extraction:** Extract specific clauses such as agreement terms, confidentiality agreements, and more.
- **User-Friendly Interface:** Provide an intuitive user interface for uploading documents, navigating through different sections, and viewing results.

## Uniqueness

- **Streamlit Integration:** Utilizes Streamlit for creating a dynamic and interactive web application.
- **Custom CSS Styling:** Enhances user experience with custom CSS for a visually appealing interface.
- **Advanced Text Processing:** Implements advanced text processing techniques for accurate clause extraction and deviation highlighting.

## Implementation Steps

1. **Installation:**
   - Clone the repository:
     ```
     git clone https://github.com/gopiikaaa/Business-contract-validation.git
     cd business-contract-validation
     ```
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   
2. **Running the Application:**
   - Run the Streamlit application:
     ```
     streamlit run app.py
     ```
   
3. **Usage:**
   - Upload a contract document and a corresponding template.
   - Navigate between "Home", "Highlighted Deviations", and "Extracted Clauses" using the top menu buttons.
   - View highlighted deviations between the contract and template, and extracted clauses from the contract.
