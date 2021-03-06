from __future__ import print_function

__author__ = "Beat Kueng"

import numpy as np


class PX4ULog:
    """
    This class contains PX4-specific ULog things (field names, etc.)
    """

    def __init__(self, ulog_object):
        """
        @param ulog_object: ULog instance
        """
        self.ulog = ulog_object

    def get_mav_type(self):
        """ return the MAV type as string from initial parameters """

        mav_type = self.ulog.initial_parameters.get('MAV_TYPE', None)
        return {1: 'Fixed Wing',
                2: 'Multirotor',
                20: 'VTOL Tailsitter',
                21: 'VTOL Tiltrotor',
                22: 'VTOL Standard'}.get(mav_type, 'unknown type')

    def get_estimator(self):
        """return the configured estimator as string from initial parameters"""

        mav_type = self.ulog.initial_parameters.get('SYS_MC_EST_GROUP', None)
        return {0: 'INAV', 1: 'LPE', 2: 'EKF2'}.get(mav_type, 'unknown')


    def add_roll_pitch_yaw(self):
        """ convenience method to add the fields 'roll', 'pitch', 'yaw' to the
        loaded data using the quaternion fields (does not update field_data).

        Messages are: 'vehicle_attitude.q' and 'vehicle_attitude_setpoint.q_d' """

        self._add_roll_pitch_yaw_to_message('vehicle_attitude')
        self._add_roll_pitch_yaw_to_message('vehicle_attitude_setpoint', '_d')


    def _add_roll_pitch_yaw_to_message(self, message_name, field_name_suffix = ''):

        message_data_all = [ elem for elem in self.ulog.data_list if elem.name == message_name]
        for message_data in message_data_all:
            q=[message_data.data['q'+field_name_suffix+'['+str(i)+']'] for i in range(4)]
            roll=np.arctan2(2.0 * (q[0] * q[1] + q[2] * q[3]),
                    1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2]))
            pitch = np.arcsin(2.0 * (q[0] * q[2] - q[3] * q[1]))
            yaw = np.arctan2(2.0 * (q[0] * q[3] + q[1] * q[2]),
                    1.0 - 2.0 * (q[2] * q[2] + q[3] * q[3]))
            message_data.data['roll'+field_name_suffix] = roll
            message_data.data['pitch'+field_name_suffix] = pitch
            message_data.data['yaw'+field_name_suffix] = yaw

