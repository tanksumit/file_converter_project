import os
import pandas as pd
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

            max_lines = max(len(input_lines), len(output_lines))
            for i in range(max_lines):
                input_line = input_lines[i].strip() if i < len(input_lines) else ""
                output_line = output_lines[i].strip() if i < len(output_lines) else ""
                print(f"{input_line:50} | {output_line:50}")

            print("=" * 100)
    except Exception as e:
        print(f"Error during comparison: {e}")


def process_and_write_output(input_content, output_filename):
    """Convert CDSL vote format and save to output file"""
    try:
        lines = [line for line in input_content.strip().split('\n') if line.strip()]
        if not lines:
            return None

        output_lines = ['EVSN~MemberID~Member Name~No. of Shares~Resolution Number~Number of votes For~Number of votes Against~Number of votes Abstain~Status~Entity Voted~User ID~Date of voting']

        for line in lines:
            if '=' in line:
                left, right = line.split('=')
                parts = right.split('~')
                if len(parts) >= 6:
                    evsn = parts[0]
                    member_id = parts[1]
                    resolution_number = left.split('~')[-1]

                    votes = [float(parts[3] or 0), float(parts[4] or 0), float(parts[5] or 0)]
                    total_shares = sum(votes)

                    current_time = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

                    row = "~".join([
                        evsn,
                        member_id,
                        "ABC",
                        f"{total_shares:.3f}",
                        resolution_number,
                        f"{votes[0]:.3f}",
                        f"{votes[1]:.3f}",
                        f"{votes[2]:.3f}",
                        "VALID",
                        "CUSTODIAN",
                        "ST(7777)-SUMIT TANK",
                        current_time
                    ])
                    output_lines.append(row)

        with open(output_filename, 'w') as f:
            f.write("\n".join(output_lines))

        print(f"Output file '{output_filename}' created successfully.")
        return "\n".join(output_lines)

    except Exception as e:
        print(f"Error processing file: {e}")
        return None


def convert(file_path: str) -> str:
    """Placeholder for Excel-based conversion (not used in this version)"""
    df = pd.read_excel(file_path)
    output_path = file_path.replace(".xlsx", "_converted.xlsx")
    df.to_excel(output_path, index=False)
    return output_path


def convert_uploaded_file(uploaded_file):
    input_content = uploaded_file.read().decode('utf-8')
    output_filename = f"output_{uploaded_file.name}"
    result = process_and_write_output(input_content, output_filename)
    return output_filename if result else None


if __name__ == "__main__":
    path = r"\\192.168.3.250\ses\Client Management\Custodian & Portal - IT Related\Vote & Respsone file Formats\CDSL"
    file_name = 'INE854D01024_PBL_20062025_CDSL.txt'

    input_file = os.path.join(path, file_name)
    output_file = get_output_filename(input_file)

    content = read_file_whole(input_file)
    if content:
        processed = process_and_write_output(content, output_file)
        if processed:
            compare_files(input_file, output_file)
