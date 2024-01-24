import sys
import random


class WrongWordLengthException(Exception):
    """Exception for the wrong length of a word."""

    pass


def read_file_as_words_list(
    file: str = None, check_input: bool = False, comment_char: str = "#"
) -> list:
    """Read a file fully into memory and return it as a list of words.
    
    Parameters:
    -----------
    - file: str (default = `None` / positional argument) \\
        A file that constitutes the dictionary for the word guessing game. Can
        be either provided as a positional argument in a shell or needs to be
        specified when calling the function within a script. If both are
        provided, the specification in the script takes precedence. More
        information on assumptions about the file can be found in the section
        'Input File' below.
    - check_input: bool (optiona, default = `False`) \\
        Toggles different checks while reading the input file. See section
        'Input File' below for more information, which cases can be handled.
        Related parameter(s): [`comment_char`]
    - comment_char: str (optional, default = `'#'`) \\
        Depends on the parameter `check_input` to be set to `True`!
        A string that represents a comment line in the dictionary if that line
        starts with this string.

    Returns:
    --------
    list: A list of all words (in uppercase) extracted from the input file.

    Input File:
    -----------
    The input file is by default expected to follow these assumptions:
    - one word per line
    - all words from one file have the same length
    - no empty or comment lines
    - no separator symbols between words (only one newline character `\\n`
      after each word)
    
    If the parameter `check_input` is toggled to `True`, the following cases are
    tried to be handled automatically:
    - ignore empty and comment lines, where a comment line starts with the
      comment character specified by the parameter `comment_char`
    - check the consistency of the length of all words and throw an exception
      (`WrongWordLengthException`) when encountering an inconsistency
    """
    # set the input file, depending on the specified parameter / given argument
    if file is None:
        try:
            file = sys.argv[1]
        except IndexError:
            raise TypeError(
                "missing input!  Please specify an input file as a positional "
                "argument or provide it as a parameter in the script."
            )

    # read the words into a list
    if check_input:
        with open(file, "r") as f:
            words = [
                w.strip().upper()
                for w in f
                if (not w.startswith(comment_char) and w.strip())
            ]
            try:
                base_len = len(words[0])
            except IndexError:
                raise ValueError("input file must not be empty")
            for w in words:
                if len(w) != base_len:
                    raise WrongWordLengthException(
                        f"invalid length of word '{w}' (actual length {len(w)},"
                        f" expected length {base_len})"
                    )
    else:
        with open(file, "r") as f:
            words = [w.strip().upper() for w in f]

    return words


def replace_char(replacement: str, in_str: str, index: int) -> str:
    """Replace a character in a string at a certain position."""
    return in_str[:index] + replacement + in_str[index + 1 :]


def match_check(guess: str, correct: str) -> tuple:
    """Compare a guess with the correct string.

    Returns a tuple, where the first element is a boolean to tell whether it is
    a full match (`True`) or not (`False`), and a return string that indicates
    the accuracy of the guess:\\
    A matching letter at the correct position is indicated by an exclamation
    mark (`!`). A matching letter at the wrong position is indicated by a
    question mark (`?`). A letter that does not match or is surplus is indicated
    by an underscore (`_`).
    """
    # find exact matches first
    for index, letter in enumerate(guess):
        if letter == correct[index]:
            guess = replace_char("!", guess, index)
            correct = replace_char("_", correct, index)

    if all([True if l == "!" else False for l in guess]):
        # already found a full match
        return (True, guess)

    # find remaining letters at the wrong position and not included letters
    for index, letter in enumerate(guess):
        if letter in correct:
            guess = replace_char("?", guess, index)
            corr_index = correct.index(letter)
            correct = replace_char("_", correct, corr_index)
        elif letter != "!":
            guess = replace_char("_", guess, index)

    return (False, guess)


def input_check(
    length: int = None, prompt: str = None, trail_whitespace: bool = False
) -> str:
    """Inquire user input according to specified rules and return the input.

    Parameters:
    -----------
    length: int (optional)
        Constraint on the length of the user input.
    prompt: str (optional)
        A preceding message shown each time the user is prompted for input.
    trail_whitespace: bool = False
        Add a trailing whitespace to the parameter `prompt` if none is found.
    """
    if prompt is None:
        prompt = ""
    else:
        if trail_whitespace and prompt[-1] != " ":
            prompt += " "

    while True:
        usr = input(prompt)
        if length is not None and len(usr) != length:
            print(f"Input must have a length of {length} characters.")
            continue
        return usr


