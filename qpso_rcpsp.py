#! /usr/bin/python
import os
import random
import sys

# Declaring Globals here
n = 32
m = n
num_resources = 4
max_iterations = 400

p_max = 1
p_min = 0
v_min = -1
v_max = 1
c1 = 2
c2 = 2
wi = 1

pred_list = []
succ_list = []
duration = []
res_req_list = []
max_resources = []

# Global bests
gBest_pos = [0 for x in range(0, n)]
gBest_vel = [0 for x in range(0, n)]
gBest_cost = sys.maxint
best_solution = []

for i in range(0, n):
    pred_list.append([])
    succ_list.append([])
    res_req_list.append([])
    duration.append(0)


class Particles:
    def __init__(self):
        self.pos = [0 for x in range(0, n)]
        self.vel = [0 for x in range(0, n)]
        self.best_pos = [0 for x in range(0, n)]
        self.best_cost = sys.maxint


# Earlier called Schedule
class Activity:
    def __init__(self):
        self.activity_id = 0
        self.start_time = 0
        self.duration = 0
        self.f_time = 0


# Creating m particles
particles = [Particles() for x in range(0, m)]


# Globals end here -----

def initialize_particles():
    for i in range(0, m):
        particles[i].pos = [random.uniform(p_min, p_max) for x in range(0, n)]
        particles[i].vel = [random.uniform(v_min, v_max) for x in range(0, n)]
        particles[i].best_pos = particles[i].pos
        particles[i].best_cost = sys.maxint


# File reader and list creator //TESTED : Perfect!
def read_file(filename):
    f = open(filename, 'r')

    i = 0
    for line in f:
        i += 1

        if i in range(19, n+19):
            numbers = map(int, line.split())
            activity_id = numbers[0] - 1
            successors = numbers[2]

            # Updating successor list
            for x in numbers[3:]:
                succ_list[activity_id].append(x - 1)

            # Updating predecessor list
            for x in numbers[3:]:
                pred_list[x - 1].append(activity_id)

        # Updating duration and resource list
        if i in range(n+19+4, n+19+4+n):
            numbers = map(int, line.split())
            activity_id = numbers[0] - 1
            duration[activity_id] = numbers[2]
            for x in numbers[3:]:
                res_req_list[activity_id].append(x)

        # Storing maximum resources available
        if i == 2*n+19+4+3 :
            global max_resources
            max_resources = map(int, line.split())


def get_feasible_activities(finished, scheduled):
    feasible_activities = []
    for x in range(0, len(finished)):
        if finished[x]:
            for succ in succ_list[x]:
                flag = 0
                for pred in pred_list[succ]:
                    if not finished[pred]:
                        flag = 1
                if flag == 0:
                    if not scheduled[succ]:
                        feasible_activities.append(succ)
    # Removing duplicates
    list_to_set = set(feasible_activities)
    return list(list_to_set)


def execute_on_file(filename):
    read_file(filename)
    initialize_particles()
    iterations = 0
    while iterations < max_iterations:
        for i in range(0, m):
            perform_ops_on_particle(i)
        best_solution.append(gBest_cost)
        iterations += 1
    # print best_solution
    print gBest_cost


def perform_ops_on_particle(i):
    global gBest_cost, gBest_pos
    # Update particle's velocity and position
    particles[i].vel = [w + v + h for w, v, h in
                        zip(([x * wi for x in particles[i].vel]),
                            ([c1 * random.uniform(0, 1) * z for z in
                              [x - y for x, y in zip(particles[i].best_pos, particles[i].pos)]]),
                            ([c2 * random.uniform(0, 1) * z for z in
                              [x - y for x, y in zip(gBest_pos, particles[i].pos)]]))]

    particles[i].vel = [min(x, v_max) for x in particles[i].vel]
    particles[i].vel = [max(x, v_min) for x in particles[i].vel]

    particles[i].pos = [sum(x) for x in zip(particles[i].pos, particles[i].vel)]
    particles[i].pos = [min(x, p_max) for x in particles[i].pos]
    particles[i].pos = [max(x, p_min) for x in particles[i].pos]

    # print "Particle no:%d" % i
    # print "Pos: ", particles[i].pos
    # print "Vel: ", particles[i].vel

    # """ Evaluating the schedule """

    scheduled = [False for x in range(0, n)]
    finished = [False for x in range(0, n)]
    scheduleList = []
    time = 0

    a0 = Activity()
    a0.activity_id = 0
    a0.start_time = 0
    a0.duration = 0

    # Adding the activity to the schedule list
    scheduleList.append(a0)
    scheduled[0] = True

    finished_activity = 0
    resources_left = max_resources

    while 1:
        # print "Activity %d finished." % finished_activity
        # Take the resources back
        if not finished[finished_activity]:
            resources_left = [x + y for x, y in zip(resources_left, res_req_list[finished_activity])]
            finished[finished_activity] = True

        if len(scheduleList) >= n:
            break

        # Finding all the activities for which precedence constraints are satisfied.
        feasible_activities = get_feasible_activities(finished, scheduled)

        # Sort the feasible_activities in descending order
        def priority(activity_id):
            return particles[i].pos[activity_id]

        feasible_activities = sorted(feasible_activities, key=priority, reverse=True)

        # print "Time: %d  Feasible Activities are: " % time,
        # for j in feasible_activities:
        #     print j,
        # print ''

        # Checking feasible activities for resource constraints.
        for activity in feasible_activities:
            flag_new = 0
            for x, y in zip(resources_left, res_req_list[activity]):
                if x < y:
                    flag_new = 1  # Resource requirement not satisfied.

            if flag_new == 0:
                # This activity can be scheduled.
                # Add it to the schedule and to the schedule list.
                a1 = Activity()
                a1.activity_id = activity
                a1.start_time = time
                a1.duration = duration[activity]
                a1.f_time = a1.start_time + a1.duration
                scheduleList.append(a1)
                scheduled[activity] = True

                # Update resources
                resources_left = [w - z for w, z in zip(resources_left, res_req_list[activity])]

        # Earliest finish time of the scheduled activities is stored in finish_time
        def finishTime(a):
            if not finished[a.activity_id]:
                return a.f_time
            return sys.maxint

        activity_with_min_finish_time = min(scheduleList, key=finishTime)
        finish_time = activity_with_min_finish_time.f_time

        if finish_time != sys.maxint and finished_activity != activity_with_min_finish_time:
            time = finish_time
            finished_activity = activity_with_min_finish_time.activity_id

    # Now, the parallel schedule has been formed for this particle
    # So, comparing it with other's now.

    # print "Activities | StartTime"
    cost = 0
    for activity in scheduleList:
        # print activity.activity_id, activity.start_time
        cost = max(cost, activity.f_time)
    # print "Total cost: ", cost

    # Update local best
    if cost < particles[i].best_cost:
        particles[i].best_pos = particles[i].pos
        particles[i].cost = cost

    # update global best
    if cost < gBest_cost:
        gBest_pos = particles[i].pos
        gBest_cost = cost


if __name__ == '__main__':
    os.chdir(os.path.join("/home/yash/Desktop/Work/Projects/QPSOinRCPSP/Dataset/j30.sm"))
    execute_on_file('j301_1.sm')
