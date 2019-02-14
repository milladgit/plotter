
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from figure import *
from configuration import *
from utils import *



class BarPlot(Configuration):

	def __init__(self, filename):
		Configuration.__init__(self, filename)

		self.put_label_on_top = "off"
		self.datatype = "float"
		self.bar_count = 0
		self.data_dict = dict()
		self.data_indexes = []

		self.index_begin = 0.0
		self.index_step = 0.1

		self.load_config_file(filename)


	
	def index_generator(self, begin, step, count):
		return np.arange(begin, begin + step * count, step)


	def load_config_file(self, filename):
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

			k = l[0]
			v = l[1]

			k = k.strip()
			v = v.strip()


			if k == "put_label_on_top":
				self.put_label_on_top = v
			elif k == "datatype":
				self.datatype = v
			elif k == "bar_count":
				self.bar_count = int(v)
			elif k == "index_begin":
				self.index_begin = isfloat(v)
			elif k == "index_step":
				self.index_step = isfloat(v)
			elif "data_" in k:
				index = int(k.split("_")[1])
				data_list = v.split(",")
				data_list = [q.strip() for q in data_list]

				if self.datatype == "float":
					data_list = [float(q) for q in data_list]
				elif self.datatype == "int":
					data_list = [int(q) for q in data_list]

				self.data_dict[index] = data_list
			elif "datatable" in k: 
				column_count = int(v)
				while i < lines_count:
					l = lines[i].strip()
					if l == "":
						i += 1
						continue
					if l[0] == "#":
						i += 1
						continue
					l = l.split(";")
					self.xticks_label.append(l[0].strip())
					for _v in range(column_count):
						if _v not in self.data_dict:
							self.data_dict[_v] = []
						val = l[_v+1].strip()
						if self.datatype == "float":
							val = float(val)
						elif self.datatype == "int":
							val = int(val)
						self.data_dict[_v].append(val)
					i += 1

				i += 1






	def autolabel(self, ax, rects, xpos='center'):
		"""
		Attach a text label above each bar in *rects*, displaying its height.

		*xpos* indicates which side to place the text w.r.t. the center of
		the bar. It can be one of the following {'center', 'right', 'left'}.
		"""

		xpos = xpos.lower()  # normalize the case of the parameter
		ha = {'center': 'center', 'right': 'left', 'left': 'right'}
		offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

		for rect in rects:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
					'{}'.format(height), ha=ha[xpos], va='bottom')



	def draw(self, ax):

		C = self
		ind = self.index_generator(self.index_begin, self.index_step, len(self.data_dict[0]))
		width = C.width  # the width of the bars

		rects_list = list()

		if C.bar_count == 1:
			index = 0
			rect = ax.bar(ind, C.data_dict[index], width, color=C.colors[index], label=C.labels[index])
			rects_list.append(rect)
		else:
			# index = 0
			# rect = ax.bar(ind - width/2, C.data_dict[index], width, color=C.colors[index], label=C.labels[index])
			# rects_list.append(rect)
			# index = 1
			# rect = ax.bar(ind + width/2, C.data_dict[index], width, color=C.colors[index], label=C.labels[index])
			# rects_list.append(rect)
			for index in range(C.bar_count):
				disposition = -width*C.bar_count/2.0 + index*width + width/2.0
				if len(C.colors) > 0:
					rect = ax.bar(ind + disposition, C.data_dict[index], width, color=C.colors[index], label=C.labels[index])
				else:
					rect = ax.bar(ind + disposition, C.data_dict[index], width, label=C.labels[index])
				rects_list.append(rect)


		ax.set_xticks(ind)
		_ha = "right"
		if C.xticks_rotation in [0, 90]:
			_ha = "center"
		ax.set_xticklabels(C.xticks_label, rotation=C.xticks_rotation, ha=_ha)


		if C.put_label_on_top == "on":
			for r in rects_list:
				self.autolabel(ax, r, "left")
				# autolabel(rects2, "right")

		super(BarPlot, self).draw(ax)


