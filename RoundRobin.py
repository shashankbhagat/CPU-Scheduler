import PCB as pcb;

# This class is designed for Round Robin module.
class RoundRobin(pcb.PCB):
    timeSlice=0;
    def __init__(self, *args, **kwargs):
        self.timeSlice=0;
        super().__init__(*args, **kwargs)

