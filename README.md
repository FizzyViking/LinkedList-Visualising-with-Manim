# LinkedList Visualising with Manim
Bachelor Project with the goal of producing a number of animations, which describes the implementations and operations of the LinkedList data structure

# Make sure manim is installed
Please refer to https://docs.manim.community/en/stable/installation.html to see how manim is installed

# Cmd for producing animation in Manim
manim -pql 'filename'.py 'classname'<br />
filename is the name of the python file containing the manim animation class<br />
classname is the name of the specific class in filename.py containing the animation<br />
Example: manim -pql linked.py LinkedList\br />
A class conataining an animation is any class deriving from Scene or MovingCameraScene\br >
linked.py contains several of these, with the most important being multiLinkcut producing the splice animation<br />
