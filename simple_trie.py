
class TNode():
    def __init__(self):
        self.Values = []
        self.Children = {}

class TSimpleTrie(object):
    def __init__(self):
        self.Root = TNode()
    def Insert(self, key, value):
        if not key:
            raise ValueError('wrong format', 'empty key')
        node = self.Root 
        for char in key:
            if not char in node.Children:
                node.Children[char] = TNode()
            node = node.Children[char]
        node.Values.append(value)

    def GetAllValuesInSubtree(self, key):
        node = self.Root 
        for char in key:
            if not char in node.Children:
                return []
            else:
                node = node.Children[char]
        values2return = node.Values
        layer = node.Children.values()
        while layer:
            new_layer = []
            for node in layer:
                values2return += node.Values
                new_layer += node.Children.values()
            layer = new_layer
        return values2return
        
        