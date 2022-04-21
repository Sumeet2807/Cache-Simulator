from parameters import *
from cache import *
from infra import *
from events import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

fig,axs = plt.subplots(2,2,figsize=(7,4))
axs = list(axs[0]) + list(axs[1])
ax_counter = 0

print('You may change the parameters in the file parameters.py per your need.\n\n')
print('This Simulation shows Response rates for various Cache types under similar situation.\n\n')

cache_types = [No_Cache,LFU_Cache,LRU_Cache,MRU_Cache]
for cache_type in cache_types:
    total_times = []
    queue_delays = []
    req_served = []
    for iteration in range(SIMULATOR_ITERATIONS):

        # initialize simulator environment
        files = Files(PARETO_PROCESS_FILE_POPULARITY_A,PARETO_PROCESS_FILE_POPULARITY_M,PARETO_PROCESS_NEW_FILE_SIZE_A,PARETO_PROCESS_NEW_FILE_SIZE_M,)
        cache = cache_type(files,capacity=CACHE_CAPACITY,max_file_size=CACHE_MAX_ALLOWED_FILE_SIZE)
        # cache = Cache(files)

        sim = Simulator_Env(files,cache)

        #initialize new req events to be processed at every second
        for i in range(TOTAL_TIME_TO_RUN):
            E_get_new_reqs(sim,i,requestrate=POISSON_PROCESS_NEW_REQUESTS_LAMBDA)


        #Main simulator loop
        while(len(sim.sim_q.q)):

            e = sim.sim_q.pop()
            e.process()    


        total_times.append(np.mean(sim.get_total_times_for_reqs()))
        queue_delays.append(np.mean(sim.queue_delays))
        req_served.append(sim.req_count)

    print("Cache system - " + cache.__class__.__name__)
    print('Average number of req served during simulations - ' + str(np.mean(req_served)))
    print('Average Response rate for the requests - ' + str(np.mean(total_times)))
    print('Average Queue delay in the process - ' + str(np.mean(queue_delays)))
    p = sns.histplot(data=total_times,kde=True,ax=axs[ax_counter])
    ax_counter += 1
    p.set_xlabel('time(sec)')
    p.set_title(cache.__class__.__name__)\

    print('\n')
    print('*********************XXXXXXXXXXXXXX*********************')
    print('\n')

print("Close the current graph to see next simulation\n\n")    
plt.show()


print("This Simulation shows dependancy of response times with cache sizes\n\n")

#Cache size experiments for LFU
SIMULATOR_ITERATIONS = 10
cache_types = [LFU_Cache]
cache_sizes = [10,50,100,150,200,250,300,350,400,450,500,700,1000]
cache_times = []
for cache_capacity in cache_sizes:
    for cache_type in cache_types:
        total_times = []
        queue_delays = []
        req_served = []
        for iteration in range(SIMULATOR_ITERATIONS):

            # initialize simulator environment
            files = Files(PARETO_PROCESS_FILE_POPULARITY_A,PARETO_PROCESS_FILE_POPULARITY_M,PARETO_PROCESS_NEW_FILE_SIZE_A,PARETO_PROCESS_NEW_FILE_SIZE_M,)
            cache = cache_type(files,capacity=cache_capacity,max_file_size=CACHE_MAX_ALLOWED_FILE_SIZE)
            # cache = Cache(files)

            sim = Simulator_Env(files,cache)

            #initialize new req events to be processed at every second
            for i in range(TOTAL_TIME_TO_RUN):
                E_get_new_reqs(sim,i,requestrate=POISSON_PROCESS_NEW_REQUESTS_LAMBDA)


            #Main simulator loop
            while(len(sim.sim_q.q)):

                e = sim.sim_q.pop()
                e.process()    


            total_times.append(np.mean(sim.get_total_times_for_reqs()))
            queue_delays.append(np.mean(sim.queue_delays))
            req_served.append(sim.req_count)

        print("Cache capacity - " + str(cache.capacity))
        print('Average number of req served during simulations - ' + str(np.mean(req_served)))
        print('Average Response rate for the requests - ' + str(np.mean(total_times)))
        print('Average Queue delay in the process - ' + str(np.mean(queue_delays)))
        cache_times.append(np.mean(total_times))
        # p = sns.histplot(data=total_times,kde=True)
        # p.set_xlabel('time(sec)')
        # p.set_title(cache.__class__.__name__)
        # p.set_xlim(0,10)

        # plt.show()
        print('\n')
        print('*********************XXXXXXXXXXXXXX*********************')
        print('\n')

p = sns.lineplot(cache_sizes,cache_times)
p.set_xlabel('Cache Size')
p.set_ylabel('Response Rate')
p.set_title(cache.__class__.__name__)
print("Close the current graph to see next simulation\n\n")    

