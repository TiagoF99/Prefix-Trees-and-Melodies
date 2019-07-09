# Prefix-Trees-and-Melodies

melody.py: given as starter code
a2_sample_test.py: given as starter code
autocomplete_engines: All class and function headers and documentation given as starter code. I implemented every method.
prefix_tree.py: All class and function headers and documentation given as starter code. Autocompleter class given as starter code. __str__ and _str_indented functions in each class given as starter code. I implemented the remaining methods and helpers.

## Info

This project was developed as part of an assignment in CSC148H1. This project included taking a text file with words or sentences and different tree algortihms to store the data. The goal was then to look up specific prefixes of words or sentences and find all the items that fit the criteria in the tree and to then test the speed of each tree storing algorithm. The algorithms included: A storing algorithm that took each peice of text and inserted it into the tree with each node storing a value with a common prefix to each of its descendant values, andan algorithm to store values in a compressed manner. This meant that every value must be stored with only the most common prefix associated with it. Role: I wrote multiple autocompleter objects to process the data in the files and clean them, as well as process the search for all the items that fit a specific prefix. I also wrote the tree storing objects using the corresponding algorithms. Each object supported an initializer, finding its length, storing values, removing values, and searching for all values that fit a specific prefix. Testing was done using pythons build in library, hypothesis.
