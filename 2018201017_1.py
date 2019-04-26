import sys
import copy

roundRobin=0

def get_OutputfileName_Obj(pythonFileName):
	pythonFileName=pythonFileName[0:len(pythonFileName)-3]
	outputFileName=pythonFileName+".txt"
	out=open(outputFileName,"w")

	return out

def Print_Vars(Dictionary):
	temp=copy.deepcopy(Dictionary)
	variables1= temp.keys()
	variables1= sorted(variables1)
	output=""
	for i in variables1:
		output=output+i + " "+str(temp[i])+" "

	return output[:-1]


def getData(InputFileName):
	secondryMemory={}
	cout= open(InputFileName)
	diskData = cout.readline().split()
	
	index=0
	for k in range(int(len(diskData)/2)):
		secondryMemory.update({diskData[index]:diskData[index+1]})
		index+=2

	cout.readline()  ## for skipping the nextline

	input_Task=[]
	while 1:
		input1=[]
		rr = cout.readline().split()
		if len(rr)==2:
			for i in range(int(rr[1])):
				temp=cout.readline()
				
				input1.append(temp[:len(temp)-1])
		else:
			break
		input_Task.append(input1)
		cout.readline()

	cout.close()
	return input_Task,secondryMemory



def Print_Write(tranNo,var,oldValue):
	return "<T" + str(tranNo) + ", " + var + ", " + str(oldValue) + ">"+"\n"

def convert(list):
	res = "".join(list)
	return(res) 



def main(InputFileName,pythonFileName):
	input_Task, secondryMemory=getData(InputFileName)
	out = get_OutputfileName_Obj(pythonFileName)
	all_Output=[]
	mainMemory={}
	variables={}   ### to hold the global variable which r in transaction

	count=0
	totalTrans=0


	for i in range(len(input_Task)):
		totalTrans=totalTrans+len(input_Task[i])

	
	index=0
	BigIndex=0

	while 1:
		
		if count ==totalTrans:
			break

		for task in input_Task:
			index=BigIndex
			for i in range(roundRobin):
				if index < len(task):
					#print(task[index])
					s=task[index]
					if s[0:4]=="READ":
						#print("inside Read:",i)
						if task.index(s)==0:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<START T"+str(transaction_number)+">"+"\n")
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

						#### Read operation #####
						k = s[7:-1]
					
						var =s[5:6]
						if var in mainMemory.keys():
							variables[k]=mainMemory[s[5:6]]
							
						else:
							variables[k]=secondryMemory[s[5:6]]
							#mainMemory.update({s[5:6]:variables[k]})
							mainMemory[s[5:6]]=variables[k]
							
						count+=1
						

						if task.index(s)==len(task)-1:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<COMMIT T"+str(transaction_number)+">"+"\n" )
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

					elif s[0:5]=="WRITE":
						
						if task.index(s)==0:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<START T"+str(transaction_number)+">"+"\n")
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

						count+=1
						##### write operation ####
						transaction_number=input_Task.index(task)+1
						k=s[8:-1]

						all_Output.append(Print_Write(transaction_number,s[6:7],mainMemory[s[6:7]]))

						###update the main memory
						
						mainMemory[s[6:7]]=variables[k]

						all_Output.append(Print_Vars(mainMemory))
						all_Output.append("\n")
						all_Output.append(Print_Vars(secondryMemory))
						all_Output.append("\n")
						

						if task.index(s)==len(task)-1:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<COMMIT T"+str(transaction_number)+">"+"\n" )
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

					elif s[0:6]=="OUTPUT":
						#print("inside output:",i)
						if task.index(s)==0:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<START T"+str(transaction_number)+">"+"\n")
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

						count+=1
						k=s[7:8]
						secondryMemory[k]=mainMemory[k]
						

						if task.index(s)==len(task)-1:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<COMMIT T"+str(transaction_number)+">"+"\n" )
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

					else:
						#### for operation
						if task.index(s)==0:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<START T"+str(transaction_number)+">"+"\n")
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

						k = s.strip().split(':=')
						left_side = k[0]
						operators = ['+','-','*','\/']
						rightside = k[1]

						for op in operators:
							if op in rightside:
								r1 = variables[rightside.strip().split(op)[0]]
								r2 = int(rightside.strip().split(op)[1])
								break

						
						variables[left_side.strip()]=eval(str(r1)+str(op)+str(r2))
						
						count+=1
						if task.index(s)==len(task)-1:
							transaction_number=input_Task.index(task)+1
							all_Output.append("<COMMIT T"+str(transaction_number)+">"+"\n" )
							all_Output.append(Print_Vars(mainMemory))
							all_Output.append("\n")
							all_Output.append(Print_Vars(secondryMemory))
							all_Output.append("\n")

					
					index+=1
				else:
					break
		BigIndex+=roundRobin





	# print("variables:",variables)
	# print("secondryMemory",secondryMemory)
	# print("mainMemory",mainMemory)


	
	all_out=convert(all_Output)
	#print(all_Output)
	out.write(all_out)
	
	out.close()


if __name__ == '__main__':
	roundRobin = int(sys.argv[2])
	main(sys.argv[1],sys.argv[0])
	

