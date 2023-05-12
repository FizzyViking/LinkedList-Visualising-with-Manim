import os

from manim import *
from pathlib import Path

class PseudoCode(VGroup):
    """
    A Manim class for PseudoCode highlighting.

    Parameters:
    code_file: File of pseudocode
    code: Optional string of pseudocode, if code_file is not given
    font_size: Size of font, default: 24
    line_space: space between lines, default: 0.1
    """
    def __init__(self, 
                 code_file: str | os.PathLike | None = None, 
                 code: str | None = None,
                 font_size : float = 24,
                 line_space : float = 0.1
                 ):
        
        super().__init__()

        self.code = code
        self.code_file = code_file
        self.lines = []
        self.font_size = font_size
        self.line_height = Text("fg",font_size=self.font_size).height+0.1
        self.line_space = line_space
        
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
            raise ValueError("No file or code was given")

        for idx, line in enumerate(self.code_string.split("\n")):
            self.add_line(f'{idx+1}' + " " f'{line}')

    def isValidPath(self):
        if self.code_file is None:
            raise ValueError("Code file path is not properly defined")
        return Path(self.code_file)
    
    def add_line(self,content,col:list = []):
        self.linecount += 1
        l = TextWithBoundingBox(content,self.font_size)
        self.add(l)
        self.lines.append(l)
        if(self.lastline != None):
            l.align_to(self.lastline,UP)
            l.align_to(self.lastline,LEFT)
            l.shift(DOWN*(self.line_height+self.line_space))
        if self.highlighting_box.width < l.width:
            self.highlighting_box.stretch_to_fit_width(l.width).stretch_to_fit_height(l.height)
            self.highlighting_box.align_to(l,LEFT)
            self.max_line_length = self.highlighting_box.width
            #print("streching", self.highlighting_box.width, l.width),
        self.lastline = l
        for start,end,c in col:
            l.text[start:end].set_color(c)

    def highlight(self,i):
        i -=1
        self.highlighting_box.stroke_width=2
        self.highlighting_box.align_to(self.lines[i],UP)
        self.highlighting_box.align_to(self.lines[i],LEFT)
    @override_animation(highlight)
    def _highlight(self,i, **kwargs):
        if(self.highlighting_box.stroke_width == 0):
            self.highlight(i)
            return Create(self.highlighting_box, **kwargs)
        else:
            l = self.lines[i-1]
            y = self.highlighting_box.get_edge_center(DOWN)[1]-l.get_edge_center(DOWN)[1]
            x = self.highlighting_box.get_edge_center(LEFT)[0]-l.get_edge_center(LEFT)[0]
            return self.highlighting_box.animate(**kwargs).shift(DOWN*y+LEFT*x)
    def highlight_section(self,line,start,end):
        l = self.get_text_of_line(line)
        first = l[start]
        last = l[end]
        subhighlighter = Rectangle(width = last.get_edge_center(RIGHT)[0]-first.get_edge_center(LEFT)[0], height= self.line_height)
        subhighlighter.stroke_width = 1
        #l[1:4].set_color(YELLOW)
        subhighlighter.align_to(first,LEFT).align_to(l,UP)
        self.add(subhighlighter)
        return(subhighlighter)
    def get_text_of_line(self,line):
        return self.lines[line-1].text

class TextWithBoundingBox(VGroup):
    def __init__(self, text, fontsize:int=48,col:str = WHITE):
        super().__init__()
        self.text = Text(("o"+text),font_size=fontsize,color=col)
        mob = Text("o",font_size=  fontsize)
        mob.move_to(self.text[0])
        self.text.remove(self.text[0])
        height = Text("fg", font_size=fontsize).height
        padding = 0.1 #might make this a parameter
        self.box = Rectangle()
        self.box.stroke_width = 0
        self.box.stretch_to_fit_width(self.text.width+padding)
        self.box.stretch_to_fit_height(height+padding)
        self.box.move_to(mob)
        self.box.shift(DOWN*(self.box.get_edge_center(LEFT)[1]-mob.get_edge_center(LEFT)[1]))
        #self.box.align_to(mob,DOWN)
        #self.box.shift(DOWN*(padding/2))
        #self.box.shift(DOWN*0.2118770857773395*height)
        self.box.align_to(self.text,LEFT)
        self.box.shift(LEFT*padding/2)
        self.add(self.text,self.box)
class CodeLine(VGroup):
    def __init__(self, text, fontsize:int=48,  linenumber:int=1, indentation:int = 1,  col:str = WHITE):
        super().__init__()
        self.number = TextWithBoundingBox(str(linenumber),fontsize,WHITE)
        self.text = TextWithBoundingBox(text,fontsize,col)
        self.text.align_to(self.number,UP)
        self.text.align_to(self.number,LEFT)
        self.text.shift(RIGHT*indentation)
        self.add(self.text)
        self.add(self.number)
        self.boundingbox = get_box(self)
        self.add(self.boundingbox)

def get_box(mob): 
    r = Rectangle().stretch_to_fit_height(mob.height).stretch_to_fit_width(mob.width).align_to(mob,DOWN).align_to(mob,LEFT)
    r.stroke_width = 1
    return (r)

