"""
DM1

Implementation of the Spectral Partition Algorithm
"""

edges = []
adjacency_matrix = {}
number_nodes = 0

# Open the file
with open("facebook_combined.txt", "r") as datafile:
    for line in datafile:
        node1, node2 = line.split()
        node1 = int(node1)
        node2 = int(node2)
        edges.append({node1, node2})
        # The adjancency matrix is symmetric
        adjacency_matrix[(node1, node2)] = 1
        adjacency_matrix[(node2, node1)] = 1
        number_nodes = max(number_nodes, node1, node2)

number_nodes += 1  # We only had the maximum index of the nodes
print("Imported {} nodes with {} edges".format(number_nodes, len(edges)))

def A(i,j):
    return adjacency_matrix.get((i,j), 0)

# Random grouping
# s[i] =  1 if i belongs to group 1
#        -1 if i doesn't
import random
print("Computing a random grouping...")
s = [1 if random.randint(0,1) == 1 else -1 for _ in range(number_nodes)]

# Compute the degree of each node
print("Computing the degree of each node...")
d = []
for i in range(number_nodes):
    d.append(sum([A(i,j) for j in range(number_nodes)]))

# Laplacian matrix
print("Computing the Laplacian matrix...")
L = {}
for i in range(number_nodes):
    # Diagonal terms
    L[(i, i)] = d[i]

for (i, j) in edges:
    L[(i, j)] = -1
    L[(j, i)] = -1