def check_word_vs_guess_and_hints(word: str, guess: str, hints: str) -> bool:
    """Return `True` if `word` matches `hints` and `guess`, else `False`."""
    # first iteration for definite cases
    for ind, hint in enumerate(hints):
        if not hint in ["!", "?", "_"]:
            # invalid hint character
            raise ValueError(
                f"invalid character '{hint}', hints must be '!', '?', or '_'"
            )
        elif hint == "!":
            # letters should match
            if guess[ind] == word[ind]:
                # letters do match, so sort out letter at specific position
                word = replace_char("*", word, ind)
            else:
                # letters do not match
                return False
        elif hint == "?" and guess[ind] == word[ind]:
            # letter is correct, but should be at a different position
            return False
    # second iteration for more special cases
    for ind, hint in enumerate(hints):
        if hint == "?":
            # letter should be included
            if guess[ind] in word:
                # letter is included and can be sorted out
                word = word.replace(guess[ind], "*", 1)
            else:
                # letter is not included
                return False
        elif hint == "_" and guess[ind] in word:
            # letter should not be included, but it is
            return False
    return True


def reduce_list(in_list: list, guess: str, hints: str) -> list:
    """Remove words from a list of words, following the applied hints.

    Parameters:
    -----------
    in_dict: list
        A list of words that make up the dictionary.
    guess: str
        The current guess.
    hints: str
        The hint-string provided by `match_check`, which is valid for the
        current guess, i.e., `!` for a correct letter and position, `?` for a
        correct letter, and `_` for a wrong or surplus letter, e.g., `!_??_`
        for a 5-letter word.

    Returns:
    --------
    list: The reduced list of words, based on the guess and the provided hints.
    """
    return [w for w in in_list if check_word_vs_guess_and_hints(w, guess, hints)]


def yn_prompt(prompt: str, default: str = None, verbose: bool = False) -> bool:
    """
    A short function to give the user a prompt and ask yes-or-no.

    It is possible to choose a default answer, which is then indicated
    automatically.

    Parameters:
    -----------
    prompt: str
        A user prompt, typically a question, which has a yes-or-no answer.
    default: str (optional, default = `None`)
        If set must be one of the following: [`'y'`, `'yes'`] / [`'n'`, `'no'`].
        If one of the options is given the respective default setting is
        indicated. Otherwise no answer is indicated.
    verbose: bool (optional, default = `False`)
        Toggle printing of information for some special cases.

    Returns:
    --------
    Depending on the user's choice returns a boolean value: `True` for yes and
    `False` for no.

    Dependencies:
    -------------
    None
    """
    if default is None:
        deflt, opt = " [y/n] ", -1
    else:
        if not isinstance(default, str):
            raise Exception("Parameter `default` must be class `str`.")
        if default.lower() in ["y", "yes"]:
            deflt, opt = " [Y/n] ", 1
        elif default.lower() in ["n", "no"]:
            deflt, opt = " [y/N] ", 0
        else:
            if verbose:
                print("`default` parameter not recognized.")
            deflt, opt = " [y/n] ", -1

    while True:
        inp = input(prompt + deflt)
        if (not inp and opt == 1) or inp.lower().startswith("y"):
            re = True
            break
        elif (not inp and opt == 0) or inp.lower().startswith("n"):
            re = False
            break
        else:
            if verbose:
                print("Not understood. Please try again.")
            continue
    return re


def game_routine(
    words: list,
    correct: str,
    corr_length: int,
    allow_wild_guess: bool,
    show_wrong_letters: bool,
    auto_solver: bool,
    prompt: str,
):
    """Game routine for the word guessing game."""
    counter = 1
    correct_letters, wrong_letters = [], []
    while True:
        if auto_solver:
            # initiate auto solver guess
            guess = random.choice(words)
            print(guess)
        else:
            # process user input for validity
            guess = input_check(length=corr_length, prompt=prompt).upper()
            if not allow_wild_guess and not guess in words:
                print("Word is not part of the dictionary!")
                continue

        # keep track of in- and excluded letters
        # (not dependent on the show_wrong_letters parameter as it is cheap)
        # (not included in `match_check` as this was a later spontaneous idea)
        for l in guess:
            if l in correct:
                correct_letters.append(l)
            else:
                wrong_letters.append(l)
        # remove duplicates and sort
        correct_letters = list(set(correct_letters))
        correct_letters.sort()
        wrong_letters = list(set(wrong_letters))
        wrong_letters.sort()

        # check the user input and provide feedback; repeat if not guessed
        state, hints = match_check(guess, correct)
        if show_wrong_letters and hints != corr_length * "!":
            print(hints, f" out: {wrong_letters}")
        else:
            print(hints)
        if state:
            if counter == 1:
                msg = "Woah, first try! Way too much luck. Congratulations!"
            elif counter == 2:
                msg = "Very nice! Only two guesses needed."
            elif counter < 7:
                msg = f"Nice! You got it after {counter} tries."
            else:
                msg = f"You go it! It took you {counter} tries."
            print(msg)
            return counter
        else:
            if auto_solver:
                words = reduce_list(words, guess, hints)
                if not words:
                    raise Exception(
                        "Whoops! Somehow no word was found to match anymore. "
                        "That should not happen, as the solution was chosen "
                        "from the same dictionary as the guesses. The code has "
                        "a bug. Please fix me."
                    )
            counter += 1
            continue


