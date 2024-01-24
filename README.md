
# Word Guessing Game in Python

This is a word guessing game written in Python as a small hobby project.
The basic game essentially follows the same rules as a popular online game, where a 5-letter word has to be guessed on a daily basis.

It should work with any Python 3.6+ version, but it is only tested using Python 3.7+ environments.
The script makes use of two standard Python packages (`sys` & `random`), while the rest is written in pure Python.
Below are more information on [how to play and use different options & functions](#how-to-play) and on the necessary [input file to run the game](#the-input-file).

## Table of Contents

1. [Table of Contents](#table-of-contents)
2. [How to Play](#how-to-play)
    1. [Further Options](#further-options)
    2. [Get Statistics About the Game Playing Itself](#get-statistics-about-the-game-playing-itself)
    3. [Find Words from Hints](#find-words-from-hints)
3. [The Input File](#the-input-file)
    1. [Sources for Dictionary Files](#sources-for-dictionary-files)
    2. [Assumptions About the Input File](#assumptions-about-the-input-file)
    3. [Convert an Input File to a Word-Per-Line Basis](#convert-an-input-file-to-a-word-per-line-basis)

## How to Play

The Python script can be used as it is uploaded in this repository from a shell, if a positional argument is provided that represents a valid input file, e.g.,  if the file 'input_file.txt' is in the same directory as the Python script, then  
`$ python word_guessing_game.py input_file.txt`.  
The input file represents a dictionary of words that are used for the game.
More information, for example about the assumed format and where to find such files, is described below in a [section about the input file](#the-input-file).

When playing, each guess is checked to have the same length as the solution, i.e., the same number of characters.
The solution is randomly chosen from all words of the input file.
User input is automatically transformed to uppercase.
There is no limit to the number of tries for each game.

The game provides hints after every guess, where each hint corresponds to a letter of the current guess.
An exclamation mark (`!`) shows that the right letter is at the right position, a question mark (`?`) shows that the letter is included, but at another position, and an underscore (`_`) shows that the letter is surplus or not included at all.  
**An example:**
If the guess is `crane` and the respective hints are `_!?!?`, it is known that the letter 'c' is not included in the solution, the letters 'r' and 'n' are included and correctly placed, and the letters 'a' and 'e' are included, but not as the third and fifth letter, respectively. In this case the solution `ARENA` is already quite clear after just one guess.

In order to change options, the game file has to be adjusted.
If you want to only play the game using different options, all necessary changes can be applied at the bottom of the script, i.e., below the line that says `if __name__ == "__main__":`.
There are some commented lines, which can help finding out how to run the game with different options.
The [following section](#further-options) describes the different available options.

### Further Options

The game is started using the `main`-function.
If no parameters are specified, its default parameter settings are used.
Here is a list of all available options in the form of parameters of the `main`-function:

- `file`: A string that specifies the input file. Can be a relative or absolute path. If specified within the script, the positional argument when calling the script from a shell is not required. If both are specified, the parameter within the script takes precedence over the positional argument.
- `allow_wild_guess`: A boolean (i.e, `True` or `False`) which toggles the input of any string as a word guess, as long as it has the proper length. By default it is `False`, i.e., only guesses that are part of the input file are allowed.
- `show_wrong_letters`: A boolean to toggle whether known excluded letters are printed after each guess. By default it is `True`, i.e., excluded letters are shown.
- `auto_solver`: A boolean that decides whether the game is played automatically or not. By default `False`, i.e., the user plays the game manually.
- `check_input`: A boolean to toggle whether [different checks are run while reading the input file](#assumptions-about-the-input-file). By default it is `False`, i.e., no extra checks.
- `comment_char`: A string that represents a comment line in the input file. This only makes sense, if `check_input` is set to `True`. By default a hash symbol ('#') is used to identify comments.
- `prompt`: A string as an optional message, which is displayed to the user each time they are prompted for a guess as an input. By default none is specified.

As an example, to play the game with default parameters, but do not show excluded letters during the game and check/correct the input file while reading into memory, the needed command in the script is `main(show_wrong_letters=False, check_input=True)`.

### Get Statistics About the Game Playing Itself

The script contains another function called `get_auto_solver_statistics`, which uses the automatic solving option to play the game a specified number of times.
The function collects the number of tries needed to solve each time the game is played and prints according information, such as the arithmetic mean of the number of needed tries and the best & worst game.  
For more information, please consult the docstring of the aforementioned function.

Please mind that the script still prints all games as if a human would play it, such that a large number of games creates lots of printed output.

### Find Words from Hints

Another function might help with finding words that meet certain criteria.
It is called `find_words_in_dict` and takes a list of pairs of guesses & respective hints as input.
All words from the input file that match these criteria are printed.
The docstring of this function includes more information and the Python script provides input examples in commented lines at the bottom of the file.

In case no words are found that match the given criteria, the user is informed about this.
If this is an unexpected result, it makes sense to check the input again, try with fewer pairs of guesses & hints, or use another input file as a dictionary that might contain more valid words.

## The Input File

In order to work, the game needs an input file that represents a dictionary of valid words.
The sections below describe [possible sources for such files](#sources-for-dictionary-files) and [assumptions of the script about the input file](#assumptions-about-the-input-file).
Additionally, it is described how to easily [convert an input file](#convert-an-input-file-to-a-word-per-line-basis) under certain conditions to the needed format.

### Sources for Dictionary Files

As the script does not work without an input file, finding such a dictionary is quite essential.
Given the popularity of the famous word guessing game where a 5-letter word has to be found, lists of words with 5 letters are probably the easiest to find.
Here are three examples for lists that contain 5-letter words (all links checked on 2024-01-22):

- 496 of quite common 5-letter words on [copylists.com](https://copylists.com/words/list-of-5-letter-words/)
- shmookey's list of ["3103 common 5-letter words"](https://gist.github.com/shmookey/b28e342e1b1756c4700f42f17102c2ff) (their sources are listed in a readme file)
- charlesreid1's list of 5757 ["Five Letter Words"](https://charlesreid1.com/wiki/Five_Letter_Words) (their sources are listed on the website)

The first example source gives many formatting options for downloading the list of words.
Depending on the chosen option, it might be necessary to [reformat the file](#convert-an-input-file-to-a-word-per-line-basis) before being able to use it.  
The other two examples can be saved relatively straight-forward into a file (e.g., a simple 'txt'-file) and then used for this script.

### Assumptions About the Input File

As mentioned previously, the script needs a dictionary file, which contains all valid words.
While in principle the length of the words can be chosen freely, there are certain assumptions about the input file:

- one word per line, i.e., each word is followed by a newline character
- all words from one file have the same length, i.e., same number of letters
- no empty or comment lines (except the trailing newline character of the last word, which might appear as an empty line at the end of the file)
- no additional separator symbols, such as a comma, but only the newline characters

If you have a file that does not meet these criteria, read on or check the [section below](#convert-an-input-file-to-a-word-per-line-basis), which might help converting your file to the expected format.

The `main` function of the script has a parameter `check_input`. If [this is set to](#further-options) `True` the script tries to handle/correct following cases automatically:

- ignore empty and comment lines, where a comment line starts with the string specified by the parameter `comment_char`
- check whether the length of all words is consistent

### Convert an Input File to a Word-Per-Line Basis

If the input file has all words placed in one or multiple lines with a common separator, it can easily be converted into a new file where each word is on its own line.
The example shell Python code below only uses Python built-in functions & methods.
Comment lines (i.e, lines starting with a certain string) are sorted out, empty lines are ignored, and whitespaces around a word are removed automatically.  
The example below assumes the input file is 'input_dict.txt', the newly created output file where each word is on its own line is called 'output_dict.txt', comment lines start with a hash symbol (hashtag, '#'), and the separator is a comma (',').
Please mind that if the file 'output_dict.txt' already exists, it is not erased, but new content is appended.
Simply adjust the descriptively named variables in the first four lines to your needs.

```Python
>>> input_file  = 'input_dict.txt'
>>> output_file = 'output_dict.txt'
>>> comment_character = '#'
>>> separator_symbol  = ','
>>> with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
...  content = [line.strip() for line in infile if not line.startswith(comment_character)]
...  content = [word.strip() for line in content for word in line.split(separator_symbol) if word.strip()]
...  for w in content:
...   outfile.write(w + '\n')
...
```
