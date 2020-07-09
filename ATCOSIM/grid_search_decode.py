import os
import subprocess

__author__ = "Tijs Rozenbroek"

if __name__ == "__main__":
    lmweights = [0.1, 0.5, 1.0, 1.5, 2.0, 4.0]
    wordscores = [0.1, 0.5, 1.0, 1.5, 2.0, 4.0]
    eosscores = [-10.0, -9.0, -8.0, -7.5, -6.0, -5.0, -4.0]
    beamsizes = [50]
    beamsizetokens = [5]
    beamthresholds = [5]
    attentionthresholds = [300]

    for lmweight in lmweights:
        for wordscore in wordscores:
            for eosscore in eosscores:
                for beamsize in beamsizes:
                    for beamsizetoken in beamsizetokens:
                        for beamthreshold in beamthresholds:
                            for attentionthreshold in attentionthresholds:
                                bashCommand = "/home/tijs/wav2letter/build/Decoder decode --flagsfile /home/tijs/atc/config/decode_ngram.cfg "
                                bashCommand += "--beamsize " + str(beamsize) + " --beamsizetoken " + str(beamsizetoken) + \
                                               " --beamthreshold " + str(beamthreshold) + " --attentionthreshold " + \
                                               str(attentionthreshold) + " --lmweight " + str(lmweight) + " --wordscore " \
                                               + str(wordscore) + " --eosscore " + str(eosscore)
                                outputdir = "/home/tijs/atc/decode/network1/" + str(beamsize) + \
                                            str(beamsizetoken) + str(beamthreshold) + str(attentionthreshold) + \
                                            str(lmweight) + str(wordscore) + str(eosscore)
                                bashCommand += " --sclite " + outputdir
                                os.makedirs(outputdir, exist_ok=True)
                                subprocess.run(bashCommand, shell=True)
