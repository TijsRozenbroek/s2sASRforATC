import os
import argparse
import sys
import csv
import numpy as np
import random

__author__ = "Tijs Rozenbroek"

def shuffle_and_write(lines):
    random.Random(15400031944529420895).shuffle(lines)
    train_val_test = np.split(lines, [int(.8 * len(lines)), int(.9 * len(lines))])
    arrays = ["atcosimtrainlines", "atcosimvalidlines", "atcosimtestlines"]
    for i in range(3):
        dst_file_name = arrays[i] + ".txt"
        dst = os.path.join(args.dst, dst_file_name)
        with open(dst, "w") as dst_file:
            for line in train_val_test[i]:
                if line != '':
                    dst_file.write(f"{line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCOSIM dataset preparation.")
    parser.add_argument("--src", help="fulldata.csv source directory")
    parser.add_argument("--dst", help=".lst file destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.src)), "fulldata.csv source directory not found"
    csv_src = os.path.join(args.src, "fulldata.csv")

    with open(csv_src) as csv_file:
        csv_reader = csv.reader(csv_file)

        os.makedirs(args.dst, exist_ok=True)

        sys.stdout.write("Processing...\n")
        sys.stdout.flush()

        lines = []

        row_nr = 0
        for row in csv_reader:
            if row_nr == 0:
                column_names = row
                row_nr += 1
            else:
                transcription = row[6]

                transcription = transcription.replace('[EMPTY]', '')
                transcription = transcription.replace('[FRAGMENT]', '')
                transcription = transcription.replace('[UNKNOWN]', 'U')
                transcription = transcription.replace('[HNOISE]', 'S')
                transcription = transcription.replace('[NONSENSE]', 'O')
                transcription = transcription.replace('<OT>', '')
                transcription = transcription.replace('</OT>', '')
                transcription = transcription.replace('<FL>', 'E')
                transcription = transcription.replace('</FL>', '')
                transcription = transcription.replace('@', '')
                transcription = transcription.replace('=', '')
                transcription = transcription.replace('~', '')
                transcription = transcription.rstrip()
                transcription = transcription.lstrip()

                lines.append(transcription)

    shuffle_and_write(lines)

