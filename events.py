import heapq as h
import numpy as np

POISSON_PROCESS_NEW_REQUESTS_LAMBDA = 1
PARETO_PROCESS_NEW_FILE_SIZE_A = 1
INSTITUTIONAL_BANDWIDTH = 100

class Simulation_Q():
    def __init__(self):
        self.q = []
    
    def push(self, event_tuple:tuple):
        h.heappush(self.q,event_tuple)

    def pop(self):
        return h.heappop(self.q)[1]

class Event:

    def __init__(self, sim_q: Simulation_Q, create_time: int):
        self.sim_q = sim_q
        self.create_time = create_time
        self.__enqueue__()

    def __enqueue__(self):
        pass


    def process(self):
        pass

class E_new_req(Event):
    def __enqueue__(self):
        self.size = np.random.pareto(PARETO_PROCESS_NEW_FILE_SIZE_A)        
        self.process_time = self.create_time + (self.size/INSTITUTIONAL_BANDWIDTH)
        self.sim_q.push([self.process_time,self])


class E_get_new_reqs(Event):

    def __enqueue__(self):
        self.process_time = self.create_time
        self.sim_q.push([self.process_time,self])

    def process(self):
        reqs_to_handle = np.random.poisson(POISSON_PROCESS_NEW_REQUESTS_LAMBDA)
        for i in reqs_to_handle:
            E_new_req(self.sim_q,self.create_time)