plt.show()

print("This Simulation shows dependancy of response times on Request Rate")


#Cache size experiments for LFU
SIMULATOR_ITERATIONS = 10
cache_types = [LFU_Cache]
lmdas = [10,20,50,75,100]
cache_times = []
for lmda in lmdas:
    for cache_type in cache_types:
        total_times = []
        queue_delays = []
        req_served = []
        for iteration in range(SIMULATOR_ITERATIONS):

            # initialize simulator environment
            files = Files(PARETO_PROCESS_FILE_POPULARITY_A,PARETO_PROCESS_FILE_POPULARITY_M,PARETO_PROCESS_NEW_FILE_SIZE_A,PARETO_PROCESS_NEW_FILE_SIZE_M,)
            cache = cache_type(files,capacity=CACHE_CAPACITY,max_file_size=CACHE_MAX_ALLOWED_FILE_SIZE)
            # cache = Cache(files)

            sim = Simulator_Env(files,cache)

            #initialize new req events to be processed at every second
            for i in range(TOTAL_TIME_TO_RUN):
                E_get_new_reqs(sim,i,requestrate=lmda)


            #Main simulator loop
            while(len(sim.sim_q.q)):

                e = sim.sim_q.pop()
                e.process()    


            total_times.append(np.mean(sim.get_total_times_for_reqs()))
            queue_delays.append(np.mean(sim.queue_delays))
            req_served.append(sim.req_count)

        print("Request rate - " + str(lmda))
        print('Average number of req served during simulations - ' + str(np.mean(req_served)))
        print('Average Response rate for the requests - ' + str(np.mean(total_times)))
        print('Average Queue delay in the process - ' + str(np.mean(queue_delays)))
        cache_times.append(np.mean(total_times))
        # p = sns.histplot(data=total_times,kde=True)
        # p.set_xlabel('time(sec)')
        # p.set_title(cache.__class__.__name__)
        # p.set_xlim(0,10)

        # plt.show()
        print('\n')
        print('*********************XXXXXXXXXXXXXX*********************')
        print('\n')

p = sns.lineplot(lmdas,cache_times)
p.set_xlabel('Request Rate')
p.set_ylabel('Response Rate')
p.set_title(cache.__class__.__name__)
plt.show()

print("Close the current graph to see next simulation\n\n")    


print("This simulation shows dependancy of response times with Pareto distributions for file size parameter alpha")


#Cache size experiments for LFU
SIMULATOR_ITERATIONS = 10
cache_types = [LFU_Cache]
Pareto_File_Size_A = [10,20,50,75,100]
cache_times = []
for alpha in Pareto_File_Size_A:
    for cache_type in cache_types:
        total_times = []
        queue_delays = []
        req_served = []
        for iteration in range(SIMULATOR_ITERATIONS):

            # initialize simulator environment
            files = Files(PARETO_PROCESS_FILE_POPULARITY_A,PARETO_PROCESS_FILE_POPULARITY_M,alpha,PARETO_PROCESS_NEW_FILE_SIZE_M,)
            cache = cache_type(files,capacity=CACHE_CAPACITY,max_file_size=CACHE_MAX_ALLOWED_FILE_SIZE)
            # cache = Cache(files)

            sim = Simulator_Env(files,cache)

            #initialize new req events to be processed at every second
            for i in range(TOTAL_TIME_TO_RUN):
                E_get_new_reqs(sim,i,requestrate=POISSON_PROCESS_NEW_REQUESTS_LAMBDA)


            #Main simulator loop
            while(len(sim.sim_q.q)):

                e = sim.sim_q.pop()
                e.process()    


            total_times.append(np.mean(sim.get_total_times_for_reqs()))
            queue_delays.append(np.mean(sim.queue_delays))
            req_served.append(sim.req_count)

        print("File Size Pareto alpha - " + str(alpha))
        print('Average number of req served during simulations - ' + str(np.mean(req_served)))
        print('Average Response rate for the requests - ' + str(np.mean(total_times)))
        print('Average Queue delay in the process - ' + str(np.mean(queue_delays)))
        cache_times.append(np.mean(total_times))
        # p = sns.histplot(data=total_times,kde=True)
        # p.set_xlabel('time(sec)')
        # p.set_title(cache.__class__.__name__)
        # p.set_xlim(0,10)

        # plt.show()
        print('\n')
        print('*********************XXXXXXXXXXXXXX*********************')
        print('\n')

p = sns.lineplot(lmdas,cache_times)
p.set_xlabel('Request Rate')
p.set_ylabel('Pareto Alphas')
p.set_title(cache.__class__.__name__)
plt.show()

print("Close the current graph to continue\n\n")    

a = input('Press a key to exit')
if a:
    exit(0)
