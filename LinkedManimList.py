from manim import *

class TextBox(VGroup):
    def __init__(self, content):
        super().__init__()
        self.sq = Rectangle(width = 3)
        self.pt = Rectangle(width =3,height=1)
        self.back = Circle(radius=0)
        self.content = Text(content)
        self.add(self.sq,self.content,self.pt,self.back)
        self.pt.move_to([self.sq.get_center()[0],-1.5,0])
        self.content.move_to(self.sq.get_center())
        self.back.move_to(self.pt.get_edge_center(LEFT))
        #self.back.shift(UP*0.3)
        self.arrow = None
        self.next_node = None
    def new_next(self,content):
        self.next_node = TextBox(content)
        self.next_node.move_to(self)
        self.next_node.shift(RIGHT*(self.sq.width+1))
        self.arrow = link(self.pt,self.next_node.back)
        self.add(self.arrow)
        return(self.next_node)
    def disconnect(self, s):
        self.next_node = None
        self.arrow.disconnect(s)
    def connect(self, node,s):
        self.next_node = node
        self.arrow.connect(node.back,s)
    def attach(self,node):
        self.next_node = node
        self.arrow.end = node.back

class DoubleLinked(TextBox):
    def __init__(self,content):
        super().__init__(content)
        self.backpt = Rectangle(width = self.pt.width,height = self.pt.height)
        self.backpt.shift(UP*1.5)
        self.front = Circle(radius = 0)
        self.front.move_to(self.backpt.get_edge_center(RIGHT))
        self.add(self.front,self.backpt)
        self.backarrow = None
        self.previous = None
    def attachprevious(self, prev): #only for initialisation
        self.previous = prev
        self.backarrow = link(self.backpt,self.previous.front)
        self.add(self.backarrow)
        #print(self.content.text, " : ",prev.content.text)
    def connectprevious(self,prev,s):
        self.previous = None
        self.backarrow.connect(prev.front,s)
    def connect(self,node,s):
        super().connect(node,s)
        self.next_node.connectprevious(self,s)
    def new_next(self, content):
        self.next_node = DoubleLinked(content)
        self.next_node.move_to(self)
        self.next_node.shift(RIGHT*(self.sq.width+1))
        self.arrow = link(self.pt,self.next_node.back)
        self.add(self.arrow)
        self.next_node.attachprevious(self)
        return(self.next_node)
    def disconnect_back(self,s):
        self.previous = None
        self.backarrow.disconnect(s)
    def disconnect(self, s):
        self.next_node.disconnect_back(s)
        super().disconnect(s)
    def attach(self,node):
        super().attach(node)
        self.next_node.attachprevious

class link(Arrow):
    def __init__(self, s, e):
        super().__init__()
        self.start = s
        self.end = e
        def update(mob):
            if(mob.end != None):
                mob.put_start_and_end_on(mob.start.get_center(), mob.end.get_center())
        update(self)
        self.add_updater(update)
    def getAngle(self,e):
        sx,sy,sz = self.start.get_center()
        ex,ey,sz = e.get_center()
        return((ey-sy)/(ex-sx))
    def connect(self,e,s):
        p = Point(self.get_end())
        self.end = p
        s.play(p.animate.move_to(e))
        self.end = e
    def disconnect(self,s):
        dy = self.getAngle(self.end)
        sx,sy,sz = self.start.get_center()
        ex,ey,ez = self.end.get_center()
        distance = ex-sx
        middlex = (distance)*0.35+sx
        cutpoint = (middlex,(middlex-sx)*dy+sy,0)
        cutstartx = cutpoint[0]-0.2
        cutstarty = cutpoint[1]+0.5

        #deltay = (cutpoint[1]/cutstarty)(cutpoint[0]-cutstartx)
        cutendx = cutpoint[0]+0.2
        cutendy = cutpoint[1]-0.5
        #print(distance)
        endpoint = self.end.get_center()
        self.end= None
        slash((cutstartx,cutstarty,0),(cutendx,cutendy,0),s)
        self.put_start_and_end_on(self.start.get_center(),(middlex,(middlex-sx)*dy+sy,0))


        a = Arrow()
        a.put_start_and_end_on((middlex,(middlex-sx)*dy+sy,0),endpoint)
        s.play(a.animate.shift(DOWN*10))
        s.remove(a)


class LinkedListNode(VGroup):
    def __init__(self, node):
        super().__init__()
        self.start = node
        self.add(self.start)
        self.last = node
    def add_node(self, t):
        """""
        self.count += 1
        newnode = LinkedListNode(t)
        self.add(newnode)
        center = self.last.get_x()+4
        newnode.move_to([(center),-1,0])
        #arrow = Arrow()
        #arrow.put_start_and_end_on(self.last.box.pt.get_edge_center(RIGHT),newnode.box.sq.get_edge_center(LEFT))
        arrow = link(self.last.box.pt,newnode.box.back)
        self.last.arrow = arrow
        #self.last.add(arrow)
        self.last = newnode
        """""
        newnode = self.last.new_next(t)
        self.last = newnode
        
        self.add(self.last)
        return (self.last)
    def append_existing_node(self,n):
        self.last.attach(n)
        self.add(n)
        self.last = n
    def cut_range(self,x,y,s):
        n = self.start
        for _ in range(x-1):
            if(n.next_node == None):
                return None
            n = n.next_node
        cutstart = n
        n = cutstart.next_node
        segment = LinkedListNode(n)
        for _ in range(y-x):
            if(n.next_node == None):
                break
            n = n.next_node
            segment.append_existing_node(n)
            self.remove(n)
        if(n.next_node == None):
            self.last = cutstart
            cutstart.diconnect(s)
            return segment
        diff = cutstart.next_node.get_x()-cutstart.get_x()
        print(diff)
        cutend = n.next_node
        n.disconnect(s)
        cutstart.disconnect(s)
        n = cutend
        g = VGroup()
        g.add(n)
        while (n.next_node != None):
            n = n.next_node
            g.add(n)
        self.last = n
        s.play(segment.animate.shift(UP*(segment.height+1)))

        cutstart.connect(cutend,s)
        s.play(g.animate.shift(LEFT*(cutend.sq.get_x()-cutstart.sq.get_x()-diff)))
        return segment



        

def slash(p1,p2,s):
    l = Line(p1,p2)
    s.play(Create(l).set_run_time(0.25))
    l.reverse_direction()
    s.play(Uncreate(l).set_run_time(0.25))







"""""
class link2(Arrow):
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
"""