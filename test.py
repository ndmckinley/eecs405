from BPlus import BPTree

tree = BPTree(1,0,0,0,4)  #leaves are order 4, internal nodes can have 5 children
print str(tree)
tree.insert(1)
print str(tree)
tree.insert(2)
print str(tree)
tree.insert(3)
print str(tree)
tree.insert(4)
print str(tree)
tree.insert(5)
print str(tree)
tree.insert(6)
print str(tree)
tree.insert(7)
print str(tree)
tree.insert(8)
print str(tree)
tree.insert(9)
print str(tree)
tree.insert(10)
print str(tree)
tree.insert(11)
print str(tree)
tree.insert(12)
print str(tree)
tree.insert(13)
print str(tree)


print " "
print " "

tree2 = BPTree(1,0,0,0,2)  ##leaves are order 2, internal nodes can have 3 children
print str(tree2)
tree2.insert(5)
print str(tree2)
tree2.insert(8)
print str(tree2)
tree2.insert(1)
print str(tree2)
tree2.insert(7)
print str(tree2)
tree2.insert(3)
print str(tree2)
tree2.insert(12)
print str(tree2)
tree2.insert(9)
print str(tree2)
tree2.insert(6)
print str(tree2)
tree2.delete(7)
print str(tree2)
tree2.delete(8)
print str(tree2)
tree2.delete(3)
print str(tree2)
tree2.delete(1)
print str(tree2)

from gui import get_tree_view, draw_a_tree

tv = get_tree_view(tree2).mainloop()
