from manim import *
from LinkedManimList import *
from ManimPseudoCode import *
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
        for x in range(8):
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
        five = mob.get_node(5)
        #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
        self.play(cam.animate(run_time=y/10).move_to((4*5.5,1,0)))
        self.play(cam.animate.set_width(50))
        five = mob.get_node(5)
        #print(five.content.text,"gotten",five.next_node.content.text)
        #five.shift(UP)
        #line = CodeLine("peepeepoopoo",DEFAULT_FONT_SIZE,6,1)
        #line.shift(RIGHT*18)
        #self.add(line)
        #self.add(linker(five.backarrow,line.boundingbox,2))
        cutstart, anim, cutend, tail = mob.cut_range(5,6,self)
        self.add(anim)
        #self.play(anim.animate.shift(UP*7))

        #cutting animations
        vertdist = (anim.height+1)
        self.play(anim.animate.shift(UP*vertdist))

        c1,c2 = cutstart.connect(cutend)
        self.play(c1[0])
        cutstart.arrow.end = c1[1]
        self.play(c2[0])
        cutend.backarrow.end = c2[1]

        dcl1, dcl2 = anim.last.disconnect()
        self.play(dcl1[0])
        dc1, dc2= anim.start.disconnect_back()
        self.play(dc1)
        diff = cutend.sq.get_x()-anim.start.sq.get_x()
        self.play(tail.animate.shift(LEFT*diff))
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
        cs,ce,g = mob2.insert(anim,5)
        self.play(g.animate.shift(RIGHT*3.640625*anim.count))


        c1,c2 = anim.last.connect(ce)
        self.play(c1[0])
        anim.last.arrow.end = c1[1]
        self.play(c2[0])
        ce.backarrow.end = c2[1]

        c1,c2 = cs.connect(anim.start)
        self.play(c1[0])
        cs.arrow.end = c1[1]
        self.play(c2[0])
        anim.start.backarrow.end = c2[1]

        self.play(anim.animate.shift(DOWN*vertdist))
        #x = mob2.cut_range(5,20,self)
        #self.play(x.animate.shift(RIGHT*(3.640625*2)))
        #anim.last.connect(x.start,self)
        #mob2.last.connect(anim.start,self)
        self.play(mob2.animate.shift(RIGHT*10))
        
        self.wait(1)

class linker(Circle):
    def __init__(self, observed,highligted,state):
        self.observed = observed
        self.highlighted = highligted 

        super().__init__(radius=0)
        def update(mob):
            #print(mob.observed.state)
            if(mob.observed.state == state):
                mob.highlighted.stroke_width = 2
            else:
                mob.highlighted.stroke_width = 0
        self.add_updater(update)