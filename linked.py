from manim import *
from LinkedManimList import *
from ManimPseudoCode import *
class LinkedList(Scene):
    def construct(self):
        my_mobject = LinkedNodes(SingleLinked("Hello"))
        self.play(Create(my_mobject))
        
        boxy = SingleLinked("a")
        boxy.move_to(my_mobject.get_center())
        boxy.shift(RIGHT*4+UP*10)
        self.play(boxy.animate.shift(DOWN*10))
        anim = my_mobject.add_node("a")
        self.add(anim)
        self.remove(boxy)
        self.play(Create(my_mobject.start.arrow))

class DLinkedList(Scene):
    def construct(self):
        my_mobject = LinkedNodes(DoubleLinked("Hello"))
        self.play(Create(my_mobject))
        
        boxy = DoubleLinked("a")
        boxy.move_to(my_mobject.get_center())
        boxy.shift(RIGHT*4+UP*10)
        self.play(boxy.animate.shift(DOWN*10))
        anim = my_mobject.add_node("a")
        self.add(anim)
        self.remove(boxy)
        self.play(Create(anim.back_arrow),Create(anim.previous.arrow))
        self.play(my_mobject.animate.shift(UP))


class multiLink(MovingCameraScene):
    def construct(self):
        sq = Arrow()
        arrowname = Text("The Allmighty Finger of God")
        arrowname.move_to((0,3.5,0))
        self.add(arrowname)
        sq.put_start_and_end_on((0,3,0),(0,1.5,0))
        self.add(sq)
        mob = LinkedNodes(SingleLinked("0"))
        self.play(Create(mob))
        center = mob.get_center()
        cam = VGroup(self.camera.frame,sq,arrowname)
        arr = mob.start
        for x in range(4):
            y = x+1
            name = str(y)
            boxy = SingleLinked(name)
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
        boxy = SingleLinked(name)
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
        #Creating original list
        original_list = LinkedNodes(DoubleLinked("0"))
        self.add(original_list)
        cam = VGroup(self.camera.frame)
        for x in range(8):
            y = x+1
            name = str(y)
            original_list.add_node(name)

        #Move camera into place and size
        self.play(cam.animate(run_time=y/10).move_to((4*5.5,1,0)))
        self.play(cam.animate.set_width(50))

        #cutting animations
        cutstart, segment, cutend, tail = original_list.cut_range(5,6,self)
        self.add(segment)
        vertdist = (segment.height+1)
        self.play(segment.animate.shift(UP*vertdist))

        #Connect cutstart and cutend
        c1,c2 = cutstart.connect(cutend)
        self.play(c1[0])
        cutstart.arrow.end = c1[1]
        self.play(c2[0])
        cutend.back_arrow.end = c2[1]

        #Disconnect segment
        dcl1, dcl2 = segment.last.disconnect()
        self.play(dcl1[0])
        dc1, dc2= segment.start.disconnect_back()
        self.play(dc1)

        #Move Tail next to cutstart
        diff = cutend.sq.get_x()-segment.start.sq.get_x()
        self.play(tail.animate.shift(LEFT*diff))
        self.play(original_list.animate.shift(DOWN*50))

        #Creating a new list
        new_list = LinkedNodes(DoubleLinked("A"))
        new_list.add_node("B")
        new_list.add_node("C")
        new_list.add_node("D")
        new_list.add_node("E")
        new_list.add_node("F")
        new_list.add_node("G")
        new_list.add_node("H")
        self.play(Create(new_list))
        self.add(new_list)

        #Inserting into the vgroup
        cs,ce,g = new_list.insert(segment,5)
        self.play(g.animate.shift(RIGHT*3.640625*segment.count))

        #Connect last of segment with first of tail
        c1,c2 = segment.last.connect(ce)
        self.play(c1[0])
        segment.last.arrow.end = c1[1]
        self.play(c2[0])
        ce.back_arrow.end = c2[1]

        #Connect new_list to first of segment
        c1,c2 = cs.connect(segment.start)
        self.play(c1[0])
        cs.arrow.end = c1[1]
        self.play(c2[0])
        segment.start.back_arrow.end = c2[1]

        #Happy ending
        self.play(segment.animate.shift(DOWN*vertdist))
        self.play(Rotate(new_list,PI*100))
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