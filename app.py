import streamlit as st
import os
from converters import cdsl, nsdl  # Add other imports as you expand
from datetime import datetime



st.set_page_config(page_title="Voting File Converter", page_icon="📄", layout="centered")

st.title("📥 Voting File to Response File Converter")

file_type = st.selectbox("Select File Type", ["CDSL", "NSDL"])  # Add more as needed
uploaded_file = st.file_uploader("Upload your file", type=['txt', 'xlsx'])

status_placeholder = st.empty()
download_btn = st.empty()


def detect_format(content: str):
    """Rudimentary format detection based on structure"""
    if '~' in content and '=' in content:
        return 'CDSL'
    elif '^' in content:
        return 'NSDL'
    return 'UNKNOWN'

if uploaded_file:
    file_bytes = uploaded_file.read()
    try:
        content_str = file_bytes.decode('utf-8')
    except Exception:
        status_placeholder.error("❌ Unable to read file. Please upload a valid .txt file.")
        st.stop()

    # Step 1: Show progress
    status_placeholder.info("📤 Uploading file... 25%")

    # Step 2: Validate format
    detected_type = detect_format(content_str)
    if detected_type != file_type:
        status_placeholder.error(f"❌ File format mismatch. You selected {file_type}, but file looks like {detected_type}. Delet the file by clicking ❌ next to file name and upload again")
        st.stop()

    status_placeholder.info("🔍 Validating file format... 50%")

    # Step 3: Process based on type
    status_placeholder.info("⚙️ Processing file... 75%")
    output_file = None
    if file_type == "CDSL":
        output_file = cdsl.process_and_write_output(content_str, f"output_{uploaded_file.name}")
    elif file_type == "NSDL":
        output_file = nsdl.process_and_write_output(content_str, f"output_{uploaded_file.name}")

    print(output_file)    
    # Assuming `output_file` is the path to the file generated
    if output_file:
        # Create dynamic file name with timestamp
        download_filename = f"Output_Response_File_{uploaded_file.name}"

        # Display success message
        status_placeholder.success("✅ File processed. Ready to download!")

        # Display download button
        if st.download_button(
            label="📥 Download Converted File",
            data=output_file,
            file_name=download_filename,
            mime="text/plain"
        ):
            st.success("✅ File downloaded. Please check your download folder.")

            st.success("Reset the page by deleting the uploaded file by clicking ❌ on button next to the file name.")
