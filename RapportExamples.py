from manim import *

class SimpleCircle(Scene):
    def construct(self):
        circle = Circle(radius=2.0) # Create the circle
        self.add(circle) # Add the circle to the scene

