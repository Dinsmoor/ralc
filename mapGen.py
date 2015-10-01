#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mapGen.py
#
#  Copyright 2015 Tyler Dinsmoor <pappad@airmail.cc>
#

try:
    import random
    import townGen
    import caveGen
    from dungeongenerator import dungeon
    from markovnames import nameGen
    from PIL import Image, ImageDraw, ImageTk, ImageFilter
except ImportError as err:
    print "You are missing essential Libraries. See README.md"
    print err
    exit()

def getFromFile_T(fi):
    fi = open(fi)
    li = [i.strip().split('\n') for i in fi if not i.startswith("#")]
    li = [x for x in li if x != ['']]
    tu = tuple(li)
    fi.close()
    return tu

def getSettlementName():
    names = random.choice(getFromFile_T('data/settlement_names'))
    return nameGen.get_name(names)

def wChoice(wCh):
    '''must be in format: wChoice(('a',1.0),('b',2.0),('c',3.0))'''
    totalChoice = sum(w for c, w in wCh)
    random_uniform = random.uniform(0, totalChoice)
    upto = 0
    for c, w in wCh:
        if upto + w > random_uniform:
            return c
        upto += w
    assert False, "Shouldn't get here"
def gridDistance(points):
    import math
    p0, p1 = points
    return int(math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2))

