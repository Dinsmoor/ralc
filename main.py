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


pcdata={
	'name0':'billy',
	'name1':'mandy'
	}
bldgdata={
	'name':'bldg0',
	'inhabitants':pcdata
	}
testdata={
	'bldg':bldgdata['name'],
	'bldg1':bldgdata['inhabitants']
	}

import Tkinter as tk
import ttk

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		
		self.tree = ttk.Treeview(self)
		ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
		xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
		self.tree.heading('#0', text='Name', anchor='w')
		
		root_node = self.tree.insert('', 'end', text='Name', open=True)
		
		self.addDataToTree(root_node)
		
		self.tree.grid(row=0, column=0)
		ysb.grid(row=0, column=1, sticky='ns')
		xsb.grid(row=1, column=0, sticky='ew')
		self.grid()
	
	def createWidgets(self):
		self.quitButton = tk.Button(self, text="Quit",
			command=self.quit)
			
		self.quitButton.grid()
		
	def addDataToTree(self, parent):
		self.tree.column('#0')
		self.tree.heading('#0',text='ID')
		for itm in testdata:
			self.tree.insert(parent, 'end', text=itm)


def main():
	app = Application()
	app.master.title('RALC v0.1')
	app.mainloop()

if __name__ == '__main__':
    main()
