import re
import sys
from multiprocessing import Pool

import spacy

spacy.require_gpu()
nlp = None


def init():
    global nlp
    #nlp = spacy.load('en', disable=['tagger', 'ner', 'textcat'])
    nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner", "lemmatizer", "attribute_ruler"])
    nlp.enable_pipe("senter")



def segment(line):
    global nlp
    return ''.join([str(sent) + '\n'
                    for sent in nlp(line).sents
                    if not re.match(r'^\W+$', str(sent))])


def main():
    #with Pool(4, initializer=init) as pool:
    #with Pool(1, initializer=init) as pool:
    #    for text in pool.imap(segment, sys.stdin, chunksize=64):
    #        sys.stdout.write(text)
    init()
    lines = []
    for line in sys.stdin:
        lines.append(line)
        if len(lines) == 1024:
            merged_line = " ".join(lines)
            text = segment(merged_line)
            sys.stdout.write(text)
            lines = []

    if len(lines) > 0:
        merged_line = " ".join(lines)
        text = segment(merged_line)
        sys.stdout.write(text)
        lines = []


if __name__ == '__main__':
    main()
