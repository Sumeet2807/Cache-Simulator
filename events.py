import heapq as h
import numpy as np
from infra import *


class Event:

    def __init__(self, sim: Simulator_Env, create_time: int, parent:object=None,requestrate=100):
        self.sim = sim
        self.create_time = create_time
        self.process_time = create_time
        self.parent = parent
        self.requestrate = requestrate
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


class E_get_new_reqs(Event):

    def __enqueue__(self):
        self.name = 'Get New Requests'
        self.sim.sim_q.push([self.process_time,self])

    def process(self):
        reqs_to_handle = np.random.poisson(self.requestrate)
        for i in range(int(reqs_to_handle)):
            E_new_req(self.sim, self.process_time)


class E_new_req(Event):
    def __enqueue__(self):
        self.name = 'New Request'
        self.sim.req_count += 1
        self.file_index = np.argmax(np.random.multinomial(1,self.sim.files.popularity))
        self.file_size = self.sim.files.size[self.file_index]        
        # self.process_time = self.create_time + (self.file_size/INSTITUTIONAL_BANDWIDTH)
        self.sim.sim_q.push([self.process_time,self])

    def process(self):
        if self.sim.cache.file_present(self.file_index):
            E_file_recieved(self.sim,self.process_time,self)
        else:
            E_arrive_at_queue(self.sim,self.process_time,self)


class E_file_recieved(Event):
    def __enqueue__(self):
        self.name = 'File recieved'
        initial_req = self.get_super_parent()
        file_size = self.sim.files.size[initial_req.file_index]
        self.process_time = self.create_time + (file_size/ self.sim.institutional_bandwidth)
        self.sim.sim_q.push([self.process_time,self])

    def process(self):
        initial_req = self.get_super_parent()
        log_data = [self.process_time - initial_req.create_time, initial_req.file_index, initial_req.file_size,self]
        self.sim.log.append(log_data)


class E_arrive_at_queue(Event):
    def __enqueue__(self):
        self.name = 'Arrive at queue'
        self.process_time = self.create_time + np.random.lognormal(self.sim.lognormal_mean,
                                                                    self.sim.lognormal_sigma)
        
        self.sim.sim_q.push([self.process_time,self])

    def process(self):
        self.sim.fifo_size.append(len(self.sim.fifo))
        self.sim.fifo.append(self)
        if len(self.sim.fifo) < 2:
            E_depart_from_queue(self.sim,self.process_time,self)


class E_depart_from_queue(Event):
    def __enqueue__(self):
        self.name = 'Depart from queue'
        initial_req = self.get_super_parent()
        self.process_time = self.create_time + (initial_req.file_size/self.sim.access_link_bandwidth)
        self.sim.sim_q.push([self.process_time,self])
        self.queue_delay = 0
        if isinstance(self.parent, E_arrive_at_queue):
            self.queue_delay = self.create_time - self.parent.process_time
            # print(self.queue_delay)
        self.sim.queue_delays.append(self.queue_delay)


    def process(self):
        initial_req = self.get_super_parent()
        self.sim.cache.add_file(initial_req.file_index)
        E_file_recieved(self.sim,self.process_time,self)
        self.sim.fifo.pop(0)
        if len(self.sim.fifo):
            E_depart_from_queue(self.sim,self.process_time,self.sim.fifo[0])
