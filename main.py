"""Simple check script: the repo has been cloned and the program runs."""

from datetime import datetime


def main():
    print("The repo has been cloned and the program works!")
    print(f"Run at: {datetime.now()}")


if __name__ == "__main__":
    main()