def main(
    file: str = None,
    allow_wild_guess: bool = False,
    show_wrong_letters: bool = True,
    auto_solver: bool = False,
    check_input: bool = False,
    comment_char: str = "#",
    prompt: str = None,
) -> int:
    """Word guessing game, where the dictionary file is fully read into memory.

    Run the script to initialize the game sequence. Start by guessing a word and
    then use the provided hints based on this guess to find the solution.

    The hints are given as a string of the same length as the guess/solution,
    where each character of the hints provides information about each letter of
    the guess. Their meanings are as follows:
     `!`: the letter is correct and at the right position
     `?`: the letter is included in the solution, but at a different position
     `_`: the letter is surplus or not included

    Parameters:
    -----------
    - file: str (default = `None` / positional argument) \\
        A file that constitutes the dictionary for the word guessing game. Can
        be either provided as a positional argument or needs to be specified
        when calling the function within a script. If both are provided, the
        specification in the script takes precedence. More information on
        assumptions about the file can be found in the section 'Input File'
        below. Related parameter(s): [`check_input`, `comment_char`]
    - allow_wild_guess: bool (optional, default = `False`) \\
        Allow the user to input any string that has the right length. Otherwise
        only guesses that are part of the dictionary are allowed.
    - show_wrong_letters: bool (optional, default = `True`) \\
        After each guess, print the letters that are known to be excluded.
    - auto_solver: bool (optional, default = `False`) \\
        Run an automated solver instead of guessing via user input.
    - check_input: bool (optiona, default = `False`) \\
        Toggles different checks while reading the input file. See section
        'Input File' below for more information, which cases can be handled.
        Related parameter(s): [`comment_char`]
    - comment_char: str (optional, default = `'#'`) \\
        Depends on the parameter `check_input` to be set to `True`!
        A string that represents a comment line in the dictionary if that line
        starts with this string.
    - prompt: str (optional, default = `None`) \\
        An optional message displayed to the user each time they are asked for
        a guess as input.

    Returns:
    --------
    list: A list that contains the number of needed tries for each game.

    Input File:
    -----------
    The input file is by default expected to follow these assumptions:
    - one word per line
    - all words from one file have the same length
    - no empty or comment lines
    - no separator symbols between words (only one newline character `\\n`
      after each word)
    
    If the parameter `check_input` is toggled to `True`, the following cases are
    tried to be handled automatically:
    - ignore empty and comment lines, where a comment line starts with the
      comment character specified by the parameter `comment_char`
    - check the consistency of the length of all words and throw an exception
      (`WrongWordLengthException`) when encountering an inconsistency

    Dependencies:
    -------------
    packages: [`sys`, `random`]
    functions: [
        `read_file_as_words_list`, `replace_char`, `input_check`, `match_check`,
        `check_word_vs_guess_and_hints`, `reduce_list`, `yn_prompt`
    ]
    exception: `WrongWordLengthException`
    """
    # read the file into memory as a list of words
    words = read_file_as_words_list(file, check_input, comment_char)

    # create list to collect the number of needed tries per game
    tries = []

    # start repeating game sequence
    while True:
        # select a word that has to be guessed
        correct = random.choice(words)
        corr_length = len(correct)

        # initiate game by showing user an introductory message
        print(
            f"Use guessing and then provided hints to find this word: "
            f"'{corr_length*'*'}' (length {corr_length})\n"
            f"(Input is automatically converted into uppercase.)\n"
            f"Explanation of hints: [`!`: matching letter and position; `?`: "
            f"matching letter at wrong position; `_`: wrong/surplus letter]"
        )

        if auto_solver:
            print("NOTE: Automatic solving enabled")

        # start the routine of guessing, while counting the number of guesses
        tries.append(
            game_routine(
                words,
                correct,
                corr_length,
                allow_wild_guess,
                show_wrong_letters,
                auto_solver,
                prompt,
            )
        )

        if not auto_solver and yn_prompt("Play again?", "y"):
            continue
        else:
            break

    return tries


