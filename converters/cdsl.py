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

def get_output_filename(input_file):
    """Generate output filename by adding 'output_' prefix to input filename"""
    import os
    dirname = os.path.dirname(input_file)
    basename = os.path.basename(input_file)
    return os.path.join(dirname, f"output_{basename}")  # Fixed the order of arguments

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
    """Process input content and generate formatted CDSL output file"""
    try:
        # Import datetime for dynamic timestamp
        from datetime import datetime

        # Split content into non-empty lines
        lines = [line for line in input_content.strip().split('\n') if line.strip()]
        if not lines:
            return None

        # Initialize output content as list
        output_content = []
        output_header = 'EVSN~MemberID~Member Name~No. of Shares~Resolution Number~Number of votes For~Number of votes Against~Number of votes Abstain~Status~Entity Voted~User ID~Date of voting'
        output_content.append(output_header)
        
        # Process voting data lines
        for line in lines:
            if '=' in line:
                primary_parts = line.split('=')
                if len(primary_parts) == 2:
                    secondary_parts = primary_parts[1].split('~')
                    if len(secondary_parts) >= 6:  # Need at least 6 parts
                        evsn = secondary_parts[0]          # EVSN
                        member_id = secondary_parts[1]     # Member ID
                        resolution_number = secondary_parts[2]  # Get resolution number from first part
                        
                        # Get the three share positions
                        share_positions = [
                            float(secondary_parts[3] or 0),  # FOR
                            float(secondary_parts[4] or 0),  # AGAINST
                            float(secondary_parts[5] or 0)   # ABSTAIN
                        ]
                        
                        # Format total shares (sum of all positions)
                        total_shares = sum(share_positions)
                        shares_formatted = f"{total_shares:.3f}"
                        
                        # Format each position with 3 decimal places
                        votes_for = f"{share_positions[0]:.3f}"
                        votes_against = f"{share_positions[1]:.3f}"
                        votes_abstain = f"{share_positions[2]:.3f}"
                        
                        # Generate current timestamp
                        current_time = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
                        
                        vote_line = "~".join([
                            evsn,                   # EVSN
                            member_id,              # Member ID
                            "ABC",                  # Member Name (hardcoded)
                            shares_formatted,       # No. of Shares
                            resolution_number,      # Resolution Number from input
                            votes_for,             # Number of votes For
                            votes_against,         # Number of votes Against
                            votes_abstain,         # Number of votes Abstain
                            "VALID",               # Status
                            "CUSTODIAN",           # Entity Voted
                            "ST(7777)-SUMIT TANK", # User ID
                            current_time           # Dynamic timestamp
                        ])
                        output_content.append(vote_line)

        # Write to output file
        final_content = "\n".join(output_content)
        with open(output_filename, 'w') as outfile:
            outfile.write(final_content)
        
        print(f"Output file '{output_filename}' created successfully.")
        return final_content

    except Exception as e:
        print(f"Error processing file: {e}")
        return None

if __name__ == "__main__":
    
    path = r"\\192.168.3.250\ses\Client Management\Custodian & Portal - IT Related\Vote & Respsone file Formats\CDSL" # No trailing slash needed with os.path.join
    file_name = 'INE854D01024_PBL_20062025_CDSL.txt'
   
    input_file = os.path.join(path, file_name)

    output_file = get_output_filename(input_file)
    
    if content := read_file_whole(input_file):
        if processed_content := process_and_write_output(content, output_file):
            compare_files(input_file, output_file)