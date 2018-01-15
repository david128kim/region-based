import os
import commands
import string

from tree import Tree

(_ROOT, _DEPTH, _BREADTH) = range(3)

tree = Tree()

#tree.add_node("Harry")  # root node
#tree.add_node("Jane", "Harry")
#tree.add_node("Bill", "Harry")
#tree.add_node("David", "Jane")
#tree.add_node("Joe", "Jane")

#tree.display("Harry")
#print("***** DEPTH-FIRST ITERATION *****")
#for node in tree.traverse("Harry"):
    #print(node)
#print("***** BREADTH-FIRST ITERATION *****")
#for node in tree.traverse("Harry", mode=_BREADTH):
    #print(node)

#file = open("select_region1.c")
source_line = []
program_name = raw_input("Please key in your program name: \n")
temp_name = program_name
file = open(program_name)
for line in file:
        if ("(" in line):
                break
        source_line.append(line)
file.close()


file = open("r1-r2_source.txt")
treeID = 0
info = []
height = 0
brackets_match = 0
branch_point = []
branch_boundrary = 0
branch_leaf = []
counter_if = 0
execution_path = 0
breakpoint = []
counter_bp = 0
dfs = []
start, end, counter_r2, r2_flag, main_flag= 1, 0, 0, 0, 0
for line in file:
	counter_r2 += 1
	if "region2" in line:
		r2_flag = counter_r2
	elif "main" in line:
		main_flag = counter_r2
	info.append(line)

tree.add_node(info[treeID])
print "len(info): ", len(info)
print info[1]
print r2_flag

#for i in range(1, len(info)):
for i  in range(1, r2_flag):
	if (("if" in info[i]) and ("else" not in info[i])):
		#height += 1
		counter_if += 1
		brackets_match += 1
		#branch_point = treeID
		branch_point.append(treeID)
		temp = branch_point[brackets_match-1]
		tree.add_node(info[i], info[temp])
		#tree.add_node(info[i], info[branch_point])
		#print "if(i, treeID, bp):", i, treeID, branch_point
		#print "if_height: ", brackets_match
	
	elif (("else" in info[i]) and ("if" in info[i])):
		brackets_match += 1
		#if height > 1:
		#else:
		#branch_point.append(treeID)
		temp = branch_point[brackets_match-1]
		#tree.add_node(info[i], info[branch_point])
		tree.add_node(info[i], info[temp])
		#print "elif(i, treeID, bp):", i, treeID, branch_point[brackets_match-1]
		#print "elif_height: ", brackets_match

	elif (("else" in info[i]) and ("if" not in info[i])):
		brackets_match += 1
		temp = branch_point[brackets_match-1]
		#tree.add_node(info[i], info[branch_point])
                tree.add_node(info[i], info[temp])
		#print "else(i, treeID, bp):", i, treeID, branch_point[brackets_match-1]	
		#print "else_height: ", brackets_match	
	else:	
		if "end of branch" in info[i]:
			branch_boundrary = i
			#print i
			break
			#print i
			#tree.add_node(info[i], info[treeID])
		else: 
			tree.add_node(info[i], info[treeID])
		if("}" in info[i]):
		######## layer problem #########
                        brackets_match -= 1
			if brackets_match == 0:
				#print i
				branch_leaf.append(i)
			#if ((counter_if - brackets_match) == 1):
				#print i
                                #branch_leaf.append(i)
			#elif 
		#tree.add_node(info[i], info[branch_point+1])
		#print "normal(i, treeID, bp):", i, treeID, branch_point		
		#print "height: ", height
	treeID += 1
	#print treeID
#print "len(branch_leaf): ", len(branch_leaf)
#print "branch_leaf[0]: ", branch_leaf[0]
#print branch_leaf[1]
#print branch_leaf[2]
#print "branch_boundrary: ", branch_boundrary
#print "info[branch_boundrary]: ", info[branch_boundrary]
#counter = 0
#for i in range(branch_boundrary, len(info)):
	#for j in range(0, len(branch_leaf)):
		#temp = branch_leaf[j]
		#tree.add_node(info[i], branch_leaf[j])
		#tree.add_node(info[i], info[temp])
		#branch_leaf.insert(j, i)
		#branch_leaf.remove(branch_leaf[j+1])
		#print "!"
for i in range(0, len(branch_leaf)-1):
	counter = 0
	#print "i: ",  i
	for j in range(branch_boundrary, len(info)):
		temp = branch_leaf[i]
		if counter == 0:
			tree.add_node(info[j], info[temp])
		else:
			tree.add_node(info[j], info[j-1])
		counter += 1
		#print "counter: ", counter
		#print "j: ", j		
	#print "###############################################"
tree.add_node("/* #############breakline############### */", info[len(info)-1])
tree.display(info[0])

print("***** DEPTH-FIRST ITERATION *****"), '\n'
for node in tree.traverse(info[0]):
    	dfs.append(node)
	if "#######breakline#######" in node:
		execution_path += 1	
	#print node
print "dfs: ", dfs
print "execution_path: ", execution_path
#dfs.pop()
#print "dfs.pop(): ", dfs
counter_bp = len(dfs)-1
for i in range(len(dfs)-1, -1, -1):
	#counter_bp += 1
	if "#######breakline#######" in dfs[i]:
		breakpoint.append(counter_bp)
	counter_bp -= 1	

print breakpoint

#partition = open("partition.c", "w")
while(execution_path > 0):
	partition = open("partition.c", "w")
	for i in range(0, len(source_line)):
        	partition.write(source_line[i])
	partition.write("int main(){")
	execution_path -= 1
	end = breakpoint.pop()-1
	for i in range(start, end):
		partition.write(dfs[i])
	partition.write("return 0; }")
	partition.close()
	os.system("mv partition.c exe_r1_path"+str(execution_path)+".c")
	start = end+1

file.close()
partition.close()
os.system("python app_r2.py")
















