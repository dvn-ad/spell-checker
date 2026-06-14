from trie import Trie, TrieNode
import heapq
from keyboard import KeyboardLayout

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
    
def astar_search(typed_word: str, trie: Trie, keyboard: KeyboardLayout, 
                 cost_ins: float = 1.0, cost_del: float = 1.0, 
                 max_cost: float = float('inf')):
    
    typed_word = typed_word.lower().strip()
    L = len(typed_word)
    root = trie.root
    
    # Priority Queue state format: (f_score, g_score, typed_index, path_word, state_id, trie_node)
    # Including path_word in the tuple serves two purposes:
    # 1. Resolves tie-breaks lexicographically (alphabetical preference for same-cost words).
    # 2. Avoids comparing TrieNode objects directly.
    state_id = 0
    h_root = get_heuristic(root, 0, L, cost_ins, cost_del)
    pq = [(h_root, 0.0, 0, "", state_id, root)]
    
    # Track minimum g-score for visited states: (node_ref, typed_index) -> min_g
    visited = {}
    best_cost = max_cost
    best_word = None
    nodes_visited_count = 0
    
    while pq:
        f, g, i, path_word, _, node = heapq.heappop(pq)
        nodes_visited_count += 1
        
        # If the lowest f-score in PQ is >= best_cost, we can stop immediately due to A* properties.
        if f >= best_cost:
            break
            
        # Check visited states to prune duplicates
        state_key = (node, i)
        if state_key in visited and visited[state_key] <= g:
            continue
        visited[state_key] = g
        
        # Check if we reached a terminal node representing a full dictionary word
        if i == L and node.is_terminal:
            if g < best_cost:
                best_cost = g
                best_word = node.word
            # Since f = g + h, and h = 0 at goal, this is the optimal path.
            # Tie-breaking by path_word in the tuple ensures it's alphabetically optimal.
            return best_word, best_cost, nodes_visited_count
            
        # 1. Deletion from typed_word: advance typed_index (i), keep current trie node
        if i < L:
            new_g = g + cost_del
            new_h = get_heuristic(node, i + 1, L, cost_ins, cost_del)
            new_f = new_g + new_h
            
            if new_f < best_cost:
                state_id += 1
                heapq.heappush(pq, (new_f, new_g, i + 1, path_word, state_id, node))
                
        # 2. Match/Substitution: advance i, transition to child node
        if i < L:
            typed_char = typed_word[i]
            for child_char, child_node in node.children.items():
                sub_cost = keyboard.get_substitution_cost(typed_char, child_char)
                new_g = g + sub_cost
                new_h = get_heuristic(child_node, i + 1, L, cost_ins, cost_del)
                new_f = new_g + new_h
                
                if new_f < best_cost:
                    state_id += 1
                    # Append child_char to path_word for alphabetical ordering
                    heapq.heappush(pq, (new_f, new_g, i + 1, path_word + child_char, state_id, child_node))
                    
        # 3. Insertion into dictionary: keep i, transition to child node
        for child_char, child_node in node.children.items():
            new_g = g + cost_ins
            new_h = get_heuristic(child_node, i, L, cost_ins, cost_del)
            new_f = new_g + new_h
            
            if new_f < best_cost:
                state_id += 1
                heapq.heappush(pq, (new_f, new_g, i, path_word + child_char, state_id, child_node))
                
    return best_word, best_cost, nodes_visited_count
