import os
import argparse
import sys

__author__ = "Tijs Rozenbroek"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCOSIM lexicon preparation.")
    parser.add_argument("--src", help="wordlist.txt source directory")
    parser.add_argument("--dst", help="atcosimlexicon.txt file destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.src)), "Source directory not found"
    txt_src = os.path.join(args.src, "wordlist.txt")

    with open(txt_src) as txt_file:

        os.makedirs(args.dst, exist_ok=True)

        dst = os.path.join(args.dst, "atcosimlexicon.txt")
        sys.stdout.write("Processing...\n")
        sys.stdout.flush()

        with open(dst, "w") as dst_file:
            for word in txt_file.readlines():
                word = word.replace('[EMPTY]', '')
                word = word.replace('[FRAGMENT]', '')
                word = word.replace('[UNKNOWN]', '[UNINTELLIGIBLE]')
                # word = word.replace('[NONSENSE]', '')
                word = word.replace('[HNOISE]', '[SPEAKER]')
                word = word.replace('<OT>', '')
                word = word.replace('</OT>', '')
                word = word.replace('<FL>', '[NOTENG]')
                word = word.replace('</FL>', '')
                word = word.replace('@', '')
                word = word.replace('=', '')
                word = word.replace('~', '')

                new_line = str(word).rstrip() + " "
                for letter in list(word):
                    if letter != '\n':
                        new_line += letter + " "
                new_line += "|\n"
                if new_line != " |\n":
                    dst_file.write(new_line)

    



