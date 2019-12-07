"""
Created on Fri Sep 22 16:28:46 2017
@author: jeff
"""

import time
from SKCOMWrapper import SKCOMWrapper
from config import trading_settings, key

apiTest = SKCOMWrapper()
apiTest.setKey(key)
apiTest.setTradingConfig(trading_settings)
apiTest.login()
#apiTest.connectToQuoteServer();
#time.sleep(10)
#apiTest.SKQuoteLib_RequestTicks()



#apiTest.SKQuoteLib_RequestKLine()
#apiTest.initialOrderSystem()
#apiTest.SKOrderLib_GetOpenInterest();
#apiTest.SKOrderLib_SendFutureOrder()

#apiTest.SKOrderLib_GetFutureRights('N125147695','9280838')

while(1):
    pass