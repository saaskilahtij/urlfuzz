from mutator import url_mutator
from typing import List
import argparse
import os
import sys
import subprocess


def main():
    args = parse_args()
    corpuses = read_corpuses(args.i)
    target = args.c.split()
    output_folder = args.o
    crash_dir = f'{args.o}/crashes'
    hang_dir = f'{args.o}/hangs'
    if not os.path.isdir(hang_dir):
        os.makedirs(hang_dir)
    if not os.path.isdir(crash_dir):
        os.makedirs(crash_dir)

    fuzz_index = 1
    for i in range(0,len(target)):
        if target[i] == "FUZZ":
            fuzz_index = i
    count = 0    
    print("Fuzzing...")
    while True:
        for corpus in corpuses:
            try:
                target[fuzz_index] = url_mutator(corpus)
                result = subprocess.run(target, capture_output=True, check=True, text=True)
                count += 1
            except KeyboardInterrupt:
                sys.exit(0)
            except subprocess.TimeoutExpired:
                print(f"Caused a hang, written to {args.o}/hangs/hang{count}.txt")
                with open(f"{args.o}/hangs/hang{count}.txt", "w") as f:
                    f.write(target[fuzz_index])
                    f.close()
            except subprocess.CalledProcessError:
                print(f"Caused a crash, written to {args.o}/hangs/crash{count}.txt")
                with open(f"{args.o}/crashes/crash{count}.txt", "w") as f:
                    f.write(target[fuzz_index])
                    f.close()

# Parses arguments
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", 
                        type=str, 
                        help="The folder where the input files are specified")
    parser.add_argument("-c",
                        type=str,
                        help="A command to run the target program add FUZZ where fuzzing is needed")

    parser.add_argument("-o",
                        type=str,
                        help="The folder where the output files get written")

    return parser.parse_args()

# Reads corpuses from the specified input file
def read_corpuses(directory: str) -> List[str]:
    corpuses= []
    for file in os.listdir(directory):
        with open(f"{directory}/{file}", "r") as f:
            corpuses.append(f.readline().rstrip())
            
    f.close()
    return corpuses


if __name__ == '__main__':
    main()
