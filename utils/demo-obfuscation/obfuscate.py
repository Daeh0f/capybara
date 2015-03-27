#!/bin/python

import string
import random
from llvm import *
from llvm.core import *
import networkx as nx

def get_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

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

def insert_graph_into_func(graph, function, place=(0, 1)):
    block_dict = {}
    for n in graph.nodes():
        block = function.append_basic_block(str(n))
        block_dict[n] = block

    counter = 0
    flag = True
    while flag:
        curr_level_list = get_nodes_appropriate_level(graph, 0, counter)
        print(curr_level_list, len(curr_level_list))
        for node in curr_level_list:
            print(graph.successors(node), len(graph.successors(node)))
            if len(graph.successors(node)) > 0:
                builder_root = Builder.new(block_dict[node])
                if len(graph.successors(node)) > 1:
                    next_block_value = Constant.int(Type.int(), random.randint(1, len(graph.successors(node))))
                else:
                    next_block_value = Constant.int(Type.int(), 1)
                switch = builder_root.switch(next_block_value, block_dict[random.randint(node, node + len(graph.successors(node)))], len(graph.successors(node)))
                for i in range(1, len(graph.successors(node)) + 1 ):
                    block_value = Constant.int(Type.int(), i)
                    switch.add_case(block_value, block_dict[graph.successors(node)[i - 1]])
            else:
                insert_something_between(function.basic_blocks[place[0]], block_dict[0], block_dict[node], function.basic_blocks[place[1]])
                flag = False
        counter += 1


def insert_something_between(block_A, block_start, block_finish, block_B):
    "You may insert something like block or graph between block A and B"
    builder_A = Builder.new(block_A)
    block_A.instructions[-1].erase_from_parent()
    builder_A.branch(block_start)

    fill_block_a_trash(block_finish)

    builder_fi = Builder.new(block_finish)
    builder_fi.branch(block_B)



def create_variable(block):
    builder = Builder.new(block)
    instruction_name_length = 10
    instruction_name = get_random_string(instruction_name_length)
    const = Constant.int(Type.int(), 25) #value
    memory = builder.alloca(Type.int()) #allocate memory
    builder.store(const, memory)   # write value to memory
    var = builder.load(memory,name="var") # get pointer for use in our purpose (in actually "instruction that loads a value at the memory pointed by ptr")

    #TODO for all: write class variable. Something like that ->>   variable.create_var("some_value")
    #print(variable.value) >>> some_value

def if_then_else(function):
    block_entry = function.basic_blocks[0]
    block_entry.instructions[-1].erase_from_parent()
    block_then = function.append_basic_block('then')
    block_else = function.append_basic_block('else')
    block_after = function.append_basic_block('ifcont')
    block_B = function.basic_blocks[1]
    builder = Builder.new(block_entry)

    const = Constant.real(Type.double(), 1)
    memory = builder.alloca(Type.int())
    builder.store(const, memory)
    condition = builder.load(memory,name="condition")
    condition_bool = builder.fcmp(FCMP_ONE, condition, Constant.real(Type.double(), 1), "ifcond")
    builder.cbranch(condition_bool, block_then, block_else)

    builder.position_at_end(block_then)
    body = builder.fadd(condition, Constant.real(Type.double(), 1), "body")
    builder.branch(block_after)

    builder.position_at_end(block_else)
    body = builder.fadd(condition, Constant.real(Type.double(), 2), "body")
    builder.branch(block_after)

    builder.position_at_beginning(block_after)
    phi = builder.phi(Type.double(), 'iftmp')
    phi.add_incoming(body, block_then)
    phi.add_incoming(body, block_else)
    builder.branch(block_B)

def loop_for(function):
    block_entry = function.basic_blocks[1]
    operand_one, operand_three, operand_two = block_entry.instructions[-1].operands
    #instr_name = block_entry.instructions[-1].opcode_name
    block_entry.instructions[-1].erase_from_parent()
    block_after = operand_two
    block_loop = function.append_basic_block('loop')

    builder = Builder.new(block_entry)
    builder.cbranch(operand_one, block_loop, operand_three)

    builder.position_at_end(block_loop)
    variable_phi = builder.phi(Type.double(), 'i')
    variable_phi.add_incoming(Constant.real(Type.double(), 1), block_entry)
    #something body
    step_value = Constant.real(Type.double(), 1)
    next_value = builder.fadd(variable_phi, step_value, "next")
    variable_phi.add_incoming(next_value, block_loop)

    end_condition_bool = builder.fcmp(ICMP_EQ, Constant.real(Type.double(), 3), variable_phi, "end_cond")
    builder.cbranch(end_condition_bool, block_after, block_loop)
    builder.position_at_beginning(block_after)

def obfuscate_function(function):
    #name_length = 8
    #new_block_name  = get_random_string(name_length)
    #new_trash_block = function.append_basic_block(new_block_name)
    #insert_block_between(function.basic_blocks[0], function.basic_blocks[1], new_trash_block)

    rand_graph = generate_graph(4, 3)
    insert_graph_into_func(rand_graph, function, place=(0, 1))
    #TODO for Alex!!!!: check hypothesis: "function.basic_blocks" return block in call order. If yes then place=(0,1) transform place=1

def obfuscate_module(module):
    #integer_type = Type.int()
    #variable = module.add_global_variable(integer_type, "gv1")
    for function in module.functions:
        if function.name == "compare":
            #obfuscate_function(function)
            loop_for(function)
    print(module.get_function_named("compare"))

if __name__ == '__main__':
    llfile = file("crackme.ll")
    crackme_module = Module.from_assembly(llfile)
    obfuscate_module(crackme_module)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)