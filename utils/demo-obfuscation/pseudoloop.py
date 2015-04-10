import random as rnd
import string
from llvm import *
from llvm.core import *
import networkx as nx

#area with one input and one output  == OIOO

#notion: CFG is considered without loop!

def get_random_string(length):
    return ''.join(rnd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def find_all_paths(function):
    graph = nx.DiGraph()
    terminators = []
    graph.add_node(function.basic_blocks[0])
    for block in function.basic_blocks:
        for successor in block.successors:
            graph.add_edge(block, successor)
        if block.terminator.opcode_name == 'ret': # warning! resume terminator is not tracked. Fix it please
            terminators.append(block)
    ways = []
    for ter in terminators:
        for path in nx.all_simple_paths(graph, source=function.basic_blocks[0], target=ter): # The function.basic_blocks[0] is bad way!
            ways.append(path)
    return ways

def deep_in(lst, element):
    for i in lst:
        if element in i:
            return True
    return False

def search_of_OIOO(ways):   # OIOO - 0_0 ?? look at header
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
                        list_of_OIOO.add((node, path[path.index(next_node)]))
    return list_of_OIOO

def create_pseudoloop(block_start, block_loop, block_end, kind='br2br'):
    pass
    if kind == 'br2br':
        block_loop = block_start.instructions[-1].operands[0]
        #print(block_loop)
        builder = Builder.new(block_loop)
        builder.position_at_beginning(block_loop)
        variable_phi = builder.phi(Type.double(), 'i')
        variable_phi.add_incoming(Constant.real(Type.double(), 0), block_start)
        next_value = builder.fadd(variable_phi, Constant.real(Type.double(), 1), "next")
        variable_phi.add_incoming(next_value, block_end)

        builder.position_at_end(block_end)
        block_after = block_end.instructions[-1].operands[0]
        block_end.instructions[-1].erase_from_parent()
        end_condition_bool = builder.fcmp(ICMP_EQ, Constant.real(Type.double(), 1), variable_phi, "end_cond")
        builder.cbranch(end_condition_bool, block_after, block_loop)

def decision_making(list_of_OIOO, function):
    list_of_OIOO = list(list_of_OIOO)
    block_start = list_of_OIOO[1][0]
    block_end = list_of_OIOO[1][1]
    create_pseudoloop(block_start, block_loop='', block_end=block_end)

if __name__ == '__main__':
    llfile = file("crackme.ll")
    module = Module.from_assembly(llfile)
    #print module
    function = module.get_function_named('main')
    print(function)
    function.basic_blocks[1].instructions[-1].erase_from_parent()
    block_new = function.append_basic_block('<label>: 15')
    builder = Builder.new(function.basic_blocks[1])
    builder.branch(block_new)
    builder.position_at_end(block_new)
    builder.branch(function.basic_blocks[-2])

    decision_making(search_of_OIOO(find_all_paths(function)), function)
    print(function)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    module.to_bitcode(obfuscated_bitcode_file)
