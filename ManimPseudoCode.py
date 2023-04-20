from manim import *
from pathlib import Path
import os


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

        self.code_string = None
        self.file_path = Path(self.code_file)
        if code_file:
            # check_valid_path()
            self.code_string = self.file_path.read_text(encoding="utf-8")
        else:
            self.code_string = self.code
    
    def get_codestring(self):
        return self.code_string
    

    """ Mark up to n lines """
    def marklines(self, line_numbers):
        for line in line_numbers:
            # mob = get_line(line)
            height = Text("fg",font_size=self.font_size).height
            padding = 0.1 
            r = Rectangle()
            r.stretch_to_fit_width(mob.width+padding)
            r.move_to(mob)
            r.stretch_to_fit_height((height+padding))
            r.align_to(mob,DOWN)
            r.shift(DOWN*(padding/2))
            diffp = (height-mob.height) / height
            print(diffp)
            if diffp == 0 or (diffp >= 0.23 and diffp <= 0.24):
                return r
            r.shift(DOWN*0.2118770857773395*height)
        return r
class TextWithBoundingBox(VGroup):
    def __init__(self, text, fontsize):
        super().__init__()
        self.text = Text(text, font_size= fontsize)
        self.box = get_box(self.text,fontsize)
        self.add(self.text,self.box)




def get_box(self,mob, fontsize : float = DEFAULT_FONT_SIZE): 
    height = Text("fg", font_size=fontsize)
    padding = 0.0 #might make this a parameter
    r = Rectangle()
    r.stroke_width = 0
    r.stretch_to_fit_width(mob.width+padding)
    r.move_to(mob)
    r.stretch_to_fit_height((self.height+padding))
    r.align_to(mob,DOWN)
    r.shift(DOWN*(padding/2))
    diffp = (height-mob.height)/height
    print(diffp)
    if diffp == 0 or (diffp >= 0.23 and diffp <= 0.24):
        return r
    r.shift(DOWN*0.2118770857773395*height)
    return r