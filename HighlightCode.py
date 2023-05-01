from manim import *
from LinkedManimList import *
from ManimPseudoCode import *

class PseudoCodeExample(Scene):
    def construct(self):
        pseudo = PseudoCode(code_file="DoubleLinkedList.py")

class HighlightCode(Scene):
    def construct(self):

        pseudo = PseudoCode(code_file="DoubleLinkedList.py")


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



class SquareAroundTextExperiments(Scene):
    def construct(self):
        a = Text("lg")
        b = Text("goo")
        c=  Text("oo")
        d = Text("loo")
        e = Text("AGURK")
        e.shift(UP)
        self.add(a,b,c,d,e)
        b.shift(RIGHT*2)
        c.shift(RIGHT*4)
        d.shift(LEFT*2)
        l = Line()
        #l.put_start_and_end_on((-10,0,0),(10,0,0))
        #self.add(l)
        #print(a.height,a.get_y())
        #print(b.height,b.get_y())
        #print(c.height,c.get_y())
        #print(d.height,d.get_y())
        #print((a.height-b.height))
        #print((a.height-c.height))

        #print((b.height-c.height)/a.height)
        t = TextSquarer(a.font_size)
        #self.add(t.get_box(a))
        #self.add(t.get_box(b))
        r = t.get_box(a)
        l = Line()
        self.add(r)
        l.put_start_and_end_on(r.get_edge_center(UP),r.get_edge_center(UP)+RIGHT*2)
        #self.add(l)
        #self.add(t.get_box(d))
        #self.add(t.get_box(e))
        self.add(CodeLine("mone",DEFAULT_FONT_SIZE,4,0.5))
        self.add(linker(a,r))
        self.play(a.animate.shift(UP))
        a.set_color(YELLOW)
        print(color_to_int_rgba(a.get_color()))
        print(r.get_color())
        self.wait(1)
        self.play(r.animate.shift(UP))
        r.stroke_width = 0
        self.play(a.animate.shift(DOWN))
        a.set_color(WHITE)
        self.wait(1)
class CodeLineTest(Scene):
    def construct(self):
        #self.add(CodeLine("gggg",DEFAULT_FONT_SIZE,1,1))
        #self.add(CodeLine("dddd",DEFAULT_FONT_SIZE,1,1))
        #self.add(CodeLine("llll",DEFAULT_FONT_SIZE,1,1))
        pse = PseudoCode(code_file="DoubleLinkedList.py")
        sq = Square()
        sq.shift(LEFT*4)
        self.add(sq)
        pse.shift(UP)
        # pse.add_line("Spin",1,BLUE)
        # pse.add_line("Speen",2,WHITE)
        # pse.add_line("Speeeen",3,YELLOW)
        # pse.add_line("Speeeeeeeen",1,WHITE)
        #pse.lines[3].shift(RIGHT)
        self.add(pse)
        self.play(pse._highlight(1))
        self.play(Rotate(sq,PI))
        self.play(pse._highlight(2))
        self.play(Rotate(sq,PI*2))
        self.play(pse._highlight(3))
        self.play(Rotate(sq,PI*3))
        self.play(pse._highlight(4))
        self.play(Rotate(sq,PI*8))
        self.play(Create(pse.highlight_section(3,3,5)))
        self.wait(1)