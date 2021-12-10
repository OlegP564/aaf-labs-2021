# Binary tree
# Binary tree
class Row:
    def __init__(self, values, index):
        self.value = values
        self.index = index
    
    
    def disp(self):
        row_text = "|"
        for v in self.values:
            row_text  = row_text + " " + str(v) + " |"
        return row_text

class Node:
    def __init__(self, row):
        self.value = row
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None
        self.size = 0
    

    def get_root(self):
        return self.root


    def add(self, row):
        if self.root is None:
            self.root = Node(row)
        else:
            self.__add(row, self.root)


    def __add(self, row, node):
        if row.index < node.value.index:
            if node.left is None:
                node.left = Node(row)
            else:
                self.__add(row, node.left)

        else:
            if node.right is None:
                node.right = Node(row)
            else:
                self.__add(row, node.right)


    def find(self, row):
        if self.root is None:            
            return None
        else:
            return self.__find(row, self.root)


    def __find(self, row, node):
        if row.index == node.value.index:
            return node
        elif (row.index < node.value.index and node.left is not None):
            return self.__find(row, node.left)
        elif (row.index > node.value.index and node.right is not None):
            return self.__find(row, node.right)


    def find_successor(self, node):
        while node.left is not None:
            node = node.left
        return node


    def delete(self, node, row):
        if node == None:
            return node
        if row.index == node.value.index:
            if node.left is None:
                node = node.right
            elif node.right is None:
                node = node.left
            else:
                node = self.find_successor(node)
                node.right = self.delete(node.right, node.value)
        elif row.index < node.value.index:
            node.left = self.delete(node.left, node.value)
        else:
            node.right = self.delete(node.right, node.value)
        return node





    def depth(self, node):
        if node == None:
            return 1
        
        
        return max(self.depth(node.left), self.depth(node.right)) + 1

    def display(self):
        if self.root is not None:
            self.__disp(self.root, self.depth(self.root))

    def __disp(self, node, c):
        if node is not None:
            self.__disp(node.left, c+1)
            print( '   '*c, str(node.value.disp()))
            self.__disp(node.right, c+1)



def pass_tree(node, array):
    if node:
        pass_tree(node.left, array)
        array.append(node.value)
        pass_tree(node.right, array)


