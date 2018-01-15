import os
import commands
import string
import itertools
import time

testcase = open('testcase.ll','w')
file = open('r1-r2_recorder.txt')
#SV = raw_input("Enter shared variable name: ")
#In region-based approach, we let user select two thread function 
#to show their SVAs combination merging to one main and serial funtion.
#region1 = raw_input("Enter thread1 function name: ")
#region2 = raw_input("Enter thread2 function name: ")

interleaving = []
#inter = []
#combination = []
combination = {}
a = []
#a = {}
b = []
#b = {}
#true_branch = []
#false_branch = []
temp = []
old_order = []
counter_t1 = 0
counter_t2 = 0
t1_insert_number = 0
t2_insert_number = 0
strthread1 = "SVA from thread 1: "
strthread2 = "SVA from thread 2: "
strmerge = "merge two thread function to main: "
strpermutation = "exhaustive representation of interleaving combination ...  "
strwrite = "generate feasible testcase: "

#test region
constraints = [[1, 2], [3, 4], [5, 6]]
test = []
recording = []
filetest = []
counter = 0
path_amount = 0
file_length = 0
a_tie = []
b_tie = []
temp_exe_result = 0
#print constraints
#

def merge_two_dicts(x, y):
	z = x.copy()
	z.update(y)
	return z

def extract_t1():
	global counter_t1, a_tie, t1_insert_number
	insert_temp = 0
	for line in file:
		#counter_t1 += 1
		#if (""+SV+"" in line) or (("nsw" in line) or ("nuw" in line)) or ("mutex" in line):
                #if "%0" in line:
		if "region1" not in line and "region2" not in line: #unnecessary prune
			a.append(line)
			counter_t1 += 1
			if (("load" in line) or ("store" in line) or ("mutex" in line)):
				a.insert(counter_t1+insert_temp, "tie")
				insert_temp += 1
				t1_insert_number += 1
				#print strthread1
				#print a
	
		elif "region2" in line:
			break
	a_tie = " ".join(a)
	a_tie = a_tie.split('tie')
	#a_tie.remove("")
	a_tie.pop()	
	print "a_tie: ", a_tie
	#print "a_tie length: ", len(a_tie)

def extract_t2():
	global counter_t2, b_tie, t2_insert_number
	insert_temp = 0
	for line in file:
		#counter_t2 += 1
		#if "%" in line:
		#if (""+SV+"" in line) or (("nsw" in line) or ("nuw" in line)) or ("mutex" in line):
		b.append(line)
		counter_t2 += 1
		if (("load" in line) or ("store" in line)) or ("mutex" in line):
			b.insert(counter_t2+insert_temp, "tie")
			insert_temp += 1
			t2_insert_number += 1
			#print strthread2
			#print b
		elif "main" in line:
			break
	
	b_tie = " ".join(b)
        b_tie = b_tie.split('tie')
        #b_tie.remove("")
	b_tie.pop()
        print "b_tie: ", b_tie
        #print "b_tie length: ", len(b_tie)


extract_t1()
extract_t2()

#print "a_tie: ", a_tie
#print "a_tie length: ", len(a_tie)
#print "b_tie: ", b_tie
#print "b_tie length: ", len(b_tie)

print "##################################################################"

#	divide to two sublist. depends on list length
if(len(a_tie) >= len(b_tie)):
	combination = a_tie + b_tie
	#print len(combination)
	#print combination
	interleaving = [combination[i:i+len(a_tie)] for i in range(0, len(combination), len(a_tie))]
	print "interleaving: ", interleaving
else:
	combination = b_tie + a_tie
	interleaving =  [combination[i:i+len(b_tie)] for i in range(0, len(combination), len(b_tie))]
	print "interleaving: ", interleaving

#	list permutation
print strpermutation
inter_permutation = [i for i, group in enumerate(interleaving) for j in range(len(group))]
for new_order in itertools.permutations(inter_permutation):
	if new_order <= old_order:
		continue
	old_order = new_order
	iters = [iter(group) for group in interleaving]
	#print [next(iters[i]) for i in new_order]
	for i in new_order:
		test = next(iters[i])
		#print "test: ", test
		testcase.write(test)
file.close()
testcase.close()

