#!/usr/bin/python

# Load required modules
import pandas as pd 
import scipy.spatial
import scipy.cluster
import numpy as np
import json
import matplotlib.pyplot as plt
import hierarchy_analysis as hi

# Example data: gene expression
geneExp = {'genes' : ['a', 'b', 'c', 'd', 'e', 'f'],
     	   'exp1': [-2.2, 5.6, 0.9, -0.23, -3, 0.1],
	   'exp2': [5.4, -0.5, 2.33, 3.1, 4.1, -3.2]
          }
df = pd.DataFrame( geneExp )

# Determine distances (default is Euclidean)
dataMatrix = np.array( df[['exp1', 'exp2']] )
distMat = scipy.spatial.distance.pdist( dataMatrix )
distMat = hi.b

# Cluster hierarchicaly using scipy
clusters = scipy.cluster.hierarchy.linkage(distMat, method='single')
clusters = hi.c
T = scipy.cluster.hierarchy.to_tree( clusters , rd=False )

# Create dictionary for labeling nodes by their IDs
labels = hi.subreddit_names
id2name = dict(zip(range(len(labels)), labels))

# Draw dendrogram using matplotlib to scipy-dendrogram.pdf
scipy.cluster.hierarchy.dendrogram(clusters, labels=labels, orientation='right')
plt.savefig("scipy-dendrogram.png")

# Create a nested dictionary from the ClusterNode's returned by SciPy
def add_node(node, parent ):
	# First create the new node and append it to its parent's children
	newNode = dict( node_id=node.id, children=[] )
	parent["children"].append( newNode )

	# Recursively add the current node's children
	if node.left: add_node( node.left, newNode )
	if node.right: add_node( node.right, newNode )

# Initialize nested dictionary for d3, then recursively iterate through tree
d3Dendro = dict(children=[], name="Root1")
add_node( T, d3Dendro )

# Label each node with the names of each leaf in its subtree
def label_tree( n ):
	# If the node is a leaf, then we have its name
	if len(n["children"]) == 0:
		leafNames = [ id2name[n["node_id"]] ]
                n["name"] = leafNames
	
	# If not, flatten all the leaves in the node's subtree
	else:
		leafNames = reduce(lambda ls, c: ls + label_tree(c), n["children"], [])
		n["name"] = ""

	# Delete the node id since we don't need it anymore and
	# it makes for cleaner JSON
	del n["node_id"]

	# Labeling convention: "-"-separated leaf names
	#n["name"] = name = "-".join(sorted(map(str, leafNames)))
	
	return leafNames

label_tree( d3Dendro["children"][0] )

# Output to JSON
json.dump(d3Dendro, open("d3-dendrogram.json", "w"), sort_keys=True, indent=4)
