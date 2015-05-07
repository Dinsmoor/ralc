#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2014 Tyler Dinsmoor <d@D-LM>
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
	from PIL import Image, ImageTk
	import cPickle as pickle
except ImportError:
	print "You are missing essential Libraries. See README.md"

class AppData(object):
	def __init__(self):
		self.new_data()

	def new_data(self):
		(self.im, self.cityName, self.villageNames,
			self.campNames, self.streets) = mapGen.main('tk')
		#mapGen just needs to make maps. Leave getting
		#names and shit to AppData, then tell mapGen what
		#names you want to use as lists.
		print "AppData.new_data.Retrieved Data"

	def save_all(self):
		def save_image():
			self.im.save('save/img','PNG')

		def save_names():
			savef = open('save/name', 'w')
			pickle.dump((self.cityName, self.villageNames,
				self.campNames),savef)
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
			(self.cityName, self.villageNames,
				self.campNames) = pickle.load(savef)
			savef.close

		load_image()
		print 'AppData.load_all.Loaded Image From Disk'
		load_names()
		print 'AppData.load_all.Loaded Names From Disk'
		ui.create_widgets()
		print 'AppData.load_all.Refreshed Widgets'

	def load_photo(self):
		return ImageTk.PhotoImage(self.im)

	def get_tree_data(self):
		return (self.villageNames + self.campNames, self.streets)



class UI(tk.Frame,AppData):
	def __init__(self, master=None):
		tk.Frame.__init__(self)
		self.frame = tk.Frame(self)
		#self.master = master
		#self.win = tk.Toplevel(self.master)
		self.master.title('RALC v0.3')
		self.create_widgets()
		self.grid()
		self.get_photo()

		self.grid()

		print "UI.__init__.Done"



	def create_widgets(self):
		def make_menu_bar():
			self.option_add('*tearOff', False)
			self.menubar = tk.Menu(self.master)
			self.filemenu = tk.Menu(self.menubar)
			self.editmenu = tk.Menu(self.menubar)

			self.menubar.add_cascade(label="File", menu=self.filemenu)
			self.menubar.add_cascade(label="Edit", menu=self.editmenu)
			self.filemenu.add_command(label="New", command=self.new_state)
			self.filemenu.add_command(label="Save", command=dat.save_all)
			self.filemenu.add_command(label="Load", command=self.load_state)
			self.filemenu.add_command(label="Exit", command=self.quit)

			self.tk.call(self.master, "config", "-menu", self.menubar)

			print 'UI.make_menu_bar.Done'

		def make_tree_view():
			self.tree = ttk.Treeview(self, height=28,
				selectmode='browse', columns=('pop'))
			ysb = ttk.Scrollbar(self, orient='vertical',
				command=self.tree.yview)
			xsb = ttk.Scrollbar(self, orient='horizontal',
				command=self.tree.xview)
			ysb.grid(row=0, column=1, sticky='ns')
			xsb.grid(row=1, column=0, sticky='ew')
			self.tree.heading('#0', text='Name', anchor='w')
			self.tree.heading('pop', text='Population', anchor='w')
			self.tree.column('pop', stretch=0, width=80)
			self.tree.grid(row=0, column=0, sticky='NSEW')

			#self.tree.bind("<<TreeviewOpen>>", self.update_tree)
			self.tree.bind("<<TreeviewSelect>>", self.callback)
			#self.tree.insert('', 'end', text=dat.cityName, open=True)




		make_tree_view()
		print 'UI.create_widgets.make_tree_view.Done'
		make_menu_bar()
		self.fill_tree('')
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
		self.label = tk.Label(image = self.img)
		self.label.grid(sticky='E', column=3, row=0)
		print 'UI.get_photo.Done'

	def fill_tree(self, parent):
		tree_locations, settlement_streets = dat.get_tree_data()
		#for street, bldgs in self.streets.iteritems():
		#	print bldgs[0]['Rooms'][0][0]['Actors'][0]['Name']
		city_icon = ImageTk.PhotoImage(Image.open("data/sprites/city.png"))

		city_parent = self.tree.insert('', 'end', text=dat.cityName,
				open=False, image=city_icon)

		for street, bldgs in settlement_streets.iteritems():
			street_parent = self.tree.insert(city_parent,
					'end', text=street)
			for bldg in bldgs:
				bldg_parent = self.tree.insert(street_parent,
						'end', text=bldg['Purpose'])
				for room, roomdat in bldg.iteritems():

					room_parent = self.tree.insert(bldg_parent,
						'end', text=roomdat["Actors"])#[0][0]['Actors'])

		for settlement in tree_locations:
			self.tree.insert('', 'end', text=settlement)

	def update_tree(self, item):
		pass

	def callback(self, event):
		print "Callback:", event
		print "Selection", self.tree.selection()

dat = AppData()
ui = UI()


ui.mainloop()

