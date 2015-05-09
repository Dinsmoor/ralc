#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2014 Tyler Dinsmoor <pappad@airmail.cc>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
try:
	import Tkinter as tk
	import ttk, mapGen
	import collections as col
	from PIL import Image, ImageTk
	import cPickle as pickle
	from libdndGen import *
except ImportError:
	print "You are missing essential Libraries. See README.md"

class AppData(object):
	def __init__(self):
		self.new_data()
		self.loading_compensation = False

	def new_data(self):
		(self.im, self.cityName, self.villageNames,
			self.campNames, self.streets) = mapGen.main('tk')
		self.other_locations = (self.villageNames + self.campNames)
		#mapGen just needs to make maps. Leave getting
		#names and shit to AppData, then tell mapGen what
		#names you want to use as lists.
		print "AppData.new_data.Retrieved Data"

	def save_all(self):
		def save_image():
			self.im.save('save/img','PNG')

		def save_names():
			savef = open('save/name', 'w')
			pickle.dump((self.cityName, self.other_locations,
				self.streets),savef)
			savef.close

		save_image()
		print 'AppData.save_all.Image Saved'
		save_names()
		print 'AppData.save_all.Names Saved'


	def load_all(self):
		def load_image():
			self.im = Image.open('save/img')


		def load_names():
			savef = open('save/name', 'r')
			(self.cityName, self.other_locations,
				self.streets) = pickle.load(savef)
			savef.close

		load_image()
		print 'AppData.load_all.Loaded Image From Disk'
		load_names()
		print 'AppData.load_all.Loaded Names From Disk'
		self.loading_compensation = True
		ui.create_widgets()
		self.loading_compensation = False
		print 'AppData.load_all.Refreshed Widgets'

	def load_photo(self):
		return ImageTk.PhotoImage(self.im)

	def get_tree_data(self):
		return self.other_locations, self.streets



class UI(tk.Frame,AppData):
	def __init__(self, master=None):
		tk.Frame.__init__(self)
		self.frame = tk.Frame(self)
		self.master.title('RALC v0.6')
		self.create_widgets()
		self.grid()
		self.get_photo()

		print "UI.__init__.Done"



	def create_widgets(self):
		def make_menu_bar():
			self.option_add('*tearOff', False)
			self.menubar = tk.Menu(self.master)
			self.filemenu = tk.Menu(self.menubar)
			self.editmenu = tk.Menu(self.menubar)

			self.menubar.add_cascade(label="File", menu=self.filemenu)
			self.menubar.add_cascade(label="About", menu=self.editmenu)
			self.filemenu.add_command(label="New", command=self.new_state)
			self.filemenu.add_command(label="Save", command=dat.save_all)
			self.filemenu.add_command(label="Load", command=self.load_state)
			self.filemenu.add_command(label="Exit", command=self.quit)

			self.tk.call(self.master, "config", "-menu", self.menubar)

			print 'UI.make_menu_bar.Done'

		def make_tree_view():
			self.tree = ttk.Treeview(self, height=25,
				selectmode='browse')
			ysb = ttk.Scrollbar(self, orient='vertical',
				command=self.tree.yview)
			xsb = ttk.Scrollbar(self, orient='horizontal',
				command=self.tree.xview)
			ysb.grid(row=0, column=1, sticky='ns')
			xsb.grid(row=1, column=0, sticky='ew')
			self.tree.heading('#0', text='Name', anchor='w')
			self.tree.column('#0', width=300, anchor='w')
			self.tree.grid(row=0, column=0, sticky='NSEW')

			self.tree.bind("<<TreeviewSelect>>", self.update_details)
			print "UI.make_tree_view.Done"

		def make_details_pane():
			self.details_frame = ttk.Frame(self, borderwidth=2,
				relief="sunken", width=200, height=600)
			self.details = tk.Text(self.details_frame, width=50,
				height=40, state='disabled')

			self.details_frame.grid(row=0, column=4, sticky='N', pady=5)
			self.details.grid(row=0, column=0)

			print "UI.make_details_pane.Done"


		make_tree_view()
		print 'UI.create_widgets.make_tree_view.Done'
		make_menu_bar()
		make_details_pane()
		self.fill_tree()
		print 'UI.create_widgets.make_menu_bar.Done'



	def load_state(self):
		dat.load_all()
		self.create_widgets()
		self.get_photo()
		print 'UI.load_state.Done'

	def new_state(self):
		dat.new_data()
		self.create_widgets()
		self.get_photo()
		print 'UI.new_state.Done'

	def get_photo(self):
		self.img = dat.load_photo()
		self.label = tk.Label(self, image = self.img)
		self.label.grid(column=3, row=0)
		print 'UI.get_photo.Done'

	def fill_tree(self):
		tree_locations, settlement_streets = dat.get_tree_data()
		self.actor_coor={}

		# top level
		city_parent = self.tree.insert('', 'end', text=dat.cityName)
		
		
		for street, bldg_li in settlement_streets.iteritems():
			# add streets
			street_parent = self.tree.insert(city_parent,
					'end', text=street)
			for bldg in bldg_li:
				# add buildgins
				bldg_parent = self.tree.insert(street_parent,
					'end', text=bldg['Purpose'])
				for rooms, roomsdata in bldg.iteritems():
					# add list of rooms
					if rooms != 'Purpose':
						rooms_parent = self.tree.insert(bldg_parent,
						'end', text=rooms)
					if type(roomsdata) == list:
						for room in roomsdata: # list
							
							# ensure that the room type gets parsed first
							room = col.OrderedDict(room)
							tempvalue = room.pop('Actors')
							room['Actors'] = tempvalue
							
							for key, value in room.iteritems(): # dict
								if key == 'Type':
									# add the rooms themselves
									room_parent = self.tree.insert(rooms_parent,
										'end', text=value)
								else:
									# add the name of the actors
									actor_parent = self.tree.insert(room_parent,
									'end', text=key)
									for actor_name, actor_info in value.iteritems():
										#The data of the actor
										actor = self.tree.insert(actor_parent,
										'end', text=actor_name, value=actor_info,
										tags=actor_name)
										self.actor_coor[actor] = actor_info
										
										


		for settlement in tree_locations:
			self.tree.insert('', 'end', text=settlement)
		
		
		print "UI.fill_tree.Done"

	def update_details(self, event):
		try:
			self.details.config(state='normal')
			self.details.delete(1.0, 'end')
			self.details.insert('end',self.actor_coor[self.tree.focus()]['Info'])
			self.details.config(state='disabled')
			print "UI.update_details.Done."
		except KeyError:
			#print "Selected item: %s has no values"%self.tree.focus()
			self.details.config(state='normal')
			self.details.delete(1.0, 'end')
			self.details.insert('end',"Selected item has no values.")
			self.details.config(state='disabled')

	def callback(self, event):
		try:
			neatDicPrint(self.actor_coor[self.tree.focus()])
		except KeyError:
			print "Item has no values"

dat = AppData()
ui = UI()
ui.mainloop()
