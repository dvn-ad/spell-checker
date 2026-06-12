class TrieNode:
    def __init__(self, char: str = "", depth: int = 0):
        self.char = char
        self.depth = depth
        self.children = {}
        self.is_terminal = False
        self.word = None
        self.min_word_len = float('inf')
        self.max_word_len = -float('inf')

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.total_nodes = 1

    def insert(self, word: str):
        """
        Inserts a word into the Trie.
        """
        word = word.lower().strip()
        if not word:
            return
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char, node.depth + 1)
                self.total_nodes += 1
            node = node.children[char]
        node.is_terminal = True
        node.word = word

    def compute_length_bounds(self):
        """
        Calculates the minimum and maximum lengths of valid words in the subtree 
        rooted at each node. This runs once after all words have been inserted.
        """
        def _dfs(node: TrieNode):
            min_len = float('inf')
            max_len = -float('inf')
            
            if node.is_terminal:
                min_len = node.depth
                max_len = node.depth
                
            for child in node.children.values():
                child_min, child_max = _dfs(child)
                min_len = min(min_len, child_min)
                max_len = max(max_len, child_max)
                
            node.min_word_len = min_len
            node.max_word_len = max_len
            return min_len, max_len

        _dfs(self.root)
