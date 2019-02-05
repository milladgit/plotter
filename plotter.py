
import os,sys
from figure import *
from configuration import *
from barplot import *
from findconfig import *


if len(sys.argv) < 2:
    print "Please provide the config file."
    exit(1)


F = Figure(sys.argv[1])

F.draw()


