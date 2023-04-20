from manim import *
from LinkedManimList import *
from ManimPseudoCode import *

class HighlightCode(Scene):
    def construct(self):

        pseudo = PseudoCode(code_file="DoubleLinkedList.py")
        print(pseudo.get_codestring())


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
        #self.add(a,b,c,d,e)
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
        r = VGroup(t.get_box(c),c)
        l = Line()
        l.put_start_and_end_on(r.get_edge_center(UP),r.get_edge_center(UP)+RIGHT*2)
        #self.add(l)
        #self.add(t.get_box(d))
        #self.add(t.get_box(e))
        self.add(CodeLine("mone",DEFAULT_FONT_SIZE,4,0.5))

class TextSquarer:
    def __init__(self,fontsize): #Define fontsize using index on Text object does not return tex object and might not have fontsize property
        self.height = Text("fg",font_size=fontsize).height 
    def get_box(self,mob): 
        padding = 0.1 #might make this a parameter
        r = Rectangle()
        r.stretch_to_fit_width(mob.width+padding)
        r.move_to(mob.width+padding)
        r.stroke_width = 0
        r.stretch_to_fit_height((self.height+padding))
        r.align_to(mob,DOWN)
        r.shift(DOWN*(padding/2))
        topr = r.get_edge_center(UP)[1]
        topm = mob.get_edge_center(UP)[1]
        diffp = (self.height-mob.height)/self.height
        print(diffp)
        if diffp == 0 or (diffp >= 0.23 and diffp <= 0.24):
            return r
        r.shift(DOWN*0.2118770857773395*self.height)
        return r

