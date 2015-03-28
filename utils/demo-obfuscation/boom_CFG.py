import random as rnd
import string
from llvm import *
from llvm.core import *
import networkx as nx

def get_random_string(length):
    return ''.join(rnd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def get_nodes_appropriate_level(graph, root, level):
    list_of_nodes = set([root])
    for _ in range(level):
        list_of_nodes = set(node for n in list_of_nodes for node in graph[n])
    return list_of_nodes

rnd_name_list = [get_random_string(6)]

def generate_graph(number_successors, depth):
    digraph = nx.DiGraph()
    level = 0
    nodes_counter = 0

    digraph.add_node(rnd_name_list[nodes_counter])
    rnd_name_list.append(get_random_string(5))
    nodes_counter += 1
    while level < depth:
        for node in get_nodes_appropriate_level(digraph, rnd_name_list[0], level):
            for i in range(rnd.randint(1, number_successors)):
                digraph.add_edge(node, rnd_name_list[nodes_counter])
                rnd_name_list.append(get_random_string(5))
                nodes_counter += 1
        level += 1
    nodes = get_nodes_appropriate_level(digraph, rnd_name_list[0], level)

    while len(nodes) > 1:
        while nodes:
            digraph.add_node(rnd_name_list[nodes_counter])
            if len(nodes) > 3:
                for node in rnd.sample(nodes, rnd.randint(1, len(nodes)/2)):
                    digraph.add_edge(node, rnd_name_list[nodes_counter])
                    nodes.remove(node)
            else:
                for node in nodes:
                    digraph.add_edge(node, rnd_name_list[nodes_counter])
                nodes = set([])
            rnd_name_list.append(get_random_string(5))
            nodes_counter += 1
        level += 1
        nodes = get_nodes_appropriate_level(digraph, rnd_name_list[0], level)
    return digraph

def insert_graph_into_func(graph, function, place=(0, 1)):
    block_dict = {}
    for n in graph.nodes():
        block = function.append_basic_block(str(n))
        block_dict[n] = block
    counter = 0
    flag = True
    while flag:
        curr_level_list = get_nodes_appropriate_level(graph, rnd_name_list[0], counter)
        for node in curr_level_list:
            if len(graph.successors(node)) > 0:
                builder_root = Builder.new(block_dict[node])
                if len(graph.successors(node)) > 1:
                    next_block_value = Constant.int(Type.int(), rnd.randint(1, len(graph.successors(node))))
                else:
                    next_block_value = Constant.int(Type.int(), 1)
                switch = builder_root.switch(next_block_value, block_dict[rnd.sample(graph.successors(node), 1)[0]], len(graph.successors(node)))
                for i in range(1, len(graph.successors(node)) + 1 ):
                    block_value = Constant.int(Type.int(), i)
                    switch.add_case(block_value, block_dict[graph.successors(node)[i - 1]])
            else:
                insert_something_between(place[0], block_dict[rnd_name_list[0]], block_dict[node], place[1])
                flag = False
        counter += 1

def insert_something_between(block_A, block_start, block_finish, block_B):
    "You may insert something like block or graph between block A and B"
    builder_A = Builder.new(block_A)
    block_A.instructions[-1].erase_from_parent()
    builder_A.branch(block_start)
    builder_fi = Builder.new(block_finish)
    builder_fi.branch(block_B)

def main(function):
    flag = True
    for block in function.basic_blocks:
        if block.instructions[-1].opcode_name == 'br' and len(block.instructions[-1].operands) == 1:
            if flag:
                graph = generate_graph(number_successors=rnd.randint(2, 4), depth=rnd.randint(2, 4))
                insert_graph_into_func(graph, function, place=(block, block.instructions[-1].operands[0]))
                flag = False
                print('yes')
            else:
                flag = True
