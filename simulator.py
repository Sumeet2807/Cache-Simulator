from parameters import *
from cache import *
from infra import *
from events import *
import numpy as np


# initialize simulator environment
# np.random.seed(11)
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

print(sim.req_count)
print(np.mean(sim.get_total_times_for_reqs()))
print(np.mean(sim.queue_delays))