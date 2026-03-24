#!/usr/bin/env python3
import os
import sys
import datetime
import subprocess

# 5x7 font dictionary (1 means commit, space means no commit)
FONT = {
    'A': [" 111 ", "1   1", "1   1", "11111", "1   1", "1   1", "1   1"],
    'B': ["1111 ", "1   1", "1   1", "1111 ", "1   1", "1   1", "1111 "],
    'C': [" 111 ", "1   1", "1    ", "1    ", "1    ", "1   1", " 111 "],
    'D': ["1111 ", "1   1", "1   1", "1   1", "1   1", "1   1", "1111 "],
    'E': ["11111", "1    ", "1    ", "1111 ", "1    ", "1    ", "11111"],
    'F': ["11111", "1    ", "1    ", "1111 ", "1    ", "1    ", "1    "],
    'G': [" 111 ", "1   1", "1    ", "1 111", "1   1", "1   1", " 111 "],
    'H': ["1   1", "1   1", "1   1", "11111", "1   1", "1   1", "1   1"],
    'I': ["11111", "  1  ", "  1  ", "  1  ", "  1  ", "  1  ", "11111"],
    'J': ["  111", "    1", "    1", "    1", "1   1", "1   1", " 111 "],
    'K': ["1   1", "1  1 ", "1 1  ", "11   ", "1 1  ", "1  1 ", "1   1"],
    'L': ["1    ", "1    ", "1    ", "1    ", "1    ", "1    ", "11111"],
    'M': ["1   1", "11 11", "1 1 1", "1   1", "1   1", "1   1", "1   1"],
    'N': ["1   1", "11  1", "1 1 1", "1  11", "1   1", "1   1", "1   1"],
    'O': [" 111 ", "1   1", "1   1", "1   1", "1   1", "1   1", " 111 "],
    'P': ["1111 ", "1   1", "1   1", "1111 ", "1    ", "1    ", "1    "],
    'Q': [" 111 ", "1   1", "1   1", "1   1", "1 1 1", "1  1 ", " 1111"],
    'R': ["1111 ", "1   1", "1   1", "1111 ", "1 1  ", "1  1 ", "1   1"],
    'S': [" 111 ", "1   1", "1    ", " 111 ", "    1", "1   1", " 111 "],
    'T': ["11111", "  1  ", "  1  ", "  1  ", "  1  ", "  1  ", "  1  "],
    'U': ["1   1", "1   1", "1   1", "1   1", "1   1", "1   1", " 111 "],
    'V': ["1   1", "1   1", "1   1", "1   1", "1   1", " 1 1 ", "  1  "],
    'W': ["1   1", "1   1", "1   1", "1   1", "1 1 1", "11 11", "1   1"],
    'X': ["1   1", "1   1", " 1 1 ", "  1  ", " 1 1 ", "1   1", "1   1"],
    'Y': ["1   1", "1   1", " 1 1 ", "  1  ", "  1  ", "  1  ", "  1  "],
    'Z': ["11111", "    1", "   1 ", "  1  ", " 1   ", "1    ", "11111"],
    '0': [" 111 ", "1  11", "1 1 1", "11  1", "1   1", "1   1", " 111 "],
    '1': ["  1  ", " 11  ", "  1  ", "  1  ", "  1  ", "  1  ", " 111 "],
    '2': [" 111 ", "1   1", "    1", "  11 ", " 1   ", "1    ", "11111"],
    '3': [" 111 ", "1   1", "    1", "  11 ", "    1", "1   1", " 111 "],
    '4': ["   1 ", "  11 ", " 1 1 ", "11111", "   1 ", "   1 ", "   1 "],
    '5': ["11111", "1    ", "1111 ", "    1", "    1", "1   1", " 111 "],
    '6': [" 111 ", "1    ", "1111 ", "1   1", "1   1", "1   1", " 111 "],
    '7': ["11111", "    1", "   1 ", "  1  ", "  1  ", "  1  ", "  1  "],
    '8': [" 111 ", "1   1", "1   1", " 111 ", "1   1", "1   1", " 111 "],
    '9': [" 111 ", "1   1", "1   1", " 1111", "    1", "    1", " 111 "],
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "]
}

def generate_commits(text, start_date, num_commits=5, repo_path='.'):
    # Ensure start_date is a Sunday (since GitHub graph columns start on Sunday)
    if start_date.weekday() != 6:
        days_to_subtract = (start_date.weekday() + 1)
        start_date -= datetime.timedelta(days=days_to_subtract)

    # Build the 2D array representation of the text
    grid = ["", "", "", "", "", "", ""]
    for char in text.upper():
        char_grid = FONT.get(char, FONT[' '])
        for i in range(7):
            grid[i] += char_grid[i] + " "
    
    rows = 7
    cols = len(grid[0])
    
    current_date = start_date
    os.chdir(repo_path)
    
    if not os.path.exists(".git"):
         subprocess.run(["git", "init"], check=True)
    
    print(f"Drawing '{text}' starting from {start_date.strftime('%Y-%m-%d')} (Sunday)...")
    
    data_file = "commit_data.txt"
    
    # Iterate through columns (weeks), then rows (days of the week)
    for col in range(cols):
        for row in range(rows):
            if col < len(grid[row]) and grid[row][col] == '1':
                # Create dated commits
                date_str = current_date.strftime("%Y-%m-%dT12:00:00")
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = date_str
                env['GIT_COMMITTER_DATE'] = date_str
                
                # Make multiple commits to make the color darker on the chart
                for i in range(num_commits):
                    with open(data_file, "a") as f:
                        f.write(f"Commit {i} for {char} at {date_str}\n")
                    subprocess.run(["git", "add", data_file], check=True)
                    subprocess.run(["git", "commit", "-m", f"Draw {text} - pixel {col},{row}"], env=env, stdout=subprocess.DEVNULL, check=True)
            # Move to the next day
            current_date += datetime.timedelta(days=1)
            
    print("Execution complete.")
    print("You can verify the commits created with 'git log' and then push:")
    print("  git push -u origin master")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate GitHub contribution graph text by creating dated commits.")
    parser.add_argument("text", type=str, help="The text to draw (A-Z, 0-9, space).")
    parser.add_argument("--start-date", type=str, default=None, help="Start date in YYYY-MM-DD format. Defaults to 52 weeks ago.")
    parser.add_argument("--commits", type=int, default=5, help="Number of commits per active pixel (default 5). Higher means darker green.")
    
    args = parser.parse_args()
    
    if args.start_date:
        start = datetime.datetime.strptime(args.start_date, "%Y-%m-%d")
    else:
        # Default to ~1 year ago
        start = datetime.datetime.now() - datetime.timedelta(days=365)
        
    generate_commits(args.text, start, args.commits)
