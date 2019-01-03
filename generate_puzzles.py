from itertools import permutations
import enchant

test_word = 'testing'
three_letter_perms = set([''.join(p) for p in permutations(test_word, 3)])
dictionary = enchant.Dict('en_US')

for perm in three_letter_perms:
    if dictionary.check(perm):
        print(perm)

