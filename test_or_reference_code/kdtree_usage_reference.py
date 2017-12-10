"""
Illustrates how to work with the kd_tree module.

"""

import kdtree

# Create an empty tree by specifying the number of
# dimensions its points will have
emptyTree = kdtree.create(dimensions=3)

# A kd-tree can contain different kinds of points, for example tuples
point1 = (2, 3, 4)

# Lists can also be used as points
point2 = [4, 5, 6]

# Other objects that support indexing can be used, too
import collections
Point = collections.namedtuple('Point', 'x y z')
point3 = Point(5, 3, 2)

# A tree is created from a list of points
tree = kdtree.create([point1, point2, point3])

# Each (sub)tree is represented by its root node
print(tree)

# Adds a tuple to the tree
tree.add( (5, 4, 3) )

# Removes the previously added point and returns the new root
tree = tree.remove( (5, 4, 3) )

# Retrieving the Tree in inorder
print(list(tree.inorder()))

# Retrieving the Tree in level order
print(list(kdtree.level_order(tree)))

# Find the nearest node to the location (1, 2, 3)
tree.search_nn( (1, 2, 3) )

# Add a point to make the tree more interesting
tree.add( (10, 2, 1) )

# Visualize the Tree
kdtree.visualize(tree)

# Take the right subtree of the root
subtree = tree.right

# and detatch it
tree.right = None
kdtree.visualize(tree)
kdtree.visualize(subtree)

# and re-attach it
tree.right = subtree
kdtree.visualize(tree)


# Add a node to make the tree unbalanced
print(tree.is_balanced)
tree.add( (6, 1, 5) )
tree.is_balanced
kdtree.visualize(tree)

# rebalance the tree
tree = tree.rebalance()
print(tree.is_balanced)
kdtree.visualize(tree)
