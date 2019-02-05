
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from figure import *
from configuration import *
from utils import *



class LinePlot(Configuration):

	def __init__(self, filename):
		Configuration.__init__(self, filename)

		self.xaxis_datatype = ""
		self.datatype = "float"
		self.line_styles = []
		self.data_x = []
		self.data_y = dict()

		self.load_config_file(filename)



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


			if k == "line_styles":
				self.line_styles = v.split(",")
				self.line_styles = [q.strip() for q in self.line_styles]
			elif k == "datatype":
				self.datatype = v
			elif "data_" in k:
				index = int(k.split("_")[1])
				data_list = v.split(",")
				data_list = [q.strip() for q in data_list]

				if self.datatype == "float":
					data_list = [float(q) for q in data_list]
				elif self.datatype == "int":
					data_list = [int(q) for q in data_list]

				self.data_y[index] = data_list
				self.data_x = self.xticks_label

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

					self.data_x.append(l[0].strip())
					for _v in range(column_count):
						if _v not in self.data_y:
							self.data_y[_v] = []
						val = l[_v+1].strip()
						if self.datatype == "float":
							val = float(val)
						elif self.datatype == "int":
							val = int(val)
						self.data_y[_v].append(val)
					i += 1


				i += 1

		if self.xaxis_datatype == "int":
			self.data_x = [int(q) for q in self.data_x]
		elif self.xaxis_datatype == "float":
			self.data_x = [float(q) for q in self.data_x]

		print self.data_x
		print self.data_y



	def draw(self, ax):

		for series_index, series_data_vector in self.data_y.items():
			if len(self.colors) > 0:
				ax.plot(self.data_x, series_data_vector, self.line_styles[series_index], color=self.colors[series_index])
			else:
				ax.plot(self.data_x, series_data_vector, self.line_styles[series_index])


		ax.set_xticks(self.data_x)
		ax.set_xticklabels(self.data_x, rotation=self.xticks_rotation)

		super(LinePlot, self).draw(ax)


