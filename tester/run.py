import os
import shutil
from datetime import datetime

def create_dated_directory_and_process(file_path):
    # Get current date and time
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d_%H%M%S")
    
    # Create directory name
    dir_name = f"{date_time_str}_{os.path.basename(file_path)}"
    
    # Create the directory
    os.makedirs(dir_name, exist_ok=True)
    
    # Copy the file into the new directory
    shutil.copy2(file_path, os.path.join(dir_name, os.path.basename(file_path)))
    
    # # Change working directory to the new directory
    # os.chdir(dir_name)
    
    # Run the tests and create output files
    num_processes = 50
    for i in range(num_processes):
        output_file = f"./{dir_name}/output_{i}.txt"
        command = f"make test TEST_FILE=\"{os.path.basename(file_path)}\" > {output_file}"
        os.system(command)
    
    print(f"All tests completed. Output files are in the directory: {dir_name}")
    
    # Parse and rank move prefixes
    # parse_and_rank_moves()

def parse_and_rank_moves():
    move_prefixes = defaultdict(int)
    game_pattern = re.compile(r'\[Event.*?\n\n(.*?)\n\n', re.DOTALL)
    move_pattern = re.compile(r'\d+\.\s(\S+)\s+(\S+)')

    for filename in os.listdir('.'):
        if filename.startswith('output_') and filename.endswith('.txt'):
            with open(filename, 'r') as file:
                content = file.read()
                games = game_pattern.findall(content)
                
                for game in games:
                    moves = move_pattern.findall(game)
                    for i in range(1, len(moves) + 1):
                        prefix = ' '.join([move for pair in moves[:i] for move in pair])
                        move_prefixes[prefix] += 1

    # Write sorted prefixes to the output file
    with open('move_prefixes_ranking.txt', 'w') as file:
        for prefix, count in sorted(move_prefixes.items(), key=lambda x: (-x[1], x[0])):
            file.write(f"{count}: {prefix}\n")

    print("Ranking of move prefixes has been written to move_prefixes_ranking.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <configuration_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    create_dated_directory_and_process(file_path)
