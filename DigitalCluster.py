#**********************************************
#
#   Title:  DigitalCluster
#   Ver:    1.0
#   Autor:  Steven Lippmann
#   Date:   Feb. 11, 2016
#
#-Last Modified-------------------------------
#
#   By:     Steven Lippmann
#   Date:   Feb. 11, 2016
#
#//////////////////////////////////////////////

from tkinter import *
from CarMonitor_App import *

#GUI setup
root = Tk()
root.title("BOOOOOOOOOOST")
geom = "{0}x{1}".format(root.winfo_screenwidth(), root.winfo_screenheight())
root.geometry(geom)

app = GaugeCluster(root)

root.overrideredirect(True)
root.bind("<Button-1>", lambda e: app.Dispose())

app.UpdateClusterLoop()

#Main event loop
root.mainloop()
