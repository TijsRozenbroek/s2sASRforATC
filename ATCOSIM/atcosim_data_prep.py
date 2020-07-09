import os
import argparse
import sys
import csv
import numpy as np
import random


def shuffle_and_write(lines):
    random.Random(15400031944529420895).shuffle(lines)
    train_val_test = np.split(lines, [int(.8 * len(lines)), int(.9 * len(lines))])
    arrays = ["atcosimtrain", "atcosimvalid", "atcosimtest"]
    for i in range(3):
        dst_file_name = arrays[i] + ".lst"
        dst = os.path.join(args.dst, dst_file_name)
        with open(dst, "w") as dst_file:
            for line in train_val_test[i]:
                dst_file.write(f"{line}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCOSIM dataset preparation.")
    parser.add_argument("--csvsrc", help="fulldata.csv source directory")
    parser.add_argument("--datasrc", help="Audio data source directory")
    parser.add_argument("--dst", help=".lst file destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.csvsrc)), "fulldata.csv source directory not found"
    assert os.path.isdir(str(args.datasrc)), "Audio data source directory not found"
    csv_src = os.path.join(args.csvsrc, "fulldata.csv")

    with open(csv_src) as csv_file:
        csv_reader = csv.reader(csv_file)

        os.makedirs(args.dst, exist_ok=True)

        dst = os.path.join(args.dst, "fulldata.lst")
        sys.stdout.write("Processing...\n")
        sys.stdout.flush()
       
        lines = []
        
        row_nr = 0
        for row in csv_reader:
            if row_nr == 0:
                column_names = row
                print(f'Column names are {", ".join(row)}')
                row_nr += 1
            else:
                filename = row[2]
                subdir = filename.split("_", 1)[0]
                subsubdir = subdir + "_" + filename.split("_", 2)[1]
                end_of_subdir = os.path.join(subdir, subsubdir)
                file_location = os.path.join(args.datasrc, os.path.join(end_of_subdir, filename) + ".wav")
                length_ms = round((float(row[9]) * 1000), 3)
                transcription = row[6]

                transcription = transcription.replace('[EMPTY]', '')
                transcription = transcription.replace('[FRAGMENT]', '')
                transcription = transcription.replace('[UNKNOWN]', '[UNINTELLIGIBLE]')
                # transcription = transcription.replace('[NONSENSE]', '')
                transcription = transcription.replace('[HNOISE]', '[SPEAKER]')
                transcription = transcription.replace('<OT>', '')
                transcription = transcription.replace('</OT>', '')
                transcription = transcription.replace('<FL>', '[NOTENG]')
                transcription = transcription.replace('</FL>', '')
                transcription = transcription.replace('@', '')
                transcription = transcription.replace('=', '')
                transcription = transcription.replace('~', '')

                full_line = filename + " " + file_location + " " + str(length_ms) + " " + transcription
        
                lines.append(full_line)

    shuffle_and_write(lines)

