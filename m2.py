import os
import qpso_rcpsp as prog
import sys

"""
	Python scipt for automatic execution of QPSO program
	on multiple files.
"""


n = 32		# just change this and rest is automatic
m = n

def reset_globals():
	prog.pred_list = []
	prog.succ_list = []
	prog.duration = []
	prog.res_req_list = []
	prog.max_resources = []

	prog.n = n
	prog.m = n 
	# Global bests
	prog.gBest_pos = [0 for x in range(0, n)]
	prog.gBest_vel = [0 for x in range(0, n)]
	prog.gBest_cost = sys.maxint
	prog.best_solution = []

	for i in range(0, n):
	    prog.pred_list.append([])
	    prog.succ_list.append([])
	    prog.res_req_list.append([])
	    prog.duration.append(0)
	prog.particles = [prog.Particles() for x in range(0, m)]
    
if __name__ == '__main__':
	folder_name = 'j%d' % (n-2)
	os.chdir(os.path.join("/home/yash/Desktop/Work/Projects/QPSOinRCPSP/Dataset/%s.sm"%folder_name))   

	u = 1
	while u<11:
		l = 1
		while l<11:
			filename = "j30%d_%d.sm" % (u,l)
			print "Running on file: ", filename, " Time: ",
			prog.execute_on_file(filename)
			reset_globals()
			l = l+1
		u = u+1	 
