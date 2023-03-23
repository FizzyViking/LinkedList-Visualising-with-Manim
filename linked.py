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


    def add_node(self, t):
        if self.nextnode == None:
            self.nextnode = LinkedListNode(t)
            self.add(self.nextnode)
            center = self.box.get_x()
            self.nextnode.move_to([(center+3),-1,0])
            arrow = link(self.box.pt,self.nextnode.box.sq)
            #arrow = Arrow()
            #arrow.put_start_and_end_on(self.box.pt.get_center(), self.nextnode.box.sq.get_center())
            self.add(arrow)
            return (self.nextnode.box,arrow,self.nextnode.get_x())
        else:
            return self.nextnode.add_node(t)





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
        boxy.shift(RIGHT*3+UP*10)
        self.play(boxy.animate.shift(DOWN*10))
        anim = my_mobject.add_node(Text("a"))
        self.add(anim[0])
        self.remove(boxy)
        self.play(Create(anim[1]))

class multiLink(Scene):
    def construct(self):
        t = Text("hello!")
        mob = LinkedListNode(t)
        self.play(Create(mob))
        center = mob.get_center()

        for x in range(4):
            y = x+1
            name = str(y)
            boxy = TextBox(Text(name))
            boxy.move_to(center)
            boxy.shift(UP*10)
            self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
            self.play(boxy.animate.shift(DOWN*10))
            anim = mob.add_node(Text(name))
            self.add(anim[0])
            self.remove(boxy)
            self.play(Create(anim[1]))
            self.play(mob.animate(run_time = 0.25).shift(RIGHT*3*y))
            self.play(Wait(run_time=0.25))

        for z in range(50):
            name = str(z+y+1)
            mob.add_node(Text(name))

        y += 51
        name = str(y)
        boxy = TextBox(Text(name))
        boxy.move_to(center)
        boxy.shift(UP*10)
        self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
        self.play(boxy.animate.shift(DOWN*10))
        anim = mob.add_node(Text(name))
        self.add(anim[0])
        self.remove(boxy)
        self.play(Create(anim[1]))
