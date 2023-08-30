#!/usr/bin/env python
# coding: utf-8

# # Base Programs
# Creates basic programs implementing BiologicProgram.

#
# ## CV scan
# Performs a CV scan.

        """
        Ewe ^
            |        E1
            |        /\
            |       /  \        Ef
            |      /    \      /
            |     /      \    /
            |    /        \  /
            |  Ei          \/
            |              E2
            |
            -----------------------> t
        """

# ### Params
# **E1:** Boundary potenital that first reaches (E1).
#
# **E2:** Boundary potential that reaches later.
#
# **Ef:** Potential *vs* reference.
#[Default: 0]
#
# **start:** Initial voltage (Ei).
# [ Defualt: 0 ]
#
# **step:** Voltage step.
# [Default: 0.001]
#
# **rate:** Scan rate in V/s.
# [Default: 0.05]
#
# **average:** Average over points.
# [Default: False]


import os
import math
import time
from datetime import datetime as dt
import asyncio
from collections import namedtuple

from . import BiologicProgram
from .program import CallBack
from .lib import ec_lib as ecl
from .lib import data_parser as dp
from .lib import technique_fields as tfs


class CallBack_Timeout:
    """
    A timeout callback.
    The callback must be started before it can be called.
    """

    def __init__(
        self,
        program,
        cb,
        timeout,
        repeat = True,
        args = [],
        kwargs = {},
        timeout_type = 'interval'
    ):
        """
        Creates a CallBack_Timeout.

        :param program: BiologicProgram the function is running in.
        :param cb: Callback function to run.
            Should accept the program as the first parameter.
        :param timeout: Timeout is seconds.
        :param repeat: Repeat the callback.
            If True, repeats indefinitely.
            If a number, repeats that many times.
            If False, only runs once.
            [Default: True]
        :param args: List of arguments to pass to the callback function.
            [Default: []]
        :param kwargs: Dictionary of keywrod arguments to pass to the callback function.
            [Default: {}]
        :param timeout_type: Type of timeout.
            Values are [ 'interval', 'between' ]
            interval: Time between callback starts
            between: Time between last finish and next start
            [Default: 'interval']
        """
        self.__program = program
        self.__cb = CallBack( cb, args, kwargs )
        self.timeout  = timeout
        self.timeout_type = timeout_type
        self.is_alive = False

        self.repeat = 1 if ( repeat is False ) else repeat

        self.__calls     = 0
        self.__last_call = None


    @property
    def callback( self ):
        """
        :returns: CallBack structure of the callback function.
        """
        return self.__cb


    @property
    def elapsed( self ):
        """
        :returns: time since last call.
        """
        return ( time.time() - self.__last_call )


    @property
    def calls( self ):
        """
        :returns: Number of calls.
        """
        return self.__calls


    @property
    def exhausted( self ):
        """
        :returns: If number of calls has reached number of repititions.
        """
        if self.repeat is True:
            return False

        return ( self.calls >= self.repeat )


    def is_due( self ):
        """
        :returns: If the function is due to be run or not.
        """
        return ( self.elapsed >= self.timeout )


    def run( self ):
        """
        Runs the callback function.
        """
        # function set up
        cb     = self.callback.function
        args   = self.callback.args
        kwargs = self.callback.kwargs

        # internal trackers
        self.__calls += 1
        if self.timeout_type is 'interval':
            self.__last_call = time.time()

        # callback
        cb( self.__program, *args, **kwargs )

        if self.timeout_type is 'between':
            self.__last_call = time.time()


    def start( self ):
        """
        Starts the callback.
        """
        self.is_alive = True
        self.__last_call = time.time()


    def cancel( self ):
        """
        Cancels the callback.
        """
        self.is_alive = False


    def call( self ):
        """
        Runs the callback is all conditions are met.
        """
        if (
            self.is_alive and
            not self.exhausted and
            self.is_due()
        ):
            self.run()


#--- helper function ---

def set_defaults( params, defaults, channels ):
    """
    Combines parameter and default dictionaries.

    :param params: Parameter or channel parameter dictionary.
    :param defaults: Default dictionary.
        Values used if key is not present in parameter dictionary.
    :param channels: List of channels or None if params is keyed by channel.
    :returns: Dictionary with defualt values set, if not set in parameters dictionary.
    """
    if channels is None:
        # parameters by channel
        for ch, ch_params in params.items():
            params[ ch ] = { **defaults, **ch_params }

    else:
         params = { **defaults, **params }

    return params


