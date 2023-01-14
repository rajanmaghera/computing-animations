from manim import *


class Stack:

    def __init__(self, scene: Scene):
        self.stack_size = 6
        self.offset = 4
        self.stack: list[Rectangle] = [None] * self.stack_size
        self.addrs = [None] * self.stack_size
        self.data = [None] * self.stack_size
        self.top = 0
        self.scene = scene

    def get_value_at(self, index: int):
        return self.data[self.top - index]

    def construct(self):

        for i in range(self.stack_size):
            self.stack[i] = Rectangle(width=1.6, height=0.6, color=WHITE)

        self.stack[0].set_fill(color=RED, opacity=0.2)

        self.stack_boxes_g = VGroup(*self.stack)
        self.stack_boxes_g.arrange(direction=DOWN, buff=0)

        # add stack addresses

        for i in range(self.stack_size):
            self.addrs[i] = Text(f"0x7F{0xFC - (i*(self.offset)):02X}", font_size=20).next_to(self.stack[i], RIGHT*0.6)
        self.addrs_g = VGroup(*self.addrs)

        # add stack titles

        self.title_stack = Text("Stack", font_size=20).next_to(self.stack_boxes_g, UP*2.0)
        self.title_addrs = Text("Address", font_size=20).next_to(self.addrs_g, UP).align_to(self.title_stack, UP)

        # TODO text : Note, these are example addresses. They may not necessarily match
        # the addresses you see in RARS

        # TODO text : area on screen "what are we doing now?"
        # examples: allocating 4 bytes on the stack

        # TODO text : the filled in boxes represent allocated memory on the stack

        # TODO text : allocation and deallocation is as simple as adding or subtracting
        # from the sp

        self.title_g = VGroup(self.title_stack, self.title_addrs)

        # add stack pointer

        left_dot = Dot(color=RED).next_to(self.addrs[0], RIGHT*0.6)
        right_dot = Dot(color=RED).next_to(self.addrs[0], RIGHT*2.4)
        self.sp_arrow = Arrow(right_dot.get_center(), left_dot.get_center(), color=GREEN)
        self.sp_text = Text("sp", font_size=20, color=BLUE).next_to(self.sp_arrow, RIGHT*0.5)

        self.sp_g = VGroup(self.sp_arrow, self.sp_text)

        # add sp register box

        self.sp_reg = Rectangle(width=1.6, height=0.6, color=BLUE).next_to(self.stack[self.stack_size-1], DOWN*1.0)
        self.title_sp = Text("sp (register)", font_size=20, color=BLUE).next_to(self.sp_reg, RIGHT*0.6)
        self.sp_reg_text = Text("0x7FFC", font_size=20, color=BLUE).next_to(self.sp_reg, 0)

        self.sp_reg_g = VGroup(self.sp_reg, self.title_sp, self.sp_reg_text)


        self.stack_g = VGroup(self.stack_boxes_g, self.addrs_g, self.title_g, self.sp_g, self.sp_reg_g)

        return self.stack_g

    def push_sp(self, amount=1, pop=False):

        things_to_do = []


        if pop:
            for i in range(amount):
                things_to_do.append(self.stack[self.top - i].animate.set_fill(color=WHITE, opacity=0.0))
            self.top -= amount
        else:
            for i in range(amount):
                things_to_do.append(self.stack[self.top + 1 + i].animate.set_fill(color=WHITE, opacity=0.2))
            self.top += amount


        self.sp_g.generate_target()
        new_dot = Dot(color=RED).next_to(self.addrs[self.top], RIGHT*0.6)
        self.sp_g.target.align_to(new_dot, DOWN)

        op = "-" if pop else "+"

        add_text = Text(f"{op} {amount * self.offset}", font_size=24, color=RED).next_to(self.sp_reg, DOWN*0.9)

        self.scene.play(Write(add_text))
        self.scene.wait(0.4)

        new_reg_text = Text(f"0x7F{0xFC - (self.top*(self.offset)):02X}", font_size=20, color=BLUE).next_to(self.sp_reg, 0)



        self.scene.play(
            *things_to_do,
            MoveToTarget(self.sp_g),
            FadeOut(self.sp_reg_text),
            Transform(add_text, new_reg_text),
        )


        self.scene.wait(0.4)

        # TODO check that vgroup gets updated
        self.sp_reg_text = add_text

    def explain_current_stack_frame(self):
        # draw a brace to explain the current stack frame
        upper_dot = Dot(color=GREEN, radius=0.0001).align_to(self.stack[0], DOWN+LEFT)
        lower_dot = Dot(color=GREEN, radius=0.0001).align_to(self.stack[self.top], DOWN+LEFT)
        brace = BraceBetweenPoints(upper_dot.get_center(), lower_dot.get_center(), color=GREEN, direction=LEFT)
        text = Text("Current Stack Frame", font_size=20, color=GREEN).next_to(brace, LEFT*0.5)
        self.scene.play(GrowFromCenter(brace), GrowFromEdge(text, RIGHT))
        self.scene.wait(2)
        self.scene.play(FadeOut(brace), FadeOut(text))


        pass

    def insert_value(self, value: Mobject, index, explain_calculation=False):

        if explain_calculation:

            # calculate index
            temp_addr = self.sp_reg_text.copy()
            temp_addr.generate_target()
            temp_addr.target.next_to(self.sp_reg, LEFT*5)
            self.scene.play(MoveToTarget(temp_addr))

            temp_index = Text(f"i = {index}", font_size=24, color=RED).next_to(temp_addr, DOWN*1)
            self.scene.play(Write(temp_index))

            temp_mul = Text(f"x {self.offset}", font_size=24, color=RED).next_to(temp_index, RIGHT*0.8)
            self.scene.play(Write(temp_mul))

            temp_add = Text(f"+ {index * self.offset}", font_size=24, color=RED).next_to(temp_addr, RIGHT*0.8).match_height(temp_addr)

            self.scene.play(Transform(temp_index, temp_add), Transform(temp_mul, temp_add))
            self.scene.remove(temp_mul)
            temp_add = temp_index

            real_addr = Text(f"0x7F{0xFC - ((self.top - index)*(self.offset)):02X}", font_size=20, color=BLUE).next_to(temp_addr, 0)

            self.scene.play(Transform(temp_add, real_addr), Transform(temp_addr, real_addr))
            self.scene.remove(temp_addr)
            real_addr = temp_add

            copy_addr_table = self.addrs[self.top - index].copy()
            self.scene.play(Transform(real_addr, copy_addr_table))
            self.scene.remove(copy_addr_table, real_addr)

        # highlight address of stack item
        self.addrs[self.top - index].generate_target()
        self.addrs[self.top - index].target.set_fill(color=RED, opacity=1)
        self.scene.play(MoveToTarget(self.addrs[self.top - index]))

        # move item to stack
        value.generate_target()
        value.target.next_to(self.stack[self.top - index], 0).scale_to_fit_height(0.3)
        if value.target.width > 1.2:
            value.target.scale_to_fit_width(1.2)

        anims = []
        if self.data[self.top - index] is not None:
            anims.append(FadeOut(self.data[self.top - index]))
        self.scene.play(
            MoveToTarget(value),
            *anims
        )
        self.data[self.top - index] = value
        self.scene.wait(0.4)

        # unhighlight address of stack item
        self.addrs[self.top - index].generate_target()
        self.addrs[self.top - index].target.set_fill(color=WHITE, opacity=1)
        self.scene.play(MoveToTarget(self.addrs[self.top - index]))

        if explain_calculation:
            self.scene.play(FadeOut(real_addr))
