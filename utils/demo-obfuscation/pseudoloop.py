import random as rnd
from llvm import *
from llvm.core import *
import networkx as nx
#area with one input and one output  == OIOO

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

def min_by_len(list_of_lists):
    min = 999999999
    min_list = []
    for lst in list_of_lists:
        if len(lst) < min:
            min = len(lst)
            min_list = lst
    return min_list

def deep_in(lst, element):
    for i in lst:
        if element in i:
            return True
    return False

def search_of_OIOO(ways):   # OIOO - 0_0 ?? look at header
    list_of_OIOO = []
    for path in ways:
        for node in path:
            if not deep_in(list_of_OIOO, node):
                ways_list = [curr_path for curr_path in ways if node in curr_path]
                for i in range(1,len(min_by_len(ways_list))-2):
                    last_node = ways_list[0][-i]
                    search_flag = True
                    for pa in ways_list[1:]:
                        try:
                            pa.index(last_node)
                        except ValueError:
                            search_flag = False
                            break
                    if search_flag:
                        list_of_OIOO.append([node, last_node])
                        print(list_of_OIOO[-1][0])
                        print(list_of_OIOO[-1][1] )
                        break
    return list_of_OIOO


if __name__ == '__main__':
    llfile = file("crackme.ll")
    module = Module.from_assembly(llfile)
    cpm = module.get_function_named("compare")
    search_of_OIOO(find_all_paths(cpm))
    print(cpm)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    module.to_bitcode(obfuscated_bitcode_file)
