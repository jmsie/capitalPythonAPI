# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:28:46 2017
http://kwedr.blogspot.tw/2017/07/api-python-pythonnet.html
@author: jeff
"""

# -*- coding: utf-8 -*-

import sys, os, clr, time

is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
    
from switch import *
import logging
logging.basicConfig(level=logging.DEBUG)

q = queue.Queue ()

class Job:
    Quote_EnterMonitor = 1
    GetStockByIndex = 2
    GetStockByIndexResult = 3
    OnNotifyQuote = 4
    def __init__ (self, do_type):
        self.do_type = do_type

class SKCenterLibEvent:
    def __init__(self, parent, bot):
        self.parent = parent
        self.bot = bot

    def Bind(self, obj):
        obj.OnTimer += self.OnTimer

    def OnTimer(self, nTime):
        print ("OnTimer: " + str(nTime))
        
    def OnShowAgreement(self, bstrData):
        print ("OnShowAgreement: " + str(bstrData))

class SKReplyLibEvent:
    def __init__(self):
        self.parent = None
        self.bot = None        
    def OnConnect(bstrUserID, nErrorCode ):
        print ("OnConnect: user:" + bstrUserID + " error:" + str(nErrorCode))
        
class SKQuoteLibEvent:
    def __init__(self, parent, bot):
        self.parent = parent
        self.bot = bot
        
    def Bind(self, obj):
        obj.OnConnection += self.OnConnection
        obj.OnNotifyQuote += self.OnNotifyQuote

    def OnConnection(self, nKind, nCode):
        print ("OnConnection: kind:" + str(nKind) + " error:" + str(nCode))
        self.bot.SKQuoteLibOnOnConnection (nKind, nCode)

    def OnNotifyQuote(self, sMarketNo, sIndex):        
        j = Job (Job.GetStockByIndexResult)
        j.sMarketNo = sMarketNo
        j.sIndex = sIndex
        q.put (j)
    
class SKCOMWapper:
    def __init__(self, uid, bot):
        self.uid = uid
        self.bot = bot

        sys.path.append(os.path.join(os.getcwd(), "dll", "x64"))
        clr.AddReference("Interop.SKCOMLib")
        import SKCOMLib as SKCOMLib
        
        self.Template = SKCOMLib
        self.SKCenterLib = SKCOMLib.SKCenterLib ()
        self.SKCenterLibEvent = SKCenterLibEvent(self, bot)
        self.SKCenterLibEvent.Bind (self.SKCenterLib)
        
        self.SKReplyLib = SKCOMLib.SKReplyLib ()

        #國內報價物件。
        self.SKQuoteLib = SKCOMLib.SKQuoteLib ()
        self.SKQuoteLibEvent = SKQuoteLibEvent(self, bot)
        self.SKQuoteLibEvent.Bind (self.SKQuoteLib)

        self.SKSTOCK = SKCOMLib.SKSTOCK ()

class StockBot:
    def __init__(self, stockno):
        self.SKCOM = SKCOMWapper (0, self)
        self.Stock = {}
        self.StockNo = stockno

    def DoLogin (self, account, pwd):
        ret = self.SKCOM.SKCenterLib.SKCenterLib_Login (account, pwd)        
        print ("CeterLib Login: " + str (ret))
        q.put (Job (Job.Quote_EnterMonitor))
        
    def SKQuoteLibOnOnConnection (self, nKind, nCode):
        if nKind == 3003 and nCode == 0:
            q.put (Job (Job.GetStockByIndex))

    def DoOnNotifyQuote (self, sMarketNo, sIndex):
        ret, Stock = self.SKCOM.SKQuoteLib.SKQuoteLib_GetStockByIndex(sMarketNo, sIndex, self.SKCOM.SKSTOCK)
        j = Job(Job.OnNotifyQuote)
        j.Stock = Stock
        q.put (j)

    def DoGetStockByIndex (self):
        self.SKCOM.SKQuoteLib.SKQuoteLib_RequestStocks (-1, self.StockNo)

    def DoEnterMonitor (self):
        return  self.SKCOM.SKQuoteLib.SKQuoteLib_EnterMonitor()

def DoJob(Bot, x):    
    print ("DoJob: " + str (x.do_type))
    if (x.do_type == Job.Quote_EnterMonitor):
        Bot.DoEnterMonitor ()
        
    if (x.do_type == Job.GetStockByIndex):
        Bot.DoGetStockByIndex ()
        
    if (x.do_type == Job.GetStockByIndexResult):
        Bot.DoOnNotifyQuote (x.sMarketNo, x.sIndex)
        
    if (x.do_type == Job.OnNotifyQuote):
        print ("OnNotifyQuote: " + x.Stock.bstrStockName + " Close: " + str (x.Stock.nClose))
        Bot.Stock[x.Stock.bstrStockNo] = x.Stock
        
        
if __name__ == "__main__":
    Bot = StockBot("TXF00")
    Bot.DoLogin('N125147695', 'newabc54321')

    while 1:
        while not q.empty():
            next_job = q.get()
            DoJob (Bot, next_job)
        time.sleep(1)
