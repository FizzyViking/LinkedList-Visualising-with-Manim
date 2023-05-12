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
        #Set starting state
        pc = PseudoCode("multiadd.txt")
        self.add(pc)
        pc.to_corner(UL)
        cam = VGroup(self.camera.frame,pc)
        cam.set_width(30)
        cam.shift(UP*2)
        mob = LinkedNodes(SingleLinked("0"))
        self.play(Create(mob))
        center = mob.get_center()
        arr = mob.start

        self.play(pc.animate(run_time = 0.25).highlight(1))
        for x in range(4): #Moved to position of new node, node moved down from offscreen, then gets connected
            y = x+1
            name = str(y)
            boxy = SingleLinked(name)
            boxy.move_to(center)
            boxy.shift(UP*10+RIGHT*4*y)
            self.play(pc.animate(run_time = 0.25).highlight(2))
            self.play(cam.animate(run_time=y/4).move_to((4*y,cam.get_y(),0)))
            self.play(pc.animate(run_time = 0.25).highlight(3))
            self.play(boxy.animate.shift(DOWN*10))
            anim = mob.add_node(name)
            self.add(anim)
            self.remove(boxy)
            self.remove(arr.arrow)
            self.play(pc.animate(run_time = 0.25).highlight(4))
            self.play(Create(arr.arrow))
            self.play(pc.animate(run_time = 0.25).highlight(1))
            self.play(cam.animate(run_time = 0.25).move_to((0,cam.get_y(),0)))
            self.play(Wait(run_time=0.25))
            arr = anim

        for z in range(50): #Creates 50 nodes
            name = str(z+y+1)
            a = mob.add_node(name)
            self.add(a)
        
        #Traversal to 50+
        y += 51
        name = str(y)
        boxy = SingleLinked(name)
        boxy.move_to(center)
        boxy.shift(UP*10+RIGHT*4*y)
        t = Text("Linear runtime.")
        t.shift(UP*3)
        self.add(t)
        sh = pc.highlight_section(2,6,15)
        cam.add(t)
        self.play(pc.animate(run_time = 0.25).highlight(2))
        self.play(cam.animate(run_time=y/10).move_to((4*y,cam.get_y(),0)))
        self.remove(t)
        pc.remove(sh)

        #Cration of last node
        self.play(pc.animate(run_time = 0.25).highlight(3))
        self.play(boxy.animate.shift(DOWN*10))
        last = mob.last
        anim = mob.add_node(name)
        self.add(anim)
        self.remove(boxy)
        self.remove(last.arrow)
        self.play(pc.animate(run_time = 0.25).highlight(4))
        self.play(Create(last.arrow))
        self.wait(1)


class multiLinkcut(MovingCameraScene):
    def construct(self):
        h = 1
        p = PseudoCode(code_file= "splice.txt",font_size=18)
        self.add(p)
        p.to_corner(UL)

        #Creating original list
        original_list = LinkedNodes(DoubleLinked("0"))
        self.add(original_list)
        cam = VGroup(self.camera.frame,p)
        for x in range(8):
            y = x+1
            name = str(y)
            original_list.add_node(name)

        #Move camera into place and size
        cam.set_width(30)
        cam.move_to((4*5,5,0))

        #cutting animations
        h += 1
        self.play(p._highlight(h))
        cutstart, segment, cutend, tail = original_list.cut_range(5,6,self)
        self.add(segment)
        vertdist = (segment.height+1)
        self.play(segment.animate.shift(UP*vertdist))
        #Connect cutstart and cutend
        h += 1
        self.play(p._highlight(h))
        c1,c2 = cutstart.connect(cutend)
        self.play(c1)
        h += 1
        self.play(p._highlight(h))
        self.play(c2)

        #Disconnect segment
        dcl1 = segment.last.disconnect()
        h += 1
        self.play(p._highlight(h))        
        self.play(dcl1[0])
        dc1= segment.start.disconnect_back()
        h += 1
        self.play(p._highlight(h))
        self.play(dc1)

        #Move Tail next to cutstart
        diff = cutend.sq.get_x()-segment.start.sq.get_x()
        self.play(tail.animate.shift(LEFT*diff))
        self.play(original_list.animate.shift(DOWN*50))

        #Creating a new list
        h += 1
        self.play(p._highlight(h))
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
        self.play(g.animate.shift(RIGHT*4*segment.count))

        #Connect last of segment with first of tail
        h += 1
        self.play(p._highlight(h))
        c1,c2 = segment.last.connect(ce)
        self.play(c1)
        h += 1
        self.play(p._highlight(h))
        self.play(c2)

        #Connect new_list to first of segment
        c1,c2 = cs.connect(segment.start)
        h += 1
        self.play(p._highlight(h))
        self.play(c1)
        h += 1
        self.play(p._highlight(h))
        self.play(c2)

        #Happy ending
        self.play(segment.animate.shift(DOWN*vertdist))
        self.wait(1)
