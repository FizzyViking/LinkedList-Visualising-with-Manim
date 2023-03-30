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
            sx,sy,sz = mob.start.get_center()
            ex,ey,sz = mob.end.get_center()
            cutx,cuty,cutz = mob.end.get_edge_center(LEFT)
            dy = (ey-sy)/(ex-sx)*(cutx-sx)
            mob.put_start_and_end_on(mob.start.get_center(), (cutx,dy+sy,0))
        update(self)
        self.add_updater(update)


class LinkedListNode(VGroup):
    def __init__(self, content):
        super().__init__()
        self.nextnode = None
        self.box = TextBox(content)
        self.add(self.box)
        self.count = 0
        self.last = self
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
        self.last = newnode
        
        self.add(arrow)
        return (self.last.box,arrow)
        

            
