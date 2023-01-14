from manim import *
from models.InputString import *
from models.Stack import *

inp = "a(car)(dog(egg))"

class BasicStackAllocation(Scene):

    def construct(self):


        stack = Stack(self)
        self.add(stack.construct())
        stack.push_sp()
        stack.push_sp()
        stack.push_sp(amount=2)
        stack.explain_current_stack_frame()
        stack.push_sp(pop=True)
        stack.push_sp(amount=2, pop=True)
        stack.explain_current_stack_frame()

        # self.wait(2)
        # stack.insert_value(value, 0)
        # self.wait(2)
        # stack.push_sp()
        self.wait(2)

class InsertingStackValues(Scene):

    def construct(self):

        title = Text("Return Address Stack", font_size=18).to_corner(UP + LEFT).shift((DOWN + RIGHT)*0.4)
        subtitle = Text(f"Input: {inp}", font_size=14).next_to(title, DOWN*0.2)

        value = Text("0x12AB34CD", font_size=25).to_corner(DOWN+LEFT)
        value2 = Text("WOW", font_size=25).to_corner(DOWN+LEFT)

        stack = Stack(self)
        self.add(title, subtitle)
        self.add(stack.construct())
        stack.push_sp(amount=3)
        stack.insert_value(value, 0, explain_calculation=True)
        stack.insert_value(value2, 0)
        stack.push_sp(amount=3, pop=True)
        self.wait(2)

class IteratingThroughString(Scene):

    def construct(self):

        vstring = InputString(self, inp)
        vstring.construct()
        vstring.convert_to_boxes()
        vstring.explain_size_of_char()
        vstring.convert_to_hex()
        vstring.move_to_index(2)
        vstring.move_to_index(7)
        vstring.move_to_index(3)
        self.wait(2)
