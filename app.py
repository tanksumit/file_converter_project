import streamlit as st
import os
import tempfile
from converters import cdsl, nsdl #, linkintime, karvy, pruva, bigshare

# Mapping
converter_map = {
    "CDSL": cdsl,
    "NSDL": nsdl,
#     "LinkIntime": linkintime,
#     "Karvy": karvy,
#     "Pruva": pruva,
#     "Bigshare": bigshare,
}

st.set_page_config(page_title="File Converter", layout="centered")

st.title("🗃️ Voting File to Response File Converter")
selected_type = st.selectbox("Select File Type", list(converter_map.keys()))

uploaded_file = st.file_uploader("Upload your file", type=["txt", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name[-5:]) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    st.info(f"File uploaded. Processing as `{selected_type}`...")

    try:
        output_path = converter_map[selected_type].convert(temp_file_path)
        with open(output_path, "rb") as f:
            st.download_button("Download Converted File", f, file_name=os.path.basename(output_path))

        # Cleanup after download
        os.remove(temp_file_path)
        os.remove(output_path)
    except Exception as e:
        st.error(f"Error during conversion: {e}")
