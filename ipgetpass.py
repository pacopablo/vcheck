# -*- coding: utf-8 -*-
#
# Module net_getpass
# Getting password from console in IronPython (Python.NET)
#
# Author: Roman Miklos (RMiklos@pss.sk)
#
# Taken from: http://www.tek-tips.com/viewthread.cfm?qid=1288373&page=8 

import clr
import System
from System import Console

def getpass(prompt="Password:"):
  '''Read Password from Console without echo'''
  # Prompt
  Console.Write(prompt)
  # create Instance of ConsoleKeyInfo
  key = System.ConsoleKeyInfo()
  # initialize vars
  pwd =""
  EnterPressed = False
  # Read while input not ends
  while not EnterPressed:
    key = Console.ReadKey(True)
    if key.Key == System.ConsoleKey.Enter:
      # End of Input
      EnterPressed = True

    elif key.Key == System.ConsoleKey.Backspace:
      if len(pwd)>0:
        # Clear last character in password
        pwd = pwd[:-1]
        Console.Write(key.KeyChar)
        Console.Write(" ")
        Console.Write(key.KeyChar)
      else:
        Console.Beep()

    else:
      pwd += key.KeyChar
      Console.Write("*")

  # Next line
  Console.WriteLine()
  # return password
  return (pwd)

################################################################################
# Module Test
################################################################################
if __name__ == "__main__":
  print "Your Password is: %s" % getpass("Enter your password please:")

