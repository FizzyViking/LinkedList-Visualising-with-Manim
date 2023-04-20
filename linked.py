from manim import *
from LinkedManimList import *

class LinkedList(Scene):
    def construct(self):
        my_mobject = LinkedListNode(TextBox("Hello"))
        self.play(Create(my_mobject))
        
        boxy = TextBox("a")
        boxy.move_to(my_mobject.get_center())
        boxy.shift(RIGHT*4+UP*10)
        self.play(boxy.animate.shift(DOWN*10))
        anim = my_mobject.add_node("a")
        self.add(anim)
        self.remove(boxy)
        self.play(Create(my_mobject.start.arrow))

class DLinkedList(Scene):
    def construct(self):
        my_mobject = LinkedListNode(DoubleLinked("Hello"))
        self.play(Create(my_mobject))
        
        boxy = DoubleLinked("a")
        boxy.move_to(my_mobject.get_center())
        boxy.shift(RIGHT*4+UP*10)
        self.play(boxy.animate.shift(DOWN*10))
        anim = my_mobject.add_node("a")
        self.add(anim)
        self.remove(boxy)
        self.play(Create(anim.backarrow),Create(anim.previous.arrow))
        self.play(my_mobject.animate.shift(UP))


class multiLink(MovingCameraScene):
    def construct(self):
        sq = Arrow()
        arrowname = Text("The Allmighty Finger of God")
        arrowname.move_to((0,3.5,0))
        self.add(arrowname)
        sq.put_start_and_end_on((0,3,0),(0,1.5,0))
        self.add(sq)
        mob = LinkedListNode(TextBox("0"))
        self.play(Create(mob))
        center = mob.get_center()
        cam = VGroup(self.camera.frame,sq,arrowname)
        arr = mob.start
        for x in range(4):
            y = x+1
            name = str(y)
            boxy = TextBox(name)
            boxy.move_to(center)
            boxy.shift(UP*10+RIGHT*4*y)
            #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
            self.play(cam.animate(run_time=y/4).move_to((4*y,0,0)))
            self.play(boxy.animate.shift(DOWN*10))
            anim = mob.add_node(name)
            self.add(anim)
            self.remove(boxy)
            self.play(Create(arr.arrow))
            #self.play(mob.animate(run_time = 0.25).shift(RIGHT*3*y))
            self.play(cam.animate(run_time = 0.25).move_to((0,0,0)))
            self.play(Wait(run_time=0.25))
            arr = anim

        for z in range(50):
            name = str(z+y+1)
            a = mob.add_node(name)
            self.add(a)

        y += 51
        name = str(y)
        boxy = TextBox(name)
        boxy.move_to(center)
        boxy.shift(UP*10+RIGHT*4*y)
        #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
        self.play(cam.animate(run_time=y/10).move_to((4*y,0,0)))
        self.play(boxy.animate.shift(DOWN*10))
        last = mob.last
        anim = mob.add_node(name)
        self.add(anim)
        self.remove(boxy)
        self.play(Create(last.arrow))


class multiLinkcut(MovingCameraScene):
    def construct(self):
        #sq = Arrow()
        #arrowname = Text("The Allmighty Finger of God")
        #arrowname.move_to((0,3.5,0))
        #self.add(arrowname)
        #sq.put_start_and_end_on((0,3,0),(0,1.5,0))
        #self.add(sq)
        mob = LinkedListNode(DoubleLinked("0"))
        self.add(mob)
        #self.play(Create(mob))
        cam = VGroup(self.camera.frame)
        for x in range(4):
            y = x+1
            name = str(y)
            #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
            #self.play(cam.animate(run_time=y/4).move_to((4*y,0,0)))
            #self.play(boxy.animate.shift(DOWN*10))
            anim = mob.add_node(name)
            self.add(anim)
            #self.play(Create(arr.arrow))
            #self.play(mob.animate(run_time = 0.25).shift(RIGHT*3*y))
            #self.play(cam.animate(run_time = 0.25).move_to((0,0,0)))
            #self.play(Wait(run_time=0.25))
            arr = anim

        for z in range(15):
            name = str(z+y+1)
            a = mob.add_node(name)
            self.add(a)

        #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
        self.play(cam.animate(run_time=y/10).move_to((4*5.5,1,0)))
        #self.play(cam.animate.set_width(50))
        anim = mob.cut_range(5,6,self)
        #self.play(anim.animate.shift(UP*7))
        self.play(mob.animate.shift(DOWN*50))
        mob2 = LinkedListNode(DoubleLinked("A"))
        mob2.add_node("B")
        mob2.add_node("C")
        mob2.add_node("D")
        mob2.add_node("E")
        mob2.add_node("F")
        mob2.add_node("G")
        mob2.add_node("H")
        self.play(Create(mob2))
        self.add(mob2)
        mob2.insert(anim,5,self)
        #x = mob2.cut_range(5,20,self)
        #self.play(x.animate.shift(RIGHT*(3.640625*2)))
        #anim.last.connect(x.start,self)
        #mob2.last.connect(anim.start,self)
        self.play(mob2.animate.shift(RIGHT*100))
        self.wait(1)