class Land_Image(object):
    '''
    All data needed to create a new image representing a land-generated
    area.
    '''

    def __init__(self, biome_ovr):
        '''
        Collects needed data to draw on top of a canvas. Order matters!
        '''
        biome = self.get_biome(biome_ovr)
        self.biome = biome
        self.city_name = getSettlementName()

        blacktext = ('tundra','desert','marsh','hills')
        if biome in blacktext:
            self.text_color = 'black'
        else:
            self.text_color = 'white'

        # set base img size
        self.imgx = 600
        self.imgy = self.imgx
        # initilize the image
        self.im = Image.new('RGBA',(self.imgx,self.imgy),'limegreen')
        self.draw = ImageDraw.Draw(self.im)

        # start drawing on top of the image
        self.draw_biome(biome)
        self.draw_water(biome)
        #self.draw_terrain()
        self.draw_flora(biome)

        self.used_coords = list()
        city_dic = self.draw_city()
        self.town_names, self.uninhab = self.draw_smalls()#camp_dic + vil_dic
        city_dic['Image'] = self.im
        self.town_names.append(city_dic)

    def get_biome(self, override):

        if override != None:
            print "mapGen: biome is %s (override)" %override
            return override.lower()

        biomeLeanVal = (('marsh' ,1.0),('plains'  ,3.0),
                        ('hills' ,1.5),('tundra'  ,1.0),
                        ('desert',2.0),('forest'  ,3.0))
        biome = wChoice(biomeLeanVal)
        print "mapGen: biome is %s" %biome
        return biome

    def draw_biome(self,biome):

        # new method for drawing biome, but my images are ugly D;
        image_to_paste = Image.open('data/sprites/%s_texture.png'%biome)
        y_paste = 0
        for y_row in xrange(0,5):
            for x_paste_interval in xrange(0,self.imgx):
                if x_paste_interval % 128 == int():
                    self.im.paste(image_to_paste,
                        (x_paste_interval,y_paste), image_to_paste)
            y_paste += 128

    def draw_city(self):

        x, y = self.get_some_coords()
        self.used_coords.append((x,y))
        image_to_paste = Image.open('data/sprites/city.png')
        self.im.paste(image_to_paste, (x,y), image_to_paste)
        self.draw.text((x-10,y+18),str(self.city_name), fill=self.text_color)
        self.city_location = (x,y)
        city_dic = {
            'Name':self.city_name,
            'Type':'Region Capital',
            'Distance':0,
            'click_area':self.city_location,
            'Image':None, #added at end
                    }
        return city_dic

    def get_some_coords(self):
        x = random.randrange(10,self.imgx-50)
        y = random.randrange(10,self.imgy-50)
        return x, y

    def is_far_enough_away(self, x_cor, y_cor):

        x_used_li = y_used_li = list()

        for coord in self.used_coords:
            x_used_li.append(coord[0])
            y_used_li.append(coord[1])

        for x in x_used_li:
            closest_x = min(x_used_li, key=lambda x:abs(x-x_cor))
            if closest_x <= 22:
                return False

        for y in y_used_li:
            closest_y = min(y_used_li, key=lambda x:abs(x-y_cor))
            if closest_y <= 22:
                return False

        return True

    def draw_smalls(self):

        smalls_li = list()
        uninhab_li = list()
        types = ['Cave','Village',
                'Camp','Temple', 'Dungeon']
        uninhabs = ['Cave', 'Dungeon']

        for TYPE in types:
            density = random.randint(1,5)
            image_to_paste = Image.open('data/sprites/'+TYPE.lower()+'.png')
            for c in xrange(0,density):
                name = getSettlementName()
                x, y = self.get_some_coords()

                while not self.is_far_enough_away(x,y):
                    x, y = self.get_some_coords()

                self.used_coords.append((x,y))
                self.im.paste(image_to_paste, (x,y), image_to_paste)
                self.draw.text((x-10,y+18),name, fill=self.text_color)
                roadLength = int(gridDistance((self.city_location,(x,y))) / 15) # to be used for km
                self.draw.text((x-10,y+25),'to city: %dkm'%(roadLength), fill=self.text_color)
                smallsDat = {
                'Type':TYPE,
                'Name':name,
                'Distance':str(roadLength),
                'click_area':[x,y],
                'Image':None,
                }
                if TYPE == 'Cave':
                    ci = Cave_Image()
                    smallsDat['Image'] = ci.im
                    uninhab_li.append(smallsDat)
                elif TYPE == 'Dungeon':
                    di = Dungeon_Image()
                    smallsDat['Image'] = di.im
                    uninhab_li.append(smallsDat)
                else:
                    smalls_li.append(smallsDat)
        return smalls_li, uninhab_li

    def draw_terrain(self):

        def draw_scorch_marks():
            density = random.randint(0,9)
            if density > 2:
                for c in xrange(0,density):
                    x = random.randrange(10,self.imgx-50)
                    y = random.randrange(10,self.imgy-50)
                    image_to_paste = Image.open('data/sprites/scorch_texture.png')
                    self.im.paste(image_to_paste, (x,y), image_to_paste)



        def hills():
            density = random.randint(1,3)
            for c in xrange(0,density*100):
                x = random.randint(0,self.imgx)
                y = random.randint(0,self.imgy)
                self.draw.arc((x,y,x+20,y+20),220,340, fill='gray')

        draw_scorch_marks()

    def draw_water(self, biome):
        river_points = []

        def river(densityFactor):

            density = random.randint(0,4)
            streamCount = int(density + (density*densityFactor))
            for c in xrange(0,streamCount):
                # determines whether to start on x or y axis
                dir_num = random.randint(4,9)
                if random.random() >= 0.5:
                    x = random.randrange(0,self.imgx)
                    y = 0
                else:
                    x = 0
                    y = random.randrange(0,self.imgy)
                for null in xrange(0,10000): # try to make it at least reach end of screen
                    # decides which direction to wander
                    if random.random() >= 0.5:
                        if random.randint(0,random.randint(5,9)) < random.randint(0,9):
                            x -= 1
                        else:
                            x += 1
                        if (x >= self.imgx):
                            break
                    else:
                        if random.randint(0,dir_num) < random.randint(0,random.randint(5,9)):
                            y -= 1
                        else:
                            y += 1
                        if (y >= self.imgy):
                            break
                    self.draw.point((x,y), fill='#2A2CD8')
                    self.draw.point((x-1,y-1), fill='navy')
                    self.draw.point((x+1,y+1), fill='navy')
                    river_points.append((x,y))

        def lake():

            # just have it be a shallow-looking pond, I suppose
            lake_amount = random.randint(0,5)

            for lake in xrange(0,lake_amount):
                point = random.choice(river_points)
                x = point[0]
                y = point[1]

                self.draw.ellipse((x,y,x+35,y+15), fill='#2A2CD8')


        d ={
        'forest':0.7,
        'plains':0.6,
        'hills':0.7,
        'tundra':0.3,
        'marsh':1,
        'desert':0.1
        }

        river(d[biome])
        print len(river_points)
        if len(river_points) > 1:
            lake()

    def draw_flora(self,biome):

        def trees(density,artList):

            density = density*225
            #using tree sprites
            for t in xrange(0,int(density)):
                image_to_paste = Image.open('data/sprites/'+random.choice(artList)+'.png')
                x = random.randrange(0,self.imgx)
                y = random.randrange(0,self.imgy)
                self.im.paste(image_to_paste, (x,y), image_to_paste)


        # Tree intensity Modifiers
        tree_mod ={
        'forest':[random.randint(2,4),('tree1','tree2')],
        'plains':[0.5,  ('tree3','desertF1')],
        'hills':[0.5,   ('tree3','desertF1')],
        'tundra':[0.2,  ('tree3','desertF1')],
        'marsh':[1,     ('marshF1','tree2')],
        'desert':[0.1,  ('desertF1','desertF2')]
        }

        trees(tree_mod[biome][0],tree_mod[biome][1])

    def draw_kingdom_flag(self):
        pass

    def save_image(self):
        self.im.save('landMap', "PNG")

    def show_image(self):
        self.im.show()

