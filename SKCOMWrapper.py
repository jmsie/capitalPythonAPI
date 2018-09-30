# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:30:19 2017

@author: jeff
"""

from ctypes import *
import sys, os, clr, time
import queue as queue
from errorMsg import errorMsg
from SKEventWrapper import SKCenterLibEvent,SKQuoteLibEvent,SKReplyLibEventEvent,SKOrderLibEvent
import pandas as pd
#import event
        

class SKCOMWrapper :
    def __init__(self):        
        #Load the dll
        clr.AddReference("x64/Interop.SKCOMLib")        
        #Import the dll 
        import SKCOMLib as SKCOMLib
        
        
        
        self.SKCOMLib = SKCOMLib
        self.SKTICK = SKCOMLib.SKTICK ()
        self.FUTUREORDER = SKCOMLib.FUTUREORDER ()        
        self.SKCenterLib = SKCOMLib.SKCenterLib() #登入 環境設定
        self.SKQuoteLib = SKCOMLib.SKQuoteLib() #國內報價物件
        
        self.SKOrderLib = self.SKCOMLib.SKOrderLib() #下單物件
        self.SKOSQuoteLib = self.SKCOMLib.SKOSQuoteLib() #海期報價物件
        self.SKOOQuoteLib = self.SKCOMLib.SKOOQuoteLib() #海選報價物件
        self.SKReplyLib = self.SKCOMLib.SKReplyLib() #回報物件
        
        self.SKQuoteLibEvent = SKQuoteLibEvent(self)
        self.SKReplyLibEvent = SKReplyLibEventEvent(self)
        self.SKOrderLibEvent = SKOrderLibEvent(self)
        
        self.SKCenterLibEvent.bind(self.SKCenterLib)
        self.SKQuoteLibEvent.bind(self.SKQuoteLib)
        self.SKReplyLibEvent.bind(self.SKReplyLib)
        self.SKOrderLibEvent.bind(self.SKOrderLib)
        
        self.isLogin = False

    #input: key.config
    def importKey(self,configFile)        :
        key = open('key.config', 'r')
        self.username = key.readline().split('=')[1].replace('\n','')
        self.password = key.readline().split('=')[1].replace('\n','')
        
    def importConfig(self,configFile)        :
        self.config = pd.read_csv(configFile)
        
    def getConfig(self,key):
        return self.config[self.config.name == key]['settings'].values[0]
    
    #The API has this function to interpre the error code
    def translateCode(self,errorCode):
        return str(self.SKCenterLib.SKCenterLib_GetReturnCodeMessage(errorCode))
        
    def login(self):
       result = self.SKCenterLib.SKCenterLib_Login (self.username, self.password)
       if(result == 0):
           print("Login success: " + self.username)
           self.isLogin = True;
       else:
           errorMsg(result)

    def getLoginStatus(self):
       return self.isLogin;
   
    def connectToQuoteServer(self):
        print("Connecting to quote server...")
        msg = errorMsg(self.SKQuoteLib.SKQuoteLib_EnterMonitor())
        if msg == 0:
            print("Quote server connected")
        else:    
            print("Quote server connect fail: " + self.translateCode(msg))
    
    
    #TODO Need to active after SKQuoteLibEvent.onConnection == 3003
    def SKQuoteLib_RequestTicks(self):
        print("Requesting data: " + self.getConfig('quoteIndex'))
        print(self.SKQuoteLib.SKQuoteLib_RequestTicks(-1,self.getConfig('quoteIndex')))
        #print(self.SKQuoteLib.SKQuoteLib_RequestLiveTick(-1,'TX00'))  ##WHY fail????
        
    def SKQuoteLib_RequestKLineAM(self):
        print(self.SKQuoteLib.SKQuoteLib_RequestKLineAM(self.getConfig('quoteIndex'),0,1,0))
        
    def SKQuoteLib_RequestKLine(self):
        print(self.SKQuoteLib.SKQuoteLib_RequestKLine(self.getConfig('quoteIndex'),0,"1"))
        
    def initialOrderSystem(self):
        self.SKOrderLib.SKOrderLib_Initialize();
        self.SKOrderLib.GetUserAccount()
        self.SKOrderLib.ReadCertByID(self.username)
        
    #TODO: finish this    
    def SKOrderLib_SendFutureOrder(self):        
        bstrLogInID = self.username
        bAsyncOrder = 0
        
        pOrder = self.SKCOMLib.FUTUREORDER()
        pOrder.bstrFullAccount = self.getConfig('tradingAccount')
        pOrder.bstrStockNo = self.getConfig('tradingIndex')
        pOrder.sTradeType = 0 #ROD
        pOrder.sBuySell = 1
        pOrder.sDayTrade = 0
        pOrder.sNewClose = 2
        pOrder.bstrPrice = '10500'
        pOrder.nQty = 1
        pOrder.bstrTrigger = ''
        pOrder.bstrMovingPoint = ''
        pOrder.sReserved = 0
        test = ""
        #bstrMessage = c_wchar_p()
        #bstrMessage = create_string_buffer(50)
        #ptr_bstrMessage = byref(c_char_p(addressof(bstrMessage)))
        
        #test = self.SKOrderLib.SendFutureOrder
        #test.argtypes = [c_wchar, c_wchar_p, POINTER(c_char_p), POINTER(c_wchar_p)]
        #test(bstrLogInID, bAsyncOrder, pOrder,byref(QQ))
        result = self.SKOrderLib.SendFutureOrder(bstrLogInID, bAsyncOrder, pOrder, test)
        print("QQ: " + str(result))
        #print("AA:"+bstrMessage)
        print("order send: "+ test)
        
        
    def SKOrderLib_GetFutureRights(self,username, account):
        self.SKOrderLib.GetFutureRights(username, account, 1);
                                       
    def SKOrderLib_GetOpenInterest(self):
        bstrLogInID = self.username        
        bstrAccount = self.getConfig('tradingAccount')
        print("getOpenInterest " + str(self.SKOrderLib.GetOpenInterest(bstrLogInID,bstrAccount)))
        
"""        
sys.path.append(os.path.join(os.getcwd(), "dll", "x64"))
clr.AddReference("Interop.SKCOMLib")
#clr.AddReference("SKCOM")
import SKCOMLib as SKCOMLib
COM = SKCOMLib

bstrLogInID = "QQ"
bAsyncOrder = 0

pOrder = COM.FUTUREORDER()
ptr_pOrder = c_char_p(id(pOrder))     

msg = create_string_buffer(50)
ptr_msg = hex(addressof(msg))

QQ = ""
#ptr_msg = hex(id(msg))

fun = COM.SKOrderLib.SendFutureOrder
#fun.argtypes = [str, bool,POINTER(c_char_p),POINTER(c_char_p) ]
fun(bstrLogInID, bAsyncOrder, pOrder, QQ)
 
COM.SKOrderLib.SendFutureOrder(bstrLogInID, bAsyncOrder, pOrder, QQ)
"""


