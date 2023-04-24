from manim import *

from LinkedManimList import *


class Front(Scene):
    def construct(self):
        mob = LinkedNodes(SingleLinked("0"))
        center = mob.get_center()

        for x in range(3):
            y = x+1
            name = str(y)
            mob.add_node(name)

        self.add(mob)
        headtext = Text("Header")
        headbox = Rectangle(width=2.5)
        header = VGroup(headbox,headtext)
        header.shift(LEFT*5+DOWN)
        self.play(Create(header))
        l = Arrow()
        l.put_start_and_end_on(header.get_edge_center(RIGHT), mob.start.back.get_center())
        self.play(Create(l))

        boxy = SingleLinked("1000")
        boxy.move_to(center)
        boxy.shift(UP*10)
        self.play(mob.animate.shift(RIGHT*4))
        self.add(boxy)
        self.play(boxy.animate.shift(DOWN*10))
        l2 = link(boxy.pt,mob.start.back)
        self.play(Create(l2))
