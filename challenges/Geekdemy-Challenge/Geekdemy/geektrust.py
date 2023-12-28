from sys import argv
from src.solution import Solution

def main():
    
    """
    Sample code to read inputs from the file

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()
    //Add your code here to process the input commands
    """
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    lines = f.readlines()
    
    solution = Solution(input_lines=lines)
    solution.process_input()
    solution.process_output()
    solution.print_output()

if __name__ == "__main__":
    main()