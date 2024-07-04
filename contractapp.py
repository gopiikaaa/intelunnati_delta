import streamlit as st
from transformers import pipeline
import os
import re

# Load a pre-trained model for named entity recognition (NER)
ner_pipeline = pipeline("ner", grouped_entities=True)

# List of keywords to highlight
keywords = ["agreement", "party", "confidential", "termination", "liability"]

# Function to load synthetic contracts
def load_synthetic_contracts():
    contracts = {}
    for filename in os.listdir():
        if filename.startswith("contract_") and filename.endswith(".txt"):
            with open(filename, "r") as file:
                contracts[filename] = file.read()
    return contracts

# Highlight keywords in the text
def highlight_keywords(text, keywords):
    for keyword in keywords:
        # Use regular expression to match whole words only
        pattern = re.compile(rf'\b({keyword})\b', re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

# Highlight NER entities in the text
def highlight_entities(text, entities):
    for entity in entities:
        pattern = re.compile(rf'\b({re.escape(entity["word"])})\b', re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text

# Streamlit app
st.title("Business Contract Highlighter")

st.write("Upload your business contract or select a synthetic contract to see the highlighted terms.")

# Load synthetic contracts
synthetic_contracts = load_synthetic_contracts()

# Select synthetic contract
selected_contract = st.selectbox("Select a synthetic contract", list(synthetic_contracts.keys()))
uploaded_file = st.file_uploader("Or upload your own contract")

if uploaded_file is not None:
    # Read the content of the uploaded file
    contract_text = uploaded_file.read().decode("utf-8")
elif selected_contract:
    # Use the selected synthetic contract
    contract_text = synthetic_contracts[selected_contract]
else:
    contract_text = None

if contract_text:
    # Display the original contract text
    st.subheader("Original Contract")
    st.text_area("", contract_text, height=300)
    
    # Perform NER and keyword highlighting
    ner_results = ner_pipeline(contract_text)
    highlighted_text = highlight_keywords(contract_text, keywords)
    highlighted_text = highlight_entities(highlighted_text, ner_results)

    # Display the highlighted contract text
    st.subheader("Highlighted Contract")
    st.markdown(highlighted_text, unsafe_allow_html=True)