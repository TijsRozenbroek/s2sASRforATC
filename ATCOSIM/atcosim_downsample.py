import os
import argparse
import sys
import csv
import librosa

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATCOSIM dataset preparation.")
    parser.add_argument("--csvsrc", help="fulldata.csv source directory")
    parser.add_argument("--datasrc", help="Audio data source directory")
    parser.add_argument("--dst", help="Audio data destination directory")
    args = parser.parse_args()

    assert os.path.isdir(str(args.csvsrc)), "fulldata.csv source directory not found"
    assert os.path.isdir(str(args.datasrc)), "Audio data source directory not found"
    csv_src = os.path.join(args.csvsrc, "fulldata.csv")

    with open(csv_src) as csv_file:
        csv_reader = csv.reader(csv_file)

        os.makedirs(args.dst, exist_ok=True)

        sys.stdout.write("Processing...\n")
        sys.stdout.flush()

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
                write_location = os.path.join(args.dst, os.path.join(subdir, subsubdir))
                write_filename_location = os.path.join(write_location, filename + ".wav")

                os.makedirs(write_location, exist_ok=True)

                y, sr = librosa.load(file_location, sr=8000)
                librosa.output.write_wav(write_filename_location, y, sr)
