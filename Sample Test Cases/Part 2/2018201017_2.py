import sys

def get_OutputfileName_Obj(pythonFileName):
	pythonFileName=pythonFileName[0:len(pythonFileName)-3]
	outputFileName=pythonFileName+".txt"
	out=open(outputFileName,"w")

	return out


def getData(InputFileName):
	secondryMemory={}
	cout= open(InputFileName)
	diskData = cout.readline().split()
	
	index=0
	input_Task=[]
	for k in range(int(len(diskData)/2)):
		secondryMemory.update({diskData[index]:diskData[index+1]})
		index+=2

	cout.readline()  ## for skipping the nextline
	while 1:
		line=cout.readline()
		if line=='':
			break
		else:
			input_Task.append(line[:len(line)-1])
	
	cout.close()
	return input_Task,secondryMemory


def Print_Vars(secondryMemory):
	variables= secondryMemory.keys()
	variables= sorted(variables)
	output=""
	for i in variables:
		output=output+i + " "+str(secondryMemory[i])+" "

	output=output[:-1]+"\n"
	return output


def main(pythonFileName,InputFileName):
	input_Task, secondryMemory = getData(InputFileName)
	
	out = get_OutputfileName_Obj(pythonFileName)
	

	input_Task=	input_Task[::-1]  ### reverse the list
	 
	committed=[]
	for task in input_Task:
		if task[1:6]=="START":
			continue
		if task[1:7]=="COMMIT":
			committed.append(task[8:10])
		else:
			transaction=task[1:3]
			if transaction in committed:
				continue
			else:
				secondryMemory[task[5:6]]=int(task[8:-1])

	
	### writing secondry memory values to the file
	output=Print_Vars(secondryMemory)
	out.write(output)

	
	out.close()


if __name__ == '__main__':
	main(sys.argv[0],sys.argv[1])
	

