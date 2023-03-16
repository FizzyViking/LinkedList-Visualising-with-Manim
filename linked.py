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
            mob.put_start_and_end_on(mob.start.get_center(), mob.end.get_edge_center(LEFT))
        update(self)
        self.add_updater(update)


class LinkedListNode(VGroup):
    def __init__(self, content):
        super().__init__()
        self.nextnode = None
        self.box = TextBox(content)
        self.add(self.box)
        #content.move_to(self.circle.get_center())


    def add_nodewithoutanim(self, t):
        if self.nextnode == None:
            self.nextnode = LinkedListNode(t)
            self.add(self.nextnode)
            center = self.box.get_x()
            self.nextnode.move_to([(center+3),-1,0])
            arrow = link(self.box.pt,self.nextnode.box.sq)
            #arrow = Arrow()
            #arrow.put_start_and_end_on(self.box.pt.get_center(), self.nextnode.box.sq.get_center())
            self.add(arrow)
            return (self.nextnode.box,arrow)
        else:
            return self.nextnode.add_nodewithoutanim(t)





    def add_node(self, t):
        b,a = self.add_nodewithoutanim(t)
        return (b,Create(a))
    def getnode(self,index):
        if(index == 0):
            return self.box
        elif(self.nextnode == None):
            return None
        else:
            return self.nextnode.getnode(index-1)
            

class LinkedList(Scene):
    def construct(self):
        t = Text("hello!")
        my_mobject = LinkedListNode(t)
        self.play(Create(my_mobject))

        boxy = TextBox(Text("a"))
        boxy.move_to(my_mobject.get_center())
        boxy.shift(RIGHT*3)
        self.play(Create(boxy))

        anim = my_mobject.add_node(Text("a"))
        self.add(anim[0])
        self.remove(boxy)
        self.play(anim[1])
        anim = my_mobject.add_node(Text("a"))
        self.play(anim[1])
        my_mobject.add_nodewithoutanim(Text("b"))
        self.play(my_mobject.animate.shift(UP))
        mover = my_mobject.getnode(1)
        self.play(mover.animate.shift(DOWN))
        self.wait()