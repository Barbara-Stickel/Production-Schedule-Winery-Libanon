def main():
    # This function returns the optimal schedule and the Lmax associate
    
    # We collect the data
    dic = collect_jobs()
    
    # We initialize teh time
    t=0
    
    # It represents the final schedule we want to return
    final_schedule = {}
    Total_L_max = 0
    
    # We look each month
    for key in dic:

        # For each month, we compute the list of possible schedule
        schedule_list = list_schedule(dic[key])

        # Then, we take the optimal schedule
        (schedule_optimal, Lmax, time) = optimal_schedule(schedule_list, dic[key], t)

        # We update the final schedule with the schedule of the given month
        final_schedule.update(schedule_optimal)

        # We update Lmax
        Total_L_max= max(Total_L_max, Lmax)

        # We increase t
        t=round(time, 1)
    return(final_schedule, Total_L_max)


def collect_jobs():
    
    # We import the data
    import pandas as pd
    excel_file = pd.read_excel("data.xlsx", sheetname = "Jobs")
    
    # We create the list of jobs
    list_job =[]

    for i in range(1, len(excel_file)+1):
        #print(i)
        job_id = i
        job_name = excel_file.loc[i][0]
        d_j = round(float(excel_file.loc[i][1]), 3)
        r_j = round(float(excel_file.loc[i][2]), 3)
        p_j = round(float(excel_file.loc[i][3]), 3)
        dic = {'d_j':d_j, 'job_id':job_id, 'job_name':job_name, 'p_j':p_j, 'r_j':r_j}
        list_job.append(dic)
    
    # We seperate the data per month
    list_job_per_dj = {}
    i=15
    while i<236:
        list_job_per_dj[i]=[]
        for job in list_job:
            if job['d_j']==i:
                list_job_per_dj[i].append(job)
        i+=20
    
    return list_job_per_dj
    # We create the different schedule for each month
    
def list_schedule(gen_list_jobs): 
    
    #the input should be a list of n jobs:
    #  jobs = [job_1, job_2, ... , job_n]
    #
    #Each job should be a dictionary with all specs
    #  job_k = {"job_id": 1, "p_j":2.0, "r_j": 1, "d_j": 30}
    #where 
    #  job_i is the job's numer (or ID)
    #  p_k is the processing time for job k
    #  d_k is the deadline of job k
    
    list_jobs_id = [x['job_id'] for x in gen_list_jobs]
    list_schedule = perms(list_jobs_id)
    return list_schedule


def optimal_schedule(list_schedule, gen_list_jobs, t):
    
    # This function creates the schedules from the list_scheudule, then compute for each schedule, Lmax.
    # It returns the lowest Lmax and the associated schedule 
    Lmax_total = 100
    best_schedule = []
    first_possible_schedule = True
    
    for job_list in list_schedule:
        
        #from the list of job_id, we construe the schedule
        schedule, time = make_schedule(job_list, gen_list_jobs, t)
        
        #if the schedule is not feasible (because of the release date), schedule returns a string
        if type(schedule)==str:
            continue
        
        #otherwise we continue
        Lmax = L_max(schedule, gen_list_jobs)
        
        #if it's the first element, we initialize Lmax_total and best_schedule
        if first_possible_schedule:
            Lmax_total = Lmax
            best_schedule = schedule
            first_possible_schedule = False
        else:
            if Lmax<Lmax_total:
                Lmax_total = Lmax
                best_schedule = schedule
    return (best_schedule, Lmax_total, time)
    
#This function was found on a forum on Internet, the name of the author was not precised.
def perms(nums):
    if len(nums)==1:
        return [nums]
    else:
        all = []
        for line in perms(nums[:-1]):
            for i in range(len(nums)):
                all += [line[:i] + nums[-1:] + line[i:]]
        return all

def L_max(schedule, gen_list_jobs):
    
    #This function computes L_max for a given schedule
    L_max = 0
    
    for key in schedule:
        
        if schedule[key]==0:
            continue
        
        #for each job we take in jobs_list its processing time and its deadline
        for i in range(0, len(gen_list_jobs)):
            if gen_list_jobs[i]["job_id"] == schedule[key]:
                p_j = gen_list_jobs[i]["p_j"]
                d_j = gen_list_jobs[i]["d_j"]
        
        #Then we compute the completion time
        
        C_j = round(key + p_j,1)
        if C_j > d_j:
            L_max = max(L_max, round(C_j-d_j,1))
    return L_max 

def make_schedule(job_list, gen_list_jobs, t):
    #THE_SCHEDULE is what we return. The keys are times and values are what job is running at that time.
    #Example: THE_SCHEDULE = {0:1, 3.4:3, 5:0, 6:2}
    #This schedule runs job_1 from time t=0 to t=3.4, then job_3 from time t=3.4 to t=5, then it is idle from time t=5 to t=6 and then job_2 starts at time t=6 and finishes its processing time
    all_jobs = gen_list_jobs
    schedule = {}
    for i in job_list:
        for job in all_jobs:
            if i == job["job_id"]:
                if t<job["r_j"]:
                    schedule[t]=0
                    t = job["r_j"]
                schedule[t]=i
                t= round(t+job["p_j"],1)
    return (schedule, t)

