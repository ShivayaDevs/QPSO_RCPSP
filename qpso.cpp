#include <bits/stdc++.h>

#define MAX_ITERS 400
#define NUM_RESOURCES 4
#define P_MAX = 1
#define P_MIN = 0


using namespace std; 

int N = 32;
int M = N-2 ;
float G = 1.7 ;

string potential = "delta" ;
vector<int> succ_list[123];
vector<int> pred_list[123];
vector<int> res_req_list[123];
int duration[123];
int max_resources[NUM_RESOURCES];

double gBest_pos[123];
int gBest_cost = INT_MAX;


double getRandom0to1(){
	return (float) rand()/RAND_MAX ; 
}
void read_file(char*);

class Activity{
	public:
	int activity_id ;
	int start_time ;
	int duration ;
	int f_time ;
};

class Particle{
	public:
	double pos[123] ; 
	double best_pos[123] ;
	int best_cost ;
	Particle(){
		// cout<<"\nCreating particle: ";
		for(int i=0; i<N ; i++){
			best_pos[i] = pos[i] = getRandom0to1();
			// cout<<" "<<best_pos[i];
		}
		best_cost = INT_MAX ;
	}
	void performOps();
};
Particle particles[123];

int current_particle_id = 0;
int compare(const int &a, const int &b){
		return (particles[current_particle_id].pos[a] > particles[current_particle_id].pos[b]);
}

vector<int> getFeasibleActs(bool scheduled[], int completed_preds[]){
	vector<int> feasible_acts;
	for(int i=0 ; i<N ; i++){
		if(completed_preds[i] == pred_list[i].size()  &&  !scheduled[i])
			feasible_acts.push_back(i);
	}
	return feasible_acts ;
}

void executeOnFile(char* filename){
	read_file(filename);
	int i, iterations = MAX_ITERS ;
	while(iterations--)
		for(i=0 ; i<M ; i++){
			// cout<<"Perform Ops on particle "<<i<<"\n";
			current_particle_id = i ;
			particles[i].performOps();
		}
	printf("%d", gBest_cost) ;
}

void Particle::performOps(){
	
	double c1 = getRandom0to1();
	double c2 = getRandom0to1();
	double u = getRandom0to1();

	bool scheduled[N], finished[N] ;
	int completed_preds[N];

	double P[N] ;				//Optimization : Allocate dynamically and reuse 
	double up[N], z ;
	// cout<<sizeof(best_pos);
	// cout<<"\nParticle :"<<current_particle_id<<".......\n" ;
	for(int i=0 ; i<N ; i++){

		P[i] = (c1*best_pos[i] + c2* gBest_pos[i])/(c1+c2) ;
	
		z = (pos[i]-P[i]) ;
		up[i] = z/(G*log(2)) ;
		
		//ATTENTION: This needs to be filled!!
		// Plus the comparison formula
		/*if(potential == "delta"){}
		else if(potential == "harmonic"){}*/  
		
		pos[i] = up[i] + P[i] ;
		scheduled[i] = finished[i] = false ;
		completed_preds[i] = 0 ;
	}		
	
	vector<Activity> scheduleList ;
    int time = 0;

	//Creating the first activity
    Activity a0 ;
    a0.activity_id = 0 ;
    a0.start_time = 0 ;
    a0.duration = 0 ;
    a0.f_time = 0 ;

    //Adding the activity to the schedule list
    scheduleList.push_back(a0) ;
    scheduled[0] = true ;

    int finished_activity = 0 ;
    int resources_left[NUM_RESOURCES] ;
    for(int i=0; i<NUM_RESOURCES ; i++)
    	resources_left[i] = max_resources[i] ;

    while(1){
    	// printf("Activity %d finished.\n", finished_activity);
    	 //Take resources back
        if(finished[finished_activity] == false){
        	for(int i=0 ; i<NUM_RESOURCES ; i++)
        		resources_left[i] = resources_left[i] + res_req_list[finished_activity][i] ;
        	for(int i=0 ; i<succ_list[finished_activity].size() ; i++){
        		completed_preds[succ_list[finished_activity][i]]++ ;
        	}
        	finished[finished_activity] = true;
        }

        if( scheduleList.size() >= N)
        	break ;
        // Get activities satisfying precedence constraints
        vector<int> feasible_activities = getFeasibleActs(scheduled, completed_preds) ;
		sort( feasible_activities.begin(), feasible_activities.end(), compare ) ;	//sort by decreasing priority ---====CHECk

		//test for sorting Result: Working perfectly
		/*for(int i=0 ; i<feasible_activities.size();i++){
			printf("Activity: %d priority: %f\n", feasible_activities[i], pos[feasible_activities[i]]);
		}*/

		// Now get activities which are also satisfying resource constraints
		int flag, activityId;
		for (int i=0 ; i<feasible_activities.size() ; i++){
			activityId = feasible_activities[i] ;
			flag = 0 ;
			for(int j=0; j<4 ;j++)
				if(resources_left[j] < res_req_list[activityId][j])
					flag = 1 ;
			if(flag == 0){
				// Schedule this activity
				Activity a1 ;
				a1.activity_id = activityId ;
				a1.start_time = time ;
				a1.duration = duration[activityId];
				a1.f_time = a1.start_time + a1.duration ;
				scheduleList.push_back(a1) ;
				scheduled[activityId] = true ;

				for(int j=0 ; j<4 ; ++j)
					resources_left[j] -= res_req_list[activityId][j] ;
			}
		}

		int minFinTime = INT_MAX ;
		int minFinAct = -1 ;
		for(int i=0 ; i<scheduleList.size() ; i++){
			if(finished[scheduleList[i].activity_id] == false && minFinTime>scheduleList[i].f_time){
				minFinTime = scheduleList[i].f_time ;
				minFinAct = scheduleList[i].activity_id ;
			}
		}

		if(minFinTime != INT_MAX && minFinAct != finished_activity){
			time = minFinTime ;
			finished_activity = minFinAct ;
		}
    }
    // Now, the parallel schedule has been formed for this particle
    // So, comparing it with other's now.

    // pritnf("Activities | StartTime\n");
    int mCost = 0 ;
    for(int i=0 ; i<scheduleList.size() ; i++){
		// printf("%d  %d\n", scheduleList[i].activity_id, scheduleList[i].start_time);
        mCost = max(mCost, scheduleList[i].f_time) ; 
    }
	// printf("Total cost: %d\n", mCost);

    // Update local best
    if (mCost < best_cost){
        for(int i=0 ; i<N ; i++)
        	best_pos[i] = pos[i];
        best_cost = mCost ;
	}

    // update global best
    if (mCost < gBest_cost){
        for(int i=0 ; i<N ; i++)
        	gBest_pos[i] = pos[i];
        gBest_cost = mCost;
    }

}



