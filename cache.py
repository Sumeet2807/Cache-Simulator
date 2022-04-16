from parameters import *
from infra import *

class Cache():
    def __init__(self,
    all_files:Files,
    init_file_list=[]):

        self.capacity = CACHE_CAPACITY
        self.store = {}
        self.storage_left = CACHE_CAPACITY
        self.all_files = all_files
        self.__subclass_declarations__()
        for i in range(len(init_file_list)):
            if not self.add_file(init_file_list[i]):
                break
    
    def __subclass_declarations__(self):
        pass

    def file_present(self,file_index):
        if file_index in self.store:
            return True
        return False


    def add_file(self,file_index):
        if file_index not in self.store:
            if self.storage_left > self.all_files.size[file_index]:
                self.store[file_index] = self.all_files.size[file_index]
                self.storage_left -= self.all_files.size[file_index]
            else:
                return False
        return True


class LRU_File():
    def __init__(self,file_index,file_size):
        self.next = None
        self.prev = None
        self.id = file_index
        self.size = file_size
        self.hits = 0


class LRU_Cache(Cache):
    
    def __subclass_declarations__(self):
        self.lru_root = None
        self.lru_tail = None
        self.hit_counter = 0

    def file_present(self,file_index):
        if file_index in self.store:
            file = self.store[file_index]
            # self.hit_counter += 1
            if file.prev is not None and file.next is not None:
                file.prev.next = file.next
                file.next.prev = file.prev
                self.lru_tail.next = file
                file.prev = self.lru_tail   
                self.lru_tail = file
                self.lru_tail.next = None
            elif file.prev is None and file.next is not None:
                self.lru_root = file.next
                self.lru_root.prev = None
                self.lru_tail.next = file
                file.prev = self.lru_tail   
                self.lru_tail = file
                self.lru_tail.next = None
            file.hits += 1
            
            # print(file_index,'R',self.get_lru_list())
            return True
        return False


    def add_file(self,file_index):    
        if self.all_files.size[file_index] > CACHE_MAX_ALLOWED_FILE_SIZE or self.all_files.size[file_index] > CACHE_CAPACITY:
            return False  
        if file_index not in self.store:
            file = LRU_File(file_index,self.all_files.size[file_index]) 
            # if increment_counter:
            #     self.hit_counter += 1
            if self.storage_left > self.all_files.size[file_index]:

                if self.lru_root is None:
                    self.lru_root = file
                if self.lru_tail is None:
                    self.lru_tail = file
                else:
                    self.lru_tail.next = file
                    file.prev = self.lru_tail                    
                    self.lru_tail = file
                    self.lru_tail.next = None
                self.store[file.id] = file
                self.storage_left -= file.size
                file.hits += 1

            else:
                while(self.storage_left <= file.size):
                    if self.lru_root is None:
                        raise Exception('LRU Cache - Storage inconsistency')                       

                    file_to_discard = self.lru_root
                    self.lru_root = file_to_discard.next
                    if self.lru_root is None:
                        self.lru_tail = None
                    else:
                        self.lru_root.prev = None
                    del self.store[file_to_discard.id]
                    self.storage_left += file_to_discard.size
                self.add_file(file_index)

            # print(file_index,'W',self.get_lru_list(),file.size)  
        else:
            self.file_present(file_index)        
        
        return True
        

    def get_stored_file_list(self):
        file_list = []
        for key in self.store:
            file_list.append([self.store[key].id,self.store[key].hits])
        return file_list

    def get_lru_list(self):
        file_list = []
        node = self.lru_root
        while(node is not None):
            file_list.append(node.id)
            node = node.next
        return file_list



class MRU_Cache(Cache):
    
    def __subclass_declarations__(self):
        self.mru_root = None
        # self.lru_tail = None
        self.hit_counter = 0

    def file_present(self,file_index):
        if file_index in self.store:
            file = self.store[file_index]
            # self.hit_counter += 1

            if file.prev is not None:                
                file.prev.next = file.next
                if file.next is not None:
                    file.next.prev = file.prev

                file.next = self.mru_root
                self.mru_root.prev = file
                self.mru_root = file
                self.mru_root.prev = None
                
            file.hits += 1
            
            print(file_index,'R',self.get_mru_list())
            return True
        return False


    def add_file(self,file_index):    
        if self.all_files.size[file_index] > CACHE_MAX_ALLOWED_FILE_SIZE or self.all_files.size[file_index] > CACHE_CAPACITY:
            return False  
        if file_index not in self.store:
            file = LRU_File(file_index,self.all_files.size[file_index]) 
            # if increment_counter:
            #     self.hit_counter += 1
            if self.storage_left > self.all_files.size[file_index]:

                if self.mru_root is None:
                    self.mru_root = file
                else:
                    file.next = self.mru_root
                    self.mru_root.prev = file
                    self.mru_root = file
                    self.mru_root.prev = None
                self.store[file.id] = file
                self.storage_left -= file.size
                file.hits += 1

            else:
                while(self.storage_left <= file.size):
                    if self.mru_root is None:
                        raise Exception('LRU Cache - Storage inconsistency')                       

                    file_to_discard = self.mru_root
                    self.mru_root = file_to_discard.next
                    if self.mru_root is not None:
                        self.mru_root.prev = None
                    del self.store[file_to_discard.id]
                    self.storage_left += file_to_discard.size
                self.add_file(file_index)

            print(file_index,'W',self.get_mru_list(),file.size)  
        else:
            self.file_present(file_index)        
        
        return True



    def get_stored_file_list(self):
        file_list = []
        for key in self.store:
            file_list.append([self.store[key].id,self.store[key].hits])
        return file_list

    def get_mru_list(self):
        file_list = []
        node = self.mru_root
        while(node is not None):
            file_list.append(node.id)
            node = node.next
        return file_list