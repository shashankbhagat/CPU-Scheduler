# This class is parent class or generalised class for all scheduling algorithm classes.
# This class defines the common parameters of the 3 scheduling algorithm.
class PCB:
    ID=0;
    arrivalTime=0;
    burstTime=0;
    completionTime=0;

    def __init__(self, *args, **kwargs):
        self.ID=0;
        self.arrivalTime=0;
        self.burstTime=0;
        self.completionTime=0;
        return super().__init__(*args, **kwargs)

    
