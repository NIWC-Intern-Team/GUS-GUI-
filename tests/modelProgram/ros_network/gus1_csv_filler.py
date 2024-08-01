# -> denotes python version used !/usr/bin/env python3
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.node import Node
import numpy as np

from std_msgs.msg import Header, Float64
from std_srvs.srv import Empty

import random
import time
import math
from numpy import long
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS = ['lat','lon','status','mode','name','ip_address','network_status','temp_sensor_1','temp_sensor_2','temp_sensor_3',
           'volt_5v_line_sensor','volt_killsig_line_sensor','volt_24v_line_sensor','volt_curr_24v_line_sensor','volt_curr_thr_line_sensor',
           'battery_status','lidar_sensor','video_feed','teensy_status','thruster_status', 'speed', 'average_temp', 'battery', 'heading']
NUMBER_OF_CSV_FILES = 6

class sub_to_csv(Node):
    """Generates random data for CSV files."""
    def __init__(self):
        super().__init__('gus1_subscribers')

        self.angle = 0 

        self.my_callback_group = ReentrantCallbackGroup()

        self.temp0_sub = self.create_subscription(Float64, "/gus1/phidget/temperature0", self.temp0_callback, qos_profile=1, callback_group=self.my_callback_group)
        self.amp0_sub = self.create_subscription(Float64, "/gus1/phidget/amperage0", self.amp0_callback, qos_profile=1, callback_group=self.my_callback_group)
        self.amp1_sub = self.create_subscription(Float64, "/gus1/phidget/amperage1", self.amp1_callback, qos_profile=1, callback_group=self.my_callback_group)
        self.volt0_sub = self.create_subscription(Float64, "/gus1/phidget/voltage0", self.volt0_callback, qos_profile=1, callback_group=self.my_callback_group)
        self.volt1_sub = self.create_subscription(Float64, "/gus1/phidget/voltage1", self.volt1_callback, qos_profile=1, callback_group=self.my_callback_group)
        self.volt2_sub = self.create_subscription(Float64, "/gus1/phidget/voltage2", self.volt2_callback, qos_profile=1, callback_group=self.my_callback_group)
    
    def temp0_callback(self, msg):
        self.gus1_update_data(msg.data, 'temp_sensor_1')

    def amp0_callback(self, msg):
        self.gus1_update_data(msg.data, 'volt_curr_24v_line_sensor')

    def amp1_callback(self, msg):
        self.gus1_update_data(msg.data, 'volt_curr_thr_line_sensor')

    def volt0_callback(self, msg):
        self.gus1_update_data(msg.data, 'volt_killsig_line_sensor')

    def volt1_callback(self, msg):
        self.gus1_update_data(msg.data, 'volt_24v_line_sensor')

    def volt2_callback(self, msg):
        self.gus1_update_data(msg.data, 'volt_5v_line_sensor')

    #updater by variable type

    def create_data(self):
        '''Creates data structure.'''
        #create and initialize multiple CSV files
        filename = os.path.join(BASE_DIR, '1_gus.csv')
        try:
            df = pd.read_csv(filename)
            print("File 1_gus.csv exists")
            
        except Exception as e:
            print(f"Error: {e}")
            df = pd.DataFrame(columns=HEADERS)
            df.loc[0] = 0  # Initialize with zeros
            df.to_csv(f'{filename}', index=False)            

    def gus1_update_data(self, msg_data, data_type):
        '''Fills csv files with dummy data.'''
        try:
            filename = os.path.join(BASE_DIR, '1_gus.csv')
            df = pd.read_csv(filename)

            for x in HEADERS:
                if x == data_type:
                    df[x] = msg_data

            df.to_csv(filename, index=False)
        except Exception as e:
            print(f"Error: {e}")


    def main(self, args=None):
        rclpy.init(args=args)
        # dd = sub_to_csv()
        self.create_data()
        rclpy.spin(self)
        self.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    dd = sub_to_csv()
    dd.main()