def map_params( key_map, params, by_channel = True, keep = False, inplace = False ):
    """
    Returns a dictionary with names mapped.

    :param key_map: Dictionary keyed by original keys with new keys as values.
    :param params: Dictionary of parameters.
    :param by_channel: Whether params is by channel, or only parameters.
        [Default: True]
    :param keep: True to keep original name, False to remove it.
        [Default: False]
    :param inplace: Transform original params dictionary, or create a new one.
        [Default: False]
    :returns: Dictionary with mapped keys.
    """
    def map_ch_params( ch_params ):
        """
        Maps channel parameters inplace.

        :param ch_params: Parameter dictionary.
        :returns: Modified parameter dictionary.
        """
        for o_key, n_key in key_map.items():
            ch_params[ n_key ] = ch_params[ o_key ]

        if not keep:
            # remove original keys
            for o_key in key_map:
                del ch_params[ o_key ]


    if not inplace:
        params = params.copy()

    if by_channel:
        for ch, ch_params in params.items():
            map_ch_params( ch_params )

    else:
        map_ch_params( params )

    return params


# --- Base Classes ---

class CV( BiologicProgram ):
    """
    Runs a CV scan.
    """
    def __init__(
        self,
        device,
        params,
        **kwargs
    ):
        """
        :param device: BiologicDevice.
        :param params: Program parameters.
            Params are
            start: Dictionary of start voltages keyed by channels. [Defualt: 0]
            end: Dictionary of end voltages keyed by channels.
            step: Voltage step. [Default: 0.01]
            rate: Scan rate in V/s. [Default: 0.05]
            average: Average over points. [Default: False]
        :param **kwargs: Parameters passed to BiologicProgram.
        """

        # defaults
        defaults = {
            'vs_initial': False,
            'start': 0,
            'E2': 0,
            'Ef': 0,
            'step':  0.001,
            'rate':  0.05, #V/s
            'average': False,
            'N_Cycles': 0,
            'Begin_measuring_I':0.5,
            'End_measuring_I': 1
            
        }
        channels = kwargs[ 'channels' ] if ( 'channels' in kwargs ) else None
        params = set_defaults( params, defaults, channels )

        super().__init__(
            device,
            params,
            **kwargs
        )

        self._techniques = [ 'cv' ]
        self._parameter_types = tfs.CV
        self._data_fields = (
            dp.SP300_Fields.CV
            if ecl.is_in_SP300_family( self.device.kind ) else
            dp.VMP3_Fields.CV
        )

        self.field_titles = [ 'Voltage', 'Current', 'Time', 'Power [W]', 'Cycle' ]
        
        self._fields = namedtuple( 'CV_Datum', [
           'voltage', 'current', 'time', 'power', 'cycle'
        ] )

        self._field_values = lambda datum, segment: (
            datum.voltage,
            datum.current,
            dp.calculate_time(
                datum.t_high,
                datum.t_low,
                segment.info,
                segment.values
             ),
             
            datum.voltage* datum.current,  # power
            datum.cycle
        )

    def run( self, retrieve_data = True ):
        """
        :param retrieve_data: Automatically retrieve and disconenct form device.
            [Default: True]
        """
        # setup scan profile ( start -> end -> start )
        params = {}
        for ch, ch_params in self.params.items():
            # voltage_profile = [ ch_params[ 'start' ] ]* 5
            voltage_profile = [ 
                ch_params[ 'start' ],
                ch_params['E1'], 
                ch_params['E2'], 
                ch_params['start'], 
                ch_params['Ef'] 
            ]
            # voltage_profile[ 1 ] = ch_params[ 'end' ]

            params[ ch ] = {
                'vs_initial':   [ ch_params['vs_initial'] ]* 5,
                'Voltage_step': voltage_profile,
                'Scan_Rate':    [ ch_params[ 'rate' ] ]* 5,
                'Scan_number':  2,
                'Record_every_dE':   ch_params[ 'step' ],
                'Average_over_dE':   ch_params[ 'average' ],
                'N_Cycles':          ch_params['N_Cycles'],
                'Begin_measuring_I': ch_params['Begin_measuring_I'], # start measurement at beginning of interval
                'End_measuring_I':   ch_params['End_measuring_I']  # finish measurement at end of interval
            }

        # run technique
        data = self._run( 'cv', params, retrieve_data = retrieve_data )
