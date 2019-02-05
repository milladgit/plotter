
import os, sys
import numpy as np
import matplotlib.pyplot as plt

from configuration import *
from findconfig import *


class Figure(object):

	def __init__(self, filename):
		self.configuration_list = []

		self.subplot = []
		self.figsize = []
		self.output_filename = ""
		self.show_plot = ""

		# For following paramemters, please visit:
		# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html 
		self.subplots_adjust = "off"
		self.subplots_left  = 0.125  
		self.subplots_right = 0.9    
		self.subplots_bottom = 0.1   
		self.subplots_top = 0.9      
		self.subplots_wspace = 0.2   
		self.subplots_hspace = 0.2   

		self.tight_layout = "on"

		self.load_config_file(filename)


	def add_configuration(self, config):
		self.configuration_list.append(config)


	def load_config_file(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		f.close()

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
			elif k == "plot":
				params = v.split(",")
				if len(params) != 2:
					print "The plot field should have two fields: <plot_id> <plot_filename>"
					exit(1)
				plot_id = int(params[0].strip())
				config_filename = params[1].strip()
				C = findconfig(config_filename)
				C.ax_id = plot_id
				self.add_configuration(C)



	def draw(self):
		fig, ax = None, None
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
				i_x = ax_id / self.subplot[0]
				i_y = ax_id % self.subplot[0]
				_ax = ax[i_x, i_y]


			self.configuration_list[i].draw(_ax)



		if self.subplots_adjust == "on":
			plt.subplots_adjust(left=self.subplots_left, right=self.subplots_right, top=self.subplots_top, bottom=self.subplots_bottom, wspace=self.subplots_wspace, hspace=self.subplots_hspace)

		if self.tight_layout == "on":
			plt.tight_layout()
		elif self.tight_layout != "off":
			print "plotter - Unreconized 'tight_layout' value: %s" % (self.tight_layout)
			exit(1)

		if self.output_filename != "":
			plt.savefig(self.output_filename, dpi=800)

		if self.show_plot == "on":
			plt.show()
