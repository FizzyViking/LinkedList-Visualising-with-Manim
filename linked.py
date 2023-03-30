from manim import *

from LinkedManimList import *

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

class multiLink(MovingCameraScene):
    def construct(self):
        sq = Arrow()
        arrowname = Text("The Allmighty Finger of God")
        arrowname.move_to((0,3.5,0))
        self.add(arrowname)
        sq.put_start_and_end_on((0,3,0),(0,1.5,0))
        self.add(sq)
        t = Text("0")
        mob = LinkedListNode(t)
        self.play(Create(mob))
        center = mob.get_center()
        cam = VGroup(self.camera.frame,sq,arrowname)
        for x in range(4):
            y = x+1
            name = str(y)
            boxy = TextBox(Text(name))
            boxy.move_to(center)
            boxy.shift(UP*10+RIGHT*3*y)
            #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
            self.play(cam.animate(run_time=y/4).move_to((3*y,0,0)))
            self.play(boxy.animate.shift(DOWN*10))
            anim = mob.add_node(Text(name))
            self.add(anim[0])
            self.remove(boxy)
            self.play(Create(anim[1]))
            #self.play(mob.animate(run_time = 0.25).shift(RIGHT*3*y))
            self.play(cam.animate(run_time = 0.25).move_to((0,0,0)))
            self.play(Wait(run_time=0.25))

        for z in range(50):
            name = str(z+y+1)
            a,b = mob.add_node(Text(name))
            self.add(a,b)

        y += 51
        name = str(y)
        boxy = TextBox(Text(name))
        boxy.move_to(center)
        boxy.shift(UP*10+RIGHT*3*y)
        #self.play(mob.animate(run_time=y/4).shift(LEFT*3*y))
        self.play(cam.animate(run_time=y/10).move_to((3*y,0,0)))
        self.play(boxy.animate.shift(DOWN*10))
        anim = mob.add_node(Text(name))
        self.add(anim[0])
        self.remove(boxy)
        self.play(Create(anim[1]))
