import os
import commands
import string

###############  initialization  ##############################
temp_testcase = []
temp_path1 = []
file = open('testcase.ll')
for line in file:
	temp_testcase.append(line)
testcase_length = len(temp_testcase)
#print testcase_length
file.close()
file = open('answer.ll')
for line in file:
	temp_path1.append(line)
path_length = len(temp_path1)
file.close()
path_amount = testcase_length / path_length
#print "path_amount: ", path_amount	
###############  start point of scapbooking  ##################
#for j in range(1, path_amount+1):
file = open('whole_program.ll')
#path_name = raw_input("verify path...") 
scrap = open('answer_ok.ll','w')
#scrap = open('path'+str(j)+'_ok.ll','w')
#scrap = open(''+path_name+'_ok.ll','w')
#scrap = open('path1_ok.ll','w')
scrapping = []
for line in file:
	if "entry" in line:
		break
	else:
		#scrap.write(line)
		#print line
		scrapping.append(line)

for i in range(0, len(scrapping)):
	scrap.write(scrapping[i])

scrap.write("entry: \n")
file.close()
scrap.close()
#print "scrapbooking path_amount: ", interleaving.path_amount
#################  replace part #####################
file = open('answer.ll')
booking = open('answer_ok.ll','a')
#file = open('path'+str(j)+'.ll')
#booking = open('path'+str(j)+'_ok.ll','a')
#file = open(''+path_name+'.ll')
#booking = open(''+path_name+'_ok.ll','a')
#booking = open('path1_ok.ll','a')
counter_load = -1
counter_operation = 0
load_number = ""
load_number_1 = ""
operation_name = ""
second_operation = ""
counter_store = 0
counter_call = 0
instruction = []
temp = ""
assert_answer = ""
counter_temp = -1
first_number = ""
#print "path name: ", path_name
#print "replace part"
def rename(first_number):
	counter_temp += 1
        instruction.append(line)
       	if counter_temp >= 1:
           	temp = line
             	temp_1 = temp.split()
             	first_number = str(temp_1[0])
              	#print "old: ", temp
            	temp = temp.replace(str(first_number), str(first_number)+str(counter_temp))
           	#print "new: ", temp
              	instruction.pop()
            	instruction.append(temp)
               	temp = ""

for line in file:
	#print "line. "
	#if ("load" in line) and ("%0" in line):
	if "load" in line:
		counter_load += 1
		instruction.append(line)
		if counter_load >= 1:
			temp = line
			temp_1 = temp.split()
			load_number = str(temp_1[0])
			#print "old: ", temp
			temp = temp.replace(str(load_number), "%"+str(counter_load))
			#print "new: ", temp
			instruction.pop()
			instruction.append(temp)
			temp = ""
			#print instruction
	elif ("store" in line):
                instruction.append(line)
                counter_store += 1
                temp = line
                temp = temp.split()
                second_operation = str(temp[2])
                if "%" not in second_operation:
                        second_operation = str(temp[3])
                if counter_store >= 2:
                        temp = line
                        temp_assert_answer = temp.split()
                        assert_answer = str(temp_assert_answer[2])
                        if "%" not in assert_answer:
                                assert_answer = str(temp_assert_answer[3])
                        #print "op. name: ", operation_name
                        temp = temp.replace(str(assert_answer), str(operation_name)+",")
                        instruction.pop()
                        instruction.append(temp)
                        temp_assert_answer = temp.split()
                        assert_answer = str(temp_assert_answer[2])
                        if "%" not in assert_answer:
                                assert_answer = str(temp_assert_answer[3])
        elif ("call" in line):
                if counter_call > 0:
                        temp = line
                        #print "old: ", temp
                        temp_1 = temp.split()
                        call_number = str(temp_1[0])
                        temp = temp.replace(call_number, "%call"+str(counter_call))
                        #instruction.pop()
                        #print "new: ", temp
                        instruction.append(temp)
                        #temp = ""
                else:
                        instruction.append(line)
                counter_call += 1

	#elif ("load" not in line) and ("call" not in line) and ("store" not in line):
	else:
		counter_operation += 1
		instruction.append(line)
		temp = line
		temp_1 = temp.split()
		#print len(temp_1)
		load_number = str(temp_1[1])
		i = 1
		while (("%" not in load_number) and ("mutex" not in load_number) and i < len(temp_1)):
			load_number = str(temp_1[i])
			i += 1
		#operation_name = str(temp_1[0])
		temp = temp.replace(str(load_number), "%"+str(counter_load)+",")
		instruction.pop()
		instruction.append(temp)
		temp = ""
		if counter_operation >= 2:
			temp = line
			temp_1 = temp.split()
			#load_number5 = str(temp_1[5])
			#print "old: ", temp
			#load_number_back = str(temp_1[5])
			load_number_back = str(temp_1[1])
			load_number_front = str(temp_1[0])
			i = 1
			while (("%" not in load_number_back) and ("mutex" not in load_number_back) and i < len(temp_1)):
			#while ("%" not in load_number_back):
                        	load_number_back = str(temp_1[i])
                        	i += 1
			#print i
			#print load_number_back
			#print "2nd: ", second_operation
                       	temp = temp.replace(str(load_number_back), str(second_operation))
			#print "nearest store operation: ", temp
			temp_1 = temp.split()
			load_number_back = str(temp_1[1])
			i = 1
                        while (("%" not in load_number_back) and ("mutex" not in load_number_back) and i < len(temp_1)):
                                load_number_back = str(temp_1[i])
                                i += 1
                        load_number_front = str(temp_1[0])
			#i = 1
			#while (("%" not in load_number_front) and ("mutex" not in load_number_front) and i < len(temp_1)):
                        	#load_number_front = str(temp_1[i])
                        	#i += 1
			#print i
			#print load_number_front
			#print "load_number_front: ", str(load_number_front)
			#print "load_number_back: ", str(load_number_back)
			if str(load_number_front)+"," == str(load_number_back):
				temp = temp.replace(str(load_number_front), str(load_number_front)+str(counter_operation), 1)
				temp_1 = temp.split()
			operation_name = str(temp_1[0])
				#print "multiple: ", temp
				#print "op. name: ", operation_name
                       	#print "new: ", temp
			instruction.pop()
                       	instruction.append(temp)
                       	temp = ""

