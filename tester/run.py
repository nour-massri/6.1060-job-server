import os
import shutil
import datetime
import subprocess
import glob
from multiprocessing import Pool
import sys

def process_file(args):
    file_path, i = args
    print(f"spawn file: {file_path}")
    command = f'make test TEST_FILE="{file_path}"'
    subprocess.run(command, shell=True, check=True)

def main(file_path, num_runs):
    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create the output directory
    output_dir = os.path.join("pgnout", date_time)
    os.makedirs(output_dir, exist_ok=True)

    # Extract just the file name without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Copy the input file to num_runs files
    file_paths = []
    for i in range(1, num_runs + 1):
        new_file = f"{base_name}_{i}.txt"
        new_path = os.path.join(output_dir, new_file)
        shutil.copy(file_path, new_path)
        file_paths.append((new_path, i))

    # Spawn num_runs processes to run the command on each file
    with Pool(num_runs) as pool:
        pool.map(process_file, file_paths)
    
    # At this point all processes have exited
    print("now: combined pgn analysis")

    # Combine all .pgn files into one
    pgn_files = glob.glob(os.path.join(output_dir, "*.pgn"))
    combined_pgn = os.path.join(output_dir, "combined.pgn")
    with open(combined_pgn, 'w') as outfile:
        for pgn_file in pgn_files:
            with open(pgn_file, 'r') as infile:
                outfile.write(infile.read())

    # Run command2 on the combined file and display the result
    result = subprocess.run(f"cd pgn/ && ./pgnrate.tcl ../{combined_pgn}", shell=True, capture_output=True, text=True, check=True)
    print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <number_of_runs>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    
    try:
        num_runs = int(sys.argv[2])
        if num_runs <= 0:
            raise ValueError("Number of runs must be a positive integer.")
    except ValueError as e:
        print(f"Error: Invalid number of runs. {str(e)}")
        sys.exit(1)
    
    main(file_path, num_runs)