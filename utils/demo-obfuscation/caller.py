from llvm import *
from llvm.core import *
import boom_CFG as CFG

if __name__ == '__main__':
    llfile = file("crackme.ll")
    crackme_module = Module.from_assembly(llfile)
    for func in crackme_module.functions:
        CFG.main(func)
    print(crackme_module)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)
