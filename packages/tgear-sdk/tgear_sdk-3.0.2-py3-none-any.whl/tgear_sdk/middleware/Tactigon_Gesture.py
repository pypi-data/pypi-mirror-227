import multiprocessing
import logging
import time
from .utilities.Tactigon_RT_Computing import Tactigon_RT_Computing

from ..models import RealTimeConfig

class Tactigon_Gesture(multiprocessing.Process):

    TSAMPLE_MARGIN_SEC = 1

    def __init__(
        self,
        config: RealTimeConfig,
        tactigon,
        num_sample,
        sensor_pipe,
        gesture_pipe=False,
        gesture_prob_th=0.5,
        confidence_th=1,
        debug=False,
    ):

        super(Tactigon_Gesture, self).__init__(
            target=self.loop_iterator,
            args=(
                config,
                tactigon,
                num_sample,
                sensor_pipe,
                gesture_pipe,
                gesture_prob_th,
                confidence_th,
                debug,
            ),
        )

    def loop_iterator(
        self, config: RealTimeConfig, tactigon, num_sample, sensor_pipe, gesture_pipe, gesture_prob_th, confidence_th, debug
    ):

        if debug:
            print("Tactigon Gesture ", tactigon, " object created")
        self.rt_comp = Tactigon_RT_Computing(config, tactigon)

        self.tactigon = tactigon
        self.data_counter = 0
        self.num_sam = num_sample
        self.sensor_pipe = sensor_pipe
        self.gesture_pipe = gesture_pipe
        self.confidence_th = confidence_th
        self.gesture_prob_th = gesture_prob_th

        self.debug = debug
        self.timer = time.perf_counter()

        if debug:
            print("Tactigon Gesture recognition", self.tactigon, " process started")

        while True:
            self.loop()

    def loop(self):
        """Geture recognition loop routine"""

        self.timer = time.perf_counter()
        for _ in range(0, self.num_sam):
            self.rt_comp.push_data(self.sensor_pipe.recv())

        tsample = time.perf_counter() - self.timer

        if(tsample > (Tactigon_RT_Computing.NEW_DATA_INT_SEC + Tactigon_Gesture.TSAMPLE_MARGIN_SEC)):
            self.rt_comp.data_init()
            return
        else:
            # run ocatve
            gest, gest_prob, conf, disp = self.rt_comp.run()

            ## if gesture found add to the queue
            if (gest != "niente") and (conf >= self.confidence_th) and (gest_prob >= self.gesture_prob_th):
                if self.debug:
                    print(
                        "Tactigon  ",
                        self.tactigon,
                        " Gesture : ",
                        gest,
                        " Gesture Probability: ",
                        gest_prob,
                        " Confidence : ",
                        conf,
                        " Disp : ",
                        disp,
                    )

                if self.gesture_pipe != False:
                    self.gesture_pipe.send([gest, disp, gest_prob, conf])


# Start point of the application
# if __name__ == "__main__":

#     import sys
#     from os import path

#     CLIENT_PY_PATH = path.join(path.dirname(__file__), "../")

#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "utilities"))
#     from Config_Manager import Config_Manager

#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "hal"))
#     from Tactigon_BLE import Tactigon_BLE

#     # logging
#     multiprocessing.log_to_stderr()
#     logger = multiprocessing.get_logger()
#     logger.setLevel(logging.DEBUG)

#     # import json config
#     hal_config = Config_Manager.from_file("hal.json")

#     R_add = hal_config.get("BLE_RIGHT_ADDRESS")
#     L_add = hal_config.get("BLE_LEFT_ADDRESS")
#     R_en = hal_config.get("BLE_RIGHT_ENABLE")
#     L_en = hal_config.get("BLE_LEFT_ENABLE")
#     num_sample = hal_config.get("NUM_SAMPLE")

#     # data pipe variables
#     if R_en == "True":
#         rx_sensor_r_pipe, tx_sensor_r_pipe = multiprocessing.Pipe(duplex=False)

#     if L_en == "True":
#         rx_sensor_l_pipe, tx_sensor_l_pipe = multiprocessing.Pipe(duplex=False)

#     # create serial process
#     if R_en == "True":
#         pro_in_r = Tactigon_BLE("RIGHT", R_add, tx_sensor_r_pipe)
#         pro_g_r = Tactigon_Gesture(
#             "RIGHT", num_sample, rx_sensor_r_pipe, gesture_prob_th = 0.9, confidence_th=1, debug=True
#         )

#     if L_en == "True":
#         pro_in_l = Tactigon_BLE("LEFT", L_add, tx_sensor_l_pipe)
#         pro_g_l = Tactigon_Gesture(
#             "LEFT", num_sample, rx_sensor_l_pipe, gesture_prob_th = 0.9, confidence_th=1, debug=True
#         )

#     input("type to start proceses")
#     if R_en == "True":
#         pro_g_r.start()
#         pro_in_r.start()

#     if L_en == "True":
#         pro_g_l.start()
#         pro_in_l.start()

#     input("type any key to close the program")
#     if R_en == "True":
#         pro_in_r.terminate()
#         pro_g_r.terminate()

#     if L_en == "True":
#         pro_in_l.terminate()
#         pro_g_l.terminate()
