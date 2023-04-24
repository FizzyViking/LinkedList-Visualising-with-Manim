from manim import *
import numpy as np

class SimpleCircle(Scene):
    def construct(self):
        circle = Circle(radius=2.0) # Create the circle
        self.add(circle) # Add the circle to the scene

class BezierCurve(Scene):
    def construct(self):
        curve = ParametricFunction(bezier([np.array([x, y, 0]) for x,y in [(0, 0), (3, 5), (6, 0)]]))
        axes = Axes(x_range=(0,6,1), 
                    y_range=(0,6,1),
                    )
        self.add(curve, axes)
        self.play(Create(curve), run_time=2, rate_func=linear)