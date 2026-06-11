import math

# QWERTY coordinates for the 26 lowercase english keys
# row 1 is at y = 0.0
# row 2 is offset by 0.5 horizontally and placed at y = 1.0
# row 3 is offset by 1.5 horizontally and placed at y = 2.0
COORDINATES = {
    'q': (0.0, 0.0), 'w': (1.0, 0.0), 'e': (2.0, 0.0), 'r': (3.0, 0.0), 't': (4.0, 0.0),
    'y': (5.0, 0.0), 'u': (6.0, 0.0), 'i': (7.0, 0.0), 'o': (8.0, 0.0), 'p': (9.0, 0.0),
    'a': (0.5, 1.0), 's': (1.5, 1.0), 'd': (2.5, 1.0), 'f': (3.5, 1.0), 'g': (4.5, 1.0),
    'h': (5.5, 1.0), 'j': (6.5, 1.0), 'k': (7.5, 1.0), 'l': (8.5, 1.0),
    'z': (1.5, 2.0), 'x': (2.5, 2.0), 'c': (3.5, 2.0), 'v': (4.5, 2.0), 'b': (5.5, 2.0),
    'n': (6.5, 2.0), 'm': (7.5, 2.0)
}

def get_keyboard_graph():
    """
    Builds the adjacency list for Graph A (Keyboard Layout Graph).
    Two keys are connected by an undirected edge if their Euclidean distance <= 1.45.
    """
    keys = list(COORDINATES.keys())
    adj = {k: {} for k in keys}
    threshold = 1.45
    
    for i in range(len(keys)):
        k1 = keys[i]
        x1, y1 = COORDINATES[k1]
        for j in range(i + 1, len(keys)):
            k2 = keys[j]
            x2, y2 = COORDINATES[k2]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2) #euclidean
            if dist <= threshold:
                adj[k1][k2] = dist
                adj[k2][k1] = dist
    return adj

def compute_cost_matrix():
    """
    Runs Floyd-Warshall to generate the 26x26 substitution cost matrix M.
    """
    keys = sorted(list(COORDINATES.keys()))
    n = len(keys)
    key_to_idx = {key: i for i, key in enumerate(keys)}
    
    # Initialize distance matrix
    dist_matrix = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist_matrix[i][i] = 0.0
        
    adj = get_keyboard_graph()
    for k1, neighbors in adj.items():
        i = key_to_idx[k1]
        for k2, weight in neighbors.items():
            j = key_to_idx[k2]
            dist_matrix[i][j] = weight
            
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i][k] + dist_matrix[k][j] < dist_matrix[i][j]:
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]
                    
    # Map to (char1, char2) -> distance
    cost_map = {}
    for i, c1 in enumerate(keys):
        for j, c2 in enumerate(keys):
            cost_map[(c1, c2)] = dist_matrix[i][j]
            
    return cost_map, keys


class KeyboardLayout:
    def __init__(self):
        self.cost_map, self.keys = compute_cost_matrix()
        
    def get_keyboard_graph(self):
        """
        Returns the undirected keyboard layout adjacency graph.
        """
        return get_keyboard_graph()

    def get_substitution_cost(self, c1: str, c2: str) -> float:
        """
        Returns the substitution cost between two characters.
        If identical, cost is 0. If adjacent, cost is low. If far, cost is higher.
        """
        c1 = c1.lower()
        c2 = c2.lower()
        if c1 == c2:
            return 0.0
        if c1 not in self.cost_map or c2 not in self.cost_map:
            # Fallback for characters outside the alphabet (e.g. punctuation, spaces)
            return 4.0
        return self.cost_map[(c1, c2)]