from pprint import pprint


class Link:
    def __init__(self, input_id, name, parent_name):
        self.vertex = input_id
        self.next = None
        self.name = name,
        self.nodeName = parent_name,
        self.direction = "ASYN"

    def to_json(self):
        return {
            "name": self.name[0],
            "nodeName": self.nodeName[0],
            "direction": "ASYN"
        }

class Node:
    def __init__(self, node_info):
        self.id = node_info['jobid'],
        self.nodeName = node_info['name'],
        self.name = node_info['name'],
        self.type = "type1",
        self.code = node_info['status'],
        self.label = node_info['log'],
        self.version = '',
        self.inputs = node_info['input'],
        self.outputs = node_info['output'],
        self.link = {
            "name": "Link node 2.3 to 3.4",
            "nodeName": "NODE NAME 3.4",
            "direction": "ASYN"
        }
        self.children = []

    def get_input(self):
        return self.inputs[0]

    def get_outputs(self):
        return self.outputs[0]

    def add_child(self, node):
        self.children = self.children + [node]

    def print_node(self):

        return {
            "nodeName": self.nodeName[0],
            "name": self.name[0],
            "type": self.type[0],
            "code": self.code[0],
            "label": self.label[0],
            "version": self.version[0],
            "link": self.link.to_json(),
            "children": [child.print_node() for child in self.children]
        }


class Graph:
    def __init__(self, num):
        self.V = num
        self.graph = {}

    # Add nodes
    def add_node(self, node):
        new_node = Node(node)
        if self.graph:
            for k in self.graph.keys():
                out = self.graph[k].get_outputs()
                inputs = self.graph[k].get_input()
                for i in node['input']:
                    if i in out:
                        new_node.link = Link(k, i, self.graph[k].name)
                        self.graph[k].add_child(new_node)
                        return
                for i in node['output']:
                    if i in inputs:
                        self.graph[k].link = Link(new_node.id, k, new_node.name)
                        new_node.add_child(self.graph.pop(k))
                        self.graph[new_node.id] = new_node
                        return
        else:
            new_node.link = Link(-1, new_node.get_input(), new_node.name)

            self.graph[node['jobid']] = new_node


                        # Add edges
    def add_edge(self, s, d):
        node = Link(d)
        node.next = self.graph[s.id]
        self.graph[s] = node

        node = Link(s)
        node.next = self.graph[d.id]
        self.graph[d] = node

    # Print the graph
    def print_agraph(self):
        for i in range(self.V):
            print("Vertex " + str(i) + ":", end="")
            temp = self.graph[i]
            while temp:
                print(" -> {}".format(temp.vertex), end="")
                temp = temp.next
            print(" \n")

    def export_agraph(self):
        for v in self.graph.items():
            pprint(v)
        return {'children': [v[1].print_node() for v in self.graph.items() ]}


