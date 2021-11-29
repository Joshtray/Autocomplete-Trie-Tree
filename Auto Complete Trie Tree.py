class Node:
    """This class represents one node of a trie tree.

    Parameters
    -----------
    string : str
        The string value of the node
    children : list
        A list of all the children of the node
    parent : Node
        The parent of the current node. Default set to 'None' (for the root node)
    valid : boolean
        Defines whether the node holds a valid word
    frequency : int
        The number of times the node is inserted into the tree
    max_child : Node
        The descendant of the current node with maximum frequency.
    
    """

    def __init__(self, string, parent=None):        
        self.string = string
        self.children = []
        self.parent = parent
        
        #Attribute that determines whether a given node has a valid word (True) or not (False)
        self.valid = False
        
        #Attribute that defines the frequency of insertion of a node into the tree
        self.frequency = 0
        
        #New attribute that defines the most common descendant of each node in the tree
        self.max_child = None
        
    def __repr__(self):
        return f"Node {self.string} => {[self.children]} <=> End"
    
    def __lt__(self, other):
        return self.string < other.string
        
class Trie:
    """This class represents the entirety of a trie tree.
    
    Parameters
    -----------
    root : Node
        A node that represents the root of the tree. The node has a parent attribute of 'None'

    Methods
    -------
    insert(self, word)
        Inserts a word into the trie, creating and updating nodes as required.
    lookup(self, word)
        Determines whether a given word is present in the trie.
    alphabetical_list(self)
        Lists all the nodes in the tree alphabetically
    k_most_common(self, k)
        Lists the k most common words in the trie tree
    autocomplete(self, prefix)
        Given an input string, provides the most common valid word in the tree prefixed by that string
    """
    
    def __init__(self, word_list = None):
        """Creates the Trie instance, inserts initial words if provided.
        
        Parameters
        ----------
        word_list : list
            List of strings to be inserted into the trie upon creation.
        """
        
        #Define the root node
        self.root = Node("")
        
        #If given a word list, then insert each word in the word list into the tree
        for word in word_list:
            self.insert(word.lower())
            
    
    def insert(self, word):
        """Inserts a word into the trie, creating missing nodes on the go.
        
        Parameters
        ----------
        word : str
            The word to be inserted into the trie.
        """        
        node = self.root
        
        #Replace the word to be inserted with its lowercase
        word = word.lower()
        i = 0
        
        while i < len(word):
            j = i
            
            #For each substring from the start of the word, we check if it is equal to a child of the current node
            for child in node.children:
                
                #If we come across the child that is equal to the substring, then the word must be a descendant of that child. So we move down to the child and increase the size of the substring being considered
                if word[:i+1] == child.string:
                    i += 1
                    node = child
                    break
                    
            #If we go through the for loop and don't find any children equal to the substring, then we need to create a new child of the current node for that substring and move down to the child
            if i == j:
                child = Node(word[:i+1], node)
                node.children.append(child)
                i += 1
                node = child
                
        #When we have gotten to/created the final node that contains the word, we increase its frequency by 1.
        node.frequency += 1

        
        #This section maintains the max_child attribute whenever a node is inserted
        if node.max_child:
            
            #If the node for the inserted word has a max_child, then we compare the max_child of the node with the node's frequency and update it to be the node itself if the node's frequency is higher.
            if node.max_child.frequency <= node.frequency:
                node.max_child = node
                
        #If the node doesn't have a max_child, then set the max_child to be the node itself.
        else:
            node.max_child = node
            
        while node.parent:
            #Starting from the inserted node, we update the max_child of each parent of the node until the root
            if node.parent.max_child:
                
                #If the current node's parent has a max_child, then we compare the max_child of the node's parent with the node's max_child's frequency and update it to be the node itself if the node's max_child's frequency is higher.
                if node.parent.max_child.frequency <= node.max_child.frequency:
                    node.parent.max_child = node.max_child
            
            #If the node's parent doesn't have a max_child, then set the max_child to be the node max_child.
            else:
                node.parent.max_child = node.max_child
            node = node.parent
            
            
        #When we have gotten to/created the final node that contains the word, we set its valid attribute to True.
        node.valid = True
        
        
    def lookup(self, word):
        """Determines whether a given word is present in the trie.
        
        Parameters
        ----------
        word : str
            The word to be looked-up in the trie.
            
        Returns
        -------
        bool
            True if the word is present in trie; False otherwise.
        """
        
        node = self.root
        i = 0
        while i < len(word):
            j = i
            
            #For each substring from the start of the word, we check if it is equal to a child of the current node
            for child in node.children:
                
                #If we come across a child that is equal to the substring, then if the node we are searching for is in the tree, it must be a descendant of that child, so we move down to the child and increase the substring length
                if word[:i+1].lower() == child.string:
                    i += 1
                    node = child
                    break
                    
            #If we check all the children and don't find any that are equal to the substring, then the word cannot be in the tree, so we return False
            if i == j:
                return False
        
        #If the word is found in the tree, we check whether it is a valid word or not, and return the response.
        return node.valid

    def alphabetical_list(self):
        """Delivers the content of the trie in alphabetical order.
        
        Returns
        ----------
        list
            List of strings, all words from the trie in alphabetical order.
        """
        
        #Calling a helper function alpha sort
        return self.alpha_sort(self.root)
    
    def alpha_sort(self, node):
        """Sorts the subtree rooted at a node in alphabetical order
        Parameters
        ----------
        node : Node
            The node which the subtree we wish to sort is rooted at
            
        Returns
        -------
        list
            A list of the string values of the nodes in the subtree
        """
        sort_list = []
        
        #First we append the root node (because we are implementing pre-order traversal) if it is valid and has a parent.
        if node.parent and node.valid:
            sort_list.append(node.string)
        
        #Next we sort the children in alphabetical order
        node.children.sort()
        
        for child in node.children:
            
            #We call alpha_sort recrusively on each child of the current node to get the sorted list of the descendants of that child
            child_sort = self.alpha_sort(child)
            
            #We add each of the words in the sorted list of each child to sort_list
            for val in child_sort:
                sort_list.append(val)
            
        #Finally, we return the list of the strings sorted alphabetically
        return sort_list
    
    def max_frequency(self, node, bound=[]):
        """Given a subtree rooted at a node, this computes the descendant node with the maximum frequncy that is not in the bound
        Parameters
        ----------
        node : Node
            The node which the subtree is rooted at
        bound : list
            The list of nodes that should not be counted in getting the maximum frequency
        Returns
        -------
        tuple
            Returns a tuple containing the string value and frequency of the Most common descenant node
        """
        if (node.string, node.frequency) in bound:
            
            #If the given node is already in the bound list, then we set the current max_node and max_freq values to the root node
            max_node = ""
            max_freq = 0
        else:
            
            #If the given node is not in the bound list, then we set the current max_node and max_freq values to the nodes string and frequency
            max_node = node.string
            max_freq = node.frequency
        
        for i in range(len(node.children)):
            
            #We recursively get the most common node not in the bound list from the subtree of each of the current node's children
            max_child = self.max_frequency(node.children[i], bound)
            
            #We compare the current max_freq to the max_freq of the child's subtree. If the max_freq of the child's subtree is greater, then we update the max_node and max_freq values
            if max_freq < max_child[1] and max_child not in bound:
                max_node = max_child[0]
                max_freq = max_child[1]
                
            #If the frequencies are equal, we update the max_node with the string value that's lexicographicallly greater.
            elif max_freq == max_child[1]:
                max_node = min(max_child[0], max_node)
                max_freq = max_child[1]
        
        #Finally we return the tuple of the max_node and max_frequency for that node's subtree. 
        return max_node, max_freq
    
    def k_most_common(self, k):
        """Finds k words inserted into the trie most often.

        Parameters
        ----------
        k : int
            Number of most common words to be returned.

        Returns
        ----------
        list
            List of tuples.
            
            Each tuple entry consists of the word and its frequency.
            The entries are sorted by frequency.

        Example
        -------
        >>> print(trie.k_most_common(3))
        [(‘the’, 154), (‘a’, 122), (‘i’, 122)]
        
        I.e. the word ‘the’ has appeared 154 times in the inserted text.
        The second and third most common words both appeared 122 times.
        """
        
        kmc = []
        for i in range(k):
            
            #We call max_frequency() k times. Each time we pass it the current list of k_most_common nodes, which max_frequency uses as a bound
            kmc.append(self.max_frequency(self.root, kmc))
            
        #Return the list of the k most common nodes in the tree
        return kmc


    def autocomplete(self, prefix):
        """Finds the most common word with the given prefix.


        Parameters
        ----------
        prefix : str
            The word part to be “autocompleted”.

        Returns
        ----------
        str
            The complete, most common word with the given prefix.
            
        Notes
        ----------
        The return value is equal to prefix if there is no valid word in the trie.
        The return value is also equal to prefix if prefix is the most common word.
        """
        
        node = self.root
        i = 0
        
        #We perform the lookup algorithm to check the tree for the node. This gives us the node for the prefix, if it is in the tree.
        while i < len(prefix):
            j = i
            
            #For each substring from the start of the word, we check if it is equal to a child of the current node
            for child in node.children:
                
                #If we come across a child that is equal to the substring, then if the node we are searching for is in the tree, it must be a descendant of that child, so we move down to the child and increase the substring length
                if prefix[:i+1].lower() == child.string:
                    i += 1
                    node = child
                    break
            
            #Return the prefix if we do not find the node in the tree
            if i == j:
                return prefix
        
        # If the prefix corresponds to a node in the tree, then we return the most common node in the subtree rooted at that node
        return node.max_child.string

from requests import get
bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']']

SH_full = get('http://bit.ly/CS110-Shakespeare').text
SH_just_text = ''.join(c for c in SH_full if c not in bad_chars)
SH_without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in SH_just_text)
SH_just_words = [word for word in SH_without_newlines.split(" ") if word != ""]

SH_trie = Trie(SH_just_words)

assert SH_trie.autocomplete('hist') == 'history'
assert SH_trie.autocomplete('en') == 'enter'
assert SH_trie.autocomplete('cae') == 'caesar'
assert SH_trie.autocomplete('gen') == 'gentleman'
assert SH_trie.autocomplete('pen') == 'pen'
assert SH_trie.autocomplete('pent') == 'pentapolis'
assert SH_trie.autocomplete('tho') == 'thou'
assert SH_trie.autocomplete('petr') == 'petruchio'