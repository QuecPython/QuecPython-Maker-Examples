# Copyright (c) Quectel Wireless Solution, Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Flame sensor demo using ADC
@version   : 0.1
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime

def fun():
    while True:
        num=adc.read(adc.ADC1)
        utime.sleep(1)
        print(num)

    
if __name__=='__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())