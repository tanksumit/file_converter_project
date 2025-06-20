import streamlit as st
import os
from converters import cdsl, nsdl  # Add other imports as you expand

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
        status_placeholder.error(f"❌ File format mismatch. You selected {file_type}, but file looks like {detected_type}.")
        st.stop()

    status_placeholder.info("🔍 Validating file format... 50%")

    # Step 3: Process based on type
    status_placeholder.info("⚙️ Processing file... 75%")
    output_file = None
    if file_type == "CDSL":
        output_file = cdsl.process_and_write_output(content_str, f"output_{uploaded_file.name}")
    elif file_type == "NSDL":
        output_file = nsdl.process_and_write_output(content_str, f"output_{uploaded_file.name}")
    
    if output_file:
        status_placeholder.success("✅ File processed. Ready to download!")

        with open(output_file, "rb") as f:
            btn = download_btn.download_button(
                label="📥 Download Converted File",
                data=f,
                file_name=os.path.basename(output_file),
                mime="text/plain"
            )

        st.info("ℹ️ After downloading, click '🔁 Reset' to clear the file.")

        # Reset file input after download
        if btn:  # If download button is clicked
            st.success("✅ File downloaded successfully.")
            os.remove(output_file)
            st.experimental_rerun() 
             # Refreshes the app, resets upload state
    else:
        status_placeholder.error("❌ Conversion failed. Please check the file format and try again.")
