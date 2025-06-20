import os

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

def format_date(date_str):
    """Convert date from YYYYMMDD to YYYY-MM-DD format"""
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}" if len(date_str) == 8 else date_str

def get_output_filename(input_file):
    """Generate output filename by adding 'output_' prefix to input filename"""
    import os
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    return os.path.join(dirname, f"output_{basename}")

def compare_files(input_file, output_file):
    """Display input and output file contents side by side"""
    try:
        with open(input_file, 'r') as infile, open(output_file, 'r') as outfile:
            input_lines = infile.readlines()
            output_lines = outfile.readlines()
            
            print("\nFile Comparison:")
            print("=" * 100)
            print(f"{'INPUT':50} | {'OUTPUT':50}")
            print("=" * 100)
            
            # Use max length to handle files of different lengths
            max_lines = max(len(input_lines), len(output_lines))
            for i in range(max_lines):
                input_line = input_lines[i].strip() if i < len(input_lines) else ""
                output_line = output_lines[i].strip() if i < len(output_lines) else ""
                print(f"{input_line:50} | {output_line:50}")
            
            print("=" * 100)
    except Exception as e:
        print(f"Error during comparison: {e}")

def process_and_write_output(input_content, output_filename):
    """Process input content and generate formatted output file"""
    try:
        # Split content into non-empty lines
        lines = [line for line in input_content.strip().split('\n') if line.strip()]
        if not lines:
            return None

        # Initialize output content with first line
        output_content = [lines[0]]  # First line as is
        
        # Process header line
        header = lines[1].split('^')
        header_output = "##".join([
            header[0],  # batch_id
            header[1],  # header_id
            header[2],  # dp_id
            # header[3],  # rows
            header[4],  # event_id
            header[5],  # date
            header[6]   # time
        ])
        output_content.append(header_output)

        # Process voting data lines
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
                    "0"         # hardcoded value
                ])
                output_content.append(vote_line)

        # Add closing brackets with proper formatting
        output_content.append("{}")

        # Write to output file using the generated filename
        final_content = "\n".join(output_content)
        with open(output_filename, 'w') as outfile:
            outfile.write(final_content)
        
        print(f"Output file '{output_filename}' created successfully.")
        return final_content

    except Exception as e:
        print(f"Error processing file: {e}")
        return None

if __name__ == "__main__":
    
    path = r"\\192.168.3.250\ses\Client Management\Custodian & Portal - IT Related\Vote & Respsone file Formats\NSDL" # No trailing slash needed with os.path.join
    file_name = 'VOTE_HDFC_133721_Bharat Forge Limited_NSDL.txt'
   
    input_file = os.path.join(path, file_name)
    
    output_file = get_output_filename(input_file)
    
    if content := read_file_whole(input_file):
        if processed_content := process_and_write_output(content, output_file):
            # Compare input and output files
            compare_files(input_file, output_file)