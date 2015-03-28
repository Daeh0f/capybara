import random
import string
from llvm import *
from llvm.core import *

trash_operations = [
    "xor",
    "and",
    "or"
    #"addition",
    #"substraction",
    #"multiplication",
    #"division",
    #"left_shift",
    #"rigth_shift",
    #"store",
    #"load"
]



def _insert_instruction(instruction_builder, operation, operands):
    # fix me please
    const1 = Constant.int(Type.int(32), random.randint(0, 2 ** 32 - 1))
    const2 = Constant.int(Type.int(32), random.randint(0, 2 ** 32 - 1))

    storage_variable1 = instruction_builder.alloca(Type.int(32))
    instruction_builder.store(const1, storage_variable1)
    storage_variable_ptr1 = instruction_builder.load(storage_variable1)

    storage_variable2 = instruction_builder.alloca(Type.int(32))
    instruction_builder.store(const2, storage_variable2)
    storage_variable_ptr2 = instruction_builder.load(storage_variable2)

    #var = instruction_builder.alloca(Type.int(32)) 
    #builder.store(const, memory)
    #var = builder.load(memory,name="var")

    if   operation == "addition":
        return 1
    elif operation == "xor":
        result = instruction_builder.xor(storage_variable_ptr1, storage_variable_ptr2)
    elif operation == "and":
        result = instruction_builder.and_(storage_variable_ptr1, storage_variable_ptr2)
    elif operation == "or":
        result = instruction_builder.or_(storage_variable_ptr1, storage_variable_ptr2)
    elif operation == "substraction":
        return 1
    elif operation == "multiplication":
        return 1
    elif operation == "division":
        return 1
    elif operation == "left_shift":            
        return 1
    elif operation == "rigth_shift":
        return 1

    instruction_builder.store(result, storage_variable1)

def _insert_random_instruction(before_instruction, instruction_builder = None):
    if instruction_builder == None:
        builder = Builder.new(before_instruction.basic_block)
    else:
        builder = instruction_builder

    builder.position_before(before_instruction)

    operation = random.choice(trash_operations)
    # fix me please
    operands = [1, 2]
    _insert_instruction(builder, operation, operands)

def _is_instruction_fitable_for_trash(ir_instruction):
    return True

# increase block size in multiplier times
def fill_block_with_trash(block, multiplier = 2):
    instruction_builder = Builder.new(block)

    if multiplier <= 1:
        multiplier = 2

    count_of_instrurtions_to_insert = int( len(block.instructions) * (multiplier - 1) )

    suitable_for_trash_instructions = []
    for ir_instruction in block.instructions:
        if ir_instruction == block.instructions[-1]:
            break

        if _is_instruction_fitable_for_trash(ir_instruction):
            suitable_for_trash_instructions.append(ir_instruction)

    trash_insrtuctions_per_selected_median = 0
    if len(suitable_for_trash_instructions) > 0 :
        trash_insrtuctions_per_selected_median = int( count_of_instrurtions_to_insert / len(suitable_for_trash_instructions) )


    for ir_instruction in suitable_for_trash_instructions:
        is_block_filled_enough = count_of_instrurtions_to_insert <= 0
        if is_block_filled_enough:
            break

        dispersion_modificator = 0.1
        dispersion = int(len(suitable_for_trash_instructions) * dispersion_modificator)
        from_limit = count_of_instrurtions_to_insert - dispersion
        if from_limit < 0:
            from_limit = 0
        to_limit = count_of_instrurtions_to_insert + dispersion
        trash_instructions_for_current_instruction = random.randint(from_limit, to_limit)

        for i in range(trash_instructions_for_current_instruction):
            _insert_random_instruction(ir_instruction, instruction_builder)
            # fix me please
            count_of_instrurtions_to_insert -= 8

        