
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from figure import *
from configuration import *
from utils import *


# Help from this URL: 
# https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

# For all colormaps in the matplotlib, please refer to this link:
# https://matplotlib.org/tutorials/colors/colormaps.html

class HeatmapPlot(Configuration):

	def __init__(self, filename):
		Configuration.__init__(self, filename)

		self.datatype = "float"
		self.column_names = []
		self.row_names = []
		self.values = []

		self.colormap = "plasma"
		self.colorbar_label = ""

		self.show_values_in_box = "off"
		self.show_values_in_box_font = "8"

		self.square_boxes = "on" # for aspect ration of boxes

		self.load_config_file()


	
	def load_config_file(self):

		if self.lines == None:
			return

		lines = self.lines

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


			if k == "datatype":
				self.datatype = v
			elif k == "square_boxes":
				self.square_boxes = v
			elif k == "colormap":
				self.colormap = v
			elif k == "colorbar_label":
				self.colorbar_label = v
			elif k == "show_values_in_box":
				self.show_values_in_box = v
			elif "data" in k: 
				# row_count = v.split(":")
				# if len(row_count) != 1:
				# 	print "Please provide number of rows as following: 'data: <row_count>'"
				# 	exit(1)

				# row_count = int(row_count[0])

				col = lines[i].strip().split(":")
				i += 1
				if col[0] != "columns":
					print "Please provide the columns name."
					exit(1)
				col = col[1].split(",")

				self.column_names = [c.strip() for c in col]

				while i < lines_count:
					l = lines[i].strip()
					if l == "":
						i += 1
						continue
					if l[0] == "#":
						i += 1
						continue
					l = l.split(":")
					self.row_names.append(l[0].strip())
					values = l[1].split(",")
					if self.datatype == "float":
						values = [float(v) for v in values]
					elif self.datatype == "int":
						values = [int(v) for v in values]

					self.values.append(values)

					i += 1


				i += 1





	def draw(self, ax):

		hmap = np.array(self.values)
		# hmap = self.values
		aspect = "equal"
		if self.square_boxes == "off":
			aspect = "auto"
		im = ax.imshow(hmap, self.colormap, aspect=aspect)
		# im = ax.pcolor(hmap,cmap=self.colormap)


		# Create colorbar
		cbar = ax.figure.colorbar(im, ax=ax)
		if self.colorbar_label != "":
			cbar.ax.set_ylabel(self.colorbar_label, rotation=-90, va="bottom")


		ax.set_xticks(np.arange(len(self.column_names)))
		ax.set_yticks(np.arange(len(self.row_names)))

		# Setting the labels and locations of ticks on x and y manually
		# n = len(self.column_names)
		# ax.set_xticks(np.linspace(.5,1.7,4))
		# n = len(self.row_names)
		# ax.set_yticks(np.linspace(.5,n*0.4+0.5,n))


		ax.set_xticklabels(self.column_names, fontsize=self.xticks_label_fontsize)
		ax.set_yticklabels(self.row_names, fontsize=self.yticks_label_fontsize)



		if self.xticks_rotation != "":
			plt.setp(ax.get_xticklabels(), rotation=float(self.xticks_rotation), ha="right", rotation_mode="anchor")

		# Let the horizontal axes labeling appear on top.
		# ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

		if self.show_values_in_box == "on":
			for i in range(len(self.row_names)):
				for j in range(len(self.column_names)):
					text = ax.text(j, i, hmap[i, j], ha="center", va="center", color="w", fontsize=self.show_values_in_box_font)

		# ax.tick_params(which="minor", bottom=False, left=False)
		# ax.grid(which="minor", color="w", linestyle='-', linewidth=3)

		super(HeatmapPlot, self).draw(ax)




