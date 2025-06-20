import os
from datetime import datetime


def read_file_whole(filename):
    """Read and return file contents""" 
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error occurred: {e}")
    return None


def get_output_filename(input_file):
    """Generate output filename by adding 'output_' prefix to input filename"""
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    return os.path.join(dirname, f"output_{basename}")


def process_and_write_output(input_content, output_filename):
    """Process input content and generate formatted NSDL output file"""
    try:
        lines = [line for line in input_content.strip().split('\n') if line.strip()]
        if not lines:
            return None

        output_content = [lines[0]]  # First line remains as-is

        # Process header
        header = lines[1].split('^')
        if len(header) < 7:
            print("Invalid header line.")
            return None

        header_output = "##".join([
            header[0],  # batch_id
            header[1],  # header_id
            header[2],  # dp_id
            header[4],  # event_id
            header[5],  # date
            header[6]   # time
        ])
        output_content.append(header_output)

        # Process vote lines
        for line in lines[2:]:
            parts = line.split('^')
            if len(parts) >= 7:
                vote_line = "##".join([
                    parts[0],    # batch_id
                    parts[1],    # row_id
                    parts[3],    # dp_id
                    parts[5],    # resolution_no
                    parts[6],    # vote
                    "A",         # vote position
                    "0"          # hardcoded
                ])
                output_content.append(vote_line)

        output_content.append("{}")

        final_content = "\n".join(output_content)
        with open(output_filename, 'w') as outfile:
            outfile.write(final_content)

        print(f"Output file '{output_filename}' created successfully.")
        return output_filename

    except Exception as e:
        print(f"Error processing file: {e}")
        return None


def convert_uploaded_file(uploaded_file):
    """Handle Streamlit uploaded file and process it"""
    try:
        input_content = uploaded_file.read().decode('utf-8')
        output_filename = f"output_{uploaded_file.name}"
        result = process_and_write_output(input_content, output_filename)
        return output_filename if result else None
    except Exception as e:
        print(f"Error in convert_uploaded_file: {e}")
        return None


# Optional main test entry (for local dev, not needed in Streamlit)
if __name__ == "__main__":
    path = r"\\192.168.3.250\ses\Client Management\Custodian & Portal - IT Related\Vote & Respsone file Formats\NSDL"
    file_name = 'VOTE_HDFC_133721_Bharat Forge Limited_NSDL.txt'
    input_file = os.path.join(path, file_name)
    output_file = get_output_filename(input_file)

    if content := read_file_whole(input_file):
        if processed_content := process_and_write_output(content, output_file):
            print("NSDL file processed.")
