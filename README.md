# s2sASRforATC
Scripts, network architectures and config files used for the BSc thesis project of creating sequence-to-sequence ASR models for air traffic control using [wav2letter++](https://github.com/facebookresearch/wav2letter).

In the w2l++ folder, the networks for wav2letter++ that were made for the thesis project can be found. Additionally, some example configuration files and the tokens file for wav2letter++ are provided.

The following text is a slightly adapted version of the appendix that was included with the thesis. It explains some of the logic and how to run the scripts.
# Appendix
Here I will explain some of the scripts that were created for several purposes, amongst other things to extract data from the corpora, to correct commonly occurring errors and to homogenise the corpora.
The scripts that were created were all written in the Python programming language, specifically Python 3.7. They were designed to be run through a terminal, and be compatible with multiple operating systems. They were tested and confirmed to work in a PyCharm terminal in Windows 10 and a terminal in Ubuntu 18.04. There are some common dependencies, such as NumPy and the csv library.
The example commands that can be used to run the scripts in Ubuntu terminals all assume that Python 3.7 is used. Compatibility with other version of Python has not been tested.

##	Air Traffic Control Communication corpus scripts
For the [ATCC corpus](https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0001-CCA1-0), several scripts were created. Most of these scripts contain an extensive amount of replacement rules. These were introduced to fix commonly occurring errors, to adapt the transcriptions to the form that I needed them to be and to homogenise them.
###	Data preparation
There are two ATCC data preparation scripts, one that takes care of the slicing of the transcriptions called `atcc_data_prep_slice.py`, and one that does not slice called `atcc_data_prep.py`. Both scripts shuffle and split the transcriptions into three sets, a training, validation and test set, and writes these to separate files. These three files need to be of a specific form for the wav2letter++ framework, in the sense that they have to contain one sample per line, with this line containing the audio file name, audio file location, audio duration and actual transcription, separated by whitespaces (or tabs).  A fourth file called `fullatccdata.lst` is optional, which is a file that contains the aforementioned transcriptions in a single file. In contrast to the three standard files, this fourth file does not contain the location, file name and duration per transcription, but instead only the raw transcriptions. This fourth file is used for a script that creates a lexicon for the ATCC corpus, this script will be explained further below.
The `atcc_data_prep_slice.py` script is special, in that it slices the audio data WAV files, by using the [pydub](http://pydub.com/) library. How to slice the files when they are longer than five seconds, is determined by extracting the info about when utterances occur from the XML tags in the .trs files.
To demonstrate, the way to run the script that does not slice in an Ubuntu terminal is as follows:
```
python3.7 atcc_data_prep.py --src [SOURCE] --dst [DESTINATION]
```
Where `[SOURCE]` is the location path of the .trs files, and `[DESTINATION]` is the location where the .lst files should be written.
The way to run the slicing script is identical, only the name of the python file should of course be changed. The `[SOURCE]` location is also automatically assumed to also be the source of the WAV audio files.
The optional fourth file can be created by supplying the flag `-l`. This file will be written to the same destination location.
###	Lexicon preparation
A Python script for creating a lexicon of the ATCC corpus is also provided. This script is called `atcc_lexicon_prep.py`. This script reads the optional file from the data preparation scripts, and creates out of this and writes it to a text file. The lexicon that is created has the specific format that the wav2letter++ framework requires.
The way to run this script in an Ubuntu terminal is as follows:
```
python3.7 atcc_lexicon_prep.py --src [SOURCE] --dst [DESTINATION]
```
Where `[SOURCE]` is the location path of the `fullatccdata.lst` file and `[DESTINATION]` is the location where the lexicon text file should be written.
###	Sentence extraction
For the purpose of creating language models with [KenLM](https://kheafield.com/code/kenlm/), a script (`atcc_sentences_extract.py`) was written that extracts the sentences that were spoken from the transcripts. This is done by using the information when a sentence starts and ends that is contained in the .trs files. It employs the same replacement rules as the data preparation script that fix and homogenise the transcriptions. Additionally, by using a relatively complex approach, it shuffles and partitions the sentences into the training, validation and test sets in the same way that the data preparation scripts do, so that the language models are trained (and tested) on the same data as the acoustic models. This script thus takes the .trs files, and writes three text files with the sentences as plain text, one per line.
To run this script in an Ubuntu terminal, use the following line:
```
python3.7 atcc_sentences_extract.py --src [SOURCE] --dst [DESTINATION]
```
Where `[SOURCE]` is the path of the .trs files, and `[DESTINATION]` is the path where the TXT files with the sentences should be written.
##	ATCOSIM scripts
For the [ATCOSIM corpus](https://www.spsc.tugraz.at/databases-and-tools/atcosim-air-traffic-control-simulation-speech-corpus.html), similar scripts were written. The biggest differences are that for the ATCOSIM corpus, some extra files were included that made the operations easier, and much fewer replacements rules were necessary.
###	Data preparation
The `atcosim_data_prep.py` script prepares the data for the wav2letter++ framework, by again writing one sample per line, where this line should consist of the audio file name, audio file location, audio duration and actual transcription. This script is slightly different from the ATCC data prep script, since a CSV file with all transcriptions and other attributes (such as audio duration) is included with the ATCOSIM corpus, which is called `fulldata.csv`. This means that only this single CSV file servers as input for the data preparation script. Another difference is that the ATCOSIM corpus contains nested folders for the audio files, meaning that the script has to build the file location string. This script too shuffles and partitions the data into a training, validation and test set, and writes these to respective text files.
The way to run this script in an Ubuntu terminal is as follows:
```
python3.7 atcosim_data_prep.py --csvsrc [CSV SOURCE] --datasrc [DATA SOURCE] 	--dst [DESTINATION]
```
Where `[CSV SOURCE]` is the path to the `fulldata.csv` file, `[DATA SOURCE]` is the path to the top directory of the audio files (by default this should be the WAVdata folder) and `[DESTINATION]` is the location where the text files should be written.
###	Lexicon preparation
A lexicon preparation script was made for the ATCOSIM corpus as well. This script is called `atcosim_lexicon_prep.py`, and makes a lexicon that is in the format that the wav2letter++ requires. The lexicon is created from the `wordlist.txt` file, which is included with the ATCOSIM corpus. This wordlist file makes the creation of a lexicon rather easy, since this file contains all words in the ATCOSIM file line by line, which is very close to what the wav2letter++ requires. All that has to be done is append to each word, the grapheme representation of the word.
The script can be run in an Ubuntu terminal as follows:
```
python3.7 atcosim_lexicon_prep.py --src [SOURCE] --dst [DESTINATION]
```
Where `[SOURCE]` is the path to the `wordlist.txt` file, and `[DESTINATION]` is the path to where the lexicon should be written.
###	Sentence extraction
Just like for the ATCC corpus, a sentence extraction script was made for the ATCOSIM corpus, of which the output can be used to make language models. This script is a lot less complex, since the ATCOSIM corpus only contains one spoken sentence per sample. The sentences are shuffled and partitioned into training, validation and test sets in an identical fashion as in the data preparation script, again to make sure that the language model is trained on the same data as the acoustic model.
The script can be run in an Ubuntu terminal in the following way:
```
python3.7 atcosim_sentences_extract.py --src [SOURCE] --dst [DESTINATION]
```
Where `[SOURCE]` is the path to the `fulldata.csv` file, and `[DESTINATION]` is the path where the output text file should be written.
###	Downsampling
A script that is unique to the ATCOSIM corpus, is the `atcosim_downsample.py` script, which uses the [librosa](https://librosa.org/librosa/) library to downsample the ATCOSIM audio files to 8 kHz. It uses the same code as the data preparation script to deal with the nested folders of the audio files.
The way to run this script in an Ubuntu terminal is as follows:
```
python3.7 atcosim_downsample.py --csvsrc [CSV SOURCE] --datasrc [DATA SOURCE] --dst [DESTINATION]
```
Where `[CSV SOURCE]` is the path to the `fulldata.csv` file, `[DATA SOURCE]` is the path to the top directory of the audio files (by default this should be the WAVdata folder). The `[DESTINATION]` is the path to where the downsampled WAV audio files should be written. The files will be written in the same nested library architecture as the data source path.
##	Grid search script
A simple grid search script is provided for the wav2letter++ beamsearch decoder with a language model. It can be adapted to search over the values of interest. It uses the subprocess library to execute a bash command that runs the decoder, for all the different combinations of values that are to be tried. The bash command and output directory that are currently in the script might have to be changed to suit your setup.
It can be run in an Ubuntu terminal in the following way:
```
python3.7 grid_search_decode.py
```

