import sys
import runpy
import os

def main():
    """
    Runs a specified Python file from the command line.
    """
    if len(sys.argv) > 1:
        file_to_run = sys.argv[1]
        if not file_to_run.endswith('.py'):
            file_to_run += '.py'

        if os.path.exists(file_to_run):
            print(f"Running {file_to_run}...")
            try:
                runpy.run_path(path_name=file_to_run)
            except Exception as e:
                print(f"An error occurred while running {file_to_run}: {e}")
        else:
            print(f"Error: File '{file_to_run}' not found.")
    else:
        print("Please specify which file to run.")
        print("Example: python main.py 01_04_keyword_search")


if __name__ == "__main__":
    main()
