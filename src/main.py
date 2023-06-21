import argparse
import os
from glob import glob, iglob
from os.path import isdir, isfile

def is_file(filename:str):
    print("you have to pass a directory as the argument because I don't think it makes sense to try and implement a signle file branch for this tool.")

def is_dir(dir:str, recursive:bool=False):
    tabs = 0
    lines = process_dir(dir, lines=[], recursive=recursive, tabs=tabs)
    with open(f"{dir}/SUMMARY.md", "w") as summary:
        summary.writelines(lines)

def process_dir(dir, lines:list, recursive:bool=False, tabs=0):
    names = glob(f"{dir}/*")
    indent = " " * tabs * 4
    for name in names:
        if os.path.isdir(name):
            dir = os.path.basename(name)
            lines.append(f"{indent}- [{dir.replace('-', ' ').title()}]({dir}/README.md)\n")
            if recursive:
                print(f"recursing into '{name}'")
                tabs += 1
                lines.extend(process_dir(name, [], recursive=recursive, tabs=tabs))
                tabs -= 1
                continue
            continue
        if os.path.basename(name) == "SUMMARY.md":
            continue
        title = os.path.basename(name)[:-3].replace("-", " ").title()
        lines.append(f"{indent}- [{title}]({name})\n")
    return lines



def main():
    parser = argparse.ArgumentParser(prog="Auto-SUMMARYmd", description="Command-line utility to automate adding markdown files and folders to mdbook SUMMARY.md")
    parser.add_argument("filename", help="The file or directory that you want to add to SUMMARY.md")
    parser.add_argument("-d", "--directory", help="Explicitly call the utility on a Directory. This will create an error if you pass a filename.", action="store_true")
    parser.add_argument("-r", "--recursive", action='store_true', help="Recursively search and add all subdirectories to the SUMMARY.md")
    # parser.add_argument("-w", "--words", help="Print the number of words in the file", action="store_true")
    # parser.add_argument("-c", "--characters", help="Print the number of characters in the file", action="store_true")
    args = parser.parse_args()

    if isdir(args.filename) or args.directory:
        assert not isfile(args.filename)
        return is_dir(args.filename, args.recursive)
    if isfile(args.filename):
        return is_file(args.filename)
    
    

if __name__ == "__main__":
    main()
