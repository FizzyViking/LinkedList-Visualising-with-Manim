from manim import *
from LinkedManimList import *

class HighlightCode(Scene):
    def construct(self):
        code = Paragraph(
            'class LinkedList():\n', 'def _init_(self):\n','self.data = None'
        )

        rendered_code = Code("DoubleLinkedList.py", tab_width=4, background="window",
                            language="Python", font="Monospace")
        self.add(rendered_code)
        self.play(
            Indicate(rendered_code[2].chars[4]), Indicate(rendered_code[2].chars[5]))
        self.wait(1.5)
        box = Rectangle()
        self.play(
            Circumscribe(rendered_code[2].chars[4][4]), Circumscribe(rendered_code[2].chars[5][7]))
        self.play(box.animate.surround(rendered_code[2].chars[5][7]))
        g_part = VGroup(box, rendered_code[2].chars[5][7])
        self.play(g_part.animate.shift(DOWN*4))