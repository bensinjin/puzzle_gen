import csv
from itertools import permutations
import enchant


def buildJS():
    body = '';
    # with open('words.csv') as csvfile:
    with open('words_abridged.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            body += buildJSObjectForWord(''.join(row))
    header = 'export const puzzles = {\n'
    footer = '\n});'
    return header + body + footer

def buildJSObjectForWord(word):
    return ('    solution: \'' + word + '\',\n'
            '    puzzle: \'' + buildPuzzleForWord(word) + '\',\n'
            '    threeLetterPermutations: ' + buildJSArrayForWords(buildPermutations(word, 3)) + '\n'
            '    fourLetterPermutations: ' + buildJSArrayForWords(buildPermutations(word, 4)) + '\n'
            '    fiveLetterPermutations: ' + buildJSArrayForWords(buildPermutations(word, 5)) + '\n'
            '    sixLetterPermutations: ' + buildJSArrayForWords(buildPermutations(word, 6)) + '\n')

def buildJSArrayForWords(words):
    header = '[\n'
    body = ''
    for word in words:
        body += '        \'' + word + '\',\n'
    footer = '    ],'
    return header + body + footer

def buildPuzzleForWord(word):
    allPermutations = set([''.join(p) for p in permutations(word)])
    for p in allPermutations:
        if not isEnglishWord(p):
            return p
    return word

def buildPermutations(word, length):
    allPermutations = set([''.join(p) for p in permutations(word, length)])
    return [p for p in allPermutations if isEnglishWord(p)]

def isEnglishWord(word):
    dictionary = enchant.Dict('en_US')
    return dictionary.check(word)

print(buildJS())
