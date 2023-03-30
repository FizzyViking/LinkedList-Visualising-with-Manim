from manim import *

from LinkedManimList import *


class Front(Scene):
    def construct(self):
        t = Text("0")
        mob = LinkedListNode(t)
        center = mob.get_center()

        for x in range(3):
            y = x+1
            name = str(y)
            mob.add_node(Text(name))

        self.add(mob)
        headtext = Text("Header")
        headbox = Rectangle(width=2.5)
        header = VGroup(headbox,headtext)
        header.shift(LEFT*5+DOWN)
        self.play(Create(header))
        l = Arrow()
        l.put_start_and_end_on(header.get_edge_center(RIGHT), mob.box.get_edge_center(LEFT))
        self.play(Create(l))

        boxy = TextBox(Text("1000"))
        boxy.move_to(center)
        boxy.shift(UP*10)
        self.play(mob.animate.shift(RIGHT*3))
        self.add(boxy)
        self.play(boxy.animate.shift(DOWN*10))
        l2 = link(boxy.pt,mob.box.sq)
        self.play(Create(l2))