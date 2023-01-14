from manim import *

class InputString:

    # TODO addresses calculations

    def __init__(self, scene: Scene, value: str):
        self.scene = scene
        self.value_str = value
        self.boxes = [None] * len(value)
        self.letters: list[Text] = [None] * len(value)
        self.top = 0

    def construct(self):
        self.value = Text(self.value_str, font_size=30)
        for i in range(len(self.value_str)):
            self.boxes[i] = Rectangle(width=0.6, height=0.6, color=WHITE)

        self.boxes_g = VGroup(*self.boxes)
        self.boxes_g.arrange(direction=RIGHT, buff=0).center().set_opacity(0.1)

        for i in range(len(self.value_str)):
            # TODO fix heights of letters
            self.letters[i] = Text(self.value_str[i], font_size=30).next_to(self.boxes[i], 0)

        self.letters_g = VGroup(*self.letters)

        # arrow to letter
        up_dot = Dot(color=RED).next_to(self.letters[0], UP)
        down_dot = Dot(color=RED).next_to(self.letters[0], UP*2.7)
        self.arrow = Arrow(down_dot.get_center(), up_dot.get_center(), color=GREEN)

        # index text
        self.index_text = Text(f"i = {self.top}", font_size=20, color=GREEN).next_to(self.arrow, UP*0.5)

        self.scene.add(self.value)

    def convert_to_boxes(self):
        self.scene.play(Transform(self.value, self.letters_g), FadeIn(self.boxes_g), FadeIn(self.arrow), FadeIn(self.index_text))

    def move_to_index(self, index: int):
        self.arrow.generate_target()
        up_dot = Dot(color=RED).next_to(self.letters[index], UP)
        self.arrow.target.align_to(up_dot.get_center(), RIGHT)
        new_index_text = Text(f"i = {index}", font_size=20, color=GREEN).next_to(self.arrow.target, UP*0.5)
        self.scene.play(MoveToTarget(self.arrow), Transform(self.index_text, new_index_text))
        self.top = index

    def explain_size_of_char(self):
        brace = Brace(self.boxes[self.top], direction=DOWN, color=GREEN)
        text = Text("1 byte", font_size=20, color=GREEN).next_to(brace, DOWN*0.8)
        self.scene.play(GrowFromCenter(brace), GrowFromEdge(text, UP))
        self.scene.wait(2)
        self.scene.play(FadeOut(brace), FadeOut(text))

    def convert_to_hex(self, index=None, persist=False):
        texts = []
        if index is None:
            # convert all
            animations = []
            for i in range(len(self.value_str)):
                curr_text = Text(f"0x{ord(self.value_str[i]):2x}", font_size=14, color=RED).next_to(self.boxes[i], DOWN*1)
                texts.append(curr_text)
                animations.append(ReplacementTransform(self.letters[i].copy(), curr_text))
            self.scene.play(*animations)
        else:
            curr_text = Text(f"0x{ord(self.value_str[index]):2x}", font_size=14, color=RED).next_to(self.boxes[index], DOWN*1)
            texts.append(curr_text)
            self.scene.play(ReplacementTransform(self.letters[index].copy(), curr_text))

        if persist is False:
            self.scene.wait(2)
            self.scene.play(FadeOut(*texts))

    def get_char(self, index):
        return self.value_str[index]

