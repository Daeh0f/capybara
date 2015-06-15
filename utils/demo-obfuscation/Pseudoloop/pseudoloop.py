import random as rnd
import string,re
from llvm import *
from llvm.core import *
import networkx as nx

#isolated_graph = area with one input and one output (OIOO)

def get_random_string(length):
    return ''.join(rnd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def find_all_paths(function, input_block=None, output_block=None):
    graph = nx.DiGraph()
    terminators = []
    if input_block and output_block:
        graph.add_node(input_block)
    else:
        graph.add_node(function.basic_blocks[0])

    for block in function.basic_blocks:
        for successor in block.successors:
            graph.add_edge(block, successor)
        if block.terminator.opcode_name in ('ret', 'resume', 'invoke'): # warning! if you have problem - look at invoke terminator. It guards me <_<
            terminators.append(block)
    ways = []
    if input_block and output_block:
        return list(nx.all_simple_paths(graph, source=input_block, target=output_block))
    else:
        for ter in terminators:
            for path in nx.all_simple_paths(graph, source=function.basic_blocks[0], target=ter):
                ways.append(path)
        return ways

def deep_in(lst, element):
    for i in lst:
        if element in i:
            return True
    return False

def search_isolated_graph(ways):
    list_of_OIOO = set()
    for path in ways:
        for node in path:
            ways_with_node = [way for way in ways if node in way]
            ways_without_node = [way for way in ways if node not in way]
            if len(ways_with_node) > 1:
                for next_node in path[path.index(node)+1:]:
                    is_check = True
                    for way in ways_with_node:
                        try:
                            way.index(next_node)
                        except:
                            is_check = False
                            break
                    if is_check and not deep_in(ways_without_node, next_node) and node != next_node:
                        list_of_OIOO.add((node, next_node))
            else:
                for next_node in path[path.index(node)+1:]:
                    is_check = True
                    for way in ways_without_node:
                        try:
                            way.index(next_node)
                            is_check = False
                            break
                        except:
                            continue
                    if is_check and node != next_node:
                        list_of_OIOO.add((node, next_node))
    return list_of_OIOO

def create_pseudoloop(block_start, block_end):
    block_loop = block_start.splitBasicBlock(block_start.instructions[len(block_start.instructions)/2-1], 'loop')
    builder = Builder.new(block_loop)
    builder.position_at_beginning(block_loop)
    variable_phi = builder.phi(Type.double(), 'i')
    variable_phi.add_incoming(Constant.real(Type.double(), 0), block_start)
    next_value = builder.fadd(variable_phi, Constant.real(Type.double(), 1), "next")
    variable_phi.add_incoming(next_value, block_end)

    if block_end.instructions[-1].opcode_name == 'br' and len(block_end.instructions[-1].operands) == 1:
        builder.position_at_end(block_end)
        block_after = block_end.instructions[-1].operands[0]
        block_end.instructions[-1].erase_from_parent()
        end_condition_bool = builder.fcmp(ICMP_EQ, Constant.real(Type.double(), 0), variable_phi, "end_cond")
        builder.cbranch(end_condition_bool, block_after, block_loop)

    if block_end.instructions[-1].opcode_name == 'br' and len(block_end.instructions[-1].operands) == 3:
        builder.position_at_end(block_end)
        cond, block_false, block_true = block_end.instructions[-1].operands
        block_end.instructions[-1].erase_from_parent()
        #cond_int = builder.uitofp(cond, Type.float(), 'float_value')
        switch = builder.switch(cond, block_loop)
        switch.add_case(Constant.int(Type.int(), 0), block_false)
        switch.add_case(Constant.int(Type.int(), 1), block_true)

    if block_end.instructions[-1].opcode_name == 'switch':
        block_switch = block_end.splitBasicBlock(block_end.instructions[len(block_end.instructions)/2-1], 'switch')
        block_end.instructions[-1].erase_from_parent()
        builder.position_at_end(block_end)
        end_condition_bool = builder.fcmp(ICMP_EQ, Constant.real(Type.double(), 0), variable_phi, "end_cond")
        builder.cbranch(end_condition_bool, block_switch, block_loop)

    if block_end.instructions[-1].opcode_name == 'ret':
        block_ret = block_end.splitBasicBlock(block_end.instructions[len(block_end.instructions)/2-1], 'ret')
        block_end.instructions[-1].erase_from_parent()
        builder.position_at_end(block_end)
        end_condition_bool = builder.fcmp(ICMP_EQ, Constant.real(Type.double(), 0), variable_phi, "end_cond")
        builder.cbranch(end_condition_bool, block_ret, block_loop)

def decision_making(function):
    all_ways = find_all_paths(function)
    list_isograph = search_isolated_graph(all_ways)
    for isograph in list_isograph:
        create_pseudoloop(block_start=isograph[0], block_end=isograph[1])

if __name__ == '__main__':
    llfile = file("crackme.ll")
    module = Module.from_assembly(llfile)
    print(module.get_function_named('main'))
    decision_making(module.get_function_named('main'))
    print(module.get_function_named('main'))
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    module.to_bitcode(obfuscated_bitcode_file)