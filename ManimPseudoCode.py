import os
import html
import sys

from manim import *
from pathlib import Path
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.styles import get_all_styles
from collections import defaultdict

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
        self.line_height = Text("fg",font_size=self.font_size).height
        self.line_space = 0.1
        self.html_string = None
        self.language = language
        self.code_lines = defaultdict(str)
        
        self.code_string = None
        self.file_path = None
        self.linecount = 0
        self.lastline = None
        self.wordColors = dict()

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
        
        self.html_string = self.formatCodeToHtml(self.language, self.file_path, self.code_string)
        self.html_string = self.html_string.replace("<span></span>", "") # Pygment bug
        self.writeHtmlString()
        self.gen_code_text()

        for idx, line in enumerate(self.code_string.split("\n")):
            #self.code_lines[idx+1] = line
            self.add_line(f'{idx+1}' + " " f'{line}')
        
        #for i in range(len(self.code_lines)):
            #self.code_lines[i+1] = f'{i+1}' + " " f'{self.code_lines[i+1]}'
            #self.add_line(f'{i+1}' + " " f'{self.code_lines[i+1]}')
        
    def getColoredWords(self):
        textItems = []
        for word, clr in list(self.wordColors.items()):
            #textItems.append(Tex(word).set_color(clr))
            textItems.append(Text(word, color=clr))
            print(word, clr)
        return textItems

    def isValidPath(self):
        if self.code_file is None:
            raise ValueError("Code file path is not properly defined")
        return Path(self.code_file)
    
    def add_line(self,content,col:str = WHITE):
        self.linecount += 1
        l = TextWithBoundingBox(content,self.font_size,col)
        self.add(l)
        self.lines.append(l)
        if(self.lastline != None):
            l.align_to(self.lastline,UP)
            l.align_to(self.lastline,LEFT)
            l.shift(DOWN*(self.line_height+self.line_space))
        if self.highlighting_box.width < l.width:
            self.highlighting_box.stretch_to_fit_width(l.width).stretch_to_fit_height(l.height)
            self.highlighting_box.align_to(l,LEFT)
            #print("streching", self.highlighting_box.width, l.width),
        self.lastline = l

    def highlight(self,i):
        i -=1
        self.highlighting_box.stroke_width=2
        self.highlighting_box.align_to(self.lines[i],UP)
        self.highlighting_box.align_to(self.lines[i],LEFT)
    @override_animate(highlight)
    def _highlight(self,i):
        if(self.highlighting_box.stroke_width == 0):
            self.highlight(i)
            return Create(self.highlighting_box)
        else:
            l = self.lines[i-1]
            y = self.highlighting_box.get_edge_center(DOWN)[1]-l.get_edge_center(DOWN)[1]
            x = self.highlighting_box.get_edge_center(LEFT)[0]-l.get_edge_center(LEFT)[0]
            return self.highlighting_box.animate.shift(DOWN*y+LEFT*x)



    ''' format code string to html '''
    def formatCodeToHtml(self, 
                         _lexer : str, 
                         file_path: Path,
                         code : str
                         ):
        
        html_formatter = HtmlFormatter(
            linenos = False,
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

    def gen_code_text(self):
        start_ptr = self.html_string.find("<pre")
        self.html_string = self.html_string[start_ptr : ]

        ''' Read each line and count the number of tab characters 
            Save each line as its line number along with its color style value
        '''
        lines = self.html_string.split("\n")
        start = lines[0].find(">")
        lines[0] = lines[0][start + 1 : ]

        code_line_list = []
        
        for i in range(len(lines)):
            line = ""
            lineIdx = 0
            if lines[i].find("</pre>"):
                break
            while lineIdx < len(lines[i]):
                # Read color value and content of span tag
                colr_start = lines[i].find("color: ")
                colr_value = lines[i][colr_start + 7 : colr_start + 14]

                end = lines[i][lineIdx : ].find(">")
                lines[i] = lines[i][end + 1 : ]
                end_span = lines[i].find("</span>")
                line = line + lines[i][ : end_span]
                self.wordColors[line] = colr_value
                lineIdx = end_span+7

                # read everything after span tag until next span tag or end of line
                while lineIdx < len(lines[i]):
                    if lines[i][lineIdx] == '<':
                        break
                    else:
                        line = line + lines[i][lineIdx]
                        lineIdx += 1
                code_line_list.append(line)
                #print(*code_line_list)

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

