#!/bin/python

import string
import random
from llvm import *
from llvm.core import *
import networkx as nx

def get_nodes_appropriate_level(graph, root, level):
    list_of_nodes = set([root])
    for _ in range(level):
        list_of_nodes = set(node for n in list_of_nodes for node in graph[n])
    return list_of_nodes

def generate_graph(number_successors, depth):
    digraph = nx.DiGraph()
    level = 0
    nodes_counter = 0
    digraph.add_node(nodes_counter)
    nodes_counter += 1
    while level < depth:
        for node in get_nodes_appropriate_level(digraph, 0, level):
            for i in range(random.randint(1, number_successors)):
                digraph.add_edge(node, nodes_counter)
                nodes_counter += 1
        level += 1
    nodes = get_nodes_appropriate_level(digraph, 0, level)

    while len(nodes) > 1:
        while nodes:
            digraph.add_node(nodes_counter)
            if len(nodes) > 3:
                for node in random.sample(nodes, random.randint(1, len(nodes)/2)):
                    digraph.add_edge(node, nodes_counter)
                    nodes.remove(node)
            else:
                for node in nodes:
                    digraph.add_edge(node, nodes_counter)
                nodes = set([])
            nodes_counter += 1
        level += 1
        nodes = get_nodes_appropriate_level(digraph, 0, level)
    return digraph

def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def fill_block_a_trash(block):
    integer_type = Type.int()
    just_some_const = Constant.int(integer_type, 42)
    builder = Builder.new(block)
    instruction_name_length = 10
    instruction_name = get_random_string(instruction_name_length)
    some_int_variable = builder.alloca(integer_type)
    builder.store(just_some_const, some_int_variable)
    #builder.ret(some_int_variable)

def insert_block_between(block_A, block_B, block_new):
    builder_A = Builder.new(block_A)
    block_A.instructions[-1].erase_from_parent()
    builder_A.branch(block_new)

    fill_block_a_trash(block_new)

    builder_new = Builder.new(block_new)
    #builder_new.branch(block_B)
    const = Constant.int(Type.int(), 34)
    switch = builder_new.switch(const, block_A, 1)   # so far HARDCODE but instead of "const" need some PHI function! allocate memory lead to crash :(
    switch.add_case(const, block_B)
    #TODO: PHI

def obfuscate_function(function):
    name_length = 8
    new_block_name  = get_random_string(name_length)
    new_trash_block = function.append_basic_block(new_block_name)

    insert_block_between(function.basic_blocks[0], function.basic_blocks[1], new_trash_block)




def obfuscate_module(module):
    #integer_type = Type.int()
    #variable = module.add_global_variable(integer_type, "gv1")
    for function in module.functions:
        if function.name == "compare":
            obfuscate_function(function)
    print(module.get_function_named("compare"))

if __name__ == '__main__':
    llfile = file("crackme.ll")
    crackme_module = Module.from_assembly(llfile)
    obfuscate_module(crackme_module)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)