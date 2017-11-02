class Node():
    
    def __init__(self, fg = None, fd = None):
        """
        A binary tree is either a leaf or a node with two subtrees.
        
        INPUT:
            
            - children, either None (for a leaf), or a list of size excatly 2 
            of either two binary trees or 2 objects that can be made into binary trees
        """
        self._isleaf = (fg is None and fd is None)
        if not self._isleaf:
            if fg is None or fd is None:
                raise ValueError("Un arbre a 2 fils")
            self._children = [fg if isinstance(fg,Node) else Node(fg), fd if isinstance(fd,Node) else Node(fd)]
        self._size = None
        
    def __repr__(self):
        if self.is_leaf():
            return "Leaf"
        return str(self._children)
    
    def __eq__(self, other):
        """
        Return true if other represents the same binary tree as self
        """
        if not isinstance(other, Node):
            return False
        if self.is_leaf():
            return other.is_leaf()
        return self.left() == other.left() and self.right() == other.right()
    
    
    def left(self):
        """
        Return the left subtree of self
        """
        return self._children[0]
    
    def right(self):
        """
        Return the right subtree of self
        """
        return self._children[1]
    
    def is_leaf(self):
        """
        Return true is self is a leaf
        """
        return self._isleaf
    
    def _compute_size(self):
        """
        Recursively computes the size of self
        """
        if self.is_leaf():
            self._size = 1
        else:
            self._size = self.left().size() + self.right().size()
    
    def size(self):
        """
        Return the number of non leaf nodes in the binary tree
        """
        if self._size is None:
            self._compute_size()
        return self._size
    
Leaf = Node()

