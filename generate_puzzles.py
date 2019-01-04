import csv
from itertools import permutations
import enchant


def buildJSON():
    body = '';
    # with open('words.csv') as csvfile:
    with open('words_abridged.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            body += buildJSONObjectForWord(''.join(row))
    header = 'export const puzzles = {\n'
    footer = '\n});'
    return header + body + footer

def buildJSONObjectForWord(word):
    return ('    solution: \'' + word + '\',\n'
            '    puzzle: \'' + buildPuzzleForWord(word) + '\',\n'
            '    threeLetterPermutations: ' + buildJSONArrayForWords(buildPermutations(word, 3)) + '\n'
            '    fourLetterPermutations: ' + buildJSONArrayForWords(buildPermutations(word, 4)) + '\n'
            '    fiveLetterPermutations: ' + buildJSONArrayForWords(buildPermutations(word, 5)) + '\n'
            '    sixLetterPermutations: ' + buildJSONArrayForWords(buildPermutations(word, 6)) + '\n')

def buildJSONArrayForWords(words):
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

print(buildJSON())
