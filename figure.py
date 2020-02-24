
import os, sys
import numpy as np
import matplotlib.pyplot as plt

from configuration import *
from findconfig import *


class Figure(object):

	def __init__(self, filename):
		self.configuration_list = []

		self.subplot = []
		self.figsize = [8,6]
		self.output_filename = ""
		self.show_plot = ""

		# For following paramemters, please visit:
		# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html 
		self.subplots_adjust_left  = ""
		self.subplots_adjust_right = ""    
		self.subplots_adjust_bottom = ""   
		self.subplots_adjust_top = ""    
		self.subplots_adjust_wspace = ""
		self.subplots_adjust_hspace = "" 

		self.tight_layout = "on"

		self.dpi = 800

		self.lines = None

		self.load_config_file(filename)


	def add_configuration(self, config):
		self.configuration_list.append(config)

	def findspans(self, params):
		colspan = rowspan = 1
		spans_to_check = []

		if len(params) == 4:
			span = params[2]
			spans_to_check.append(span)
		elif len(params) == 5:
			span = params[2]
			spans_to_check.append(span)
			span = params[3]
			spans_to_check.append(span)

		for span in spans_to_check:
			spanlist = span.split("=")
			if spanlist[0] == "colspan":
				colspan = int(spanlist[1])
			elif spanlist[1] == "rowspan":
				rowspan = int(spanlist[1])
		return rowspan, colspan


	def load_config_file(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		f.close()

		self.lines = lines

		for L in lines:
			l = L.strip()
			if l == "":
				continue
			if l[0] == "#":
				continue
			l = l.split(":")

			k = l[0]
			v = l[1]

			k = k.strip()
			v = v.strip()


			if k == "output_filename":
				self.output_filename = v
			elif k == "show_plot":
				self.show_plot = v
			elif k == "subplot":
				self.subplot = v.split(",")
				self.subplot = [int(q.strip()) for q in self.subplot]
			elif k == "figsize":
				self.figsize = v.split(",")
				self.figsize = [int(q.strip()) for q in self.figsize]
			elif k == "tight_layout":
				self.tight_layout = v
			elif k == "subplots_adjust_left":
				self.subplots_adjust_left = v
			elif k == "subplots_adjust_right":
				self.subplots_adjust_right = v
			elif k == "subplots_adjust_top":
				self.subplots_adjust_top = v
			elif k == "subplots_adjust_bottom":
				self.subplots_adjust_bottom = v
			elif k == "subplots_adjust_wspace":
				self.subplots_adjust_wspace = v
			elif k == "subplots_adjust_hspace":
				self.subplots_adjust_hspace = v
			elif k == "dpi":
				if v in ["None", "none", "0"]:
					self.dpi = None
				else:
					self.dpi = int(v)
			elif k == "plot":
				params = v.split(",")
				if len(params) < 3:
					print "The plot field should have following format: <plot_row_num>, <plot_col_num>, [colspan=x, rowspan=y,] <plot_filename>"
					exit(1)
				# plot_id = int(params[0].strip())
				# config_filename = params[-1].strip()
				# if config_filename == "off":
				# 	C = Configuration("")
				# 	C.ax_id = plot_id
				# 	C.turn_off = True
				# else:
				# 	C = findconfig(config_filename)
				# 	C.ax_id = plot_id
				params = [p.strip() for p in params]
				ax_row_id = int(params[0])
				ax_col_id = int(params[1])
				config_filename = params[-1].strip()
				rowspan, colspan = self.findspans(params)
				C = None
				if config_filename == "off":
					C = Configuration("")
					C.turn_off = True
				else:
					C = findconfig(config_filename)
				C.ax_row_id = ax_row_id
				C.ax_col_id = ax_col_id
				C.ax_row_span = rowspan
				C.ax_col_span = colspan
				self.add_configuration(C)


	def draw_axes_obselete(self):
		if len(self.figsize) == 2:
			fig, ax = plt.subplots(self.subplot[0], self.subplot[1], figsize=(self.figsize[0], self.figsize[1]))
		elif len(self.subplot) == 2:
			fig, ax = plt.subplots(self.subplot[0], self.subplot[1])
		else:
			fig, ax = plt.subplots()


		for i in range(len(self.configuration_list)):

			_ax = None
			if self.subplot[0] == 1 and self.subplot[1] == 1:
				_ax = ax
			elif self.subplot[0] == 1 or self.subplot[1] == 1:
				_ax = ax[self.configuration_list[i].ax_id]
			else:
				ax_id = self.configuration_list[i].ax_id
				i_x = ax_id / self.subplot[1]
				i_y = ax_id % self.subplot[1]
				_ax = ax[i_x, i_y]


			if self.configuration_list[i].turn_off:
				_ax.axis("off")
			else:
				self.configuration_list[i].draw(_ax)


	def draw_axes(self):
		fig = plt.figure(figsize=(self.figsize[0], self.figsize[1]))
		for i, C in enumerate(self.configuration_list):
			ax = plt.subplot2grid((self.subplot[0], self.subplot[1]), (C.ax_row_id, C.ax_col_id), fig=fig, colspan=C.ax_col_span, rowspan=C.ax_row_span)
			if C.turn_off:
				ax.axis("off")
			else:
				C.draw(ax)


	def draw(self):
		fig, ax = None, None

		#self.draw_axes_obselete()
		self.draw_axes()
		
		if self.tight_layout == "on":
			plt.tight_layout()
		elif self.tight_layout != "off":
			print "plotter - Unreconized 'tight_layout' value: %s" % (self.tight_layout)
			exit(1)

		if self.subplots_adjust_left != "":
			plt.subplots_adjust(left=float(self.subplots_adjust_left))
		if self.subplots_adjust_right != "":
			plt.subplots_adjust(right=float(self.subplots_adjust_right))
		if self.subplots_adjust_top != "":
			plt.subplots_adjust(top=float(self.subplots_adjust_top))
		if self.subplots_adjust_bottom != "":
			plt.subplots_adjust(bottom=float(self.subplots_adjust_bottom))
		if self.subplots_adjust_wspace != "":
			plt.subplots_adjust(wspace=float(self.subplots_adjust_wspace))
		if self.subplots_adjust_hspace != "":
			plt.subplots_adjust(hspace=float(self.subplots_adjust_hspace))

		if self.output_filename != "":
			plt.savefig(self.output_filename, dpi=self.dpi)

		if self.show_plot == "on":
			plt.show()