void read_file(char* filename){		//Tested: Working perfectly!
	FILE *fp = fopen(filename, "r");
	char line[100];
	int i = 1 ;
	int num[10];
	while( fgets(line, 79, fp) != NULL ){
		istringstream iss(line) ;
		// cout<<" "<<line;
		if(19<=i && i<N+19){
			//Parse successors
			iss>>num[0]>>num[1]>>num[2] ;
			// cout<<num[0]<<" has "<<num[2]<<" successors\n";
			for(int k=0 ; k<num[2] ; k++){
				iss>>num[3];
				// cout<<" "<<num[3];
				succ_list[num[0]-1].push_back(num[3]-1) ;
				pred_list[num[3]-1].push_back(num[0]-1) ;
			}
			// cout<<"\n";
		}
		else if(N+19+4<=i && i<N+19+4+N){
			//Parse resource requirements
			iss>>num[0]>>num[1]>>num[5]>>num[1]>>num[2]>>num[3]>>num[4] ;
			// printf("Activity: %d R1:%d R2:%d R3:%d R4%d\n", num[0],num[1],num[2],num[3],num[4]);
			res_req_list[num[0]-1].push_back(num[1]);
			res_req_list[num[0]-1].push_back(num[2]);
			res_req_list[num[0]-1].push_back(num[3]);
			res_req_list[num[0]-1].push_back(num[4]);
			duration[num[0]-1] = num[5] ;
		}
		else if(i==2*N+19+4+3){
			iss>>max_resources[0]>>max_resources[1]>>max_resources[2]>>max_resources[3];
		}
			i++;
	}
}


int main(int argc, char **argv){
	
	/* Commandline Arguments format
	*	./qpso j301_1.sm 32 
	*
	*	note: G can also be added as CMD arg
	*/

	if(argc == 4){
		N = atoi(argv[2]);
		// cout<<"Received N = "<<N<<"M= "<<M<<"\n";
		M = N-2 ;

		G = atof(argv[3]) ;
		// cout<<"G = "<<G<<"\n";

		executeOnFile(argv[1]);

	}
	// char filename[10] = "j301_1.sm";
	// executeOnFile(filename);
	return 0;
}

//output: + no sync  : 44.37secs