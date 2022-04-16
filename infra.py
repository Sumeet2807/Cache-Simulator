
from parameters import *
import heapq as h
import numpy as np

class Files:
    def __init__(self):
        self.popularity = np.random.pareto(PARETO_PROCESS_FILE_POPULARITY_A,size=TOTAL_NO_OF_FILES)
        self.popularity = self.popularity/np.sum(self.popularity)
        self.size = np.random.pareto(PARETO_PROCESS_NEW_FILE_SIZE_A,size=TOTAL_NO_OF_FILES)



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


class Event:

    def __init__(self, sim: Simulator_Env, create_time: int, parent:object=None):
        self.sim = sim
        self.create_time = create_time
        self.process_time = create_time
        self.parent = parent
        self.name = 'Event'
        self.__enqueue__()

    def get_super_parent(self):
        node = self
        while(node.parent is not None):
            node = node.parent
        return node

    def __lt__(self,any):
        return True

    def __gt__(self,any):
        return True

    def __enqueue__(self):
        pass


    def process(self):
        pass