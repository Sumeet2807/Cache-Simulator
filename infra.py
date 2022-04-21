import heapq as h
import numpy as np

class Files:
    def __init__(self,ppa,ppm,pfa,pfm,total_files=10000):
        self.popularity = pareto(ppa, ppm, total_files)
        self.popularity = self.popularity/np.sum(self.popularity)
        self.size = pareto(pfa, pfm, total_files)



class Simulation_Q():
    def __init__(self):
        self.q = []
    
    def push(self, event_tuple:tuple):
        h.heappush(self.q,event_tuple)

    def pop(self):
        return h.heappop(self.q)[1]
        

POISSON_PROCESS_NEW_REQUESTS_LAMBDA = 100
PARETO_PROCESS_NEW_FILE_SIZE_A = 2
PARETO_PROCESS_NEW_FILE_SIZE_M = 1
PARETO_PROCESS_FILE_POPULARITY_A = 1
PARETO_PROCESS_FILE_POPULARITY_M = 1
LOGNORMAL_PROCESS_ARRIVE_AT_QUEUE_MEAN = 0.5
LOGNORMAL_PROCESS_ARRIVE_AT_QUEUE_SIGMA = 0.4

TOTAL_NO_OF_FILES = 10000
INSTITUTIONAL_BANDWIDTH = 1000
ACCESS_LINK_BANDWIDTH = 25
TOTAL_TIME_TO_RUN = 50
CACHE_CAPACITY = 500
CACHE_MAX_ALLOWED_FILE_SIZE = 200
SIMULATOR_ITERATIONS = 15

class Simulator_Env():
    def __init__(self,   
                 cache_type,
                 cache_capacity=100,
                 cache_max_allowed_file_size=10,
                 cache_init_files=[],
                 total_files = 10000, 
                 poisson_req_rate=100,
                 pareto_popularity_a = 1,
                 pareto_popularity_m = 1,
                 pareto_size_a=1,
                 pareto_size_m=1,                 
                 lognormal_mean=0.4,
                 lognormal_sigma=0.5,
                 access_link=15,
                 institutional_bandwidth=1000):

        self.files = Files(pareto_popularity_a,
                      pareto_popularity_m,
                      pareto_size_a,
                      pareto_size_m,
                      total_files)

        self.sim_q = Simulation_Q()
        self.cache = cache_type(self.files,cache_init_files,cache_capacity,cache_max_allowed_file_size)
        self.fifo = []
        self.log = []
        self.req_count = 0
        self.queue_delays = []
        self.fifo_size = []
        self.institutional_bandwidth = institutional_bandwidth
        self.access_link_bandwidth = access_link
        self.lognormal_mean = lognormal_mean
        self.lognormal_sigma = lognormal_sigma
        self.req_rate = poisson_req_rate

    
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