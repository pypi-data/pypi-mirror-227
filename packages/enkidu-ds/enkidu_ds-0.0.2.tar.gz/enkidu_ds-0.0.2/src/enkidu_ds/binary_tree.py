from queue import Queue

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.data}"

    def attach_child(self, side, data):
        child_node = TreeNode(data)
        if side == 'left':
            self.left = child_node
        elif side == 'right':
            self.right = child_node
        else:
            raise Exception('wrong side. need left or right.')

        return child_node


class BinaryTree:
    def __init__(self, nodes):
        self.root = self.create_binary_tree(nodes)

    
    def create_binary_tree(self, nodes):

        if len(nodes) == 0:
            return None

        # create the root node of the binary tree
        root = TreeNode(nodes[0].data)

        # create a queue and add the root node to it
        queue = Queue()
        queue.put(root)

        # start iterating over the list of nodes starting from the second node
        i = 1
        while i < len(nodes):
            # get the next node from the queue
            current = queue.get()

            # if the node is not none, create a new TreeNode object for its left child,
            # set it as the left child of the current node, and add it to the queue.
            if nodes[i] is not None:
                current.left = TreeNode(nodes[i].data)
                queue.put(current.left)

            i += 1

            # if there are more nodes in the list and the next node is not None,
            # create a new TreeNode object for its right child, set it as the right child
            # of the current node, and add it to the queue
            if i < len(nodes) and nodes[i] is not None:
                current.right = TreeNode(nodes[i].data)
                queue.put(current.right)

            i += 1

        # notice how tree == root
        return root

    # TODO print the tree visually
    def print_tree(self):
        pass


