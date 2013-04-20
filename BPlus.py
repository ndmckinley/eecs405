import math

class BPTree:
    def __init__(self, keySize, dataRecord, blockPointer, dataPointer, blockSize):
        self.keySize = keySize
        self.dataRecordSize = dataRecord
        self.blockPointerSize = blockPointer
        self.dataPointerSize = dataPointer
        self.blockSize = blockSize
        self.root = BPleaf(self, keySize, dataRecord, blockPointer, dataPointer, blockSize, keys = [])
    
    def insert(self, key):
        node = self.root
        while not isinstance(node, BPleaf):
            node = node.search(key)
        node.insert(key)
    
    def delete(self, key):
        node = self.root
        while not isinstance(node, BPleaf):
            node = node.search(key)
        node.delete(key)
    
    def __str__(self):
        return str(self.root)

class BPnode:
    def __init__(self, parent, keySize, dataRecord, blockPointer, dataPointer, blockSize, keys=[], children=[]):
        self.parent = parent
        self.order = int(math.floor(float(blockSize-blockPointer)/(keySize+blockPointer))) + 1
        self.keys = keys
        self.children = children
        
    def insert(self, node):
        minimum = node.findMin()
        
        if len(self.children) == 0:
            self.children.append(node)
        elif len(self.children) == 1:
            if self.children[0].findMin() < minimum:
                self.keys.append(minimum)
                self.children.append(node)
            else:
                self.keys.append(self.children[0].findMin())
                self.children.insert(0,node)
        else:
            index = 0
            while index < len(self.keys) and minimum >= self.keys[index]:
                index = index + 1
            self.keys.insert(index, minimum)
            self.children.insert(index+1, node)
        
        if len(self.children) > self.order:
            self.split()
    
    def split(self):
        mid = int(math.ceil(self.order/2.0))
        newKeys = self.keys[:(mid-1)]
        newChildren = self.children[:mid]
        self.keys = self.keys[mid:]
        self.children = self.children[mid:]
        newNode = BPnode(self.parent, 1, 0, 0, 0, self.order-1, keys=newKeys, children=newChildren)
        
        if isinstance(self.parent, BPTree):
            tree = self.parent
            newRoot = BPnode(tree, 1, 0, 0, 0, self.order-1, keys=[], children=[])
            tree.root = newRoot
            self.parent = newRoot
            newNode.parent = newRoot
            newRoot.insert(self)
            newRoot.insert(newNode)
        else:
            self.parent.insert(newNode)
    
    def combine(self, node):
        index = self.children.index(node)
        if index == len(self.children) - 1:
            mergeChild = self.children[index-1]
            self.children.pop(index-1)
            self.keys.pop(index-1)
        else:
            mergeChild = self.children[index+1]
            self.children.pop(index+1)
            self.keys.pop(index)
        node.merge(mergeChild)
        
        if isinstance(self.parent, BPTree) and len(self.children) == 1:
            self.parent.root = self.children[0]
            self.children[0].parent = self.parent
        elif not isinstance(self.parent, BPTree) and len(self.children) < math.ceil(self.order/2.0):
            self.parent.combine(self)
    
    def merge(self, node):
        if self.findMin() < node.findMin():
            self.keys.append(node.findMin)
            self.keys.extend(node.keys)
            self.children.extend(node.children)
        else:
            node.keys.append(self.findMin())
            node.keys.extend(self.keys)
            self.keys = node.keys
            node.children.extend(self.children)
            self.children = node.children
        
        if len(self.children) > self.order:
            self.split()
    
    def search(self, key):
        assert len(self.children) > 0
        if len(self.children) == 1:
            return self.children[0]

        child = 0
        while child < len(self.keys) and key >= self.keys[child]:
            child = child + 1
        return self.children[child]
    
    def findMin(self):
        return self.children[0].findMin()
    
    def __str__(self):
        output = "[ \n"
        output = output + str(self.children[0])
        index = 0
        while index < len(self.keys):
            output = output + str(self.keys[index]) + " " + str(self.children[index+1]) + " "
            index = index + 1
        output = output + "]\n"
        return output

class BPleaf:
    def __init__(self, parent, keySize, dataRecord, blockPointer, dataPointer, blockSize, keys=[]):
        self.parent = parent
        self.order = int(math.floor(float(blockSize-blockPointer)/(keySize+dataRecord)))
        self.keys = keys
        
    def insert(self, key):
        self.keys.append(key)
        self.keys.sort()
        if len(self.keys) > self.order:
            self.split()
    
    def split(self):
        newNodeList = self.keys[int(math.ceil(self.order/2.0)):]
        self.keys = self.keys[:int(math.ceil(self.order/2.0))]
        newNode = BPleaf(self.parent, 1, 0, 0, 0, self.order, newNodeList)
        if isinstance(self.parent, BPTree):
            tree = self.parent
            newRoot = BPnode(tree, tree.keySize, tree.dataRecordSize, tree.blockPointerSize, tree.dataPointerSize, tree.blockSize, keys=[], children=[])
            tree.root = newRoot
            self.parent = newRoot
            newNode.parent = newRoot
            newRoot.insert(self)
            newRoot.insert(newNode)
        else:
            self.parent.insert(newNode)
        
    def delete(self, key):
        if key in self.keys:
            self.keys.remove(key)
            if len(self.keys) < math.ceil(self.order/2.0) and not isinstance(self.parent, BPTree):
                self.parent.combine(self)
        
    def find(self, key):
        if key in self.keys:
            return self.keys.index(key)
        else:
            return -1
    
    def merge(self, node):
        if len(self.keys) == 0:
            self.keys = node.keys
        else:
            if node.findMin() < self.findMin():
                self.keys = node.keys + self.keys
            else:
                self.keys = self.keys + node.keys
        if len(self.keys) > self.order:
            self.split()
    
    def findMin(self):
        return self.keys[0]
    
    def __str__(self):
        output = "[ "
        index = 0
        while index < len(self.keys):
            output = output + str(self.keys[index]) + " "
            index = index + 1
        output = output + "]\n"
        return output
        