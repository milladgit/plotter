
import os, sys
import numpy as np
import matplotlib.pyplot as plt

from configuration import *
from barplot import *
from lineplot import *


def findconfig(filename):
	f = open(filename, "r")
	lines = f.readlines()
	f.close()

	filetype = ""

	i = 0
	lines_count = len(lines)
	while i < lines_count:
		l = lines[i].strip()
		if l == "":
			i += 1
			continue
		if l[0] == "#":
			i += 1
			continue
		l = l.split(":")
		i += 1

		k = l[0]
		v = l[1]

		k = k.strip()
		v = v.strip()


		if k == "type":
			filetype = v
			break

	if filetype == "barplot":
		return BarPlot(filename)
	elif filetype == "lineplot":
		return LinePlot(filename)
	else:
		print "Unable to recognize the file type."
		exit(1)

