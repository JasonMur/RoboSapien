from roboClasses.roboClass import *

robosapien = Robosapien()
robosapien.cmd_thread.start()
robosapien.watson_thread.start()
robosapien.response_thread.start()
