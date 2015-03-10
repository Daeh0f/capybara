#!/bin/python

import string
import random
from llvm import *
from llvm.core import *


def get_random_string(length):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def fill_block_with_trash(block):
	integer_type = Type.int()
	just_some_const = Constant.int(integer_type, 42)

	builder = Builder.new(block)

	print("here")

	instruction_name_length = 10
	instruction_name = get_random_string(instruction_name_length)

	print("or here")
	some_int_variable = builder.alloca(integer_type)
	builder.store(just_some_const, some_int_variable)
	builder.ret(some_int_variable)


def obfuscate_function(function):
	name_length = 8

	new_block_name  = get_random_string(name_length)
	new_trash_block = function.append_basic_block(new_block_name)

	fill_block_with_trash(new_trash_block)


def obfuscate_module(module):
	#integer_type = Type.int()
	#variable = module.add_global_variable(integer_type, "gv1")

	for function in module.functions:
		if function.name == "compare":
			obfuscate_function(function)
		print(function)


llfile = file("crackme.ll")
crackme_module = Module.from_assembly(llfile)

obfuscate_module(crackme_module)

obfuscated_bitcode_file = file("obfuscated_crackme.bc", "w")
crackme_module.to_bitcode(obfuscated_bitcode_file)