"""
printSim.py
====================================
This is a print queue simulation from 
https://runestone.academy/ns/books/published/pythonds/BasicDS/SimulationPrintingTasks.html

| Author: Seth McNeill
| Date: 2025 September 15
"""

from pythonds.basic import Queue  # basic queue class for simulating the print queue
import random  # used to simulate random processes 
from numpy import median

class Printer:
    """
    Printer class simulates a printer that prints at `ppm` pages per minute

    Parameters
    ----------
    ppm : int
      Print speed in pages per minute
    
    Attributes
    ----------
    pagerate : int
      print speed in pages per minute
    
    currentTask : Task
      current print job

    timeRemaining : int
      Amount of time left in the current print job
    """
    def __init__(self, ppm):
        self.pagerate = ppm
        self.currentTask = None
        self.timeRemaining = 0

    def tick(self):
        """
        Increments the time. If it has a current task, it decrements the `timeRemaining` for that task
        """
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        """
        Returns True if it has a current task assigned

        Returns
        -------
        bool
           True if currently has a task assigned
        """
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self,newtask):
        """
        Starts a new task and assigns `currentTask` and `timeRemaining`.

        Parameter
        ---------
        newtask : Task
          New task to assign the printer
        """
        self.currentTask = newtask
        self.timeRemaining = newtask.getPages() * 60/self.pagerate

class Task:
    """
    Class for a particular print task (print job)

    Parameter
    ---------
    time : int
      The current simulation time stamp
    
    Attributes
    ----------
    timestamp : int
      The simulation time when the task was initiated
    pages : int
      The number of pages this task needs to print (random 1-20)

    """
    def __init__(self,time):
        self.timestamp = time
        self.pages = random.randrange(1,21)

    def getStamp(self):
        """
        Return the timestamp (simulation time in seconds) when this task was created

        Returns
        -------
        int
          The simulation time when this task was created
        """
        return self.timestamp

    def getPages(self):
        """
        Return the number of pages in this task

        Returns
        -------
        int
          The number of pages this task needs to print
        """
        return self.pages

    def waitTime(self, currenttime):
        """
        Return the difference between `currenttime` and the task `timestamp` (start time)

        Parameter
        ---------
        currenttime : int
          The current simulation clock time (integer seconds)
        
        Returns
        -------
        int
          How long since the task was created
        """
        return currenttime - self.timestamp


def simulation(numSeconds, pagesPerMinute):
    """
    This runs a simulation and prints the results

    Parameters
    ----------
    numSeconds : int
      Number of seconds to run the simulation (3600 seconds in an hour)
    pagesPerMinute : int
      How fast the printer prints in pages per minute
    """
    labprinter = Printer(pagesPerMinute)
    printQueue = Queue()
    waitingtimes = []

    for currentSecond in range(numSeconds):

      if newPrintTask():
         task = Task(currentSecond)
         printQueue.enqueue(task)

      if (not labprinter.busy()) and (not printQueue.isEmpty()):
        """
        If printer is not busy and queue is not empty, start printer on new task
        """
        nexttask = printQueue.dequeue()  # get the next task from the queue
        waitingtimes.append( nexttask.waitTime(currentSecond))  # collect how long the task has been waiting in queue
        labprinter.startNext(nexttask)  # start the printer on the task

      labprinter.tick() # increment the simulation clock

    averageWait=sum(waitingtimes)/len(waitingtimes)
    maxWait = max(waitingtimes)
    medianWait = median(waitingtimes)
    minWait = min(waitingtimes)
    print(f'(min,avg,max,median) weight times ({minWait},\t{averageWait:.1f},\t{maxWait:.1f},\t{medianWait:.1f})')
    # print("Average Wait %6.2f secs %3d tasks remaining."%(averageWait,printQueue.size()))

def newPrintTask():
    """
    Returns whether a new print task should be created (1 in 180 chance)

    Returns
    -------
    bool
       True if new print task should be started
    """
    num = random.randrange(1,181)
    if num == 180:
        return True
    else:
        return False

"""
Run 10 simulations
"""
for jj in range(5,11):
    print('='*10 + f'Starting {jj}:')
    for ii in range(10):
        simulation(3600,jj)

# create graph of tasks in queue vs time
# create graph of pages in queue vs time
# amount of tasks completed
# largest print queue size
# How long documents were
# Color vs BW
# Paper size
# add amount of paper remaining
# add ink amount