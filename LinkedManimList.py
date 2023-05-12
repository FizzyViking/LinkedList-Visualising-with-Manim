from manim import *
import numpy as np

class SingleLinked(VGroup):
    def __init__(self, content):
        super().__init__()
        self.sq = Rectangle(width = 3)
        self.pt = Rectangle(width =3,height=1)
        self.back = Circle(radius=0)
        self.content = Text(content)
        self.add(self.sq,self.content,self.pt,self.back)
        self.pt.shift(DOWN*(self.sq.height/2+self.pt.height/2))
        self.content.move_to(self.get_center())
        self.back.move_to(self.pt.get_edge_center(LEFT))
        self.arrow = None
        self.next_node = None
    def new_next(self,content, spacing:int = 1):
        self.attach(self.new_of_own_class(content))
        self.next_node.shift(self.get_center()-self.next_node.get_center()+RIGHT*(self.sq.width+spacing))
        return(self.next_node)
    def new_of_own_class(self,content):
        return SingleLinked(content)
    def disconnect(self):
        self.next_node = None
        p = Circle(radius=0)
        p.move_to(self.pt.get_edge_center(RIGHT))
        self.arrow.end = None
        return ([self.arrow.connect(p)])
    def connect(self, node):
        self.next_node = node
        return([self.arrow.connect(node.back)])
    def attach(self,node):
        self.next_node = node
        if(self.arrow == None):
            self.arrow = link(self.pt,self.next_node.back)
            self.add(self.arrow)
        else:
            self.arrow.end = node.back
    def get_next(self):
        return self.next_node
    def get_center(self):
        return self.sq.get_center()

class DoubleLinked(SingleLinked):
    def __init__(self,content):
        super().__init__(content)
        self.back_pt = Rectangle(width = self.pt.width,height = self.pt.height)
        self.back_pt.shift(UP*(self.sq.height/2+self.back_pt.height/2))
        self.front = Circle(radius = 0)
        self.front.move_to(self.back_pt.get_edge_center(RIGHT))
        self.add(self.front,self.back_pt)
        self.back_arrow = None
        self.previous = None
    def attach_previous(self, prev): #only for initialisation
        self.previous = prev
        if(self.back_arrow == None):
            self.back_arrow = link(self.back_pt,self.previous.front)
        self.add(self.back_arrow)
    def connect_previous(self,prev):
        if(self.back_arrow == None):
            self.back_arrow = link(self.back_pt,self.previous.front)
            return(Create(self.back_arrow))
        self.previous = None
        self.back_arrow.connect(prev.front)
        return (self.back_arrow.connect(prev.front))
    def connect(self,node):
        frontc = super().connect(node)
        backc = self.next_node.connect_previous(self)
        frontc.append(backc)
        return(frontc)
    def new_of_own_class(self,content):
        return DoubleLinked(content)
    def disconnect_back(self):
        self.previous = None
        p = Circle(radius=0)
        p.move_to(self.back_pt.get_edge_center(LEFT))
        self.back_arrow.end == None
        return(self.back_arrow.connect(p))
    def disconnect(self):
        backd = None
        if self.next_node.previous == self:
            backd = self.next_node.disconnect_back()
        frontd = super().disconnect()
        frontd.append(backd)
        return (frontd)
    def attach(self,node):
        super().attach(node)
        self.next_node.attach_previous(self)

class link(Arrow):
    def __init__(self, s, e):
        super().__init__()
        self.start = s
        self.end = e
        self.start_record = s.get_center()
        self.end_record = e.get_center()
        def update(mob):
            if(mob.end != None and ((mob.end_record != mob.end.get_center()).any() or (mob.start_record != mob.start.get_center()).any())):
                mob.put_start_and_end_on(mob.start.get_center(), mob.end.get_center())
                mob.start_record = mob.start.get_center()
                mob.end_record = mob.end.get_center()
        update(self)
        self.add_updater(update)
    def connect(self,e):
        self.end_record = e.get_center()
        self.end = e
        return (self.animate.put_start_and_end_on(self.start.get_center(), e.get_center()))




class LinkedNodes(VGroup):
    def __init__(self, node):
        super().__init__()
        self.start = node
        self.add(self.start)
        self.count = 1
        self.last = node
    def add_node(self, t):
        newnode = self.last.new_next(t)
        self.last = newnode
        self.add(self.last)
        self.count += 1
        return (self.last)
    def append_existing_node(self,n):
        self.last.attach(n)
        self.add(n)
        self.last = n
        self.count += 1
    def cut_range(self,x,y,s):
        #Find xth node
        n = self.get_node(x)
        
        cutstart = n
        n = cutstart.get_next()
        self.remove(n)
        segment = LinkedNodes(n)

        #Defining cut segment
        for _ in range(y-x):
            if x < 0 or y < x or x > self.count:
                raise ValueError("Invalid range specified.")
            if(n.get_next() == None):
                break
            n = n.get_next()
            segment.append_existing_node(n)
            self.remove(n)
            self.count -= 1
        
        #Handling case of x+cutamount>count
        if(n.get_next() == None): 
            self.last = cutstart
            s.add(segment)
            return (cutstart,segment)
        
        #Define tail segment after cut
        cutend = n.get_next()
        n = cutend
        g = VGroup()
        g.add(n)
        while (n.get_next() != None):
            n = n.get_next()
            g.add(n)
        self.last = n
        return (cutstart,segment,cutend,g)
    def insert(self,lst,x):
        self.add(lst)
        self.count +=lst.count
        cutstart = self.get_node(x)
        n = cutstart
        if(n.get_next() == None):
            self.last = lst.last
        else:
            cutend = n.get_next()
        g = VGroup()
        while(n.get_next() != None):
            n = n.get_next()
            g.add(n)
        return (cutstart, cutend,g)
    def get_node(self,n):
        if(n == 0):
            return self.start
        node = self.start
        for _ in range(n-1):
            if node.get_next() == None:
                return node
            node = node.get_next()
        return node
