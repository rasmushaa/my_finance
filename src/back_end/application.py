


import time


class App():
    def __init__(self):
        self.running = True
        self.start_az = 1
        self.end_az = 360
        self.delta_az = 1
        self.start_po = 1
        self.end_po = 90
        self.delta_po = 1
        
        
    ############### PARAMETER SETTERS #################
    
    def set_running(self, state):
        self.running = state
        
    def set_start_az(self, value):
        if value <= self.end_az:
            self.start_az = value
        else:
            return 1
        
    def set_end_az(self, value):
        if value >= self.start_az:
            self.end_az = value
        else:
            return 1
        
    def set_delta_az(self, value):
        if value >= 0:
            self.delta_az = value
        else:
            return 1

    def set_start_po(self, value):
        if value <= self.end_po:
            self.start_po = value
        else:
            return 1
    
    def set_end_po(self, value):
        if value >= self.start_po:
            self.end_po = value
        else:
            return 1
        
    def set_delta_po(self, value):
        if value >= 0:
            self.delta_po = value
        else:
            return 1
        
        
        
    ################ METHODS ###################
    
    def load_model_file(self, path):
        
        try:
            pass
            
        except Exception as error:
            print(error)
            return 1

    
      
    def compute(self, update_signal=None):
        self.running = True
        for i in range(100):
            
            if not self.running:
                break
            
            time.sleep(0.1) 
            
            if update_signal != None:       
                update_signal.emit(i+1)