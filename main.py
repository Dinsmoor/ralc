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
otherlist=('name3','name4')
testlist=('name','name2','name3','name4','name5','name6',otherlist)

pcdata={
	'name0':'billy',
	'name1':'mandy'
	}
bldgdata={
	'name':'bldg0',
	'inhabitants':pcdata
	}
testdata=testlist
#testdata={
#	'bldg':testlist,
#	'bldg1':bldgdata['inhabitants']
#	}

import Tkinter as tk
import ttk, mapGen, ImageTk, Image


class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.im,self.cityName = mapGen.main('tk')
		self.makeMenuBar()
		self.createWidgets()
		
		

		self.grid()
	
	def makeMenuBar(self):
		self.menubar = tk.Menu(self)
		self.menubar.add_command(label="Quit!", command=self.quit)
		self.menubar.add_cascade(label="File", menu=self.menubar)
	
	def createWidgets(self):
		def makeQuitButton():
			self.quitButton = tk.Button(self, text="Quit",
			command=self.quit)
			self.quitButton.grid(sticky='n', column=2, row=1, padx=10)
		def makeShowButton():
			# needs to try to load image for whatever is highlighted in
			# the treeview
			self.showButton = tk.Button(self, text="Show",
			command=loadPhoto)
			self.showButton.grid(sticky='n', column=2, row=0, padx=10,pady=40)
		def makeTreeView():
			self.tree = ttk.Treeview(self, height=25, selectmode='browse')
			ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
			xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
			
			self.tree.heading('#0', text='Name', anchor='w')
			
			root_node = self.tree.insert('', 'end', text=self.cityName, open=True)
			
			self.addDataToTree(root_node)
			self.tree.grid(row=0, column=0)
			ysb.grid(row=0, column=1, sticky='ns')
			xsb.grid(row=1, column=0, sticky='ew')
			
			#self.tree.bind('<<TreeviewSelect>>', self.loadPhoto(''))
		def loadPhoto():
			# grabs image from mapGen, makes it Tk-compatible, puts it in
			# the grid.
			#print event
			self.img = ImageTk.PhotoImage(self.im)
			self.label = tk.Label(image = self.img)
			self.label.grid(sticky='E', column=3, row=0)
		
		makeTreeView()
		makeQuitButton()
		makeShowButton()
		
	def addDataToTree(self, parent):
		for itm in testdata:				
			self.tree.insert(parent, 'end', text=itm)
	
	
	

def main():
	app = Application()
	app.master.title('RALC v0.1')
	app.mainloop()

if __name__ == '__main__':
    main()
