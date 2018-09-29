# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:23:22 2017

@author: jeff
"""

def errorMsg(errorCode):
    
    if(errorCode == 0):
        print("Success");
        return 1
        
    elif(errorCode == 2003):
        print("Already Logined")
        return 0
    elif(errorCode == 3003):
        print("Quote server connect success!")
        return 1
    else:
        print("Undefined error")
        return 1
        
        
