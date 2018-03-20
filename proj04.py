###########################################################
# Computer Project #4
#
# Emulates a finite state autonoma (FSA) that checks if its input is any
# combination of the strings 'ha', and 'ho' that ends with a '!'. If the FSA's
# input matches this pattern, then the FSA's output is the value True.
# Otherwise the FSA's output is the value False.
#
###########################################################

def get_ch():
    """
    Prompts the user to enter a single character until the character that the
    user enters is a letter, a blank character, or an exclamation point.
    Print an error each time the user enters an invalid character
    Returns the character that the user entered
    """
    invalid = True
    while invalid:
        ch = input('Enter a character or press the Return key to finish: ')

        invalid = False
        if len(ch) > 1:
            invalid = True
        if not ch.isalpha() and ch != '' and ch != '!':
            invalid = True

        if invalid:
            print('Invalid input, please try again.')

    return ch


def find_state(state, ch):
    """
    Returns the next state of the FSA given the current state of the FSA and the
    next input character
    """

    if state == 1 and ch in 'h':
        return 2
    elif state == 2 and ch in 'ao':
        return 3
    elif state == 3 and ch in 'h':
        return 2
    elif state == 3 and ch in '!':
        return 4
    elif state == 5 or state == 4:
        return 5


def main():
    print('I can recognize if you are laughing or not.')
    print('Please enter one character at a time.')

    string = ''
    state = 1

    while True:
        ch = get_ch().lower()
        string += ch
        if ch == '':
            break
        state = find_state(state, ch)

    print('\nYou entered', string)

    # The user is laughing iff the FSA is in state 4
    if state == 4:
        print('You are laughing.')
    else:
        print('You are not laughing.')


main()

