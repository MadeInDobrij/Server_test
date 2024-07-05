import random
import math


class Event:
    def __init__(self, time, ev, Job1, Job2, Syst, S, n, Q):
        self.time = time
        self.ev = ev
        self.Job1 = Job1
        self.Job2 = Job2
        self.Syst = Syst
        self.S = S
        self.n = n
        self.Q = Q

class Simulator:
    def __init__(self, end_time):
        self.end_time = end_time
        self.system_time = 0
        self.event_list = []
        self.server_busy = True
        self.server_proc_time = 0
        self.Job1 = 0  
        self.Job2 = 0  
        self.Syst = 2.3  
        self.S = 1  
        self.n = 0  
        self.Q = []  
        self.total_jobs = 0
        self.total_queue_time = 0
        self.server_idle_time = 0
        self.max_n = 0  
        self.server_busy_time = 0  

    def schedule_event(self, time, ev, Job1, Job2, Syst, S, n, Q):
        event = Event(time, ev, Job1, Job2, Syst, S, n, Q)
        self.event_list.append(event)
        self.event_list.sort(key=lambda x: x.time)

    def init(self):
        
        self.schedule_event(0, "start", 0, 0, 0, 0, 0, "-")
        
        print("Time\tEvent\tJob1\tJob2\tSyst\tS\tn\tQ")

        while self.event_list and self.system_time < self.end_time:
            event = self.event_list.pop(0)
            self.system_time = event.time
            self.distribution_event(event)
            print(f"{event.time}\t{event.ev}\t{self.Job1}\t{self.Job2}\t{self.Syst}\t{self.S}\t{self.n}\t{','.join(event.Q)}")
            
            self.max_n = max(self.max_n, self.n)

        total_sim_time = self.end_time - 0
        load_factor = self.server_busy_time / total_sim_time
        
        print("\nMax amount of jobs in the queue:", self.max_n)
        print("Load Factor:", load_factor)

    def distribution_event(self, event):
        if event.ev == "start":
            self.Job1 = custom_func1(job_type="Job1")  
            self.Job2 = custom_func2(job_type="Job2")  
            self.schedule_event(self.Job1, "Job1 arrival", self.Job1, self.Job2, self.Syst, self.S, self.n, self.Q)
            self.schedule_event(self.Job2, "Job2 arrival", self.Job1, self.Job2, self.Syst, self.S, self.n, self.Q)
            self.schedule_event(self.Syst, "Unoccupied", self.Job1, self.Job2, self.Syst, self.S, self.n, self.Q)
            

        elif event.ev == "Job1 arrival":
            self.Job1 = self.system_time + custom_func1(job_type="Job1")  
            self.schedule_event(self.Job1, "Job1 arrival", self.Job1, self.Job2, self.Syst, self.S, self.n, self.Q)  

            self.Q.append("Job1")
            self.n += 1
            self.S = 1
            if not self.server_busy:
                self.server_busy = True               
                self.server_proc_time = custom_func3(job_type="Job") 
                event.ev = "Unoccupied"

        elif event.ev == "Job2 arrival":
            self.Job2 = self.system_time + custom_func2(job_type="Job2")  
            self.schedule_event(self.Job2, "Job2 arrival", self.Job1, self.Job2, self.Syst, self.S, self.n, self.Q)  

            self.Q.append("Job2")
            self.n += 1
            self.S = 1
            if not self.server_busy:
                self.server_busy = True              
                self.server_proc_time = custom_func4(job_type="Job")
                event.ev = "Unoccupied"

        elif event.ev == "Unoccupied":
            if not self.Q:
                self.server_busy = False
                self.server_idle_time += self.system_time - self.Syst
            else:
                job_name = self.Q.pop(0)
                self.n -= 1
                self.S = 0
                if job_name == "Job1":
                    self.Syst = self.system_time + custom_func3(job_type="Job")
                elif job_name == "Job2":
                    self.Syst = self.system_time + custom_func4(job_type="Job")
                self.total_queue_time += self.system_time - (self.Syst - self.server_proc_time) 
                self.total_jobs += 1              
                self.schedule_event(self.Syst, "Unoccupied", event.Job1, event.Job2, self.Syst, self.S, self.n, self.Q)
                self.server_busy_time += self.Syst - event.time


def custom_func1(job_type=None):   
    u = random.random()
    return round(-math.log(1 - u) / 1.4, 2)
def custom_func2(job_type=None):
    product = 1
    for _ in range(3):
        product *= random.random()
    return -math.log(product) / 7
def custom_func3(job_type=None):
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return 1 + 0.2 * z0
def custom_func4(job_type=None):
    product = 1
    for _ in range(2):
        product *= random.random()
    return -math.log(product) / 1


simulator = Simulator(500)
simulator.init()