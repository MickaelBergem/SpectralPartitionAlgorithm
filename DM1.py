"""
DM1

Implementation of the Spectral Partition Algorithm
"""
import numpy as np
import subprocess
import logging


def import_nodes(nodes_file):
    """
    Import the nodes from the file
    """

    edges = []
    adjacency_matrix = {}
    number_nodes = 0

    # Open the file
    with open(nodes_file, "r") as datafile:
        for line in datafile:
            node1, node2 = line.split()
            node1 = int(node1)
            node2 = int(node2)
            edges.append({node1, node2})
            number_nodes = max(number_nodes, node1, node2)

    number_nodes += 1  # We only had the maximum index of the nodes
    logging.info("Imported {} nodes with {} edges from {}".format(number_nodes, len(edges), nodes_file))

    # Initiate empty matrix
    adjacency_matrix = np.zeros((number_nodes, number_nodes))

    # Fill the matrix
    for node1, node2 in edges:
        # The adjancency matrix is symmetric
        adjacency_matrix[node1][node2] = 1
        adjacency_matrix[node2][node1] = 1

    return (number_nodes, edges, adjacency_matrix)


def degree_nodes(adjacency_matrix, number_nodes):
    """
    Compute the degree of each node
    Returns the vector of degrees
    """

    d = []
    for i in range(number_nodes):
        d.append(sum([adjacency_matrix[i][j] for j in range(number_nodes)]))

    return d


def print_graph(number_nodes, edges, partition, outputfile):
    """
    Writes a .gv file to use with dot
    """
    with open("graph.gv", "w") as gv:
        gv.write("strict graph communities {")

        for node, community in enumerate(partition):
            gv.write("node{} [color={}];".format(node, "red" if community else "blue"))

        for node1, node2 in edges:
            gv.write("node{} -- node{};".format(node1, node2))

        gv.write("}")
        gv.close()

    subprocess.call(["dot", "-Tpng", "graph.gv", "-o", outputfile])
    logging.warning("Wrote {} with the two communities.".format(outputfile))


def algorithm(nodes_file):
    """
    The Spectral Partitioning Algorithm
    """

    logging.warning("Computing Adjacency Matrix...")

    number_nodes, edges, adjacency_matrix = import_nodes(args.nodes_file)
    logging.debug("Adjacency matrix:\n", adjacency_matrix)

    logging.warning("Computing the degree of each node...")
    degrees = degree_nodes(adjacency_matrix, number_nodes)
    logging.debug("Degrees: ", degrees)

    logging.warning("Computing the Laplacian matrix...")
    laplacian_matrix = np.diag(degrees) - adjacency_matrix
    logging.debug("Laplacian matrix:\n", laplacian_matrix)

    logging.warning("Computing the eigenvectors and eigenvalues...")
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian_matrix)

    logging.info("Found eigenvalues: ", eigenvalues)

    # We want the lowest non-zero eigenvalue
    eigenvalues = eigenvalues.tolist()
    nzev = [ev for ev in eigenvalues if abs(ev) > 1e-15]

    # Index of the first non-zero eigenvalue
    index_fnzev = eigenvalues.index(min(nzev))

    logging.debug("Eigenvector for #{} eigenvalue ({}): ".format(
        index_fnzev, eigenvalues[index_fnzev]), eigenvectors[:, index_fnzev])

    # Partition on the sign of the eigenvector's coordinates
    partition = [val >= 0 for val in eigenvectors[:, index_fnzev]]

    logging.warning("Partition computed.")
    return number_nodes, edges, partition


if __name__ == '__main__':
    import argparse

    # Configure logging
    FORMAT = '%(asctime)s.%(msecs)03d %(message)s'
    logging.basicConfig(format=FORMAT, datefmt='%H:%M:%S')

    parser = argparse.ArgumentParser(description="Compute the partition of a "
        "graph using the Spectral Partition Algorithm.")

    parser.add_argument('--nodes-file', '-f', help='the file containing the nodes',
                        default='demo_nodes.txt')
    parser.add_argument('--output-file', '-o', help='the PNG file of the graph',
                        default='partition.png')

    args = parser.parse_args()

    # Run the algorithm
    number_nodes, edges, partition = algorithm(args.nodes_file)

    logging.info("Partition: ", partition)

    # Print the graph
    print_graph(number_nodes, edges, partition, outputfile=args.output_file)
