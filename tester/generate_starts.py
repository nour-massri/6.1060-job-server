import os
import re
from collections import defaultdict

def parse_moves(directory):
    move_prefixes = defaultdict(int)
    arrays = []
    for filename in os.listdir(directory):
        if not (filename.startswith('test_') and filename.endswith('.pgn')):
            continue
        with open(os.path.join(directory, filename), 'r') as file:
            content = file.read()

        # Split the content into individual games
        games = re.split(r'\n\n(?=\[Event)', content)

        for game in games:
            # Extract game metadata
            metadata = {}
            for line in game.split('\n'):
                if line.startswith('['):
                    key, value = re.match(r'\[(\w+)\s+"(.+)"\]', line).groups()
                    metadata[key] = value

            # Extract the moves section
            moves_section = re.search(r'\n\n(1\..*)', game, re.DOTALL)
            if not moves_section:
                continue

            moves_text = moves_section.group(1)

            # Parse individual moves
            move_pattern = re.compile(r'(\d+)\.\s(\S+)\s(\{[^}]+\})\s(\S+)\s(\{[^}]+\})')
            moves = move_pattern.findall(moves_text)

            parsed_moves = []

            for move in moves:
                move_number, white_move, white_stats, black_move, black_stats = move
                parsed_moves.append(white_move)
                parsed_moves.append(black_move)
            
            arrays.append(parsed_moves)
        
    return arrays

def rank_moves(arrays):
    prefix_counts = defaultdict(int)
    
    for array in arrays:
        for i in range(1, len(array) + 1):
            prefix = tuple(array[:i])
            prefix_counts[prefix] += 1
    
    sorted_prefixes = sorted(prefix_counts.items(), key=lambda x: (-x[1], x[0]))
    # for i in range(50):
    #     print(sorted_prefixes[i])
    return sorted_prefixes

import os
import subprocess

def create_openbook(sorted_prefixes):
    # Create the openbook directory
    openbook_dir = 'openbook'
    os.makedirs(openbook_dir, exist_ok=True)

    # Process the top 500 prefixes (or all if less than 500)
    for i, (prefix, count) in enumerate(sorted_prefixes[:50], start=1):
        filename = os.path.join(openbook_dir, f'input_{i}.txt')
        
        with open(filename, 'w') as f:
            # Write each move in the prefix
            for move in prefix:
                f.write(f'move {move}\n')
            
            # Add the last two lines
            f.write('go depth 11\n')
            f.write('quit\n')
        
        # Run nohup command for each file
        input_file = f'input_{i}.txt'
        output_file = f'output_{i}.txt'
        nohup_command = f'nohup ./leiserchess ./openbook/{input_file} > ./openbook/{output_file} 2>&1 &'
        subprocess.Popen(nohup_command, shell=True)

    print(f"Created openbook files in the '{openbook_dir}' directory and started nohup processes.")

# Example usage:
# sorted_prefixes = [(('d2U', 'b5U', 'a3b4', 'b7R', 'd0R', 'e4d3'), 17), ...]
# create_openbook(sorted_prefixes)

# Example usage:
# parse_and_rank_moves('/path/to/your/directory')
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_starts.py <directory>")
        sys.exit(1)

    dir = sys.argv[1]
    arrays = parse_moves(dir)
    sorted_prefixes = rank_moves(arrays)
    create_openbook(sorted_prefixes)