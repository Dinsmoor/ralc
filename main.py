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
RALC_VERSION = 'Beta v0.66'
DEBUG = True
try:
    import Tkinter as tk
    import tkMessageBox
    import ttk
    import dialogs
    import mapGen
    import collections as col
    from PIL import Image, ImageTk
    import cPickle as pickle
    import itemGen
    import os
    import random
except ImportError:
    import tkMessageBox

    tkMessageBox.showerror(
        "Error", "You are missing essential Libraries. See README.md")
    print "You are missing essential Libraries. See README.md"
    exit()


####################

class UI(tk.Frame):
    """
	Class that describes the UI and how the information is formatted.
	"""

    def __init__(self):

        self.init_dir()
        tk.Frame.__init__(self)
        self.settings = self.init_settings()
        self.image_frame = tk.Frame(self)
        self.master.title('RALC %s' % RALC_VERSION)

        self.actor_coor = dict()
        self.town_coor = dict()
        self.city_coor = dict()
        self.wep_coor = dict()
        self.arm_coor = dict()
        self.click_coor = dict()
        self.photo_coor = dict()

        print "UI.__init__.Starting"
        self.first_run = True
        self.create_widgets()
        print "UI.__init__.Done"

    ####
    # Data Gathering
    ####

    @staticmethod
    def init_settings():
        import def_settings
        return def_settings.get_def_settings()

    @staticmethod
    def init_dir():

        dir_list = os.listdir('.')
        if 'save' not in dir_list:
            os.makedirs('save')
        if 'data' not in dir_list:
            tkMessageBox.showerror(
                "Error", "You are missing your data folder.")
            exit()

    def new_data(self):
        self.create_widgets()
        self.new_button.destroy()
        self.grid()
        (self.city_im, self.cityName,
         self.towns) = mapGen.main('tk', self.settings)

        self.get_photo()
        self.fill_tree()
        self.image_frame.grid(row=0, column=2)
        print "UI.new_data.Retrieved Data"

    @staticmethod
    def new_items(item_type):

        if item_type == 'wep':
            return itemGen.main('wep', 'rnd')

    def save_all(self, save_name):

        def make_dir():
            if not os.path.exists('save/%s' % save_name):
                os.makedirs('save/%s' % save_name)

        def save_images():
            self.city_im.save('save/%s/img' % save_name, 'PNG')

        def save_names():
            savef = open('save/%s/name' % save_name, 'w')
            pickle.dump((self.cityName,
                         self.towns), savef)
            savef.close()

        make_dir()
        save_images()
        print 'UI.save_all.Image Saved'
        save_names()
        print 'UI.save_all.Names Saved'

    def load_all(self, load_name):

        """
		Ensures that the save name to load is valid, then loads the
		associated content and refreshes widgets.
		"""

        def check_dir():

            if os.path.exists('save/%s' % load_name):
                return 1

        def load_image():

            self.city_im = Image.open('save/%s/img' % load_name)

        def load_names():

            savef = open('save/%s/name' % load_name, 'r')
            (self.cityName,
             self.towns) = pickle.load(savef)
            savef.close()

        if check_dir():
            load_image()
            print 'UI.load_all.Loaded Image From Disk'
            load_names()
            print 'UI.load_all.Loaded Names From Disk'
            self.grid()
            self.new_button.destroy()
            self.create_widgets()
            self.get_photo()
            self.fill_tree()
            self.image_frame.grid(row=0, column=2)
            print 'UI.load_all.Refreshed Widgets'
        else:
            print 'UI.load_all.Failed[NO FOLDER PRESENT]'

            ##########
            # UI Init
            ##########

    def create_widgets(self):

        """
		Creates menu bar, tree view and details pane.
		"""

        def make_initial_button():
            """
			Used as quick options to access things that would normally
			be in the file menu when starting application.
			"""
            if self.first_run:
                self.new_button = tk.Button(text="New",
                                            padx=70, pady=30, command=self.new_data)
                self.new_button.grid()
                self.first_run = False

        def make_menu_bar():
            """
			Used for callbacks, instrumental for loading/saving and
			accessing the tools/about menus. Will feature many other
			tools later.
			"""
            self.option_add('*tearOff', False)
            self.menubar = tk.Menu(self.master)
            self.filemenu = tk.Menu(self.menubar)
            self.editmenu = tk.Menu(self.menubar)
            self.toolmenu = tk.Menu(self.menubar)
            self.infomenu = tk.Menu(self.menubar)

            self.menubar.add_cascade(label="File", menu=self.filemenu)
            self.filemenu.add_command(label="New", command=self.new_data)
            self.filemenu.add_command(label="Save", command=self.create_save_dialog)
            self.filemenu.add_command(label="Load", command=self.create_load_dialog)
            self.filemenu.add_command(label="Exit", command=self.quit)

            self.menubar.add_cascade(label="Edit", menu=self.editmenu)
            self.editmenu.add_command(label="Settings", command=self.create_settings_menu)

            self.menubar.add_cascade(label="Tools", menu=self.toolmenu)
            self.toolmenu.add_command(label="Char Sheet", command=self.create_char_sheet_dialog)

            self.menubar.add_cascade(label="Info", menu=self.infomenu)
            self.infomenu.add_command(label="About", command=self.create_about_dialog)

            self.tk.call(self.master, "config", "-menu", self.menubar)

            print 'UI.make_menu_bar.Done'

        def make_tree_view():
            """
			Defines tree instance for use later in fill_tree
			"""

            self.tree = ttk.Treeview(self, height=25,
                                     selectmode='browse')
            ysb = ttk.Scrollbar(self, orient='vertical',
                                command=self.tree.yview)
            ysb.grid(row=0, column=1, sticky='ns')
            self.tree.heading('#0', text='Name', anchor='w')
            self.tree.column('#0', width=300, anchor='w')
            self.tree.grid(row=0, column=0, sticky='NSEW')

            self.tree.bind("<<TreeviewSelect>>", self.update_ui)
            print "UI.make_tree_view.Done"

        def make_details_pane():
            """
			Defines first instance of the details pane.
			"""

            self.details_frame = ttk.Frame(self, borderwidth=2,
                                           relief="sunken", width=200, height=600)
            self.details = tk.Text(self.details_frame, width=50,
                                   height=40, state='disabled')

            self.details_frame.grid(row=0, column=4, sticky='N', pady=5)
            self.details.grid(row=0, column=0)

            print "UI.make_details_pane.Done"

        make_menu_bar()
        make_tree_view()
        make_details_pane()
        make_initial_button()

    @staticmethod
    def create_about_dialog():
        info_text = '''
RALC %s

Authored by:
Tyler Dinsmoor - (pappad@airmail.cc)
Madii Salazar - (madison.m.salazar@gmail.com)

Source:
https://github.com/Dinsmoor/ralc

Licenced under GNU GPLv2+
https://www.gnu.org/licenses/gpl-2.0.html
		''' % RALC_VERSION

        tkMessageBox.showinfo(
            "About", info_text)

    def create_load_dialog(self):

        """
		Interior handler for an external class
		"""

        dialogs.LoadDialog(self)

    def create_settings_menu(self):

        print self.settings
        dialogs.SettingsMenu(self)
        print self.settings

    def create_save_dialog(self):

        """
		Interior handler for an external class
		"""

        dialogs.SaveDialog(self)

    def create_char_sheet_dialog(self):

        """
		Interior handler for an external class
		"""

        dialogs.CharSheetGen(self)

    def get_photo(self, im_coor=None):

        """
		Converts PIL/PNG image into a Tk-compatible image type, creates
		a canvas that has a clickable surface that is able to select
		settlements using a callback to city_map_select.
		"""

        self.img = ImageTk.PhotoImage(self.city_im)

        photos = self.photo_coor.iterkeys()

        if im_coor in photos:
            self.img = ImageTk.PhotoImage(self.photo_coor[im_coor])

        self.canvas = tk.Canvas(self.image_frame, background='grey',
                                width=600, height=600)
        self.canvas.grid(row=0, column=0)
        self.canvas.create_image(301, 301, state='normal', image=self.img)
        self.canvas.bind('<Button>', self.city_map_select)
        print 'UI.get_photo.Done'

    def fill_tree(self):

        """
		Fills tree with data and configs.
		"""
        # c is to prevent addressing errors with ttk.Treeview's limited number of items,
        # preventing all sorts of wonky issues.
        c = 1
        for city_dic in self.towns:
            # Prevent overcounting population by resetting the population
            # to 0 every iteration of population

            city_dic['Population'] = 0
            if city_dic['Name'] == self.cityName:
                city_parent = self.tree.insert('',
                                               0,
                                               iid=c,
                                               text=city_dic['Name'])
                c += 1
                # Add click data to correlation dictionary
                # Give a blank separator for aesthetics
                self.tree.insert('',
                                 1,
                                 iid=c,)
                c += 1
                self.click_coor[city_parent] = city_dic['click_area']
            elif city_dic['Type'] == 'Cave':
                city_parent = self.tree.insert('',
                                               'end',
                                               iid=c,
                                               text=city_dic['Name'])
                c += 1
                self.click_coor[city_parent] = city_dic['click_area']
            else:
                # Same as above, except the blank line
                city_parent = self.tree.insert('',
                                               'end',
                                               iid=c,
                                               text=city_dic['Name'])
                c += 1
                self.click_coor[city_parent] = city_dic['click_area']

            for city_key, city_info in city_dic.iteritems():
                if city_dic['Type'] == 'Cave':
                    break
                # There is other information, such as 'Name' and others,
                # however we only need to populate from the information
                # further down the chain
                if city_key == 'Data':
                    for street, bldg_li in city_info.iteritems():
                        # add streets to the listing
                        street_parent = self.tree.insert(city_parent,
                                                         'end',
                                                         iid=c,
                                                         text=street,
                                                         tags=street)
                        c+=1
                        for bldg in bldg_li:
                            # add buildings to streets, listed by purpose
                            bldg_parent = self.tree.insert(street_parent,
                                                           'end',
                                                           iid=c,
                                                           text=bldg['Name'])
                            c+=1
                            for rooms, roomsdata in bldg.iteritems():
                                # add list of rooms
                                if type(roomsdata) == list:
                                    for room in roomsdata:  # list
                                        # ensure that the room type gets parsed first
                                        room = col.OrderedDict(room)
                                        tempvalue = room.pop('Actors')
                                        room['Actors'] = tempvalue
                                        tempvalue = room.pop('Weapons')
                                        room['Weapons'] = tempvalue
                                        tempvalue = room.pop('Armor')
                                        room['Armor'] = tempvalue

                                        for key, value in room.iteritems():  # dict
                                            if key == 'Type':
                                                # add the rooms themselves
                                                room_parent = self.tree.insert(bldg_parent,
                                                                               'end',
                                                                               iid=c,
                                                                               text=value)
                                                c+=1

                                            if key == 'Actors':
                                                if room['Actors']:
                                                    # add the name of the actors
                                                    actor_parent = self.tree.insert(room_parent,
                                                                                    'end',
                                                                                    iid=c,
                                                                                    text=key)
                                                    c+=1
                                                    for actor_name, actor_info in value.iteritems():
                                                        if city_dic['Name'] == self.cityName:
                                                            city_dic['Population'] += 1
                                                        else:
                                                            city_dic['Population'] += 1
                                                        # The data of the actor
                                                        actor = self.tree.insert(actor_parent,
                                                                                 'end',
                                                                                 iid=c,
                                                                                 text=actor_name,
                                                                                 value=actor_info,
                                                                                 tags=actor_name)
                                                        c+=1

                                                        self.actor_coor[actor] = actor_info

                                            if key == 'Weapons':
                                                wep_items_parent = self.tree.insert(room_parent,
                                                                                    'end',
                                                                                    iid=c,
                                                                                    text='Weapons')
                                                c+=1
                                                for item_dict in value:
                                                    item = self.tree.insert(wep_items_parent,
                                                                            'end',
                                                                            iid=c,
                                                                            text=item_dict['Name'])
                                                    c+=1

                                                    self.wep_coor[item] = item_dict

                                            if key == 'Armor':
                                                armor_items_parent = self.tree.insert(room_parent,
                                                                                      'end',
                                                                                      iid=c,
                                                                                      text='Armor')
                                                c+=1
                                                for item_dict in value:
                                                    item = self.tree.insert(armor_items_parent,
                                                                            'end',
                                                                            iid=c,
                                                                            text=item_dict['Name'])
                                                    c+=1

                                                    self.arm_coor[item] = item_dict

                                            self.town_coor[city_parent] = self.make_town_metadata(city_dic)

    @staticmethod
    def make_armor_metadata(arm):

        desc = '''
Name:	%s
Type:	%s
Cost:	%s
AC:	%s
		''' % (arm['Name'], arm['Type'],
               arm['Cost'], arm['AC'])
        return desc

    @staticmethod
    def make_weapon_metadata(wep):

        desc = '''
Name:	%s
Hit Die:	%s
Damage Type:	%s
Weapon Class:	%s
Weapon Type:	%s
		''' % (wep['Name'], wep['Hit Die'], wep['Damage Type'],
               wep['Weapon Class'], wep['Weapon Type'])
        return desc

    def make_town_metadata(self, town):
        desc = '''
Name:	%s
Type:	%s
Population:	%d
Distance:	%skm to %s.
		''' % (town['Name'], town['Type'],
               town['Population'],
               town['Distance'], self.cityName)
        return desc

    ####
    # Callbacks
    ####

    def draw_select_ring(self, bbox):
        try:
            self.canvas.delete(self.selection_indicator)
        except AttributeError as err:
            if DEBUG:
                print err

        self.selection_indicator = self.canvas.create_rectangle(
            bbox[0], bbox[1] + 20, bbox[0] + 20, bbox[1],
            outline='red', width=2)

    def update_ui(self, event):
        try:
            self.get_photo(event)
            self.update_details(event)
        except Exception as err:
            if DEBUG:
                print err

    def update_details(self, event):

        """
		Since multiple types fo data will be updated, it inspects various
		data sources and just plugs in whatever is applicible. Kind of dumb,
		but works. Otherwise will just empty the text box.
		"""

        def actor_update():
            try:
                self.details.insert('end', self.actor_coor[self.tree.focus()]['Info'])
                print "UI.update_details.Actor.Done"
            except KeyError as err:
                if DEBUG:
                    print err

        def object_update():
            try:
                self.details.insert('end', str(self.town_coor[self.tree.focus()]))

                print "UI.update_details.Object.Done"
            except KeyError as err:
                if DEBUG:
                    print err

        def arm_update():
            try:
                text = self.make_armor_metadata(self.arm_coor[self.tree.focus()])
                self.details.insert('end', str(text))
                print "UI.update_details.Arm.Done"
            except KeyError as err:
                if DEBUG:
                    print err

        def wep_update():
            try:
                text = self.make_weapon_metadata(self.wep_coor[self.tree.focus()])
                self.details.insert('end', str(text))
                print "UI.update_details.Wep.Done"
            except KeyError as err:
                if DEBUG:
                    print err

        self.details.config(state='normal')
        self.details.delete(1.0, 'end')

        actor_update()
        object_update()
        wep_update()
        arm_update()
        self.draw_select_ring(self.click_coor[self.tree.focus()])
        self.details.config(state='disabled')

    def city_map_select(self, event):

        """
		Checks click coordinates against a bounding box equivalent to
		the graphic size of the settlement sprite in a coorelation
		dictionary filled with each sprite's location.

		Sets selection and focus to corresponding town, then change is
		reflected in self.details automatically.
		"""

        for city_id, click_corner in self.click_coor.items():
            x_true = event.x >= click_corner[0] >= event.x - 20  # png is 20x20px
            y_true = event.y >= click_corner[1] >= event.y - 20
            if x_true and y_true:
                self.tree.selection_set(city_id)
                self.tree.focus(city_id)
                self.draw_select_ring(click_corner)


ui = UI()
ui.mainloop()
