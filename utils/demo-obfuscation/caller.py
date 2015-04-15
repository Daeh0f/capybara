from llvm import *
from llvm.core import *
import boom_CFG as CFG

if __name__ == '__main__':
    llfile = file("crackme.ll")
    crackme_module = Module.from_assembly(llfile)
    compare = crackme_module.get_function_named('compare')
    block = compare.basic_blocks[0]
    block_to = block.instructions[-1].operands
    builder = Builder.new(block)
    block.instructions[-1].erase_from_parent()
    switch = builder.switch(Constant.int(Type.int(), 1), block_to[0], 1)
    for func in crackme_module.functions:
        CFG.main(func)
    print(crackme_module)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)
