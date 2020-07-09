import os
import argparse
import sys

__author__ = "Tijs Rozenbroek"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCOSIM lexicon preparation.")
    parser.add_argument("--src", help="fullatccdata.lst source directory")
    parser.add_argument("--dst", help="atcclexicon.txt file destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.src)), "Source directory not found"
    lst_src = os.path.join(args.src, "fullatccdata.lst")

    with open(lst_src) as lst_file:

        os.makedirs(args.dst, exist_ok=True)

        dst = os.path.join(args.dst, "atcclexicon.txt")
        sys.stdout.write("Processing...\n")
        sys.stdout.flush()

        with open(dst, "w") as dst_file:
            all_tokens = str(lst_file.read()).split()
            unique_tokens = sorted(set(all_tokens))
            for word in unique_tokens:

                new_line = str(word).rstrip() + " "
                for letter in list(word):
                    if letter != '\n':
                        if letter == '-' or letter == '_':
                            new_line += "| "
                        else:
                            new_line += letter + " "
                new_line += "|\n"
                dst_file.write(new_line)





