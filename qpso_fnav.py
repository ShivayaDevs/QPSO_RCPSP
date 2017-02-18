import random
import sys
import math

# globals
def operate(file):
	n = 32
	m = 50
	iterations_max = 100
	g = 0.4
	number_resources = 4
	p_min = 0
	p_max = 1


	# predecessor list
	pred = []
	for i in range(0,n) :
		pred.append([])

	#successpor list
	succ = []
	for i in range(0,n):
		succ.append([])

	#delay list
	duration = [0 for x in range(0,n)]

	#resources list
	resources_required = []
	for i in range(0,n) : 
		resources_required.append([])

	file = open(file)

	line_number = 0

	for line in file : 
		line_number = line_number + 1
		if line_number in range(19,51) :
			numbers = map(int, line.split())
			activity_index = numbers[0]-1
			no_succ = numbers[2]
			for x in numbers[3:] :
				succ[activity_index].append(x-1)
				pred[x-1].append(activity_index)

		if line_number in range(55,87) :
			numbers = map(int, line.split())
			activity_index = numbers[0]-1
			duration[activity_index] = numbers[2]
			for x in numbers[3:] :
				resources_required[activity_index].append(x)

		if line_number == 90 :
			max_resources  = map(int, line.split())


	# printing lists==========> CHECKED
	#print "Predecessor: "
	#print pred
	#print "Successor: "
	#print succ
	#print "duration: "
	#print duration
	#print "Resources: "
	#print resources_required

	r_pred = succ
	r_succ = pred

	#print succ
	#print "r_pred", r_pred
	#print pred
	#print "r_succ", r_succ

	class Particle :
		def __init__ (self) :
			self.position = [random.uniform(p_min, p_max) for x in range(0,n)]
			self.best_cost = sys.maxint
			self.best_position = self.position

	particles = [ Particle() for x in range(0,m) ]

	global_cost = sys.maxint
	global_pos = [random.uniform(p_min,p_max) for x in range(0,n)]

	class Schedule :
		activity = 0
		start_time = 0
		finish_time = 0

	iteration = 0
	while iteration < iterations_max :

		#print "iteration : ",iteration

		mbest = []

		for i in range(0,n) :
			b=0
			for j in range(0,m) :
				b = b+particles[j].position[i]
			mbest.append(b/m)

		#print "mbest", mbest

		



		for i in range(0,m) :
			c1 = random.uniform(0,1)
			c2 = random.uniform(0,1)
			
			u = random.uniform(0,1)
			
			if u==0 :
				u = 0.5

			P = [w+u for w,u in zip( [ c1*x for x in particles[i].best_position],[c2*y for y in global_pos] ) ]
			P = [ x/(c1+c2) for x in P]

			diff = [abs(w-z) for w,z in zip(mbest, particles[i].position)]

			if u==0 :
				u = 0.5

			temp = [g*x*math.log(1/u) for x in diff]


			if random.uniform(0,1)<0.5 :
				particles[i].position = [w-z for w,z in zip(P,temp)]
			else: 
				particles[i].position = [w+z for w,z in zip(P,temp)]

			for x in range(0,n) :
				if particles[i].position[x] < p_min:
					particles[i].position[x] = p_min
				elif particles[i].position[x] > p_max:
					particles[i].position[x] =p_max
			#print particles[i].position





			#schedule1==========>FORWARD SCHEDULE
			finished = [False for x in range(0,n)]
			scheduled = []

			current_time = 0

			s = Schedule()
			s.activity = 0
			s.start_time = 0
			s.finish_time = 0

			scheduled.append(s)

			finished[0] = True
			print max_resources
			while 1:
				#print "current time: ",current_time
				#print "finished: ",finished
				#print "scheduled: "
				#print [x.activity for x in scheduled]
				#print "==============>"

				
				for s in scheduled :
					if ( (s.finish_time == current_time) ) :
						finished[s.activity] = True
						print "Activity ", s.activity
						max_resources  = [w+z for w,z in zip(max_resources, resources_required[s.activity])]

				flag = 0
				for x in range(0,n):
					if finished[x] == False:
						flag =1

				#print "flag" , flag

				if flag == 0:
					break


				feasible = []


				for w in range(0,n):
					if finished[w] == True :
						for x in succ[w] : 
							if finished[x] == False :
								flag = 0
								for y in pred[x] :
									if finished[y] == False :
										flag = 1
								if flag == 0:
									feasible.append(x)

				# removing duplicates		
				listToset = set(feasible)
				feasible = list(listToset)
				#print "feasible: ", feasible


				def priority(activity_id) :
					return particles[i].position[activity_id]

				feasible = sorted(feasible,key = priority)

				for x in feasible :
					flag2 =0 
					for w in scheduled :
						if w.activity == x :
							flag2=1
					if flag2 == 0 :

						flag = 0 
						for w in range(0,number_resources) :
							if resources_required[x][w] > max_resources[w] :
								flag = 1
						
						if flag == 0 :
							max_resources = [w-z for w,z in zip(max_resources, resources_required[x])] 
							s = Schedule()
							s.activity = x
							s.start_time = current_time
							s.finish_time = current_time + duration[x]
							if s.finish_time == s.start_time :
								print s.activity	
								finished[s.activity] = True
							scheduled.append(s)

				
				current_time = current_time + 1

			print max_resources	
			
			cost1 = 0
			for x in scheduled :
				cost1= max(cost1,x.finish_time)

			#print max_resources








			# =================> BACKWARD SCHEDULE
			finished = [False for x in range(0,n)]
			scheduled = [ ]

			current_time = 0

			s = Schedule()
			s.activity = 31
			s.start_time = 0
			s.finish_time = 0

			scheduled.append(s)

			finished[31] = True

			while 1:
				#print "current time: ",current_time
				#print "finished: ",finished
				#print "scheduled: "
				#print [x.activity for x in scheduled]
				#print "==============>"

				
				for s in scheduled :
					if ( (s.finish_time == current_time) ) :
						finished[s.activity] = True
						max_resources  = [w+z for w,z in zip(max_resources, resources_required[s.activity])]

				flag = 0
				for x in range(0,n):
					
					if finished[x] == False:
						flag =1

				#print "flag" , flag

				if flag == 0:
					break


				feasible = []


				for w in range(0,n):
					if finished[w] == True :
						for x in r_succ[w] : 
							if finished[x] == False :
								flag = 0
								for y in r_pred[x] :
									if finished[y] == False :
										flag = 1
								if flag == 0:
									feasible.append(x)

				# removing duplicates		
				listToset = set(feasible)
				feasible = list(listToset)
				#print "feasible: ", feasible


				def priority(activity_id) :
					return particles[i].position[activity_id]

				feasible = sorted(feasible,key = priority)

				for x in feasible :
					flag2 =0 
					for w in scheduled :
						if w.activity == x :
							flag2=1
					if flag2 == 0 :

						flag = 0 
						for w in range(0,number_resources) :
							if resources_required[x][w] > max_resources[w] :
								flag = 1
						
						if flag == 0 :
							max_resources = [w-z for w,z in zip(max_resources, resources_required[x])] 
							s = Schedule()
							s.activity = x
							s.start_time = current_time
							s.finish_time = current_time + duration[x]
							if s.finish_time == s.start_time :
								finished[s.activity] = True
							scheduled.append(s)

				
				current_time = current_time + 1


			
			cost2 = 0
			for x in scheduled :
				cost2= max(cost2,x.finish_time)

			#print "costs: ",cost1, cost2


			# calculating cost
			cost = min(cost1, cost2)



			#print cost
			
			if(particles[i].best_cost > cost) :
				particles[i].best_position = particles[i].position
				particles[i].best_cost = cost

			if cost<global_cost :
				global_cost = cost
				global_pos = particles[i].position

		iteration = iteration + 1



	print "global_cost",global_cost
	return global_cost

if __name__ == '__main__':
	operate("QPSO/Dataset/j30.sm/j3018_9.sm")















