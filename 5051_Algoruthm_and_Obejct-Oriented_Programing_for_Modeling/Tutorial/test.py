
def dfs_recursive(graph, start_node, visited=None, dfs_order=None):
    """
    graph: dict like graph_2
    start_node: starting vertex
    visited: set to track visited nodes (optional)
    dfs_order: list to record visit order (optional)
    Returns: (visited_set, dfs_order_list)
    """
    if visited is None:
        visited = set()
    if dfs_order is None:
        dfs_order = []

    # Mark current node as visited
    visited.add(start_node)
    dfs_order.append(start_node)

    # Visit all unvisited neighbors
    for neighbor in graph[start_node]:  # graph[start_node] returns a dict of neighbors
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, dfs_order)

    return visited, dfs_order

def dfs_stack(graph, start_node):
    """
    graph: dict like graph_2
    start_node: starting vertex
    Returns: list of nodes in DFS order
    """
    visited = set()
    stack = [start_node]
    dfs_order = []

    while stack:
        node = stack.pop()  # Always operate on the last element (top of stack)

        if node not in visited:
            visited.add(node)
            dfs_order.append(node)

            # Add all unvisited neighbors to stack (in reverse order for same result as recursive)
            # This ensures we visit them in the same order as recursive DFS
            for neighbor in reversed(list(graph[node].keys())):
                if neighbor not in visited:
                    stack.append(neighbor)

    return dfs_order


graph_2 = {
    'a': {'b': 4, 'h': 8},
    'b': {'a': 4, 'c': 8, 'h': 11},
    'c': {'b': 8, 'd': 7, 'f': 4, 'i': 2},
    'd': {'c': 7, 'e': 9, 'f': 14},
    'e': {'d': 9, 'f': 10},
    'f': {'c': 4, 'd': 14, 'e': 10, 'g': 2},
    'g': {'f': 2, 'h': 1, 'i': 6},
    'h': {'a': 8, 'b': 11, 'g': 1, 'i': 7},
    'i': {'c': 2, 'g': 6, 'h': 7}
}

# 递归版本
visited_set, order_recursive = dfs_recursive(graph_2, 'a')
print("Recursive DFS Order:", order_recursive)

# 栈版本
order_stack = dfs_stack(graph_2, 'a')
print("Stack DFS Order:", order_stack)