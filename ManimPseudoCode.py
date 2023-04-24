import os
import html
import sys

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
                 language : str | None = None,
                 ):
        
        super().__init__()

        self.code = code
        self.code_file = code_file
        self.lines = []
        self.font_size = font_size
        self.height = Text("fg",font_size=self.font_size).height
        self.line_space = 2
        self.html_string = None
        self.language = language

        self.code_string = None
        self.file_path = None

        if self.code_file:
            self.file_path = self.isValidPath()
            self.code_string = self.file_path.read_text(encoding="utf-8")
        elif self.code:
            self.code_string = self.code
        else:
            raise ValueError("No file or code was given")
        
        self.html_string = self.formatCodeToHtml(self.language, self.file_path, self.code_string)
        self.writeHtmlString()

        lines = self.html_string.split("\n")
        for i in range(len(lines)):
            print(lines[i]+"\n")
        
    def get_codestring(self):
        return self.code_string
    
    def isValidPath(self):
        if self.code_file is None:
            raise ValueError("Code file path is not properly defined")
        return Path(self.code_file)
    
    ''' format code string to html '''
    def formatCodeToHtml(self, 
                         _lexer : str, 
                         file_path: Path,
                         code : str
                         ):
        
        html_formatter = HtmlFormatter(
            linenos = 'inline',
            noclasses = True,
        )
        
        lexer = None
        html_string = ""

        if _lexer is None and file_path:
            lexer = guess_lexer_for_filename(file_path, code)
            html_string = highlight(code, lexer, html_formatter)
        else:
            html_string = highlight(code, get_lexer_by_name(_lexer, **{}), html_formatter)
        return html_string
    
    def writeHtmlString(self):
        output_dir = Path() / "assets" / "code"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{self.file_path}.html").write_text(self.html_string)
        

    """ Mark up to n lines """
    def marklines(self, line_numbers):
        for line in line_numbers:
            # mob = get_line(line)
            padding = 0.1 
            r = Rectangle()
            r.stretch_to_fit_width(mob.width+padding)
            r.move_to(mob)
            r.stretch_to_fit_height((self.height+padding))
            r.align_to(mob,DOWN)
            r.shift(DOWN*(padding/2))
            diffp = (self.height-mob.height) / self.height
            print(diffp)
            if diffp == 0 or (diffp >= 0.23 and diffp <= 0.24):
                return r
            r.shift(DOWN*0.2118770857773395*self.height)
        return r
class TextWithBoundingBox(VGroup):
    def __init__(self, text, fontsize):
        super().__init__()
        self.text = Text(text,font_size=fontsize)
        self.box = get_box(mob=self.text,fontsize=DEFAULT_FONT_SIZE)
        self.add(self.text,self.box)
class CodeLine(VGroup):
    def __init__(self, text, fontsize, linenumber, indentation):
        super().__init__()
        self.number = TextWithBoundingBox(str(linenumber),fontsize)
        self.text = TextWithBoundingBox(text,fontsize)
        self.text.align_to(self.number,UP)
        self.text.align_to(self.number,LEFT)
        self.text.shift(RIGHT*indentation)
        self.add(self.text)
        self.add(self.number)
        self.boundingbox = get_box(self,fontsize)
        self.add(self.boundingbox)






def get_box(mob:Mobject, fontsize): 
    print(mob, "a")
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
    print(diffp)
    if diffp == 0.24500146831390812:
        r.shift(DOWN*(0.24500146831390812-0.2118770857773395)*height)
        return r
    if diffp == 0 or (diffp >= 0.23 and diffp <= 0.24):
        return r
    r.shift(DOWN*0.2118770857773395*height)
    return r