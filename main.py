# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:28:46 2017
http://kwedr.blogspot.tw/2017/07/api-python-pythonnet.html
@author: jeff
"""

# -*- coding: utf-8 -*-

from errorMsg import errorMsg
from SKCOMWrapper import SKCOMWrapper
import time
 

apiTest = SKCOMWrapper()
apiTest.importKey("key.config")
apiTest.importConfig("api.config")
apiTest.login()
apiTest.connectToQuoteServer();    
time.sleep(10)    
apiTest.SKQuoteLib_RequestTicks()



#apiTest.SKQuoteLib_RequestKLine()
#apiTest.initialOrderSystem()
#apiTest.SKOrderLib_GetOpenInterest();
#apiTest.SKOrderLib_SendFutureOrder()

#apiTest.SKOrderLib_GetFutureRights('N125147695','9280838')

while(1):
    pass