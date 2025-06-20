import streamlit as st
import os
from converters import cdsl, nsdl  # add other imports as you complete them

# Mapping
converter_map = {
    "CDSL": cdsl,
    "NSDL": nsdl,
    # "LinkIntime": linkintime,
    # "Karvy": karvy,
    # "Pruva": pruva,
    # "Bigshare": bigshare,
}

st.set_page_config(page_title="File Converter", layout="centered")
st.title("🗃️ Voting File to Response File Converter")

selected_type = st.selectbox("Select File Type", list(converter_map.keys()))
uploaded_file = st.file_uploader("Upload your file", type=["txt", "xlsx"])

if uploaded_file:
    st.info(f"📂 File uploaded. Processing as `{selected_type}`...")

    # Call the appropriate convert function from the selected module
    try:
        output_path = converter_map[selected_type].convert_uploaded_file(uploaded_file)

        if output_path and os.path.exists(output_path):
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Download Converted File", f, file_name=os.path.basename(output_path), mime="text/plain")

            # Delete output file after download (optional, but better for cleanup)
            os.remove(output_path)
        else:
            st.error("⚠️ Conversion failed. Output file not found.")
    except Exception as e:
        st.error(f"❌ Error during conversion: {e}")
