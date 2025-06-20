import streamlit as st
import io
from converters import cdsl, nsdl

st.title("📥 Voting File to Response File Converter")

file_type = st.selectbox("Select File Type", ["CDSL", "NSDL"])
uploaded_file = st.file_uploader("Upload your file", type=["txt", "xlsx"])

status = st.empty()

def detect_format(content: str):
    if '~' in content and '=' in content:
        return 'CDSL'
    elif '^' in content:
        return 'NSDL'
    return 'UNKNOWN'

if uploaded_file:
    file_bytes = uploaded_file.read()
    try:
        file_str = file_bytes.decode('utf-8')
    except Exception:
        status.error("❌ Invalid file format. Upload a valid UTF-8 .txt file.")
        st.stop()

    status.info("📤 File uploaded… 25%")
    detected = detect_format(file_str)

    if detected != file_type:
        status.error(f"❌ Mismatch: You selected {file_type}, but file looks like {detected}.")
        st.stop()

    status.info("🔍 Validating… 50%")
    status.info("⚙️ Processing… 75%")

    # Process with selected converter and store result in memory
    if file_type == "CDSL":
        output_str = cdsl.process_and_write_output(file_str, output_filename=None)
    elif file_type == "NSDL":
        output_str = nsdl.process_and_write_output(file_str, output_filename=None)

    if not output_str:
        status.error("❌ Processing failed.")
        st.stop()

    # Convert string to bytes and then to a BytesIO object
    output_io = io.BytesIO()
    output_io.write(output_str.encode('utf-8'))
    output_io.seek(0)

    status.success("✅ File processed. Ready to download!")

    if st.download_button(
        label="📥 Download Converted File",
        data=output_io,
        file_name=f"converted_{uploaded_file.name}",
        mime="text/plain"
    ):
        # Trigger rerun to clear file upload UI (auto reset)
        st.experimental_rerun()
