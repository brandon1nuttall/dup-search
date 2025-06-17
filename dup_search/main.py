import sys

from .image_duplicates import DuplicateDetection

def main():
    delete_dups = False
    hash_size = 32
    d_index = None
    hash_size_index = None

    args = sys.argv[1:]

    commands = [arg for arg in args if arg.startswith("-")]

    if "-i" not in commands or args[0] != "-i":
        raise ValueError("Target directories must follow '-i' and it must be the first arg")

    if "-d" in commands:
        d_index = args.index("-d")
        delete_dups = True

    if "-hash_size" in commands:
        hash_size_index = args.index("-hash_size")
        hash_size = args[hash_size_index+1]

    if d_index and hash_size_index:
        target_dirs = args[1:min(d_index, hash_size_index)]
    elif d_index:
        target_dirs = args[1:d_index]
    elif hash_size_index:
        target_dirs = args[1:hash_size_index]
    else:
        target_dirs = args[1:]

    if len(target_dirs) < 1:
        raise ValueError("There must be target directories to search through")

    detector = DuplicateDetection(target_dirs, hash_size, delete_dups)
    detector.run()

if __name__ == "__main__":
    main()