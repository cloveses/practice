import math
import itertools

def get_all_points(center_point,plong):
    end_points = []
    for i in range(360):
        x = center_point[0] + plong * math.cos(i * math.pi / 180)
        y = center_point[1] + plong * math.sin(i * math.pi / 180)
        end_points.append((x,y))
    return end_points[270:] + end_points[:270]

def gen_end_points(center_point,plong,sep):
    # second sep 6
    # minute sep 3
    # hour sep 1
    for i,p in enumerate(get_all_points(center_point,plong)[::sep]):
        yield i,p

class MyLine:
    def __init__(self,canvas,width=1,color='black'):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.widget_id = None

    def delete(self):
        if self.widget_id:
            self.cavans.delete(self. widget_id)

class Pointer(MyLine):

    def __init__(self,ptype,canvas,center_point,plong=180,width=1,color='black'):
        super().__init__(canvas,width,color)
        self.center_point = center_point
        self.plong = plong
        self.ptype = ptype
        self.end_point = None
        self.points = itertools.cycle(gen_end_points(self.center_point,self.plong,sep))

    def draw(self):
        self.count,self.end_point = self.points.__next__()
        self.widget_id = self.canvas.create_line(self.center_point,self.end_point, 
            width=self.width, fill=self.color)

    def walk(self):
        self.delete()
        self.draw()

class Maker(MyLine):

    def __init__(self,start_point,end_point,canvas,width=2,color='black'):
        super().__init__(canvas,width,color)
        self.start_point = start_point
        self.end_point = end_point

    def draw(self):
        self.widget_id = self.canvas.create_line(self.center_point,self.end_point, 
            width=self.width, fill=self.color)

class Plate():

    def __init__(self,center_point,radius,plong):
        for start,end in zip(gen_end_points(center_point,radius,6),gen_end_points(center_point,radius + plong,6)):
            
