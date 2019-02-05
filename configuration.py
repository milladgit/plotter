
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from figure import *
import utils


class Configuration(object):

	def __init__(self, filename):
		self.ax_id = -1

		self.type = ""
		self.width = 0.35
		self.colors = []
		self.labels = []
		self.ylabel = []
		self.title = ""
		self.xticks_label = []
		self.xticks_rotation = 0
		self.legend = "on"

		self.grid = "on"
		self.grid_which = "major"   # major, minor, both
		self.grid_axis = "y"        # both, x, y

		self.background_color = ""

		self.spines = dict()

		self.load_config(filename)



	def load_config(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		f.close()

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

			if l[0] == "datatable":
				break

			k = l[0]
			v = l[1]

			k = k.strip()
			v = v.strip()


			if k == "type":
				self.type = v
			elif k == "width":
				self.width = float(v)
			elif k == "colors":
				self.colors = v.split(",")
				self.colors = [q.strip() for q in self.colors]
			elif k == "labels":
				self.labels = v.split(",")
				self.labels = [q.strip() for q in self.labels]
			elif k == "ylabel":
				self.ylabel = v
			elif k == "title":
				self.title = v
			elif k == "xticks_label":
				self.xticks_label = v.split(",")
				self.xticks_label = [q.strip() for q in self.xticks_label]
			elif k == "xticks_rotation":
				self.xticks_rotation = float(v)
			elif k == "legend":
				self.legend = v.lower()
			elif k == "background_color":
				self.background_color = v
			elif k == "spine":
				v_list = v.split(",")
				v_list = [_v.strip() for _v in v_list]
				k = "%s-%s" % (v_list[0], v_list[1])
				self.spines[k] = v_list[2]



	def draw(self, ax):

		for k, value in self.spines.items():
			k = k.split("-")
			direction = k[0]
			trait = k[1]

			if trait == "color":
				ax.spines[direction].set_color(value)
			elif trait == "linewidth":
				ax.spines[direction].set_linewidth(float(value))
			elif trait == "visible":
				ax.spines[direction].set_visible(utils.str2bool(value))

		# grid
		if self.grid == "on":
			if self.grid_which != "" and self.grid_axis != "":
				ax.grid(True, which=self.grid_which, axis=self.grid_axis)
			elif self.grid_axis != "":
				ax.grid(True, axis=self.grid_axis)
			elif self.grid_which != "":
				ax.grid(True, which=self.grid_which)
		else:
			ax.grid(False)

		ax.set_ylabel(self.ylabel)
		ax.set_title(self.title)

		if self.background_color != "":
			ax.patch.set_facecolor(self.background_color)
		if self.legend == "on":
			ax.legend()


