import subprocess
import os
import re


def update_csc_transmitting_range(csc_file_path, transmitting_range):
    with open(csc_file_path, 'r') as csc_file:
        csc_content = csc_file.read()


    # Update the transmitting_range in the csc_content
    updated_csc_content = re.sub(r'<transmitting_range>\d+\.\d+</transmitting_range>', f'<transmitting_range>{transmitting_range}</transmitting_range>', csc_content)


    with open(csc_file_path, 'w') as csc_file:
        csc_file.write(updated_csc_content)


script_directory = os.path.dirname(os.path.abspath(__file__))
contiki_ng_directory = os.path.abspath(os.path.join(script_directory, "..", ".."))


cooja_directory = os.path.join(contiki_ng_directory, "tools", "cooja")
csc_file_path = os.path.join(cooja_directory, "Example1.csc")
testlog_path = os.path.join(cooja_directory, "COOJA.testlog")
output_folder = os.path.join(cooja_directory, "filtered_logs")




# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


# Define the range of transmitting values
transmitting_range_values = [25, 50, 75, 100, 125, 150]




for transmitting_range in transmitting_range_values:
    # Update the csc file with the current transmitting range
    update_csc_transmitting_range(csc_file_path, transmitting_range)




    # Run the simulation
    try:
        subprocess.run(["./gradlew", "run", f"--args='--no-gui {csc_file_path}'"], check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


    # Read the entire testlog file
    with open(testlog_path, 'r') as log_file:
        lines = log_file.readlines()


    # Define a regular expression pattern for matching the desired lines
    pattern = re.compile(r'^\d+\s+\d+\s+CPU\s+\d+s\s+LPM\s+\d+s\s+DEEP LPM\s+\d+s\s+Total time \d+s$')


    # Filter lines that match the pattern
    filtered_lines = [line.strip() for line in lines if pattern.match(line)]


    # Save filtered lines to a new file with the name of the transmitting range value
    output_file_name = os.path.join(output_folder, f"{transmitting_range}.txt")
    with open(output_file_name, 'w') as output_file:
        output_file.write('\n'.join(filtered_lines))


    print(f"Filtered log file for transmitting range {transmitting_range} saved to: {output_file_name}")
