import multiprocessing
import logging
import pandas as pd
import os
from os import path

# resource directory - need to be referenced to exe path when used with exe bundle
# if getattr(sys, "frozen", False):
#     CLIENT_PY_PATH = sys._MEIPASS
# else:
#     CLIENT_PY_PATH = path.join(path.dirname(__file__), "../")
#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "data_managment/utilities"))

CLIENT_PY_PATH = path.join(path.dirname(__file__), "../")

from ..data_management.utilities.Data_Preprocessor import Data_Preprocessor

class Tactigon_Recorder(multiprocessing.Process):
    """
    this class uses the data_pipe to receive data and save it as csv file
    """

    def __init__(
        self,
        tactigon,
        file_path,
        gesture_name,
        num_sample,
        sensor_pipe=False,
        angle_pipe=False,
        button_pipe=False,
        debug=False,
    ):

        super(Tactigon_Recorder, self).__init__(
            target=self.loop_iterator,
            args=(
                tactigon,
                file_path,
                gesture_name,
                num_sample,
                sensor_pipe,
                angle_pipe,
                button_pipe,
                debug,
            ),
        )
        self.ready_flag = multiprocessing.Value("b", False)

    def loop_iterator(
        self,
        tactigon,
        file_path,
        gesture_name,
        num_sample,
        sensor_pipe,
        angle_pipe,
        button_pipe,
        debug,
    ):
        if debug:
            print("Tactigon Storing ", tactigon, " object created")

        self.path = file_path
        self.tactigon = tactigon
        self.num_sam = num_sample
        self.sensor_pipe = sensor_pipe
        self.angle_pipe = angle_pipe
        self.button_pipe = button_pipe
        self.debug = debug
        self.gesture_name = gesture_name

        ## create an object of preporcessor class
        self.preprocessor = Data_Preprocessor()
        self.gesture_counter = 0

        if self.debug:
            print("Tactigon Storing", self.tactigon, " process started")

        while True:
            self.loop()

    def loop(self):
        """Stroring loop routine"""

        # create dataframe with columns
        col = []
        if self.sensor_pipe != False:
            col.extend(["accX", "accY", "accZ", "gyroX", "gyroY", "gyroZ"])
        if self.angle_pipe != False:
            col.extend(["roll", "pitch", "yaw"])
        if self.button_pipe != False:
            col.extend(["buttonstatus"])

        df = pd.DataFrame(columns=col)

        self.ready_flag.value = True # type: ignore

        for _ in range(0, self.num_sam):
            new_data = []
            if self.sensor_pipe != False:
                sensor_data = self.sensor_pipe.recv()
                new_data.extend(sensor_data)
                self.preprocessor.push_data(sensor_data)
            if self.angle_pipe != False:
                new_data.extend(self.angle_pipe.recv())
            if self.button_pipe != False:
                new_data.extend(self.button_pipe.recv())

            df.loc[len(df)] = new_data

        if (self.preprocessor.run()) is not False:
            self.gesture_counter = self.gesture_counter + 1
            print(
                "Recorded ", self.gesture_counter, " ", self.gesture_name, " gestures"
            )

        if self.debug:
            print(df)

        self.save_data(df)

    def is_ready(self):

        return self.ready_flag.value # type: ignore

    def save_data(self, df):
        """
        this function save the data as csv file
        :param df: dataframe
        :return: none
        """
        if not os.path.exists(self.path):
            df.to_csv(self.path)
        else:
            df.to_csv(self.path, mode="a", header=False)


# Start point of the application
if __name__ == "__main__":

    from ..utilities.Config_Manager import Config_Manager

    from ..hal.Tactigon_BLE import BLE as Tactigon_BLE

    # logging
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.DEBUG)

    # import json config
    hal_config = Config_Manager.from_file("hal.json")
    data_coll_config = Config_Manager.from_file("data_collection.json")

    num_sample = hal_config.get("NUM_SAMPLE")
    hand = data_coll_config.get("HAND")

    if hand == "Right":
        b_add = hal_config.get("BLE_RIGHT_ADDRESS")
    else:
        b_add = hal_config.get("BLE_LEFT_ADDRESS")

    num_sample = hal_config.get("NUM_SAMPLE")

    # pipes
    rx_sensor_pipe, tx_sensor_pipe = multiprocessing.Pipe(duplex=False)
    rx_angle_pipe, tx_angle_pipe = multiprocessing.Pipe(duplex=False)
    rx_button_pipe, tx_button_pipe = multiprocessing.Pipe(duplex=False)

    # create ble process
    if hand == "Right":
        pro_in = Tactigon_BLE(
            "RIGHT",
            b_add,
            sensor_pipe=tx_sensor_pipe,
            angle_pipe=tx_angle_pipe,
            button_pipe=tx_button_pipe,
        )
        pro_store = Tactigon_Recorder(
            "RIGHT",
            "test.csv",
            "test",
            num_sample,
            rx_sensor_pipe, # type: ignore
            rx_angle_pipe, # type: ignore
            rx_button_pipe, # type: ignore
            True,
        )
    else:
        pro_in = Tactigon_BLE(
            "LEFT",
            b_add,
            sensor_pipe=tx_sensor_pipe,
            angle_pipe=tx_angle_pipe,
            button_pipe=tx_button_pipe,
        )
        pro_store = Tactigon_Recorder(
            "LEFT",
            "test.csv",
            "test",
            num_sample,
            rx_sensor_pipe, # type: ignore
            rx_angle_pipe, # type: ignore
            rx_button_pipe, # type: ignore
            True,
        )

    input("type to start proceses")
    pro_store.start()
    pro_in.start()

    input("type any key to close the program")
    pro_in.terminate()
    pro_store.terminate()
