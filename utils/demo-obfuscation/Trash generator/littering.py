#!/bin/python

import random as rnd
import sys
import string
from llvm import *
from llvm.core import *
import trashengine as trash


def obfuscate_module(module):
    for function in module.functions:
        if function.name != "compare":
            continue

        for block in function.basic_blocks:
            trash.fill_block_with_trash(block)

    print(module.get_function_named("compare"))

if __name__ == '__main__':
    ll_filename = sys.argv[1] if len(sys.argv) > 1 else "crackme.ll"

    ll_file = file(ll_filename)
    ll_module = Module.from_assembly(ll_file)

    obfuscate_module(ll_module)

    obfuscated_bitcode_file = file("obfuscated_" + ll_filename + ".bc", "w")
    ll_module.to_bitcode(obfuscated_bitcode_file)