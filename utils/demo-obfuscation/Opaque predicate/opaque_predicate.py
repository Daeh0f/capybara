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

def opaque_condition(block, function, x=None):
    builder = Builder.new(block)
    if not x:
        const = Constant.real(Type.float(), 23)
        memory = builder.alloca(Type.float()) #allocate memory
        builder.store(const, memory)   # write value to memory
        x = builder.load(memory, name="x")

    #(x^n-x) modn == 0. n is odd
    n = Constant.real(Type.float(), 3)
    raise_to_a_power = builder.call(pow_oper, [x, n], 'x^n')
    subtraction = builder.sub(raise_to_a_power, x, 'x^n_minus_x')
    modulo = builder.frem(subtraction, n)
    if_value = builder.fcmp(FCMP_OEQ, modulo, Constant.real(Type.float(), 0), "true")

    action_list = ['foward', 'back', 'to_trash_block']
    simple_action_list = ['foward', 'back']
    fake_branch = rnd.sample(simple_action_list, 1)[0]
    if fake_branch == 'foward' or 'back': # I'm sad and I did it simple
        function.basic_blocks.remove(block)
        return if_value, rnd.sample(function.basic_blocks, 1)[0]
    else:
        trash_block = function.append_basic_block(get_random_string()+'-Fake')
        # fill_block_a_trash(trash_block)
        # opaque_condition(trash_block)
        return if_value, trash_block

def split_BB(function):
    global pow_oper
    pow_oper = Function.intrinsic(crackme_module, INTR_POW, [Type.float()])
    for block in choice(function):
        true_block = function.append_basic_block(get_random_string()+'-Real')
        builder = Builder.new(block)
        if_value, unreachable_block = opaque_condition(block,function)
        builder.cbranch(if_value, true_block, unreachable_block)
        builder.position_at_end(true_block)
        builder.alloca(Type.int(32)) #only for minimise Python code. It's instruction will be removed soon

        for instr in block.instructions[1:-9]:
            instr.moveBefore(true_block.instructions[0])
            true_block.instructions[-1].erase_from_parent() # here!
            if_value, unreachable_block = opaque_condition(true_block, function)
            true_block = function.append_basic_block(get_random_string())
            builder.cbranch(if_value, true_block, unreachable_block)
            builder.position_at_end(true_block)
            builder.alloca(Type.int(32)) # here

        block.instructions[-9].moveBefore(true_block.instructions[0])
        true_block.instructions[-1].erase_from_parent() #and here

if __name__ == '__main__':
    llfile = file("crackme.ll")
    global crackme_module
    crackme_module = Module.from_assembly(llfile)
    compare = crackme_module.get_function_named('compare')
    print(compare)
    split_BB(compare)
    print('===============================================')
    print(compare)
    obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
    crackme_module.to_bitcode(obfuscated_bitcode_file)