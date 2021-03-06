"""CSC148 Assignment 2: Autocomplete engines

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for the three different autocomplete engines
you are writing for this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
import csv
from typing import Any, Dict, List, Optional, Tuple

from melody import Melody
from prefix_tree import SimplePrefixTree, CompressedPrefixTree


################################################################################
# Text-based Autocomplete Engines (Task 4)
################################################################################
class LetterAutocompleteEngine:
    """An autocomplete engine that suggests strings based on a few letters.

    The *prefix sequence* for a string is the list of characters in the string.
    This can include space characters.

    This autocomplete engine only stores and suggests strings with lowercase
    letters, numbers, and space characters; see the section on
    "Text sanitization" on the assignment handout.

    === Attributes ===
    autocompleter: An Autocompleter used by this engine.
    config: A dictionary mapping input values to its values
    """
    autocompleter: Autocompleter
    config: Dict[str, Any]

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize this engine with the given configuration.

        <config> is a dictionary consisting of the following keys:
            - 'file': the path to a text file
            - 'autocompleter': either the string 'simple' or 'compressed',
              specifying which subclass of Autocompleter to use.
            - 'weight_type': either 'sum' or 'average', which specifies the
              weight type for the prefix tree.

        Each line of the specified file counts as one input string.
        Note that the line may or may not contain spaces.
        Each string must be sanitized, and if the resulting string contains
        at least one alphanumeric character, it is inserted into the
        Autocompleter.

        *Skip lines that do not contain at least one alphanumeric character!*

        When each string is inserted, it is given a weight of one.
        Note that it is possible for the same string to appear on more than
        one line of the input file; this would result in that string getting
        a larger weight (because of how Autocompleter.insert works).
        """
        # We've opened the file for you here. You should iterate over the
        # lines of the file and process them according to the description in
        # this method's docstring.
        self.config = config

        if config['autocompleter'] == 'simple':
            self.autocompleter = SimplePrefixTree(config['weight_type'])
        else:
            self.autocompleter = CompressedPrefixTree(config['weight_type'])
        with open(config['file'], encoding='utf8') as f:
            for line in f:
                clean = line.lower()
                clean_str = ''
                for char in clean:
                    if char.isalnum() or char == ' ':
                        clean_str += char
                prefix = []
                for char in clean_str:
                    prefix.append(char)
                self.autocompleter.insert(clean_str, 1.0, prefix)

    def autocomplete(self, prefix: str,
                     limit: Optional[int] = None) -> List[Tuple[str, float]]:
        """Return up to <limit> matches for the given prefix string.

        The return value is a list of tuples (string, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Note that the given prefix string must be transformed into a list
        of letters before being passed to the Autocompleter.

        Preconditions:
            limit is None or limit > 0
            <prefix> contains only lowercase alphanumeric characters and spaces
        """
        clean = prefix.lower()
        cleaned_str = ''
        for char in clean:
            if char.isalnum() or char == ' ':
                cleaned_str += char
        new = []
        for char in cleaned_str:
            new.append(char)
        return self.autocompleter.autocomplete(new, limit)

    def remove(self, prefix: str) -> None:
        """Remove all strings that match the given prefix string.

        Note that the given prefix string must be transformed into a list
        of letters before being passed to the Autocompleter.

        Precondition: <prefix> contains only lowercase alphanumeric characters
                      and spaces.
        """
        clean = prefix.lower()
        cleaned_str = ''
        for char in clean:
            if char.isalnum() or char == ' ':
                cleaned_str += char
        new = []
        for char in cleaned_str:
            new.append(char)
        self.autocompleter.remove(new)