#print len(instruction)

for i in range(0, len(instruction)):
	booking.write(instruction[i])
	#print "123"
file.close()
booking.close()

###########  ending part of scapbooking  ##################
file = open('whole_program.ll')
scrapbooking = open('answer_ok.ll','a')
#scrapbooking = open('path'+str(j)+'_ok.ll','a')
#scrapbooking = open(''+path_name+'_ok.ll','a')
#scrapbooking = open('path1_ok.ll','a')
counter_store = 0
counter = 0
cut = 0
ending = []
temp_2 = []
temp_cut = 0

for line in file:
	temp_2.append(line)
	if ("ret" in line):
		break
		#temp.append(line)
#print "ret: ", len(temp_2)
#print "main instruction length: ", len(temp_2)-len(scrapping)+1
file.close()

file = open('whole_program.ll')
#print len(scrapping)+1+len(instruction)
#print "here: ", assert_answer
for line in file:
	counter += 1
	#cut = len(scrapping)+len(temp_2)-len(scrapping)
		
	cut = len(temp_2)	 							#before 20171121
		
	#if ("conv" in line) and ("assert" not in line):
		#cut = counter
		#ending.append(line)
	if ("cmp" in line) and ("br" not in line):	# not good
	#print "123: ", str(assert_answer.strip(","))
	#if "conv" in line:
		#print counter
	#if ("%conv" in line):
		temp_cut = counter
		temp = line
		temp_1 = temp.split()
		assert_source = str(temp_1[5])
		#print assert_source
		#i = len(temp_1)-1
		#while("%" not in temp_1[i]):
			#assert_source = str(temp_1[i])
			#print assert_source
			#i -= 1
		#print "assert_answer: ", assert_answer
		#print "assert_source: ", assert_source
		temp = temp.replace(str(assert_source), str(assert_answer))

		
		#temp = temp.replace("8*", "32")		
		#temp = temp.replace("%"+str(counter_load), "%"+str(counter_load+1))
		#print "final: ", temp
		print temp_cut
		ending.append(temp)
	else:
		#cut = len(temp_2)
		ending.append(line)

#print cut
	
if (temp_cut < cut) and (temp_cut != 0):
	cut = temp_cut
#print "cut: ", cut
for i in range(cut-1, counter):	# include cmp ( before conv )
	scrapbooking.write(ending[i])

file.close()
scrapbooking.close()	 
