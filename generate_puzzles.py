import csv
from itertools import permutations
import enchant
import time
from blacklisted_words import blackList

puzzle_id = 1

def buildJS():
    body = ''
    # with open('words_abridged.csv') as csvfile:
    with open('words.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            body += buildJSObjectForWord(''.join(row))
    header = 'export const puzzles = {\n'
    footer = '\n};'
    return header + body + footer

def buildJSObjectForWord(word):
    global puzzle_id
    return ('    ' + str(puzzle_id) + ': {\n'
            '        puzzles: ' + buildJSArrayForWords(buildPuzzlesForWord(word)) + ',\n'
            '        permutations: ' + buildJSArrayForWords(buildPermutations(word)) + ',\n'
            '    },\n')

def buildJSArrayForWords(words):
    header = '[\n'
    body = ''
    for word in words:
        body += '            \'' + word + '\',\n'
    footer = '        ]'
    return header + body + footer

def buildPuzzlesForWord(word):
    allPermutations = [''.join(p) for p in set(permutations(word))]
    nonEnglishPermutations = []
    for p in allPermutations:
        if len(nonEnglishPermutations) >= 10:
            return nonEnglishPermutations
        if not isEnglishWord(p) and word not in nonEnglishPermutations:
            nonEnglishPermutations.append(p)
    return nonEnglishPermutations

def buildPermutations(word):
    global puzzle_id
    # Build permutations of the puzzle word
    perms = []
    perms += [''.join(p) for p in set(permutations(word, 6))]
    perms += [''.join(p) for p in set(permutations(word, 5))]
    perms += [''.join(p) for p in set(permutations(word, 4))]
    perms += [''.join(p) for p in set(permutations(word, 3))]
    # Time how long check takes
    start = time.time()
    print('Starting English check for: ' + word)
    # Filter out non English words
    englishPerms = [p for p in perms if isEnglishWord(p)]
    # Collect all our permutations, our first entry ([word]) is the puzzle solution
    allPerms = [word] + englishPerms
    print('English check finished in: ' + str(time.time() - start) + ' seconds')
    puzzle_id += 1
    # Filter out blacklisted words
    return [word for word in allPerms if word not in blackList]

def isEnglishWord(word):
    if (word):
        dictionary = enchant.Dict('en_US')
        return dictionary.check(word)
    return False

file = open('puzzles.ts', 'w')
file.write(buildJS())