print "##################################################################"
#print a
#print b
#print len(a)
#print len(b)
#print t1_insert_number
#print "combination length: ", len(a)+len(b)-t1_insert_number-t2_insert_number

file = open('testcase.ll')
flag = 1
for line in file:
	temp.append(''+line+'')
temp.pop()
file_length =  len(temp)
#print "file length: ", len(temp)
file.close()
# -4 means in list a, b exist tedious line appended in them. for example: }, \n, region2{, main
path_amount = len(temp)/(len(a)+len(b)-t1_insert_number-t2_insert_number-4)
print "total path amount: ", len(temp)/(len(a)+len(b)-t1_insert_number-t2_insert_number-4)

while(counter < file_length):
	generating = open('answer.ll', 'w')
	for i in range(0,len(a)+len(b)-t1_insert_number-t2_insert_number-4, 1):
		recording.append(temp.pop())
		counter += 1
	#if counter == 6:
	if counter == (len(a)+len(b)-t1_insert_number-t2_insert_number-4):
		counter = 0
	#print counter
	for i in range(len(a)+len(b)-t1_insert_number-t2_insert_number-4-1, -1, -1):
		generating.write(recording[i])
	generating.close()
		#os.system('mv answer.ll path'+str(flag)+'.ll')
		#time.sleep(1)
	os.system('python scrapbooking_IR.py')
		#os.system('path'+str(flag))
	os.system('llc -O3 -march=x86-64 answer_ok.ll -o answer_ok.s')
        os.system('gcc -o answer_ok answer_ok.s -lpthread')
        os.system('./answer_ok')
	exe_result = commands.getoutput('./answer_ok')
	#print "exe_result: ", exe_result
		#os.system('llc -O3 -march=x86-64 path'+str(flag)+'_ok.ll -o path'+str(flag)+'_ok.s')
		#os.system('gcc -o path'+str(flag)+'_ok path'+str(flag)+'_ok.s')
		#os.system('./path'+str(flag)+'_ok')
		#exe_result = commands.getoutput('./path'+str(flag)+'_ok')
	if "failed" in exe_result:
	#if temp_exe_result != exe_result: 	
		break
	#temp_exe_result = exe_result

	#else:
		#os.system('rm answer.ll && rm answer_ok.ll && rm answer_ok.s && rm answer_ok')
	#os.system('llvm-as path'+str(flag)+'.ll -o path'+str(flag)+'.bc')
	#os.system('llc path'+str(flag)+'.bc -o path'+str(flag)+'.s')
	#os.system('gcc -o path'+str(flag)+' path'+str(flag)+'.s')
	#os.system('timeout 5 ./path'+str(flag))
	#execution_result = commands.getoutput('./path'+str(flag))
	#if flag == 1:
		#continue
	#else: 
		#if execution_result == old_result:
			#print "same output now. "
		#else:
			#print "bug find!! "
			#break	
	#old_result = execution_result
	flag += 1
	recording = []
	file_length -= (len(a)+len(b)-t1_insert_number-t2_insert_number)
	print "verifying path",flag-1
	

	#print "file_lengh dec: ", file_length
	#generating.close()
#file.close()
#generating.close()
#print "path number: ", flag

#combination = itertools.chain(a,b)
#print strmerge
#print combination
#p_result = list(itertools.permutations(combination, len(a)+len(b)))
#print strpermutation
#print p_result
#c_result = list(itertools.permutations(combination, len(a)+len(b)))
#print strpermutation
#print c_result
#print result.pop()

#	string handling
#interleaving = str(p_result.pop()).strip('()')
#inter = str(p_result.pop()).strip('\n')
#print strwrite
#print "version 1: ", inter
#print interleaving.strip('()')
#print "version 2: ", interleaving

#	write testcase file
#testcase.seek(0)
#testcase.write(interleaving)
#print interleaving.split('()')
#interleaving.append(''+result.pop()+'')
#print interleaving
#text = str(result).split(',')
#for text in text:

	#print text 
#print list(itertools.permutations(combination, len(a)+len(b)))
#print (str(result).strip('[]'))
#testcase.seek(0)
#testcase.write(result)
#for i in range(6):
	#testcase.write(result(i))
