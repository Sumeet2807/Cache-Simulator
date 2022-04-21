
from parameters import *
import heapq as h
import numpy as np

class Files:
    def __init__(self,ppa,ppm,pfa,pfm):
        self.popularity = pareto(ppa, ppm, TOTAL_NO_OF_FILES)
        self.popularity = self.popularity/np.sum(self.popularity)
        self.size = pareto(pfa, pfm, TOTAL_NO_OF_FILES)



class Simulation_Q():
    def __init__(self):
        self.q = []
    
    def push(self, event_tuple:tuple):
        h.heappush(self.q,event_tuple)

    def pop(self):
        return h.heappop(self.q)[1]
        


class Simulator_Env():
    def __init__(self, Files:Files, Cache, cache_init_files=[]):

        self.sim_q = Simulation_Q()
        self.files = Files
        self.cache = Cache
        self.fifo = []
        self.log = []
        self.req_count = 0
        self.queue_delays = []
    
    def get_total_times_for_reqs(self):
        return(np.array(self.log)[:,0])

    def print_logs(self):
        for data in self.log:    
            e = data[3]
            path = []
            while(e is not None):
                path.insert(0,e.name)
                e = e.parent
            print('file name - ' + str(data[1]))    
            print('file size - ' + str(data[2]))
            print('total time - ' + str(data[0]))
            print(path)
            print(' ')


def pareto(a,m,samples):
    return((np.random.pareto(a, samples) + 1) * m)