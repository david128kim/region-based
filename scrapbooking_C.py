import os
import commands
import string

program_name = raw_input("Please key in your program name: \n")
file = open(program_name)
region1 = open('select_region1.c','w')
region2 = open('select_region2.c','w') 
whole_program = open('whole_program.c','w')
shared_variable_name = raw_input("Please key in your shared variable name: \n")
expected_value = raw_input("Please key in your expected result: \n")
source_line = []
temp_r1 = []
temp_r2 = []
ir_r1 = []
ir_r2 = []
entry1 = 0
entry2 = 0
return1 = 0
return2 = 0
counter_r1 = 0
counter_r2 = 0
#counter_r2 = 0
whole_program.write("#include <assert.h>\n")
#################### start of scrapbooking ####################
#  build the top half of select_region1/2.c and whole program.c
#  include header to main function definition

for line in file:
	if ("(" in line):
		break
	source_line.append(line)

for i in range(0, len(source_line)):
	region1.write(source_line[i])
	region2.write(source_line[i])
	whole_program.write(source_line[i])

region1.write("int main() { \n")
region2.write("int main() { \n")
whole_program.write("int main() { \n")
#region1.write("}")
#region2.write("}")

file.close()
region1.close()
region2.close()
whole_program.close()

#  use r1-r2_source.txt to put the bottom half of select_region1/2.c and whole_program.c
#  for example: main statement in thread function
#  use assert function to verify bugs

file = open('r1-r2_source.txt')
region1 = open('select_region1.c','a')
region2 = open('select_region2.c','a')
whole_program = open('whole_program.c','a')

for line in file:
	#temp.append(line)
	if "region2" in line:
		break
	if "region1" not in line:
		temp_r1.append(line)

for line in file:
	if "main" in line:
		break
	temp_r2.append(line)

for i in range(0, len(temp_r1)):
	region1.write(temp_r1[i])

for i in range(0, len(temp_r1)-1):
	whole_program.write(temp_r1[i])

for i in range(0, len(temp_r2)):
	region2.write(temp_r2[i])

for i in range(0, len(temp_r2)-1):
	whole_program.write(temp_r2[i])

whole_program.write("assert("+shared_variable_name+" == "+str(expected_value)+"); return 0; }")
#whole_program.write(' printf('+shared_variable_name+'); return 0; }')

file.close()
region1.close()
region2.close()
whole_program.close()

os.system('clang -Os -S -emit-llvm select_region1.c -o select_region1.ll')
os.system('clang -Os -S -emit-llvm select_region2.c -o select_region2.ll')
os.system('clang -Os -S -emit-llvm whole_program.c -o whole_program.ll')

#  create r1-r2_recorder.txt from select_region1/2.ll to build enumeration source IR code 

region1 = open('select_region1.ll')
region2 = open('select_region2.ll')
r1_r2_recorder = open('r1-r2_recorder.txt','w')
r1_r2_recorder.write("region1 { \n")

for line in region1:
	counter_r1 += 1
	ir_r1.append(line)
	if "entry" in line:
		entry1 = counter_r1
		print "e1: ", counter_r1
	elif "ret" in line:
		return1 = counter_r1
		print "r1: ", counter_r1

for line in region2:
        counter_r2 += 1
	ir_r2.append(line)
        if "entry" in line:
                entry2 = counter_r2
                print "e2: ", counter_r2
        elif "ret" in line:
		return2 = counter_r2
                print "r2: ", counter_r2

for i in range(entry1, return1):
	r1_r2_recorder.write(ir_r1[i])

r1_r2_recorder.write("} \n")
r1_r2_recorder.write("region2 { \n")

for i in range(entry2, return2):
        r1_r2_recorder.write(ir_r2[i])

r1_r2_recorder.write("main() \n")

region1.close()
region2.close()
r1_r2_recorder.close()

os.system('python interleaving.py')
