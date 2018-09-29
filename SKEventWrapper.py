# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 21:47:41 2017

@author: jeff
"""
import time
class SKCenterLibEvent:
    def __init__(self, parent):
        self.parent = parent

    def bind(self, obj):
        obj.OnTimer += self.onTimer
        print("SKCenterLib event engine started")

    def onTimer(self, nTime):
        print ("onTimer: " + str(nTime))
        
    def onShowAgreement(self, bstrData):
        print ("onShowAgreement: " + str(bstrData))
##########################################################################
class SKQuoteLibEvent:
    def __init__(self, parent):
        self.parent = parent
        
    def bind(self, obj):
        obj.OnConnection += self.onConnection
        obj.OnNotifyQuote += self.onNotifyQuote
        obj.OnNotifyHistoryTicks += self.onNotifyHistoryTicks
        obj.OnNotifyTicks += self.onNotifyTicks
        obj.OnNotifyKLineData += self.onNotifyKLineData
        print("SKQuoteLib event engine started")

    def onConnection(self, nKind, nCode):
        print ("OnConnection: code:" + self.parent.translateCode(nKind) + " error:" + self.parent.translateCode(nCode))
        
       
    def onNotifyQuote(self, sMarketNo, sIndex):        
        pass
    
    def onNotifyHistoryTicks(self,sMarketNo, sIndex, nPtr, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        print("onNotifyHistoryTicks: " + str(nTimehms) + ":" + str(nTimemillismicros) + "  " + str(nClose))

    def onNotifyTicks(self, sMarketNo, sIndex, nPtr, nTimehms, nTimemillismicros, nBid, nAsk, nClose, nQty, nSimulate):
        #data = "onNotifyTicks: " + str(nTimehms) + ":" + str(nTimemillismicros) + "  " + str(nClose)
        data = time.strftime("%Y/%m/%d") + ',' +  str(nTimehms) + ',' + str(nClose) + ',' + str(nQty)
        print(data)
        
    def onNotifyKLineData(self,bstrStockNo,bstrData):
        data = time.strftime("%Y/%m/%d") + bstrStockNo + ',' + bstrData
        print(data)
        
##########################################################################

class SKReplyLibEventEvent:
    def __init__(self, parent):
        self.parent = parent
        
    def bind(self, obj):
        obj.OnDisconnect += self.onDisconnect
        print("SKReplyLibEventEvent event engine started")

    def onDisconnect(self,userId,errorCode):
        print("Disconnected: " + userId)
        print("ERROR: " + self.parent.translateCode(errorCode))
##########################################################################
class SKOrderLibEvent:
    def __init__(self, parent):
        self.parent = parent
    def bind(self, obj):
        obj.OnAccount += self.onAccount
        #obj.OnFutureRights += self.onFutureRights
        obj.OnOpenInterest += self.onOpenInterest
        print("SKOrderLibEvent event engine started")
    
    def onAccount(self,bstrLogInID, bstrAccountData):
        print("Account on: " + bstrLogInID +  " =>" + bstrAccountData)
        self.parent.accountList = bstrAccountData
    
    def onFutureRights(self, bstrData):
        print("onFutureRights: " + bstrData)
    
    def onOpenInterest(self, bstrData):
        print(bstrData)
    
    
    