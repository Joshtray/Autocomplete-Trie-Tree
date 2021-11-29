# Autocomplete-Trie-Tree
A autocomplete algorithm that uses a trie tree data structure to store and suggest common words for a given prefix from a large set of words 

Functionalities:
insert:
        Inserts a word into the trie, creating and updating nodes as required.
lookup:
    Determines whether a given word is present in the trie.
alphabetical_list:
    Lists all the nodes in the tree alphabetically
k_most_common:
    Lists the k most common words in the trie tree
autocomplete:
    Given an input string, provides the most common valid word in the tree prefixed by that string
