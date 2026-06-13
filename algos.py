from trie import Trie, TrieNode

def get_heuristic(node: TrieNode, i: int, L: int, cost_ins: float, cost_del: float) -> float:
    depth = node.depth
    rem_typed = L - i
    min_rem = node.min_word_len - depth
    max_rem = node.max_word_len - depth
    
    if rem_typed < min_rem:
        return (min_rem - rem_typed) * cost_ins
    elif rem_typed > max_rem:
        return (rem_typed - max_rem) * cost_del
    else:
        return 0.0