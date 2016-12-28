import os
import sys
import commands

#	Python scipt for automatic execution of QPSO program
#	on multiple files.

n = 62		# just change this and rest is automatic
M = 1
num_schedules = [5000] # List of total schedules to run on


optimals = []
def parseOptimals(filename):
    f = open(filename)
    i = 1
    for line in f:
        if i in range(23,503):
            numbers = map(float, line.split())
            optimals.append(numbers[2])
        i = i+1    

def getAnswerByRunningOn(foldername, filename, schedules):
	cmd = "./qpso ../Dataset/%s/%s %d %d %d" % (foldername, filename,n,M,schedules) 
	(status, output) = commands.getstatusoutput(cmd)	# python stalls during this process and waits for cpp completion.
	if status: 					#non zero value
		print "There was an error while executing file: ", filename
	return output	



if __name__ == '__main__':

	if n==32 :
		parseOptimals("j30opt.sm")
		print optimals

	folder_name = 'j%d.sm' % (n-2)
	# os.chdir(os.path.join("/home/yash/Desktop/QPSO/Dataset/%s" % folder_name))   

	print "Running on ", n-2," set"
	
	for i in num_schedules:
		print "==============================================="
		print "Running for Total schedules = ",i 
		sd = 0
		counter = 0
		u = 1
		while u<3:
			l = 1
			while l<11:
				filename = "j%d%d_%d.sm" % (n-2,u,l)
				print "Running on : ", filename, " Time:",
				
				answer = getAnswerByRunningOn(folder_name, filename, i)
				print answer,
				answer = map(int, answer.split())[0];
				
				if n==32:
					optimal_ans = optimals[(u-1)*10 + l-1]
					print " Optimal:", optimal_ans,
				else:
					f = open("../Dataset/%s/%s" % (folder_name,filename))
					j=0
					optimal_ans = 0 
					for line in f :
						if j == 14 :
							numbers = map(int,line.split())
							optimal_ans = numbers[5]
							break 
						j = j+1		
					print " Critical:", optimal_ans,

				# Solved optimally			
				if answer == optimal_ans:
					counter += 1 
				
				a = (1.0*(answer - optimal_ans))/optimal_ans
				print "SD = ",a
				sd = sd+a
				l = l+1
			u = u+1	 
			print sd 
		print "Optimally solved: ", counter 
		num_files = ((u-1)*(l-1)) ;
		print "FOR Iterations = ",i ," final sd/", num_files, "= ",sd/num_files
		