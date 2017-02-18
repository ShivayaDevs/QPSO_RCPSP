import os
import sys
import commands

#	Python scipt for automatic execution of QPSO program
#	on multiple files.
#   execute this as : "python cpp_j30_all_files.py"

# Now, you don't need to set N, M in the cpp file, you can set them here
# and the rest is automatic.
n = 32		
M = 50
num_schedules = 5000 # List of total schedules to run on

# List containing optimals for the j30 set.
optimals = []
def parseOptimals(filename):
    f = open(filename)
    i = 1
    for line in f:
        if i in range(23,503):
            numbers = map(float, line.split())
            optimals.append(numbers[2])
        i = i+1    

# Starts the execution of the C++ file whose name is given as a parameter.
def getAnswerByRunningOn(filename):
	cmd = "./qpso_all %s %d %d %d" % (filename,n,M,num_schedules) 
	(status, output) = commands.getstatusoutput(cmd)		
	# Non zero value( status has 0 if successful. return 0)
	if status: 					
		print "There was an error while executing file: ", filename
	return output	



if __name__ == '__main__':

	parseOptimals("j30opt.sm")
	print optimals

	folder_name = 'j30.sm'
	
	"""
		u = file start set-index initially and increases.
		so if u varies from 1 to 32 then we are running on 
		j301_1.sm to j3032_10.sm

		l = simply varies from 1 to 10 

	"""
	sd = 0
	counter = 0
	u = 1			
	while u<49:
		l = 1
		while l<11:
			filename = "j30%d_%d.sm" % (u,l)
			print "Running on : ", filename, " Time:",
			
			answer = getAnswerByRunningOn(filename)
			print answer,
			answer = map(int, answer.split())[0];
			
			optimal_ans = optimals[(u-1)*10 + l-1]
			print " Optimal:", optimal_ans,
			
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
	print "FOR Iterations = ",i , " final sd/", num_files, "= ", sd/num_files
		