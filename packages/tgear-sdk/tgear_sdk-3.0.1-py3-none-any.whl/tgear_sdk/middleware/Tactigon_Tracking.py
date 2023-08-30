import multiprocessing
import logging
import math
import time
import matplotlib.pyplot as plt # type: ignore

class Tactigon_Tracking(multiprocessing.Process):

    ACC_AMP_CLAMP = 0.5
    ACC_TIME_CLAMP = 5
    DT = 0.02
    
    def __init__(self, tactigon, acc_pipe, tracking_pipe = False, debug = False):
    
        super(Tactigon_Tracking, self).__init__(target=self.loop_iterator, args=(tactigon, acc_pipe, tracking_pipe, debug))
 

    def loop_iterator(self,tactigon,acc_pipe, tracking_pipe, debug):
        
        print("Tactigon Tracking ", tactigon, " object created")
        self.tactigon = tactigon
        self.acc_pipe = acc_pipe
        self.tracking_pipe = tracking_pipe
        
        self.debug = debug
        
        self.acc_clamp_cnt = [0, 0, 0]
        self.acc_clamp = [0, 0, 0]
        self.acc_pre = [0, 0, 0]

        self.vel = [0, 0, 0]
        self.vel_clamp = [0, 0, 0]
        self.vel_pre = [0, 0, 0]
        self.vel_inv_flag = [False, False, False]
        
        if(self.debug):
           #### PLOT #####
           plt.ion()
           self.acc_a = [0] * 200
           self.vel_a = [0] * 200
           self.cnt = 0
           self.fig = plt.figure()
           self.fig.canvas.set_window_title(self.tactigon) # type: ignore
           #self.acc_p = self.fig.add_subplot(121)
           self.vel_p = self.fig.add_subplot(111)
           #### PLOT #####

        print("Tactigon Tracking recognition", self.tactigon, " process started")
 
        while(True):
            self.loop()
        
    def loop(self):
        """Tracking recognition loop routine"""

        self.acc_act = self.acc_pipe.recv()
            
        self.acc_clamping()

        self.vel_integration()  
        
        self.vel_inversion_check()
        
        self.vel_clamping() 
        
        if(self.debug):
            self.plot()
        
        self.acc_pre = self.acc_clamp
        self.vel_pre = self.vel_clamp

        if(self.tracking_pipe != False):
            self.tracking_pipe.send(self.vel_clamp)
    
    def plot(self):
        """plot data"""
        
        self.acc_a.append(self.acc_clamp[2])
        self.acc_a = self.acc_a[1:]
        self.vel_a.append(self.vel_clamp[2])
        self.vel_a = self.vel_a[1:]
        self.cnt = self.cnt +1
        if(self.cnt == 20 ):
            #self.acc_p.cla()
            self.vel_p.cla()
            #self.acc_p.plot(self.acc_a, 'r-' )
            self.vel_p.plot(self.vel_a, 'b-' )
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            self.cnt = 0
        
    def acc_clamping(self):
        """acceleration data clamping"""
        
        for i in range(0,3):      
            if( abs(self.acc_act[i]) < Tactigon_Tracking.ACC_AMP_CLAMP ):
                self.acc_clamp_cnt[i]= self.acc_clamp_cnt[i] +1
            else:
                self.acc_clamp_cnt[i] = 0
        
            if(self.acc_clamp_cnt[i] >  Tactigon_Tracking.ACC_TIME_CLAMP):
                self.acc_clamp[i] = 0
            else:
                self.acc_clamp[i] = self.acc_act[i]
                

    def vel_integration(self):
        """estimate velocity"""
        
        for i in range(0,3): 
            self.vel[i] = self.vel_pre[i] + ( ( ( self.acc_pre[i] + self.acc_clamp[i]) * Tactigon_Tracking.DT ) / 2 ) # type: ignore
    
    def vel_inversion_check(self):
        """detect velocity inversion """
        
        vel_clamp_pre = self.vel_clamp
            
        for i in range(0,3):          
            
            if((self.vel[i] * vel_clamp_pre[i]) < 0):
                self.vel_inv_flag[i]=True
            
            if( (self.acc_clamp_cnt[i] >  Tactigon_Tracking.ACC_TIME_CLAMP) ):
                self.vel_inv_flag[i]=False
                
    def vel_clamping(self):
        """actual velocity clamping """
        
        for i in range(0,3):          
            if(self.vel_inv_flag[i]):
                self.vel_clamp[i]=0
            elif(self.vel[i] == self.vel_pre[i]):
                self.vel_clamp[i]=0
            else:
                self.vel_clamp[i] = self.vel[i]
        
# Start point of the application
# if __name__ == "__main__":
#     from ..hal.Tactigon_BLE import BLE
#     from ..hal.Tactigon_Serial import Tactigon_Serial


#     BLE_A_ADDRESS = "BE:A5:7F:2E:68:52"
#     BLE_B_ADDRESS = "BE:A5:7F:2E:7B:54"
#     BLE_CHARACTERISTIC_UUID = "bea5760d-503d-4920-b000-101e7306b005"

#     # logging
#     multiprocessing.log_to_stderr()
#     logger = multiprocessing.get_logger()
#     logger.setLevel(logging.DEBUG)
    
#     # data pipe variables
#     rx_data_a_pipe, tx_data_a_pipe = multiprocessing.Pipe(duplex= False)
#     rx_data_b_pipe, tx_data_b_pipe = multiprocessing.Pipe(duplex= False)
#     rx_angle_a_pipe, tx_angle_a_pipe = multiprocessing.Pipe(duplex= False)
#     rx_angle_b_pipe, tx_angle_b_pipe = multiprocessing.Pipe(duplex= False)
#     rx_acc_a_pipe, tx_acc_a_pipe = multiprocessing.Pipe(duplex= False)
#     rx_acc_b_pipe, tx_acc_b_pipe = multiprocessing.Pipe(duplex= False)
    
#     rx_tracking_a_pipe, tx_tracking_a_pipe = multiprocessing.Pipe(duplex= False)
#     rx_tracking_b_pipe, tx_tracking_b_pipe = multiprocessing.Pipe(duplex= False)

#     # create serial process
#     pro_in_a = BLE("A", BLE_A_ADDRESS, BLE_CHARACTERISTIC_UUID, tx_data_a_pipe, tx_angle_a_pipe, tx_acc_a_pipe, debug = False)
#     #pro_in_b = Tactigon_BLE("B", BLE_B_ADDRESS, BLE_CHARACTERISTIC_UUID, tx_data_b_pipe, tx_angle_b_pipe, tx_acc_b_pipe, debug = False)
    
#     pro_g_a = Tactigon_Tracking('A', rx_acc_a_pipe, tx_tracking_a_pipe, debug = True)   

#     input("type to start proceses")
#     pro_g_a.start()
#     #pro_g_b.start()
#     pro_in_a.start()
#     #pro_in_b.start()
    
#     while(True):        
#         print(rx_tracking_a_pipe.recv())

#     input("type any key to close the program")
