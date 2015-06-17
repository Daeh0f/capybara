import random as rnd
import string, os
from llvm import *
from llvm.core import *
import networkx as nx

def get_random_string(length):
    return ''.join(rnd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def randone():
    if int(os.urandom(1).encode('hex'), 16) % 2 == 0:
        return 0
    else:
        return 1

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

def insert_graph_into_func(graph, function, place=(0, 1), kind=''):
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
                insert_something_between(place[0], block_dict[rnd_name_list[0]], block_dict[node], place[1], kind)
                flag = False
        counter += 1
        #TODO: The merging is necessary make with br (not switch)

def insert_something_between(block_A, block_start, block_finish, block_B, kind):
    if kind == 'branch':
        builder_A = Builder.new(block_A)
        block_A.instructions[-1].erase_from_parent()
        builder_A.branch(block_start)
        builder_fi = Builder.new(block_finish)
        builder_fi.branch(block_B)
    if kind == 'cbranch':
        operand_one, operand_three, operand_two = block_A.instructions[-1].operands
        block_A.instructions[-1].erase_from_parent()
        block_B = operand_two
        builder = Builder.new(block_A)
        builder.cbranch(operand_one, block_start, operand_three)
        builder.position_at_end(block_finish)
        builder.branch(block_B)
    if kind == 'switch':
        operands = [n for n in block_A.instructions[-1].operands]
        block_A.instructions[-1].erase_from_parent()
        builder = Builder.new(block_A)
        switch = builder.switch(operands[0], operands[1], len(operands)-2)
        operands = operands[2:]
        for value, block in zip(operands[0::2], operands[1::2]):
            if block == block_B:
                switch.add_case(value, block_start)
            else:
                switch.add_case(value, block_start)
        builder.position_at_end(block_finish)
        builder.branch(block_B)

def main(function):
    for block in function.basic_blocks:
        if block.instructions[-1].opcode_name == 'br' and len(block.instructions[-1].operands) == 1 and randone():
            graph = generate_graph(number_successors=rnd.randint(2, 4), depth=rnd.randint(2, 4))
            insert_graph_into_func(graph, function, place=(block, block.instructions[-1].operands[0]), kind='branch')

        if block.instructions[-1].opcode_name == 'br' and len(block.instructions[-1].operands) == 3 and randone():
            graph = generate_graph(number_successors=rnd.randint(2, 4), depth=rnd.randint(2, 4))
            insert_graph_into_func(graph, function, place=(block, block.instructions[-1].operands[rnd.randint(1, 2)]), kind='cbranch')

        if block.instructions[-1].opcode_name == 'switch': # and randone():
            graph = generate_graph(number_successors=rnd.randint(2, 4), depth=rnd.randint(2, 4))
            examle = [1]
            if len(block.instructions[-1].operands) > 2:
                examle = [n for n in range(3, 2, len(block.instructions[-1].operands))]
            insert_graph_into_func(graph, function, place=(block, block.instructions[-1].operands[rnd.sample(examle, 1)[0]]), kind='switch')
#TODO: link node from different levels of graph