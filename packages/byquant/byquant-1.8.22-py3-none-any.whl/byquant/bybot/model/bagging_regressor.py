#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2022-2023 ByQuant.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import talib
import pandas as pd
import backtrader as bt
import numpy as np
#from sklearn import datasets,metrics, linear_model,ensemble,tree,neighbors,svm,neural_network
from sklearn import ensemble

class __byModel(bt.Indicator):
    lines = ('pred',)
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.ai_model = ensemble.BaggingRegressor()

    def next(self):
        if len(self.data) < self.p.period :
            return
        x = np.array(self.data.get(size=self.p.period))[:-1].reshape(-1, 1)
        y = np.array(self.data.close.get(size=self.p.period-1))

        self.ai_model.fit(x, y)
        x_latest = np.array(self.data.close.get(size=1)).reshape(-1, 1)
        self.lines.pred[0] = self.ai_model.predict(x_latest)
        
def BaggingRegressor(data,low=pd.Series(dtype=float),period=14):
    if isinstance(data, pd.DataFrame):
        top = talib.MAX(data.high, timeperiod=period)
        bot = talib.MIN(data.low, timeperiod=period)
        mid = (top + bot) / 2
        return top,mid,bot
    elif isinstance(data, pd.Series):
        top = talib.MAX(data, timeperiod=period)
        bot = talib.MIN(low, timeperiod=period)
        mid = (top + bot) / 2
        return top,mid,bot
    elif 'backtrader.' in str(type(data)):
        return __byModel(data,period=period)
    else:
        return None



baggingregressor = BaggingRegressor
#donchian = LinearRegression
#Donchian = LinearRegression
#AROON_NP = AROON


