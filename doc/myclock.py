import math
import time
import itertools
import tkinter
import threading


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
            self.canvas.delete(self.widget_id)

class Pointer(MyLine):

    def __init__(self,ptype,canvas,center_point,plong=180,width=1,color='black'):
        super().__init__(canvas,width,color)
        self.center_point = center_point
        self.plong = plong
        self.ptype = ptype
        self.end_point = None
        self.points = itertools.cycle(gen_end_points(self.center_point,self.plong,self.ptype))
        self.count,self.end_point = self.points.__next__()

    def draw(self):
        self.widget_id = self.canvas.create_line(self.center_point,self.end_point, 
            width=self.width, fill=self.color)
        self.count,self.end_point = self.points.__next__()

    def walk(self):
        self.delete()
        self.draw()

class Marker(MyLine):

    def __init__(self,start_point,end_point,canvas,width=2,color='black'):
        super().__init__(canvas,width,color)
        self.start_point = start_point
        self.end_point = end_point

    def draw(self):
        self.widget_id = self.canvas.create_line(self.start_point,self.end_point, 
            width=self.width, fill=self.color)

class PlateOuter:
    def __init__(self,canvas,center_point,radius):
        self.canvas = canvas
        self.center_point = center_point
        self.radius = radius
        self.widget_id = None

    def draw(self):
        x0 = self.center_point[0] - self.radius
        y0 = self.center_point[1] - self.radius
        x1 = self.center_point[0] + self.radius
        y1 = self.center_point[1] + self.radius
        self.canvas.create_oval(x0,y0,x1,y1)

    def delete(self):
        if self.widget_id:
            self.canvas.delete(self.widget_id)

class Plate:

    def __init__(self,canvas, center_point, radius, plong):
        self.canvas = canvas
        self.center_point = center_point
        self.radius = radius
        self.plong = plong
        self.markers = []
        self.gen_markers()

    def draw(self):
        for marker in self.markers:
            marker.draw()

    def gen_markers(self):
        for start,end in zip(gen_end_points(self.center_point,self.radius,6),
                gen_end_points(self.center_point,self.radius + self.plong,6)):
            self.markers.append(Marker(start[1],end[1],self.canvas))
        self.markers.append(PlateOuter(self.canvas,self.center_point,self.radius+20))

    def delete(self):
        for w in self.markers:
            self.canvas.delete(w)

class MyClocker:

    def __init__(self,root,canvas, center_point, radius, plong):
        self.root = root
        self.plate = Plate(canvas, center_point, radius, plong)
        self.s_pointer = Pointer(6,canvas,center_point,plong=180,width=1,color='red')
        self.m_pointer = Pointer(3,canvas,center_point,plong=150,width=2,color='blue')
        self.h_pointer = Pointer(1,canvas,center_point,plong=120,width=4,color='black')
        self.display()

    def display(self):
        self.plate.draw()
        self.s_pointer.draw()
        self.m_pointer.draw()
        self.h_pointer.draw()
        self.root.update()

    def walk(self):
        self.s_pointer.walk()
        if (self.s_pointer.count + 1) % 30 == 0:
            self.m_pointer.walk()
            if (self.m_pointer.count + 1) % 4 == 0:
                self.h_pointer.walk()

    def start(self):
        while True:
            self.walk()
            self.root.update()
            time.sleep(1)

if __name__ == '__main__':
    root = tkinter.Tk()
    cvns = tkinter.Canvas(root,width=530,height=530,bg='white')
    cvns.pack()
    mc = MyClocker(root,cvns,(260,260),200,10)
    t = threading.Thread(target=mc.start)
    t.setDaemon(True)
    t.start()
    root.resizable(False, False)
    root.mainloop()
