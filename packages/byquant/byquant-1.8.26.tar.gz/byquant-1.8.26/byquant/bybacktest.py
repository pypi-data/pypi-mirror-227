#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Author : Trabi
# Email : info@byquant.com
# Copyright (C) 2022-2023 ByQuant.com
#
#  ███████   ██    ██   ██████   ██    ██    ████    ██    ██  ████████  
#  ██    ██   ██  ██   ██    ██  ██    ██   ██  ██   ███   ██     ██     
#  ███████     ████    ██    ██  ██    ██  ████████  ██ ██ ██     ██         █████  █████  █████
#  ██    ██     ██     ██   ██   ██    ██  ██    ██  ██   ███     ██         █      █   █  █ █ █
#  ███████      ██      ███████   ██████   ██    ██  ██    ██     ██     ██  █████  █████  █ █ █
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



 
from __future__ import (absolute_import, division, print_function,unicode_literals)
import backtrader as bt
from .byanalysis import *
#import pandas as pd

class byTrades(bt.observers.Trades):
    plotlines = dict(
    pnlplus=dict(_name='Positive',
                 marker='o', color='#F05824',
                 markersize=5.0, fillstyle='full'),
    pnlminus=dict(_name='Negative',
                  marker='o', color='#009344',
                  markersize=5.0, fillstyle='none'))
                  
# 修改 BuySell 的样式
class ByQuant_com(bt.observers.BuySell):
    
    params = (('barplot', True), ('bardist', 0.05))
    
    plotlines = dict(
    #buy=dict(marker=r'$\Uparrow$', markersize=10.0, color='#F05824' ),
    #sell=dict(marker=r'$\Downarrow$', markersize=10.0, color='#009344'))
    buy=dict(marker='^', markersize=5.0, color='#F05824' ),
    sell=dict(marker='v', markersize=5.0, color='#009344'))

class byOrder(bt.observer.Observer):
    lines = ('created', 'expired',)
 
    plotinfo = dict(plot=True, subplot=True, plotlinelabels=True)
 
    plotlines = dict(
        created=dict(marker='*', markersize=8.0, color='#206BC4', fillstyle='none'),
        expired=dict(marker='o', markersize=8.0, color='#F05824', fillstyle='full')
    )
 
    def next(self):
        for order in self._owner._orderspending:
            if order.data is not self.data:
                continue
 
            if not order.isbuy():
                continue
 
            # Only interested in "buy" orders, because the sell orders
            # in the strategy are Market orders and will be immediately
            # executed
 
            if order.status in [bt.Order.Accepted, bt.Order.Submitted]:
                self.lines.created[0] = order.created.price
 
            elif order.status in [bt.Order.Expired]:
                self.lines.expired[0] = order.created.price
        
class byBroker(bt.observers.Broker):
    #alias = ('CashValue',)
    #lines = ('cash', 'value')
    
    #plotinfo = dict(plot=True, subplot=True)
    
    plotlines = dict(
        cash=dict(linestyle='-', linewidth=1.0, color='#F05824'),
        #value=dict(_method='bar', color='#206BC4', alpha=0.50, width=1.0),
        value=dict(linestyle='-', linewidth=1.0, color='#206BC4')
    )
    
    #def next(self):
    #    self.lines.cash[0] = self._owner.broker.getcash()
    #    self.lines.value[0] = value = self._owner.broker.getvalue()
    

        
class byDrawDown(bt.observers.DrawDown):

    plotlines = dict(
        #drawdown=dict(linestyle='-', linewidth=1.0, color='#009344'),
        drawdown=dict(_method='bar', color='#009344', alpha=0.30, width=1.0)
    )
    
    #def next(self):
    #    self.lines.cash[0] = self._owner.broker.getcash()
    #    self.lines.value[0] = value = self._owner.broker.getvalue()
    
class byTimeReturn(bt.observers.TimeReturn):

    plotlines = dict(
        #timereturn=dict(linestyle='-', linewidth=1.0, color='#F05824'),
        timereturn=dict(_method='bar', color='#F05824',  width=1.0)
    )


 
    
        
