from parameters import *
from cache import *
from infra import *
from events import *
import numpy as np

POISSON_PROCESS_NEW_REQUESTS_LAMBDA = 100
PARETO_PROCESS_NEW_FILE_SIZE_A = 2
PARETO_PROCESS_FILE_POPULARITY_A = 1
LOGNORMAL_PROCESS_ARRIVE_AT_QUEUE_MEAN = 0.5
LOGNORMAL_PROCESS_ARRIVE_AT_QUEUE_SIGMA = 0.4

TOTAL_NO_OF_FILES = 10000
INSTITUTIONAL_BANDWIDTH = 1000
ACCESS_LINK_BANDWIDTH = 15
TOTAL_TIME_TO_RUN = 10
CACHE_CAPACITY = 10
CACHE_MAX_ALLOWED_FILE_SIZE = 10


# initialize simulator environment
np.random.seed(11)
files = Files()
cache = LRU_Cache(files)
# cache = Cache(files)

sim = Simulator_Env(files,cache)

#initialize new req events to be processed at every second
for i in range(TOTAL_TIME_TO_RUN):
    E_get_new_reqs(sim,i)


#Main simulator loop
while(len(sim.sim_q.q)):

    e = sim.sim_q.pop()
    e.process()
    
    

print(len(sim.log) == sim.req_count)


np.mean(sim.get_total_times_for_reqs())
