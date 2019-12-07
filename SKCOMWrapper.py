# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:30:19 2017

@author: jeff
"""

import comtypes.client
from errorMsg import errorMsg
from SKEventWrapper import SKCenterLibEvent,SKQuoteLibEvent,SKReplyLibEventEvent,SKOrderLibEvent
import pandas as pd


class SKCOMWrapper :
    def __init__(self):        
        #Load the dll
        comtypes.client.GetModule(r'./x64/SKCOM.dll')
        #Import the dll 
        import comtypes.gen.SKCOMLib as sk

        self.SKCenterLib = comtypes.client.CreateObject(sk.SKCenterLib,interface=sk.ISKCenterLib)#登入 環境設定
        self.SKQuoteLib = comtypes.client.CreateObject(sk.SKQuoteLib,interface=sk.ISKQuoteLib) #國內報價物件
        self.SKOrderLib = comtypes.client.CreateObject(sk.SKOrderLib,interface=sk.ISKOrderLib) #下單物件
        self.SKOSQuoteLib = comtypes.client.CreateObject(sk.SKOSQuoteLib, interface=sk.ISKOSQuoteLib) #海期報價物件
        self.SKOOQuoteLib = comtypes.client.CreateObject(sk.SKOOQuoteLib, interface=sk.ISKOOQuoteLib) #海選報價物件
        self.SKReplyLib = comtypes.client.CreateObject(sk.SKReplyLib,interface=sk.ISKReplyLib) #回報物件

        self.SKCenterLibEvent = SKCenterLibEvent()
        self.SKQuoteLibEvent = SKQuoteLibEvent(self)
        self.SKReplyLibEvent = SKReplyLibEventEvent(self)
        self.SKOrderLibEvent = SKOrderLibEvent(self)

        SKCenterLibEventHandler = comtypes.client.GetEvents(self.SKCenterLib, self.SKCenterLibEvent)
        SKQuoteLibEventHandler = comtypes.client.GetEvents(self.SKQuoteLib, self.SKQuoteLibEvent)

        self.isLogin = False

    #input: key.config
    def setKey(self, key):
        self.key = key

    def setTradingConfig(self, config):
        self.config = config

    #The API has this function to interpre the error code
    def translateCode(self,errorCode):
        return str(self.SKCenterLib.SKCenterLib_GetReturnCodeMessage(errorCode))
        
    def login(self):
       result = self.SKCenterLib.SKCenterLib_Login (self.key.get('username'),
                                                    self.key.get('password'))
       if(result == 0):
           print("Login success: " + self.key.get('username'))
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