class Backtest():

    
    def __init__(self,datasets,strategy='',out='',style='candle',warn=False,**params):
        print('*** Start ByQuant Backtest Engine ***')
        if 'cash' in params:
            self.cash = params['cash']
        else:
            self.cash = 1000000
            
        if 'commission' in params:
            self.commission = params['commission']
        else:
            self.commission = 0.0005
            
        self.datasets = datasets
        #self.params = params
        
        #data.index=pd.to_datetime(data['datetime'])
        #self.data = bt.feeds.PandasData(dataname=data, datetime='datetime')
        
        self.strategy = strategy
        self.style = style
        self.out = out
        self.warn = warn
    
    def feedData(self,data,freq):
        if freq == '1m':
            params = dict(
                #fromdate = datetime.datetime(2011,1,4),
                #todate = datetime.datetime(2021,3,20),
                timeframe = bt.TimeFrame.Minutes, #bt.TimeFrame.Minutes,
                compression = 1,
                #dtformat=('%Y-%m-%d %H:%M:%S'),
                #tmformat=('%H:%M:%S'),
                #datetime=0,
                open=0,
                high=1,
                low=2,
                close=3,
                volume=4
            )
        else:
            params = dict(
                #fromdate = datetime.datetime(2011,1,4),
                #todate = datetime.datetime(2021,3,20),
                timeframe = bt.TimeFrame.Days, #bt.TimeFrame.Minutes,
                compression = 1,
                #dtformat=('%Y-%m-%d %H:%M:%S'),
                #tmformat=('%H:%M:%S'),
                #datetime=0,
                open=0,
                high=1,
                low=2,
                close=3,
                volume=4
            )
        data = data[['open','high','low','close','volume']]
        feed_result = bt.feeds.PandasData(dataname=data,**params)
        
        return feed_result


    def byrun(self):
        import matplotlib.pyplot as plt
        plt.style.use("default") #default、ggplot is also fine
        #plt.rcParams["figure.figsize"] = (9,8)
        #print(plt.style.available)
        cerebro = bt.Cerebro(stdstats=False)
        #cerebro.addobserver(bt.observers.BuySell)
        #cerebro.addobserver(bt.observers.Broker)
        
        cerebro.addobserver(byOrder)
        cerebro.addobserver(byTrades)
        if type(self.datasets) == list:
            cerebro.addobserver(bt.observers.BuySell)
            #cerebro.addobserver(ByQuant_com)
        else:
            cerebro.addobserver(ByQuant_com)
        cerebro.addobserver(byBroker)
        cerebro.addobserver(byTimeReturn)
        cerebro.addobserver(byDrawDown)
        #cerebro.addobserver(bt.observers.DrawDown)
        
        #cerebro.addobserver(bt.observers.TimeReturn)
        
        cerebro.addstrategy(self.strategy)
        
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='_Pyfolio')
        #cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
        #cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns')  # 用对数法计算总、平均、复合、年化收益率
        #cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤
        #cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')
            
            
        
        cerebro.broker.setcash(self.cash)
        
        cerebro.broker.setcommission(commission=self.commission)
        assetnum = 1
        if type(self.datasets) == list:
            assetnum = len(self.datasets)
            for dataset in self.datasets:
                data = dataset['data']
                symbol = dataset['symbol']
                freq = dataset['freq']
                feed_data = self.feedData(data,freq)
                cerebro.adddata(feed_data, name = symbol)
                #assetnum = assetnum +1
                
                
        else :
            #assetnum = 1
            data = self.datasets
            symbol = 'Symbol'
            freq = '1d'
            feed_data = self.feedData(data,freq)
            cerebro.adddata(feed_data, name = symbol)
            
        plt.rcParams["figure.figsize"] = (9,5+3*assetnum)
        #print(len(self.datasets))
            
        results = cerebro.run()
        datadict={}
        pyfoliozer = results[0].analyzers.getbyname('_Pyfolio')
        datadict['timereturn'], datadict['positions'], datadict['transactions'], datadict['grosslev'] = pyfoliozer.get_pf_items()

        if 'plot' == self.out or 'a' == self.out or 'all' == self.out:
            
            
            pkwargs = dict(
                
                iplot=True,
                numfigs=1,
                # to have a tight packing on the chart wether only the x axis or also
                # the y axis have (see matplotlib)
                ytight = False,
                # y-margin (top/bottom) for the subcharts. This will not overrule the
                # option plotinfo.plotymargin
                yadjust = 0.0,
                # Each new line is in z-order below the previous one. change it False
                # to have lines paint above the previous line
                zdown = True,
                # Rotation of the date labes on the x axis
                tickrotation = 15,
                # How many "subparts" takes a major chart (datas) in the overall chart
                # This is proportional to the total number of subcharts
                rowsmajor = 5,
                # How many "subparts" takes a minor chart (indicators/observers) in the
                # overall chart. This is proportional to the total number of subcharts
                # Together with rowsmajor, this defines a proportion ratio betwen data
                # charts and indicators/observers charts
                rowsminor = 1,
                # Distance in between subcharts
                plotdist = 0.0,
                # Have a grid in the background of all charts
                grid = False,
                # Default plotstyle for the OHLC bars which (line -> line on close)
                # Other options: 'bar' and 'candle'
                style = self.style,
                # Default color for the 'line on close' plot
                loc = '#206BC4',
                # Default color for a bullish bar/candle (0.75 -> intensity of gray)
                barup = '#F8A488', ##206BC4
                # Default color for a bearish bar/candle
                bardown = '#8FB5E1', ##F14A12
                # Level of transparency to apply to bars/cancles (NOT USED)
                bartrans = 0.50,
                # Wether the candlesticks have to be filled or be transparent
                barupfill = True,
                bardownfill = False,
                # Wether the candlesticks have to be filled or be transparent
                fillalpha = 0.20,
                # Wether to plot volume or not. Note: if the data in question has no
                # volume values, volume plotting will be skipped even if this is True
                volume = True,
                # Wether to overlay the volume on the data or use a separate subchart
                voloverlay = False,
                # Scaling of the volume to the data when plotting as overlay
                volscaling = 0.33,
                # Pushing overlay volume up for better visibiliy. Experimentation
                # needed if the volume and data overlap too much
                volpushup = 0.00,
                # Default colour for the volume of a bullish day
                volup = '#F8A488',
                # 0.66 of gray
                # Default colour for the volume of a bearish day
                voldown = '#8FB5E1',
                # (204, 96, 115)
                # Transparency to apply to the volume when overlaying
                voltrans = 0.50,
                # Transparency for text labels (NOT USED CURRENTLY)
                subtxttrans = 0.88,
                # Default font text size for labels on the chart
                subtxtsize = 9,
                # Transparency for the legend (NOT USED CURRENTLY)
                legendtrans = 0.25,
                # Wether indicators have a leged displaey in their charts
                legendind = True,
                # Location of the legend for indicators (see matplotlib)
                legendindloc = 'upper left',
                # Plot the last value of a line after the Object name
                linevalues = True,
                # Plot a tag at the end of each line with the last value
                valuetags = True,
                # Default color for horizontal lines (see plotinfo.plothlines)
                hlinescolor = '0.88',
                # shade of gray
                # Default style for horizontal lines
                hlinesstyle = '--',
                # Default width for horizontal lines
                hlineswidth = 0.5,
                # Default color scheme: Tableau 10
                #lcolors = tableau10,
                # strftime Format string for the display of ticks on the x axis
                #fmt_x_ticks = None,
                # strftime Format string for the display of data points values
                #fmt_x_data = None,
                
                fmt_x_ticks="%Y-%m-%d %H:%M:%S", 
                fmt_x_data="%Y-%m-%d %H:%M:%S"
        
               )
            cerebro.plot(**pkwargs)
            
            
            if 'all' == self.out:
                return datadict
            #img = cerebro.plot(style='line', plotdist=0.1, grid=True)
            #img[0][0].savefig(f'cerebro_123.png')
            
            #cerebro.plot(style = self.style,figsize=figsize)

        elif 'bokeh' == self.out or 'b' == self.out:
            from backtrader_plotting import Bokeh
            from backtrader_plotting.schemes import Tradimo,Blackly
            b = Bokeh(
                #title='symbol',
                tabs='single',  # single 和 multi
                plot=True,  # 关闭K线
                style='line',  # style='line'
                plot_mode='single',
                scheme=Tradimo(),
                # scheme=Blackly(),
                output_mode='show',  # output_mode “show”,“save”,"memory"
                #filename='filepath',
                show_headline=False
            )
            cerebro.plot(b)

            
        elif 'list' == self.out or 'dict' == self.out:
            return datadict

        else:
            """returns = results[0].analyzers._Returns.get_analysis()
            sharpe_ratio = results[0].analyzers._SharpeRatio.get_analysis()
            draw_down = results[0].analyzers._DrawDown.get_analysis()
            #print('Value: %.2f' % cerebro.broker.getvalue())
            print('Returns:%s' % returns)
            print('Sharpe Ratio: %s' % sharpe_ratio)
            print('Draw Down: %s' % draw_down)"""
            
            
            Analysis(datadict,out =self.out).show()
            
        
        #returns, positions, transactions, grosslev = pyfoliozer.get_pf_items()
        
        #byresults['returns'] = returns
        #byresults['positions'] = returns
        #byresults['transactions'] = returns
        #byresults['grosslev'] = returns
            
        

