from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
            
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:

            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
           
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)
        
        return node

    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None or node.value == value:
            return node is not None
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def traverse(self, order='inorder'):
        result = []
        if order == 'inorder':
            self._inorder(self.root, result)
        elif order == 'preorder':
            self._preorder(self.root, result)
        elif order == 'postorder':
            self._postorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def to_dict(self, node=None):
        if node is None:
            node = self.root
            if node is None:
                return None
        
        result = {'value': node.value}
        
        if node.left:
            result['left'] = self.to_dict(node.left)
        if node.right:
            result['right'] = self.to_dict(node.right)
            
        return result

bst = BST()

@app.route('/insert', methods=['POST'])
def insert_value():
    data = request.get_json()
    value = data.get('value')
    
    if value is None:
        return jsonify({'error': 'No value provided'}), 400
        
    bst.insert(value)
    return jsonify(bst.to_dict())

@app.route('/delete', methods=['POST'])
def delete_value():
    data = request.get_json()
    value = data.get('value')
    
    if value is None:
        return jsonify({'error': 'No value provided'}), 400
        
    bst.delete(value)
    return jsonify(bst.to_dict())

@app.route('/search', methods=['POST'])
def search_value():
    data = request.get_json()
    value = data.get('value')
    
    if value is None:
        return jsonify({'error': 'No value provided'}), 400
        
    found = bst.search(value)
    return jsonify({'found': found})

@app.route('/traverse', methods=['POST'])
def traverse_tree():
    data = request.get_json()
    order = data.get('order', 'inorder')
    
    if order not in ['inorder', 'preorder', 'postorder']:
        return jsonify({'error': 'Invalid traversal order'}), 400
        
    result = bst.traverse(order)
    return jsonify({'traversal': result})

@app.route('/reset', methods=['POST'])
def reset_tree():
    global bst
    bst = BST()
    return jsonify({'message': 'Tree reset successfully'})

if __name__ == '__main__':
    app.run(debug=True)