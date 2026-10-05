"""Mouvement plan d'un solide rigide : translation et rotation simultanées."""

from manim import *
import numpy as np


class RigidBodyMotion(Scene):
    def construct(self):
        title = Tex("Mouvement plan d'un corps rigide", font_size=42).to_edge(UP)
        subtitle = Tex(
            "A et B sont deux points quelconques du solide", font_size=30
        ).next_to(title, DOWN, buff=0.2)

        # Coordonnées locales des deux points, choisies sans symétrie particulière.
        local_a = np.array([1.15, 0.42, 0.0])
        local_b = np.array([-0.82, -0.37, 0.0])
        initial_center = np.array([-2.5, -0.55, 0.0])
        displacement = np.array([4.8, 1.0, 0.0])
        progress = ValueTracker(0)

        def center():
            return initial_center + progress.get_value() * displacement

        def position(local):
            angle = 1.7 * PI * progress.get_value()
            rotation = np.array(
                [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            )
            result = rotation @ local[:2]
            return center() + np.array([result[0], result[1], 0.0])

        def label_position(local):
            radial = position(local) - center()
            return position(local) + 0.34 * radial / np.linalg.norm(radial)

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            x_length=12,
            y_length=6,
            axis_config={"stroke_opacity": 0.2, "include_tip": False},
        )
        body = always_redraw(
            lambda: Rectangle(
                width=3.6,
                height=1.8,
                stroke_color=BLUE_C,
                stroke_width=5,
                fill_color=BLUE_E,
                fill_opacity=0.55,
            )
            .rotate(1.7 * PI * progress.get_value())
            .move_to(center())
        )
        point_a = always_redraw(lambda: Dot(position(local_a), color=RED_C, radius=0.11))
        point_b = always_redraw(lambda: Dot(position(local_b), color=GREEN_C, radius=0.11))
        segment = always_redraw(
            lambda: DashedLine(
                position(local_a), position(local_b), color=YELLOW, stroke_width=4
            )
        )
        label_a = always_redraw(
            lambda: MathTex("A", color=RED_C, font_size=36).move_to(label_position(local_a))
        )
        label_b = always_redraw(
            lambda: MathTex("B", color=GREEN_C, font_size=36).move_to(label_position(local_b))
        )
        center_dot = always_redraw(lambda: Dot(center(), color=WHITE, radius=0.055))
        trajectory = TracedPath(
            center_dot.get_center, stroke_color=WHITE, stroke_opacity=0.5, stroke_width=2
        )

        distance_label = MathTex(r"AB =", font_size=40)
        distance_value = DecimalNumber(
            np.linalg.norm(local_b - local_a), num_decimal_places=2, font_size=40
        )
        distance_value.add_updater(
            lambda number: number.set_value(
                np.linalg.norm(point_b.get_center() - point_a.get_center())
            )
        )
        constant_label = Tex("(constante)", font_size=32, color=YELLOW)
        measure = VGroup(distance_label, distance_value, constant_label)
        measure.arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.38)

        self.play(Write(title), FadeIn(subtitle), Create(axes))
        self.add(trajectory, body, segment, point_a, point_b, center_dot)
        self.play(FadeIn(label_a, label_b), Write(measure))
        self.wait(0.5)
        self.play(progress.animate.set_value(1), run_time=7, rate_func=linear)
        self.wait(1)
