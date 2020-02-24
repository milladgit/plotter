
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from figure import *
import utils


# To change ticks:
# Link: 
# 	https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.tick_params.html
# Example: 
# 	ax.tick_params(direction='out', length=6, width=2, colors='r', grid_color='r', grid_alpha=0.5)



class Configuration(object):

	def __init__(self, filename):
		self.turn_off = False
		self.ax_id = -1
		self.ax_row_id = -1
		self.ax_col_id = -1
		self.ax_row_span = 1
		self.ax_col_span = 1

		self.title = ""

		self.type = ""
		self.width = 0.35
		self.colors = []
		self.labels = []
		self.xlabel = ""
		self.ylabel = ""
		self.title = ""

		self.xticks_label_show = "on"
		self.yticks_label_show = "on"
		self.xticks_label_fontsize = "10"
		self.yticks_label_fontsize = "10"
		self.xticks_label = []
		self.xticks_rotation = 0

		self.legend = "on"
		self.xlim = None
		self.ylim = None
		self.xticks_pad = None
		self.yticks_pad = None

		self.grid = "on"
		self.grid_which = "major"   # major, minor, both
		self.grid_axis = "y"        # both, x, y

		self.yscale = ""

		self.background_color = ""

		self.spines = dict()

		self.hline_list = list()
		self.vline_list = list()

		self.annotate_params = list()

		self.lines = None

		self.load_config(filename)



	def load_config(self, filename):
		if filename == "":
			return 
			
		f = open(filename, "r")
		lines = f.readlines()
		f.close()

		self.lines = lines

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
			elif k == "title":
				self.title = v
			elif k == "width":
				self.width = float(v)
			elif k == "colors":
				self.colors = v.split(",")
				self.colors = [q.strip() for q in self.colors]
			elif k == "labels":
				self.labels = v.split(",")
				self.labels = [q.strip() for q in self.labels]
			elif k == "xlabel":
				self.xlabel = v
			elif k == "ylabel":
				self.ylabel = v
			elif k == "title":
				self.title = v
			elif k == "grid":
				self.grid = v
			elif k == "grid_which":
				self.grid_which = v
			elif k == "grid_axis":
				self.grid_axis = v
			elif k == "xticks_label_show":
				self.xticks_label_show = v
			elif k == "yticks_label_show":
				self.yticks_label_show = v
			elif k == "xticks_label_fontsize":
				self.xticks_label_fontsize = v
			elif k == "yticks_label_fontsize":
				self.yticks_label_fontsize = v
			elif k == "xticks_label":
				self.xticks_label = v.split(",")
				self.xticks_label = [q.strip() for q in self.xticks_label]
			elif k == "xticks_rotation":
				self.xticks_rotation = float(v)
			elif k == "xticks_pad":
				self.xticks_pad = float(v)
			elif k == "yticks_pad":
				self.yticks_pad = float(v)
			elif k == "legend":
				self.legend = v.lower()
			elif k == "background_color":
				self.background_color = v
			elif k == "spine":
				v_list = v.split(",")
				v_list = [_v.strip() for _v in v_list]
				k = "%s-%s" % (v_list[0], v_list[1])
				self.spines[k] = v_list[2]
			elif k == "xlim":
				v_list = v.split(",")
				v_list = [float(_v.strip()) for _v in v_list]
				self.xlim = v_list
			elif k == "ylim":
				v_list = v.split(",")
				v_list = [float(_v.strip()) for _v in v_list]
				self.ylim = v_list
			elif k == "hline":
				v_list = v.split(",")
				self.hline_list.append(v_list)
			elif k == "vline":
				v_list = v.split(",")
				self.vline_list.append(v_list)
			elif k == "yscale":
				self.yscale = v
			elif k == "annotate":
				self.annotate_params.append(v.split(";"))


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
		# good examples: 
		# http://jonathansoma.com/lede/data-studio/matplotlib/adding-grid-lines-to-a-matplotlib-chart/
		if self.grid == "on":
			ax.set_axisbelow(True)
			if self.grid_which in ["both", "minor"]:
				ax.minorticks_on()
				ax.tick_params(axis='x', which='minor', bottom=False)
			if self.grid_which == "both":
				ax.grid(which="major", axis=self.grid_axis, linestyle="-")
				ax.grid(which="minor", axis=self.grid_axis, linestyle=":")
			elif self.grid_which == "minor":
				ax.grid(which="minor", axis=self.grid_axis, linestyle=":")
			elif self.grid_which == "major":
				ax.grid(which="minor", axis=self.grid_axis, linestyle="-")
		else:
			ax.grid(False)
		

		if self.xlabel != "":
			ax.set_xlabel(self.xlabel.decode('string_escape'))
		if self.ylabel != "":
			ax.set_ylabel(self.ylabel)

		if self.title != "":
			ax.set_title(self.title)

		if self.xlim != None:
			ax.set_xlim(self.xlim)
		if self.ylim != None:
			ax.set_ylim(self.ylim)

		if len(self.hline_list) > 0:
			for h in self.hline_list:
				val = float(h[0])
				ax.axhline(val, color=h[1], ls=h[2], lw=h[3])

		if len(self.vline_list) > 0:
			for h in self.vline_list:
				val = float(h[0])
				ax.axvline(val, color=h[1], ls=h[2], lw=h[3])

		if self.yscale != "":
			ax.set_yscale(self.yscale)

		for annot in self.annotate_params:
			ann_text = annot[0]
			ann_xy = annot[1].strip()
			ann_xy = ann_xy[1:-1].split(",")
			ann_x = float(ann_xy[0].strip())
			ann_y = float(ann_xy[1].strip())
			ann_xy_text = annot[2].strip()
			ann_xy_text = ann_xy_text[1:-1].split(",")
			ann_x_text = float(ann_xy_text[0].strip())
			ann_y_text = float(ann_xy_text[1].strip())

			arrowprops = dict()
			tmp = annot[3].split(",")[0].strip()
			if len(tmp) > 0:
				arrowprops["facecolor"] = tmp
			tmp = annot[3].split(",")[1].strip()
			if len(tmp) > 0:
				arrowprops["shrink"] = tmp
			tmp = annot[3].split(",")[2].strip()
			if len(tmp) > 0:
				arrowprops["arrowstyle"] = tmp
			tmp = annot[3].split(",")[3].strip()
			if len(tmp) > 0:
				arrowprops["connectionstyle"] = tmp


			# Visit following link for different types of arrows:
			# https://matplotlib.org/users/annotations.html
			ax.annotate(ann_text, xy=(ann_x, ann_y), xytext=(ann_x_text, ann_y_text), arrowprops=arrowprops)
			# ax.annotate(ann_text, xy=(1, 1), xytext=(3,3), arrowprops=arrowprops)


		if self.xticks_label_show == "off":
			plt.setp(ax.get_xticklabels(), visible=False)
		if self.yticks_label_show == "off":
			plt.setp(ax.get_yticklabels(), visible=False)

		if self.xticks_pad != None:
			ax.tick_params(axis='x',pad=self.xticks_pad)
		if self.yticks_pad != None:
			ax.tick_params(axis='y',pad=self.yticks_pad)

		if self.background_color != "":
			ax.patch.set_facecolor(self.background_color)
		if self.legend == "on":
			ax.legend()

		if self.title != "":
			ax.set_title(self.title.decode('string_escape'))


