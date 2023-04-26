import os
import html

from manim import *
from pathlib import Path
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_all_styles

class PseudoCode(VGroup):
    def __init__(self, 
                 code_file: str | os.PathLike | None = None, 
                 code: str | None = None,
                 font_size : float = 24,
                 ):
        
        super().__init__()

        self.code = code
        self.code_file = code_file
        self.lines = []
        self.font_size = font_size
        self.line_height = Text("fg",font_size=self.font_size).height
        self.line_space = 0.5
        self.html_string = None

        self.code_string = None
        self.file_path = None
        self.linecount = 0
        self.lastline = None

        self.highlighting_box = Rectangle(height = self.line_height,width = 0.1)
        self.highlighting_box.stroke_width = 0
        self.add(self.highlighting_box)

        if self.code_file:
            self.file_path = self.isValidPath()
            self.code_string = self.file_path.read_text(encoding="utf-8")
        elif self.code:
            self.code_string = self.code
        else:
            print("all")
            #raise ValueError("No file or code was given")
        
        
    
    def get_codestring(self):
        return self.code_string
    
    def isValidPath(self):
        if self.code_file is None:
            raise ValueError("File of code is not properly defined")
        return Path(self.code_file)
    def add_line(self,content,indent,col):
        self.linecount += 1
        l = CodeLine(content,self.font_size,self.linecount,indent,col)
        self.add(l)
        self.lines.append(l)
        if(self.lastline != None):
            l.align_to(self.lastline,UP)
            l.align_to(self.lastline,LEFT)
            l.shift(DOWN*(self.line_height+self.line_space))
        if self.highlighting_box.width < l.width:
            self.highlighting_box=self.highlighting_box.stretch_to_fit_width(l.width)
            self.highlighting_box.align_to(l,LEFT)
            #print("streching", self.highlighting_box.width, l.width),
        self.lastline = l
    def highlight(self,i):
        self.highlighting_box.stroke_width=2
        self.highlighting_box.align_to(self.lines[i],UP)
        self.highlighting_box.align_to(self.lines[i],LEFT)
    def _highlight(self,i):
        if(self.highlighting_box.stroke_width == 0):
            self.highlight(i)
            return Create(self.highlighting_box)
        else:
            l = self.lines[i]
            y = self.highlighting_box.get_edge_center(DOWN)[1]-l.get_edge_center(DOWN)[1]
            x = self.highlighting_box.get_edge_center(LEFT)[0]-l.get_edge_center(LEFT)[0]
            return self.highlighting_box.animate.shift(DOWN*y+LEFT*x)



class TextWithBoundingBox(VGroup):
    def __init__(self, text, fontsize,col):
        super().__init__()
        self.text = Text(text,font_size=fontsize,color = col)
        self.box = get_box(mob=self.text,fontsize=fontsize)
        self.add(self.text,self.box)
class CodeLine(VGroup):
    def __init__(self, text, fontsize,  linenumber, indentation,col):
        super().__init__()
        self.number = TextWithBoundingBox(str(linenumber),fontsize,WHITE)
        self.text = TextWithBoundingBox(text,fontsize,col)
        self.text.align_to(self.number,UP)
        self.text.align_to(self.number,LEFT)
        self.text.shift(RIGHT*indentation)
        self.add(self.text)
        self.add(self.number)
        self.boundingbox = get_box(self,fontsize)
        self.add(self.boundingbox)






def get_box(mob:Mobject, fontsize): 
    height = Text("fg", font_size=fontsize).height
    padding = 0.0 #might make this a parameter
    r = Rectangle()
    r.stroke_width = 1
    r.stretch_to_fit_width(mob.width+padding)
    r.move_to(mob)
    r.stretch_to_fit_height(height+padding)
    r.align_to(mob,DOWN)
    r.shift(DOWN*(padding/2))
    diffp = (height-mob.height)/height
    #print(diffp)
    if diffp == 0.24500146831390812:
        r.shift(DOWN*(0.24500146831390812-0.2118770857773395)*height)
        return r
    if diffp <= 0.05 or (diffp >= 0.23 and diffp <= 0.24):
        return r
    r.shift(DOWN*0.2118770857773395*height)
    return r