def get_auto_solver_statistics(n: int = 100, file: str = None, **kwargs):
    """Run 'n' tests using the auto-solver and get solution statistics.

    Please mind that the input file is read each time that the game is executed,
    i.e., it is read `n` times.

    Parameters:
    -----------
    n: int (optional, default = `100`)
        The number of times the autosolver should solve a game.
    file: str (optional, default = `None` / positional argument)
        The dictionary file used for the word guesing game. If not provided as a
        parameter, it has to be specified as a positional argument.
    **kwargs (optional)
        Keyword arguments that are passed to the game's `main` function. In any
        case the parameter `auto_solver` is automatically set to `True`.

    Returns:
    --------
    int: The number of times the game was played.
    float: The arithmetic mean of the needed number of tries each game.
    float: The standard deviation of the mean number of tries each game.
    int: The lowest number of tries needed to solve a game.
    int: The highest number of tries needed to solve a game.

    All the returned information are also printed in an easily readable way.
    """
    kwargs["auto_solver"] = True

    number_of_tries = [main(file, **kwargs)[0] for _ in range(n)]
    length = len(number_of_tries)

    best, worst = min(number_of_tries), max(number_of_tries)
    mean = sum(number_of_tries) / length
    std = (sum([(t - mean) ** 2 for t in number_of_tries]) / length) ** 0.5

    print(
        "__________\n"
        "STATISTICS\n"
        f"total number of tries: {n}\n"
        f"arithmetic mean of number of tries: {mean}\n"
        f"standard deviation: {round(std, 3)}\n"
        f"best / worst number of tries: {best} / {worst}"
    )

    return (n, mean, std, best, worst)


def find_words_in_dict(guesses_and_hints: list, file: str = None, **kwargs):
    """Find all words from a dictionary that match the given guesses and hints.

    The handling of the input file and the meaning of the hints has to match the
    descriptions of the function `main`.

    Parameters:
    -----------
    guesses_and_hints: list
        A 2d-list that contains pairs of strings, each a word guess and a hint,
        e.g., `[['<guess1>', '<hints1>'], ['<guess2>', '<hints2>'], ...]`.
        These words and hints are used in combination to find all words from a
        dictionary that match all criteria.
    file: str (optional, default = `None` / positional argument)
        A file that is used as the dictionary for this function. This file is
        read into memory each time this function is called.
    **kwargs (optional)
        Keyword arguments that are passed to the function
        `read_file_as_words_list`, i.e., `check_input` and `comment_char`.

    Returns:
    --------
    list / None: A list of all remaining words that match the input criteria. If
    no words are left, returns `None`. Prints either result.
    """
    # read the file into memory as a list of words
    words = read_file_as_words_list(file, **kwargs)

    # consecutively remove non-matching words
    for guess_hint in guesses_and_hints:
        words = reduce_list(words, guess_hint[0].upper(), guess_hint[1])
        if not words:
            print("No words found matching the given criteria.")
            return

    # show all remaining matches
    if len(words) == 1:
        print(f"Only one word matches the given criteria: {words[0]}")
    else:
        print(f"Following words match the given criteria:")
        print(*words, sep=", ", end="")

    return words


if __name__ == "__main__":
    ## main game function calls
    main()
    # main(allow_wild_guess=True)
    # main(auto_solver=True)

    ## run `n` times the automatic solving and get some stats
    # get_auto_solver_statistics(n=1000)
    #
    ### EXAMPLE OUTPUT (file: 'copylists_496_5-letter_words_perline.txt')
    ## __________
    ## STATISTICS
    ## total number of tries: 1000
    ## arithmetic mean of number of tries: 3.376
    ## standard deviation: 0.836
    ## best / worst number of tries: 1 / 7
    #
    ### EXAMPLE OUTPUT (file: 'charlesreid1_5757_common_5-letter_words.txt')
    ## __________
    ## STATISTICS
    ## total number of tries: 1000
    ## arithmetic mean of number of tries: 4.61
    ## standard deviation: 1.277
    ## best / worst number of tries: 2 / 10

    ## find words in a dictionary that match some hints
    ## test file: 'charlesreid1_5757_common_5-letter_words.txt'
    # g_h = [["crane", "_?__?"], ["women", "?!_!_"]] # 'POWER', 'LOWER', etc.
    # g_h = [["ghost", "???_?"]] # only 'TOUGH' remains
    # g_h = [["guess", "__?!?"], ["hello", "_!_!_"]]  # purposely invalid
    # find_words_in_dict(g_h)
