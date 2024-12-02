import subprocess
import os
import shutil

script_directory = os.path.dirname(os.path.abspath(__file__))
contiki_ng_directory = os.path.abspath(os.path.join(script_directory, "..", ".."))

cooja_directory = os.path.join(contiki_ng_directory, "tools", "cooja")
csc_file_path = os.path.join(cooja_directory, "tsch_10m.csc")
testlog_path = os.path.join(cooja_directory, "COOJA.testlog")

os.chdir(cooja_directory)


try:
    subprocess.run(["./gradlew", "run", f"--args='--no-gui {csc_file_path}'"], check=True, shell=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

# Reading the content of the test log file
try:

    with open(testlog_path, 'r') as testlog_file:
        testlog_content = testlog_file.read()
except FileNotFoundError:
    print("Test log file not found.")
    exit(1)

# Constructing the destination directory path
destination_directory = "/home/vagrant/contiki-ng/tools/cooja/LogFiles/"


# Checking if the destination directory exists
if os.path.exists(destination_directory):
    # Constructing the new filename
    csc_filename_without_extension = os.path.splitext(os.path.basename(csc_file_path))[0]
    new_filename = f"{csc_filename_without_extension}.testlog"
    new_filepath = os.path.join(destination_directory, new_filename)
    
    # Writing the content to the new test log file
    try:
        with open(new_filepath, 'w') as new_testlog_file:
            new_testlog_file.write(testlog_content)
        print(f"Test log file copied to {new_filepath}")
    except IOError as e:
        print(f"Error writing to the new test log file: {e}")
else:
    print("Destination folder not found. Unable to copy.")
