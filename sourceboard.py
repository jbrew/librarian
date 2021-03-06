from __future__ import division
import wx
from channel import Channel
from document import Document
from log import Log
import wx.lib.scrolledpanel

class SourceBoard(wx.lib.scrolledpanel.ScrolledPanel):

	def __init__(self,parent,writer,log,channels=[]):

		wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, size=(205,450), pos=(0,28), style=wx.SIMPLE_BORDER)

		self.log = log
		self.writer = writer
		self.channels = channels
		self.colors = [(0,255,0),(0,150,255),(255,0,0),
						(255,255,0),(0,255,255),(255,0,255)]

		self.sbSizer = wx.GridSizer(0, 1, 5, 5)
		self.SetSizer( self.sbSizer )
		for c in self.channels:
			self.addChannel(c)

	def addChannel(self, corpus):
		c = Channel(self, self.writer, corpus, self.log, self.colors[len(self.channels)])
		self.channels.append(c)
		self.sbSizer.Add(c)
		self.sbSizer.Layout()
		self.Layout()
		self.SetupScrolling(scroll_x = False, scroll_y = True)

	def removeChannel(self, c):
		if c in self.channels:
			self.channels.remove(c)
			#self.sbSizer.Remove(c)
			c.Destroy()
		self.sbSizer.Layout()
		self.Layout()

	# removes all channels from this object
	def clear_all_channels(self):
		for c in self.channels:
			self.channels.remove(c)
			self.sbSizer.Remove(c)
			c.Destroy()
		self.sbSizer.Layout()
		self.Layout()

	def refresh(self):
		for c in self.channels:
			c.refresh()
			
	# activates only the given channel
	def set_solo(self, solo_channel):
		for c in self.channels:
			c.weight = 0
			c.wt_slider.SetValue(0)
		solo_channel.weight = 100
		solo_channel.wt_slider.SetValue(100)


	def average_color(self):
		color_list = [(c.color, c.weight) for c in self.channels]
		r_total = 0
		g_total = 0
		b_total = 0
		for color, weight in color_list:
			r, g, b = color
			r_total += r * weight/100
			g_total += g * weight/100
			b_total += b * weight/100

		highest_value = max(r_total, g_total, b_total)
		r_total = r_total/highest_value * 255
		g_total = g_total/highest_value * 255
		b_total = b_total/highest_value * 255
		
		return (r_total, g_total, b_total)