class Town_Image(object):

    '''
    All data needed to create a new image representing a Town-generated
    area.
    '''

    def __init__(self, pref):

        self.settings = pref

        #get cityname from Land_Image
        self.city_name = landImg.city_name

        self.towns = self.populate_area()
        self.imgx = 600
        self.imgy = self.imgx
        # initilize the image
        self.im = Image.new('RGB',(self.imgx,self.imgy),'lightgray')
        # lets not draw things until it's ready
        #self.draw = ImageDraw.Draw(self.im)

    def populate_area(self):

        city_list = list()
        for city_dict in landImg.town_names:
            cities = dict()

            if city_dict['Type'] == "Region Capital":
                streets, desc = townGen.main('big',landImg.biome, self.settings)
                city_dict['Data'] = streets
                city_dict['Desc'] = desc
            else:
                streets, desc = townGen.main('small',landImg.biome, self.settings)
                city_dict['Data'] = streets
                city_dict['Desc'] = desc
            city_list.append(city_dict)
        return city_list

    def draw_walls(self):

        img_city_walls = Image.open('data/sprites/cityWalls.png')
        self.im.paste(img_city_walls, (0,0), img_city_walls)

    def draw_streets(self):

        img_bldgSimple = Image.open('data/sprites/cityBldgSimple.png')
        total_streets = len(self.streets)
        street_interval = self.imgx / total_streets

        x_axis_assigned = random.randint(1, total_streets -1)
        y_axis_assigned = total_streets - x_axis_assigned
        bldg_interval = 6

        x = 0 - (street_interval / 2)
        y = x

        x_interval = self.imgx / x_axis_assigned
        y_interval = self.imgy / y_axis_assigned

        for street in xrange(x_axis_assigned):
            x += x_interval
            self.draw.line((x,20,x,580), fill='#9A8857', width=3)
            for bldg in xrange(1,6):
                bldg_y = self.imgy / bldg
                self.im.paste(img_bldgSimple, (x-10,bldg_y), img_bldgSimple)

        for street in xrange(y_axis_assigned):
            y += y_interval
            self.draw.line((20,y,580,y), fill='#9A8857', width=3)
            for bldg in xrange(1,6):
                bldg_x = self.imgx / bldg
                self.im.paste(img_bldgSimple, (bldg_x,y-10), img_bldgSimple)

    def draw_lots(self):
        pass

    def draw_flag(self):
        pass

    def save_image(self):
        self.im.save('landMap', "PNG")

    def show_image(self):
        self.im.show()

class Building_Image(object):
    '''
    All data needed to create a new image representing a Bldg-generated
    area.
    '''

    def __init__(self):
        #get cityname from Land_Image
        self.imgx = 600
        self.imgy = self.imgx
        # initilize the image
        self.im = Image.new('RGB',(self.imgx,self.imgy),'maroon')
        self.draw = ImageDraw.Draw(self.im)


    def save_image(self):
        self.im.save('landMap', "PNG")

    def show_image(self):
        self.im.show()