class SentenceAutocompleteEngine:
    """An autocomplete engine that suggests strings based on a few words.

    A *word* is a string containing only alphanumeric characters.
    The *prefix sequence* for a string is the list of words in the string
    (separated by whitespace). The words themselves do not contain spaces.

    This autocomplete engine only stores and suggests strings with lowercase
    letters, numbers, and space characters; see the section on
    "Text sanitization" on the assignment handout.

    === Attributes ===
    autocompleter: An Autocompleter used by this engine.
    config: A dictionary mapping input values to its values
    """
    autocompleter: Autocompleter
    config: Dict[str, Any]

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize this engine with the given configuration.

        <config> is a dictionary consisting of the following keys:
            - 'file': the path to a CSV file
            - 'autocompleter': either the string 'simple' or 'compressed',
              specifying which subclass of Autocompleter to use.
            - 'weight_type': either 'sum' or 'average', which specifies the
              weight type for the prefix tree.

        Precondition:
        The given file is a *CSV file* where each line has two entries:
            - the first entry is a string
            - the second entry is the a number representing the weight of that
              string

        Note that the line may or may not contain spaces.
        Each string must be sanitized, and if the resulting string contains
        at least one word, it is inserted into the Autocompleter.

        *Skip lines that do not contain at least one alphanumeric character!*

        When each string is inserted, it is given a weight of one.
        Note that it is possible for the same string to appear on more than
        one line of the input file; this would result in that string getting
        a larger weight.
        """
        # We haven't given you any starter code here! You should review how
        # you processed CSV files on Assignment 1.
        self.config = config

        if config['autocompleter'] == 'simple':
            self.autocompleter = SimplePrefixTree(config['weight_type'])
        else:
            self.autocompleter = CompressedPrefixTree(config['weight_type'])

        with open(config['file']) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                clean = line[0].lower()
                weight = line[1]
                cleaned_str = ''
                for char in clean:
                    if char.isalnum() or char == ' ':
                        cleaned_str += char
                cleaned_num = ''
                for num in weight:
                    if num.isnumeric() or num == '.':
                        cleaned_num += num
                if cleaned_str != '' and cleaned_num != '':
                    self.autocompleter.insert(cleaned_str, float(cleaned_num),
                                              cleaned_str.split())

    def autocomplete(self, prefix: str,
                     limit: Optional[int] = None) -> List[Tuple[str, float]]:
        """Return up to <limit> matches for the given prefix string.

        The return value is a list of tuples (string, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given prefix.

        Note that the given prefix string must be transformed into a list
        of words before being passed to the Autocompleter.

        Preconditions:
            limit is None or limit > 0
            <prefix> contains only lowercase alphanumeric characters and spaces
        """
        clean = prefix.lower()
        cleaned_str = ''
        for char in clean:
            if char.isalnum() or char == ' ':
                cleaned_str += char
        return self.autocompleter.autocomplete(cleaned_str.split(), limit)

    def remove(self, prefix: str) -> None:
        """Remove all strings that match the given prefix.

        Note that the given prefix string must be transformed into a list
        of words before being passed to the Autocompleter.

        Precondition: <prefix> contains only lowercase alphanumeric characters
                      and spaces.
        """
        clean = prefix.lower()
        cleaned_str = ''
        for char in clean:
            if char.isalnum() or char == ' ':
                cleaned_str += char
        self.autocompleter.remove(cleaned_str.split())


################################################################################
# Melody-based Autocomplete Engines (Task 5)
################################################################################
class MelodyAutocompleteEngine:
    """An autocomplete engine that suggests melodies based on a few intervals.

    The values stored are Melody objects, and the corresponding
    prefix sequence for a Melody is its interval sequence.

    Because the prefix is based only on interval sequence and not the
    starting pitch or duration of the notes, it is possible for different
    melodies to have the same prefix.

    # === Private Attributes ===
    autocompleter: An Autocompleter used by this engine.
    _melody_name: A List of tuples with the melody and its name
    config: a dictionary mapping inut values to its values
    """
    autocompleter: Autocompleter
    _melody_name: List
    config: Dict[str, Any]

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize this engine with the given configuration.

        <config> is a dictionary consisting of the following keys:
            - 'file': the path to a CSV file
            - 'autocompleter': either the string 'simple' or 'compressed',
              specifying which subclass of Autocompleter to use.
            - 'weight_type': either 'sum' or 'average', which specifies the
              weight type for the prefix tree.

        Precondition:
        The given file is a *CSV file* where each line has the following format:
            - The first entry is the name of a melody (a string).
            - The remaining entries are grouped into pairs (as in Assignment 1)
              where the first number in each pair is a note pitch,
              and the second number is the corresponding duration.

            HOWEVER, there may be blank entries (stored as an empty string '');
            as soon as you encounter a blank entry, stop processing this line
            and move onto the next line the CSV file.

        Each melody is be inserted into the Autocompleter with a weight of 1.
        """
        # We haven't given you any starter code here! You should review how
        # you processed CSV files on Assignment 1.
        self.config = config
        self._melody_name = []

        if config['autocompleter'] == 'simple':
            self.autocompleter = SimplePrefixTree(config['weight_type'])
        else:
            self.autocompleter = CompressedPrefixTree(config['weight_type'])

        with open(config['file']) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line != '':
                    self._melody_help(line)

    def _melody_help(self, line: Any)-> None:
        """
        sanitizes line then inserts it into tree appropriately
        """
        new = [line[s:s + 2] for s in range(1, len(line), 2)]
        melody = []
        for item in new:
            if item[0] != '' and item[1] != '':
                melody.append((int(item[0]), int(item[1]),))
        interval = []
        for i in range(len(melody) - 1):
            interval.append(melody[i + 1][0] - melody[i][0])
        self._melody_name.append((melody, line[0],))
        self.autocompleter.insert(melody, 1.0, interval)

    def autocomplete(self, prefix: List[int],
                     limit: Optional[int] = None) -> List[Tuple[Melody, float]]:
        """Return up to <limit> matches for the given interval sequence.

        The return value is a list of tuples (melody, weight), and must be
        ordered in non-increasing weight. (You can decide how to break ties.)

        If limit is None, return *every* match for the given interval sequence.

        Precondition:
            limit is None or limit > 0
        """
        a = self.autocompleter.autocomplete(prefix, limit)
        new = []
        name = ''
        for item in a:
            for mel in self._melody_name:
                if mel[0] == item[0]:
                    name = mel[1]
            new.append((Melody(name, item[0]), item[1],))
        return new

    def remove(self, prefix: List[int]) -> None:
        """Remove all melodies that match the given interval sequence.
        """
        self.autocompleter.remove(prefix)


###############################################################################
# Sample runs
###############################################################################
def sample_letter_autocomplete() -> List[Tuple[str, float]]:
    """A sample run of the letter autocomplete engine."""
    engine = LetterAutocompleteEngine({
        # NOTE: you should also try 'data/google_no_swears.txt' for the file.
        'file': 'data/lotr.txt',
        'autocompleter': 'compressed',
        'weight_type': 'sum'
    })
    return engine.autocomplete('frodo d', 5)


def sample_sentence_autocomplete() -> List[Tuple[str, float]]:
    """A sample run of the sentence autocomplete engine."""
    engine = SentenceAutocompleteEngine({
        'file': 'data/google_searches.csv',
        'autocompleter': 'simple',
        'weight_type': 'sum'
    })
    return engine.autocomplete('how to', 11)


def sample_melody_autocomplete() -> None:
    """A sample run of the melody autocomplete engine."""
    engine = MelodyAutocompleteEngine({
        'file': 'data/songbook.csv',
        'autocompleter': 'compressed',
        'weight_type': 'sum'
    })
    melodies = engine.autocomplete([0], 7)
    for melody, _ in melodies:
        melody.play()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['csv', 'prefix_tree', 'melody']
    })

    # This is used to increase the recursion limit so that your sample runs
    # work even for fairly tall simple prefix trees.
    import sys
    sys.setrecursionlimit(5000)

    # print(sample_letter_autocomplete())
    # print(sample_sentence_autocomplete())
    # sample_melody_autocomplete()
