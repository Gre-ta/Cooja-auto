import argparse
import csv
import re

def parse_line(line):
    """
    Parses a line of the input log file to extract the required fields.
    """
    pattern = re.compile(r'(\d+)\s+(\d+)\s+CPU\s+(\d+)s LPM\s+(\d+)s DEEP LPM\s+(\d+)s\s+Total time (\d+)s')
    match = pattern.match(line)
    if match:
        return {
            'time': match.group(1),
            'mote': match.group(2),
            'cpu': match.group(3),
            'lpm': match.group(4),
            'deeplpm': match.group(5),
            'total': match.group(6),
        }
    else:
        return None

def process_file(input_log, output_csv):
    """
    Processes the input log file and writes the extracted information into a CSV file.
    """
    with open(input_log, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        fieldnames = ['time', 'mote', 'cpu', 'lpm', 'deeplpm', 'total']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for line in infile:
            parsed_line = parse_line(line)
            if parsed_line:
                writer.writerow(parsed_line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process log files into CSV format.')
    parser.add_argument('input_log', type=str, help='The input log file path.')
    parser.add_argument('output_csv', type=str, help='The output CSV file path.')

    args = parser.parse_args()
    
    process_file(args.input_log, args.output_csv)
