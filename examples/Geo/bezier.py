import numpy as np

from examples.example_imports import *
from manim_express import *
from sparrow import clamp


class Bazier(EagerModeScene):
    def __init__(self):
        super().__init__()
        self._value_tracker = ValueTracker()

    def updater_with_line(self, line: Line):
        return lambda x: x.move_to(
            line.get_start() + (line.get_end() - line.get_start()) * self._value_tracker.get_value())

    @staticmethod
    def line_updater_with_dots(dot1: Dot, dot2: Dot):
        return lambda x: x.put_start_and_end_on(dot1.get_center(), dot2.get_center())

    def updater_with_dots(self, dot_start: Dot, dot_end: Dot, rate_func=linear):
        return lambda x: x.move_to(
            dot_start.get_center() + (dot_end.get_center() - dot_start.get_center()) * rate_func(
                self._value_tracker.get_value()))

    def clip1(self):
        # self.play(Write(gen_points(500, x_range=[-2, 2], y_range=[-2, 2])), run_time=3)
        # self.play(ShowCreation(gen_sphere_points(100, r_range=(0, 5))), run_time=3)
        dot_group = gen_points(4, x_range=(-5, 5), y_range=(-4, 4))
        dot1, dot2, dot3, dot4 = dot_group

        self._value_tracker = ValueTracker()
        line_12 = Line(dot1.get_center(), dot2.get_center()).set_stroke(color=GREY, width=5)
        line_23 = Line(dot2.get_center(), dot3.get_center()).set_stroke(color=GREY, width=5)
        line_34 = Line(dot3.get_center(), dot4.get_center()).set_stroke(color=GREY, width=5)

        d1 = Dot([0, 0, 0]).set_color(RED)
        d2 = Dot().set_color(GREEN).next_to(d1, UP)
        d3 = Dot().set_color(BLUE).next_to(d1, RIGHT)
        d4 = Dot().set_color(GREY).next_to(d1, UR)
        d_groups = VGroup(d1, d2, d3, d4).to_edge(UP)
        self.play(Write(d_groups))
        self.wait(0.5)

        self.play(*it.chain.from_iterable([[i.move_to, j.get_center()] for i, j in zip(d_groups, dot_group)]))

        self.wait(0.3)
        [self.play(ShowCreation(i), run_time=0.2) for i in [dot_group, line_12, line_23, line_34]]

        d1.add_updater(self.updater_with_line(line_12))
        d2.add_updater(self.updater_with_line(line_23))
        d3.add_updater(self.updater_with_line(line_34))
        line_d12 = Line(d1, d2).set_color(BLUE)
        line_d23 = Line(d2, d3).set_color(GREEN)
        self.play(*[Write(i) for i in [line_d12, line_d23]], run_time=0.3)

        line_d12.add_updater(self.line_updater_with_dots(d1, d2))
        line_d23.add_updater(self.line_updater_with_dots(d2, d3))

        d_d12 = Dot(color=BLUE).scale(0.5).add_updater(self.updater_with_line(line_d12))
        d_d23 = Dot(color=BLUE).scale(0.5).add_updater(self.updater_with_line(line_d23))
        self.add(d_d12, d_d23)

        target_line = Line().set_stroke(color=GREEN, width=2).add_updater(self.line_updater_with_dots(d_d12, d_d23))
        self.add(target_line)

        target_dot = Dot(color=RED).scale(0.7).add_updater(self.updater_with_line(target_line))
        path = TracedPath(target_dot.get_center).set_stroke(RED, 3)
        self.add(target_dot, path)

        self.play(self._value_tracker.increment_value, 1, run_time=5, rate_func=smooth)
        self.wait(0.5)

    def clip2(self):
        x = np.linspace(0, 1, 100)
        # self.plot(x, [smooth(i) for i in x])
        # self.plot(x, [double_smooth(i) for i in x])
        # self.plot(x, [lingering(i) for i in x])
        self.plot(x, [exponential_decay(i) for i in x])
        self.plot(x, [wiggle(i) for i in x])
        self.show_plot()
        self.hold_on()




# CONFIG.write_file = True
# CONFIG.gif = True
# CONFIG.color = WHITE

bezier = Bazier()
# bezier.render()
bezier.clip2()
