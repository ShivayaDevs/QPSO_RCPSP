import os
import sys
import commands

"""
	Python scipt for automatic execution of QPSO program
	on multiple files.

	ATTENTION: Copy cpp program's executable into the dataset folder 

"""


n = 122		# just change this and rest is automatic


optimals = []
def parseOptimals(filename):
    f = open(filename)
    i = 1
    for line in f:
        if i in range(23,503):
            numbers = map(float, line.split())
            optimals.append(numbers[2])
        i = i+1    
G = 0.8
def getAnswerByRunningOn(filename, iterations):
	cmd = "./qpso %s %d %f %d" % (filename,n,G,iterations) 
	(status, output) = commands.getstatusoutput(cmd)	# python stalls during this process and waits for cpp completion.
	if status: #non zero value
		print "There was an error while executing file: ", filename
	return output	

if __name__ == '__main__':

	# parseOptimals("j30opt.sm")
	# print optimals
	folder_name = 'j%d' % (n-2)
	os.chdir(os.path.join("/home/yash/Desktop/Work/Projects/QPSOinRCPSP/Dataset/%s.sm"%folder_name))   

	# global G
	print "Running on ",n-2," set"

	for i in range(0, 7):
		print "==============================================="
		print "Running for G = ",G 
		sd = 0
		u = 1
		while u<49:
			l = 1
			while l<11:
				filename = "j%d%d_%d.sm" % (n-2,u,l)
				print "Running on file: ", filename, " Time:",
				
				answer = getAnswerByRunningOn(filename)
				print answer
				answer = map(int, answer.split())[0];
				# optimal_ans = optimals[(u-1)*10 + l-1]
				
				f = open(filename)
				j=0
				for line in f :
					if j == 14 :
						numbers = map(int,line.split())
						optimal_ans = numbers[5]
						break 
					j = j+1		
				print "Optimal is : ", optimal_ans,	

				a = (1.0*(answer - optimal_ans))/optimal_ans
				print "SD = ",a
				sd = sd+a
				l = l+1
			u = u+1	 
			print sd 
		print "FOR G = ",G," final sd/30: ",sd/30
		G += 0.2