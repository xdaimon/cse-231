###########################################################
#  Computer Project #3
#
# Repeatedly prompt for words to collect consonants and vowels from
# until we've collected all five vowels or five consonants.
# Only collect letters that we've not collected yet.
# Only collect consonants that appear after the final vowel in a word.
# Assume that each word contains a vowel. So we collect a consonant
# from each word (the last letter), even if that word does not contain a vowel.
#
# Print collected vowels and consonants along with their counts.
#
###########################################################

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

NUM_CONSONANTS_NEEDED = 5
NUM_VOWELS_NEEDED = len(VOWELS)
consonants_found = ''
vowels_found = ''

while len(consonants_found) < NUM_CONSONANTS_NEEDED \
        and len(vowels_found) < NUM_VOWELS_NEEDED:

    word_str = input("Input a word: ")
    word_str = word_str.lower()

    # Collect vowels and consonants

    # Look for consonants in word_str[vowel_index+1:]
    vowel_index = -1

    # First collect new vowels
    for index, letter in enumerate(word_str):
        if letter in VOWELS:
            if letter not in vowels_found:
                vowels_found += letter
            vowel_index = index

    # Then collect new consonants
    for letter in word_str[vowel_index + 1:]:
        if letter not in consonants_found and letter in CONSONANTS:
            consonants_found += letter

# Output Results
print("\n"+"="*12)
print("{:8s}{:7s} | {:12s}{:7s}".format("vowels", "length", \
    "consonants", "length"))

print("{:8s}{:<7d} | {:12s}{:<7d}".format(vowels_found, len(vowels_found), \
    consonants_found, len(consonants_found)))

