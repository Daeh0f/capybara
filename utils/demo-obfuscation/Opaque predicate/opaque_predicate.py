from llvm.core import *
import random as rnd
import string

def get_random_string(length=5):
    return ''.join(rnd.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def choice(function):
    maxi = [0, None]
    for block in function.basic_blocks:
        if maxi[0] < len(block.instructions):
            maxi[0], maxi[1] = len(block.instructions), block
    return [maxi[1]]


def main(function):
    for block in choice(function):
        new_block = function.append_basic_block(get_random_string())
        builder = Builder.new(block)
        builder.branch(new_block)
        builder.position_at_end(new_block)
        builder.alloca(Type.int(32)) #only for minimise Python code. It instruction will be removed soon

        for instr in block.instructions[1:-2]:
            instr.moveBefore(new_block.instructions[0])
            new_block.instructions[-1].erase_from_parent() # here!
            new_block = function.append_basic_block(get_random_string())
            builder.branch(new_block)
            builder.position_at_end(new_block)
            builder.alloca(Type.int(32))

        block.instructions[-2].moveBefore(new_block.instructions[0])
        new_block.instructions[-1].erase_from_parent() #and here

if __name__ == '__main__':
    llfile = file("crackme.ll")
    crackme_module = Module.from_assembly(llfile)
    compare = crackme_module.get_function_named('compare')
    print(compare)
    main(compare)
    print(compare)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)