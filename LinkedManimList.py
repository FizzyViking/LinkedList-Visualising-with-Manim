from manim import *

class TextBox(VGroup):
    def __init__(self, content):
        super().__init__()
        self.sq = Square()
        self.pt = Square()
        self.content = content
        self.add(self.sq,content,self.pt)
        self.pt.move_to([self.sq.get_center()[0],-2,0])
        content.move_to(self.sq.get_center())

class link(Arrow):
    def __init__(self, s, e):
        super().__init__()
        self.start = s
        self.end = e
        def update(mob):
            if(mob.end != None):
                mob.put_start_and_end_on(mob.start.get_center(), mob.getedgepoint(mob.end))
        update(self)
        self.add_updater(update)
    def getAngle(self,e):
        sx,sy,sz = self.start.get_center()
        ex,ey,sz = e.get_center()
        return((ey-sy)/(ex-sx))
    def getedgepoint(self,e):
        sx,sy,sz = self.start.get_center()
        cutx,cuty,cutz = e.get_edge_center(LEFT)
        dy = self.getAngle(e)*(cutx-sx)
        return((cutx,dy+sy,0))
    def connect(self,e,s):
        p = Point(self.get_end())
        self.end = p
        s.play(p.animate.move_to(self.getedgepoint(e)))
        self.end = e
    def disconnect(self,s):
        dy = self.getAngle(self.end)
        sx,sy,sz = self.start.get_center()
        ex,ey,ez = self.end.get_center()
        distance = ex-sx
        middlex = (distance)*0.35+sx
        middley = (middlex-sx)*dy+sy

        diff = middley-(middlex-sx)*dy*-1

        cutstartx = sx+distance*0
        cutendx = sx+distance*0.75
        cutstarty = sy+((cutstartx-sx)*(dy*-1))-diff/2
        cutendy = sy+((cutendx-sx)*dy*-1)-diff/2
        #print(distance)
        endpoint = self.getedgepoint(self.end)
        self.end= None
        slash((cutstartx,cutstarty,0),(cutendx,cutendy,0),s)
        self.put_start_and_end_on(self.start.get_center(),(middlex,(middlex-sx)*dy+sy,0))


        a = Arrow()
        a.put_start_and_end_on((middlex,(middlex-sx)*dy+sy,0),endpoint)
        s.play(a.animate.shift(DOWN*5))

class LinkedListNode(VGroup):
    def __init__(self, content):
        super().__init__()
        self.nextnode = None
        self.box = TextBox(content)
        self.add(self.box)
        self.count = 0
        self.last = self
        self.arrow = None
        #content.move_to(self.circle.get_center())


    def add_node(self, t):
        self.count += 1
        newnode = LinkedListNode(t)
        self.add(newnode)
        center = self.last.get_x()+3
        newnode.move_to([(center),-1,0])
        #arrow = Arrow()
        #arrow.put_start_and_end_on(self.last.box.pt.get_edge_center(RIGHT),newnode.box.sq.get_edge_center(LEFT))
        arrow = link(self.last.box.pt,newnode.box)
        self.last.arrow = arrow
        #self.last.add(arrow)
        self.last = newnode
        
        self.add(arrow)
        return (self.last.box,arrow)
        

def slash(p1,p2,s):
    l = Line(p1,p2)
    s.play(Create(l).set_run_time(0.25))
    l.reverse_direction()
    s.play(Uncreate(l).set_run_time(0.25))