class Cave_Image:

    def __init__(self, name=None):
        self.CAVE_SIZE = 120

        self.cave = caveGen.CA_CaveFactory(self.CAVE_SIZE,self.CAVE_SIZE,0.5)# Density

        self.imgx = 600
        self.imgy = self.imgx
        self.im = Image.new('RGB',(self.imgx,self.imgy),'lightgray')

        walls, floors = self.parse_arry()
        self.pil_img = self.draw_cave(walls, floors)

        self.im = self.im.filter(ImageFilter.GaussianBlur(radius=1))
        #self.im = self.im.filter(ImageFilter.SHARPEN)

        #self.im.show()

    def parse_arry(self):
        arry = self.cave.arry

        walls = []
        floors = []

        for r in range(0,self.CAVE_SIZE):
            for c in range(0,self.CAVE_SIZE):
                if arry[r][c] in (caveGen.WALL,caveGen.PERM_WALL):
                    walls.append((r * 5,c * 5))
                else:
                    floors.append((r * 5,c * 5))
        return walls, floors

    def draw_cave(self, walls, floors):
        cave_draw = ImageDraw.Draw(self.im)

        for x, y in walls:
            x2 = x + 20
            y2 = y + 20
            cave_draw.rectangle((x,y,x2,y2), fill='black')

    def filter_cave(self):
        pass


class Dungeon_Image:

    def __init__(self, name=None):
        self.DUNGEON_SIZE = 7
        # second is /2 to make it square
        tile_dict = dungeon.generate(self.DUNGEON_SIZE,self.DUNGEON_SIZE,8)# Density

        self.imgx = 600
        self.imgy = self.imgx
        self.im = Image.new('RGB',(self.imgx,self.imgy),'black')

        self.pil_img = self.draw_dg(tile_dict)

        #self.im = self.im.filter(ImageFilter.GaussianBlur(radius=1))
        #self.im = self.im.filter(ImageFilter.SHARPEN)

        #self.im.show()

    def draw_dg(self, tile_dict):
        dg_draw = ImageDraw.Draw(self.im)

        colors = {
            "#":"darkgrey",
            ".":"lightgrey",
            ">":"lightgrey",#"red", No multiple levels for now
            "<":"green",
            " ":""
            }

        floors = []

        # draw everything but labled items first
        for coords, symbol in tile_dict.iteritems():
            color_fill = colors[symbol]
            x = coords[0] * 10 #to better fit 600x600 screen
            y = coords[1] * 10
            if symbol == " ":
                pass
            else:
                x2 = x + 10
                y2 = y + 10
                dg_draw.rectangle((x,y,x2,y2), fill=color_fill)
            if symbol == ".":
                floors.append(coords)

        #to make sure that text gets drawn on top
        for coords, symbol in tile_dict.iteritems():
            color_fill = colors[symbol]
            x = coords[0] * 10 #to better fit 600x600 screen
            y = coords[1] * 10
            if symbol != ("<") or (">"):
                pass
            if symbol == "<":
                dg_draw.text((x,y+10), "UP", fill=color_fill)
            if symbol == ">":
                pass
                #dg_draw.text((x,y+10), "DOWN", fill=color_fill)

        self.draw_treasure(dg_draw, floors, random.randint(1,15)) #yarr!

    def draw_treasure(self, draw_surface, valid_area, number):

        where_to_drop = random.sample(valid_area, number)
        containers = (('Open Chest',10),
                    ('Locked Chest',3),
                    ('Crate',10),
                    ('Urn',10),
                    ('Box',10),
                    ('Mimic',1),
                    ('Cursed Chest',1))

        for place in where_to_drop:
            x = place[0] * 10
            y = place[1] * 10
            x2 = x + 10
            y2 = y + 10
            draw_surface.rectangle((x,y,x2,y2), fill='brown')
            draw_surface.text((x,y+10), wChoice(containers), fill='brown')

def main(opt, pref):
    global landImg, townImg, bldgImg
    if opt == 'tk':
        landImg = Land_Image(pref['map']['biome'])
        townImg = Town_Image(pref)
        #caveImg = Cave_Image()
        #dungeonImg = Dungeon_Image()
        #bldgImg = Building_Image()
        return_dict = {
            "landimg":landImg.im,
            "cityname":landImg.city_name,
            "towns":townImg.towns,
            "uninhab":landImg.uninhab,
                }
        return return_dict
    if opt == 'small':
        pass
    if opt == 'cave':
        caveImg = Cave_Image(pref)
    else:
        landImg = Land_Image(pref['map']['biome'])
        landImg.im.show()
        #townImg = Town_Image(pref)
        #bldgImg = Building_Image()
        #caveImg = Cave_Image()
        #townImg.show_image()
        #dungeonImg = Dungeon_Image()

        return 0

if __name__ == '__main__':
    import def_settings
    default_settings = def_settings.get_def_settings()
    main('', default_settings)

