import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class GeneralTree:
    def __init__(self):
        self.root = None

    def insert(self, parent_value, value):
        if self.root is None:
            self.root = Node(value)
        else:
            parent = self.search(parent_value)
            if parent:
                parent.children.append(Node(value))
            else:
                print(f"Parent {parent_value} not found.")

    def search(self, value, node=None):
        if node is None:
            node = self.root
        if node is None:
            return None
        if node.value == value:
            return node
        for child in node.children:
            result = self.search(value, child)
            if result:
                return result
        return None

    def count_nodes(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return 0
        return 1 + sum(self.count_nodes(child) for child in node.children)

    def count_non_leaf_nodes(self, node=None):
        if node is None:
            node = self.root
        if node is None or not node.children:
            return 0
        return 1 + sum(self.count_non_leaf_nodes(child) for child in node.children)

    def display(self, node, level=0):
        if node is not None:
            print(" " * (level * 4) + str(node.value))
            for child in node.children:
                self.display(child, level + 1)

    def is_binary_tree(self, node=None):
        if node is None:
            node = self.root
        if node is None:
            return True
        if len(node.children) > 2:
            return False
        return all(self.is_binary_tree(child) for child in node.children)

    def visualize(self):
        G = nx.DiGraph()
        self._add_edges(self.root, G)
        if self.is_binary_tree():
            pos = self._binary_tree_layout(self.root, 0, 0, 1, {})
        else:
            pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=12, font_weight='bold', arrows=False)
        plt.show()

    def _add_edges(self, node, G):
        if node is not None:
            for child in node.children:
                G.add_edge(node.value, child.value)
                self._add_edges(child, G)

    def _binary_tree_layout(self, node, x, y, level_gap, pos, level=0):
        if node:
            pos[node.value] = (x, -y)
            if len(node.children) > 0:
                self._binary_tree_layout(node.children[0], x - level_gap, y + 1, level_gap / 2, pos, level + 1)
            if len(node.children) > 1:
                self._binary_tree_layout(node.children[1], x + level_gap, y + 1, level_gap / 2, pos, level + 1)
        return pos

def create_tree():
    tree = GeneralTree()
    print("Criação da árvore:")
    root_value = int(input("Digite o valor do nó raiz: "))
    tree.insert(None, root_value)

    nodes_to_process = [root_value]
    while nodes_to_process:
        current_value = nodes_to_process.pop(0)
        has_children = input(f"O nó {current_value} possui filhos? (s/n): ").strip().lower()
        if has_children == 's':
            num_children = int(input(f"Quantos filhos o nó {current_value} possui? "))
            for _ in range(num_children):
                child_value = int(input(f"Digite o valor do filho de {current_value}: "))
                tree.insert(current_value, child_value)
                nodes_to_process.append(child_value)
    return tree

# Exemplo de execução:
tree = create_tree()
print("\nÁrvore criada:")
tree.display(tree.root)
node_count = tree.count_nodes()
non_leaf_count = tree.count_non_leaf_nodes()
print(f"\nA árvore possui {node_count} nós.")
print(f"A árvore possui {non_leaf_count} nós não folha.")
if tree.is_binary_tree():
    print("\nA árvore criada é uma árvore binária.")
else:
    print("\nA árvore criada NÃO é uma árvore binária.")

print("\nVisualização gráfica da árvore:")
tree.visualize()
