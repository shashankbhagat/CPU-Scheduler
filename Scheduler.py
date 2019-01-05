import fileinput;
import FCFS as fcfs;
import SJF as sjf;
import RoundRobin as RR;
import sys;

class Scheduler:
    ch=0;
    inputVal=[];
    CPU_clock=0;
    process_clock=0;
    CPU_status=False;
    processQueue=[];
    tempSJFQueue=[];
    tempRRQueue=[];
    finalQueue=[];
    quantum=0;
    newProcess=False;
    preemptProcess=False;
    printed=False;
    fileName="";
    activateVerbose=False;
    
    #Constructor defined for intialising variables and input file name
    #Intiatiation of Scheduler also done. 
    def __init__(self,args):
        self.CPU_clock=0;
        self.process_clock=0;
        self.CPU_status=False;
        self.fileName=args[len(args)-1];
        self.inputVal=self.inputFile();
        self.initiateScheduling(args);
        return super().__init__()
    
    #This method would read the input file into a list for further processing.
    def inputFile(self):
        try:
            inputTemp=[];
            with open(self.fileName) as f:
                inputTemp=f.read().splitlines();
                            
            return inputTemp;
        except:
            print("File not found!!")
            sys.exit()

    #This method would initiate the scheduler. 
    #The scheduler would then call the required scheduling algorithm depending on the arguments passed.
    def initiateScheduling(self,args):
        for i in range(1,len(args)-1):
            if(args[i]=="-v"):
                self.activateVerbose=True;
            elif(args[i]=="-F"):
                self.executeFCFS();
            elif(args[i]=="-S"):
                self.executeSJF();
            elif("-R" in args[i]):
                self.executeRR(args[i]);
            else:
                print("Incorrect input parameters!!")
                sys.exit();                
        return;

    #intiate execution of FIFO algorithm
    def executeFCFS(self):
        print("FIFO:");
        # Following loop would create a list of FCFS objects. The objects would containd ID, Arrival Time and Burst time.
        # The FCFS objects are then stored in a list.
        for value in range(0,len(self.inputVal)):
            str=self.inputVal[value].split(",")
            obj=fcfs.FCFS();
            obj.ID=str[0];
            obj.arrivalTime=str[1];
            obj.burstTime=str[2];
            self.processQueue.append(obj);
            
        # Following loop would call the scheduling method per CPU clock cycle.
        while(len(self.processQueue)>0):
            self.scheduleFCFS();
            self.CPU_clock+=1;

        # Activate verbose flag would decide to display the output with or without the verbose. 
        # The loop woould print the process ID and final completion time.
        if(self.activateVerbose==False):
            for value in range(0,len(self.finalQueue)):
                print(self.finalQueue[value].ID,"\t",self.finalQueue[value].completionTime);

    # Following method would calculate the final completion time and also create the verbose depending on the flag
    def scheduleFCFS(self):
        # Verifies whether the CPU is busy or not
        if(self.CPU_status==True):
            # If the process is done with the burst time, the completion time is calculated and that process is popped from the list. 
            if(self.process_clock+1==int(self.processQueue[0].burstTime)):
                self.CPU_status=False;
                if(self.activateVerbose==True):
                    print("At time: ",self.CPU_clock," job ",self.processQueue[0].ID," READY->TERMINATED")                
                self.processQueue[0].completionTime=self.CPU_clock;                
                self.finalQueue.append(self.processQueue[0]);
                self.processQueue.pop(0);
            # maintain a counter of each process individually.
            self.process_clock+=1;

        #following statement verifies and alarms when the next process is available.
        if(len(self.processQueue)>0 and self.activateVerbose==True):
            for value in range(0,len(self.processQueue)):
                if(self.CPU_clock==int(self.processQueue[value].arrivalTime)):
                    print("At time: ",self.CPU_clock," job ",self.processQueue[value].ID," READY")

        #Following statement would notify of the process that is running at a specific CPU clock cycle.
        if(self.CPU_status==False and len(self.processQueue)>0):
            self.process_clock=0;
            if(self.CPU_clock>=int(self.processQueue[0].arrivalTime)):
                self.CPU_status=True;
                if(self.activateVerbose==True):
                    print("At time: ",self.CPU_clock," job ",self.processQueue[0].ID," READY->RUNNING")
        return

    #intiate execution of SJF algorithm
    def executeSJF(self):
        print("SJF-Preemptive:");
        # Following loop would create a list of SJF objects. The objects would containd ID, Arrival Time and Burst time.
        # The SJF objects are then stored in a list.
        for value in range(0,len(self.inputVal)):
            str=self.inputVal[value].split(",")
            obj=sjf.SJF();
            obj.ID=str[0];
            obj.arrivalTime=str[1];
            obj.burstTime=str[2];
            self.processQueue.append(obj);

        # Following loop would call the scheduling method per CPU clock cycle.
        while(len(self.processQueue)>0 or len(self.tempSJFQueue)>0):
            if(len(self.tempSJFQueue)>0):
                #sort the queue depending on burst time
                self.tempSJFQueue.sort(key=lambda x: int(x.burstTime))
                
            self.scheduleSJF();
            self.CPU_clock+=1;                   
        
        #sort the final result list depeding on the process ID.
        self.finalQueue.sort(key=lambda x:int(x.ID))

        # Activate verbose flag would decide to display the output with or without the verbose. 
        # The loop woould print the process ID and final completion time.
        if(self.activateVerbose==False):
            for value in range(0,len(self.finalQueue)):
                print(self.finalQueue[value].ID,"\t",self.finalQueue[value].completionTime);
                    
    # Following method would calculate the final completion time and also create the verbose depending on the flag
    def scheduleSJF(self):
        #verify whether CPU is busy or not.
        if(len(self.tempSJFQueue)>0):
            self.CPU_status=True;
        else:
            self.CPU_status=False;

        # Keeps track of a process depending on the arrival time.        
        if(len(self.processQueue)>0):
            if(self.CPU_clock==int(self.processQueue[0].arrivalTime)):
                for value in range(0,len(self.processQueue)):
                    if(self.CPU_clock==int(self.processQueue[value].arrivalTime) and self.activateVerbose==True):
                        print("At time: ",self.CPU_clock," job ",self.processQueue[value].ID," READY")
                self.tempSJFQueue.append(self.processQueue[0]);                
                self.tempSJFQueue.sort(key=lambda x: int(x.burstTime))
                self.processQueue.pop(0)

                #  Displays the remaining processes in the queue and their status.
                if(len(self.tempSJFQueue)>0 and self.activateVerbose==True):
                    for val in range(1,len(self.tempSJFQueue)):
                        print("At time: ",self.CPU_clock," job ",self.tempSJFQueue[val].ID," RUNNING->READY")
                    if(self.CPU_clock>=int(self.tempSJFQueue[0].arrivalTime)):                
                        print("At time: ",self.CPU_clock," job ",self.tempSJFQueue[0].ID," READY->RUNNING")
        

        # Decrements the burst time of the process in execution.
        if(len(self.tempSJFQueue)>0):            
            if(self.CPU_clock>=int(self.tempSJFQueue[0].arrivalTime)):
                self.tempSJFQueue[0].burstTime=int(self.tempSJFQueue[0].burstTime)-1;
        
        # Once the burst time is done for a process, the process is terminated and popped from the queue.
        # Also the completion time is calculated.
            if(int(self.tempSJFQueue[0].burstTime)==0):
                if(self.activateVerbose==True):
                    print("At time: ",self.CPU_clock+1," job ",self.tempSJFQueue[0].ID," RUNNING->TERMINATED")
                self.tempSJFQueue[0].completionTime=self.CPU_clock+1;
                self.finalQueue.append(self.tempSJFQueue[0]);
                self.tempSJFQueue.pop(0);

                #  Displays the remaining processes in the queue and their status.
                if(len(self.tempSJFQueue)>0 and self.activateVerbose==True):                    
                    for val in range(1,len(self.tempSJFQueue)):
                        print("At time: ",self.CPU_clock+1," job ",self.tempSJFQueue[val].ID," RUNNING->READY")
                    if(self.CPU_clock>=int(self.tempSJFQueue[0].arrivalTime)):
                        print("At time: ",self.CPU_clock+1," job ",self.tempSJFQueue[0].ID," READY->RUNNING")
        return

    #intiate execution of Round Robin algorithm
    def executeRR(self,args):
        print("Round Robin:");
        #intialises the time quantum from the passed parameter.
        self.quantum=int(args[(args.find("R")+1):])

        # Following loop would create a list of RR objects. The objects would containd ID, Arrival Time and Burst time.
        # The RR objects are then stored in a list.
        for value in range(0,len(self.inputVal)):
            str=self.inputVal[value].split(",")
            obj=RR.RoundRobin();
            obj.ID=str[0];
            obj.arrivalTime=str[1];
            obj.burstTime=str[2];
            obj.timeSlice=self.quantum;
            self.processQueue.append(obj);
        
        # Following loop would call the scheduling method per CPU clock cycle.
        while(len(self.processQueue)>0 or len(self.tempRRQueue)>0):
            self.scheduleRR();
            self.CPU_clock+=1;

        # Sort the final result depending on process ID for display.
        self.finalQueue.sort(key=lambda x:int(x.ID))

        # Activate verbose flag would decide to display the output with or without the verbose. 
        # The loop woould print the process ID and final completion time.
        if(self.activateVerbose==False):
            for value in range(0,len(self.finalQueue)):
                print(self.finalQueue[value].ID,"\t",self.finalQueue[value].completionTime);

    # Following method would calculate the final completion time and also create the verbose depending on the flag
    def scheduleRR(self):
        # verify whether CPU is busy or not.
        if(len(self.tempRRQueue)>0):
            self.CPU_status=True;
        else:
            self.CPU_status=False;

        # If a new process arrives, then it is appended to the queue
        # Following code also displays the status of the queue
        if(len(self.processQueue)>0):
            if(self.CPU_clock==int(self.processQueue[0].arrivalTime)):                
                if(self.activateVerbose==True):
                    print("At time: ",self.CPU_clock," job ",self.processQueue[0].ID," READY")
                self.tempRRQueue.append(self.processQueue[0]);
                self.processQueue.pop(0);
                self.newProcess=True;
                if(len(self.tempRRQueue)):
                    self.printed=True;
                    if(self.activateVerbose==True):
                        for value in range(1,len(self.tempRRQueue)):
                            print("At time: ",self.CPU_clock," job ",self.tempRRQueue[value].ID," RUNNING->READY")
                        print("At time: ",self.CPU_clock," job ",self.tempRRQueue[0].ID," READY->RUNNING")
            else:
                self.printed=False;
                self.newProcess=False
        else:
            self.printed=False;
            self.newProcess=False

        # Following code checks whether the current process needs to be preempted.
        if(len(self.tempRRQueue)>0):
            if(self.tempRRQueue[0].timeSlice==0 or self.tempRRQueue[0].burstTime==0):                
                obj=self.tempRRQueue[0];                
                if(self.tempRRQueue[0].timeSlice==0):                    
                    self.preemptProcess=True;                    
                obj.timeSlice=self.quantum;
                
                # Following code swaps the position in the queue for the new incoming process with the preempted process.
                if(obj.burstTime>0):
                    self.tempRRQueue.append(obj);
                    if(self.newProcess==True and self.preemptProcess==True):                                                
                        objNew=self.tempRRQueue[len(self.tempRRQueue)-2]
                        self.tempRRQueue.pop(len(self.tempRRQueue)-2)
                        self.tempRRQueue.append(objNew)
                        self.newProcess=False
                        self.preemptProcess=False
                        
                        # Following code displays the current process running status and also status of other processes in the queue
                        if(len(self.tempRRQueue) and self.printed==False and self.activateVerbose==True):
                            for value in range(1,len(self.tempRRQueue)):
                                print("At time: ",self.CPU_clock," job ",self.tempRRQueue[value].ID," RUNNING->READY")
                            print("At time: ",self.CPU_clock," job ",self.tempRRQueue[0].ID," READY->RUNNING")

                # Following code displays the current process running status and also status of other processes in the queue
                if(len(self.tempRRQueue) and self.printed==False and self.preemptProcess==True and self.activateVerbose==True):
                        for value in range(1,len(self.tempRRQueue)):
                            print("At time ",self.CPU_clock," job ",self.tempRRQueue[value].ID," RUNNING->READY")
                        print("At time ",self.CPU_clock," job ",self.tempRRQueue[0].ID," READY->RUNNING")

                # Checks if the burst time is completed for a process and calculates the completion time accordingly and pops that process from the queue.
                if(obj.burstTime==0):
                    if(self.activateVerbose==True):
                        print("At time: ",self.CPU_clock," job ",self.tempRRQueue[0].ID," READY->TERMINATED")
                    self.tempRRQueue[0].completionTime=self.CPU_clock;
                    self.finalQueue.append(obj)

                self.tempRRQueue.pop(0);

            # Following code maintains the time slice and burst tie of the process by decrementing it by one at every instance.
            if(len(self.tempRRQueue)>0):
                if(self.tempRRQueue[0].timeSlice>0 and int(self.tempRRQueue[0].burstTime)>0):                    
                    self.tempRRQueue[0].timeSlice-=1;
                    self.tempRRQueue[0].burstTime=int(self.tempRRQueue[0].burstTime)-1;
        return
