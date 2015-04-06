import random as rnd
from llvm import *
from llvm.core import *
import networkx as nx
#one input to one output == o2o

def find_all_paths(function):
    graph = nx.DiGraph()
    terminators = []
    graph.add_node(function.basic_blocks[0])
    for block in function.basic_blocks:
        for successor in block.successors:
            graph.add_edge(block, successor)
        if block.terminator.opcode_name == 'ret': # warning! resume terminator is not tracked. Fix it please
            terminators.append(block)
    paths = []
    for ter in terminators:
        for path in nx.all_simple_paths(graph, source=function.basic_blocks[0], target=ter): # The function.basic_blocks[0] is bad way!
            paths.append(path)
    return paths

def search_of_o2o(function):
    pass


if __name__ == '__main__':
    llfile = file("crackme.ll")
    module = Module.from_assembly(llfile)
    cpm = module.get_function_named("compare")
    print(find_all_paths(cpm))
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    module.to_bitcode(obfuscated_bitcode_file)
