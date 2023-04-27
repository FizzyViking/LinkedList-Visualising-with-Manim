from manim import *

class SingleLinked(VGroup):
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
        self.arrow = None
        self.next_node = None
    def new_next(self,content):
        self.next_node = SingleLinked(content)
        self.next_node.move_to(self)
        self.next_node.shift(RIGHT*(self.sq.width+1))
        self.arrow = link(self.pt,self.next_node.back)
        self.add(self.arrow)
        return(self.next_node)
    def disconnect(self):
        self.next_node = None
        p = Circle(radius=0)
        p.move_to(self.pt.get_edge_center(RIGHT))
        self.arrow.end = None
        return (self.arrow.connect(p))
    def connect(self, node):
        self.next_node = node
        return(self.arrow.connect(node.back))
    def attach(self,node):
        self.next_node = node
        self.arrow.end = node.back

class DoubleLinked(SingleLinked):
    def __init__(self,content):
        super().__init__(content)
        self.back_pt = Rectangle(width = self.pt.width,height = self.pt.height)
        self.back_pt.shift(UP*1.5)
        self.front = Circle(radius = 0)
        self.front.move_to(self.back_pt.get_edge_center(RIGHT))
        self.add(self.front,self.back_pt)
        self.back_arrow = None
        self.previous = None
    def attach_previous(self, prev): #only for initialisation
        self.previous = prev
        self.back_arrow = link(self.back_pt,self.previous.front)
        self.add(self.back_arrow)
    def connect_previous(self,prev):
        self.previous = None
        self.back_arrow.connect(prev.front)
        return (self.back_arrow.connect(prev.front))
    def connect(self,node):
        frontc = super().connect(node)
        backc = self.next_node.connect_previous(self)
        return(frontc,backc)
    def new_next(self, content):
        self.next_node = DoubleLinked(content)
        self.next_node.move_to(self)
        self.next_node.shift(RIGHT*(self.sq.width+1))
        self.arrow = link(self.pt,self.next_node.back)
        self.add(self.arrow)
        self.next_node.attach_previous(self)
        return(self.next_node)
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
        return (frontd,backd)
    def attach(self,node):
        super().attach(node)
        self.next_node.attach_previous

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
    def connect(self,e):
        self.end = None
        return (self.animate.put_start_and_end_on(self.start.get_center(), e.get_center()),e)




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
        n = self.start
        for _ in range(x-1):
            if(n.next_node == None):
                return None
            n = n.next_node
        
        cutstart = n
        n = cutstart.next_node
        self.remove(n)
        segment = LinkedNodes(n)

        #Defining cut segment
        for _ in range(y-x):
            if(n.next_node == None):
                break
            n = n.next_node
            segment.append_existing_node(n)
            self.remove(n)
            self.count -= 1
        
        #Handling case of x+cutamount>count
        if(n.next_node == None): 
            self.last = cutstart
            s.add(segment)
            return (cutstart,segment)
        
        #Define tail segment after cut
        cutend = n.next_node
        n = cutend
        g = VGroup()
        g.add(n)
        while (n.next_node != None):
            n = n.next_node
            g.add(n)
        self.last = n

        return (cutstart,segment,cutend,g)
    def insert(self,lst,x):
        self.add(lst)
        self.count +=lst.count
        n = self.start
        for _ in range(x-1):
            n = n.next_node
        cutstart = n
        if(n.next_node == None):
            self.last = lst.last
        else:
            cutend = n.next_node
        cx,cy,cz = cutend.sq.get_center()
        lx,ly,lz = lst.start.sq.get_center()
        g = VGroup()
        while(n.next_node != None):
            n = n.next_node
            g.add(n)
        return (cutstart, cutend,g)
    def get_node(self,n):
        if(n == 0):
            return self.start
        node = self.start
        for _ in range(n):
            if node.next_node == None:
                return node
            node = node.next_node
        return node



        





