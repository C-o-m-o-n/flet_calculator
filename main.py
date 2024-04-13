import flet as ft
from flet import (
    app,
    Container,
    Page,
    Row,
    KeyboardEvent,
    UserControl,
    MainAxisAlignment,
)
from constants import COLORS
from handle_keyboard_helpers import handle_keyboard_input
from ui_components import create_button_rows, create_text
# ------------------------------------------------------------------------------

# class CalculatorApp(UserControl):
#     # ------------------------------------------------------------------------------
#     # Initializing the layout components
#     # ------------------------------------------------------------------------------
#     def __init__(self, page: Page):
#         super().__init__()
#         self.page = page
#         self.text = create_text()
#         self.result = ft.Text(
#             value="",
#             size=20,
#             text_align="right",
#             color=ft.colors.AMBER_300,
#         )
#         self.history = ft.Text(
#             value="",
#             size=20,
#             text_align="right",
#             color=COLORS["hint_text"],
#         )
#         self.history_list = []
#         self.rows = create_button_rows(self.handle_keyboard_input)

#     def build(self):
#         calculator_container = ft.Container(
#             content=ft.Column(
#                 controls=[
#                     # ft.Stack(controls=[
#                     #     ft.PopupMenuButton
#                     #     ]
#                     # ),
#                     Container(
#                         content=ft.Column(
#                             controls=[
#                                 Row(
#                                     controls=[self.history],
#                                     alignment=MainAxisAlignment.END,
#                                 ),
#                                 Row(
#                                     controls=[self.text],
#                                     alignment=MainAxisAlignment.END,
#                                 ),
#                                 Row(
#                                     controls=[self.result],
#                                     alignment=MainAxisAlignment.END,
#                                 ),
#                             ],
#                             scroll="adaptive",
#                             alignment=ft.alignment.bottom_right,
#                         ),
#                         height=240,
#                         bgcolor=COLORS["listview_bg"],
#                         border=ft.border.all(3, COLORS["border"]),
#                         border_radius=ft.border_radius.all(20),
#                         padding=5,
#                         alignment=ft.alignment.bottom_right,
#                     ),
#                     Container(
#                         content=ft.Column(
#                             controls=[
#                                 Row(controls=[self.rows[0]]),
#                                 Row(controls=[self.rows[1]]),
#                                 Row(controls=[self.rows[2]]),
#                                 Row(controls=[self.rows[3]]),
#                                 Row(controls=[self.rows[4]]),
#                             ],
#                         ),
#                         # expand=True,
#                     ),
#                 ],
#             ),
#             # width=self.page.window_width,
#             # height=self.page.window_height,
#             bgcolor=COLORS["background"],
#             border_radius=ft.border_radius.all(20),
#             padding=5,
#             alignment=ft.alignment.center,
#         )

#         return calculator_container

#     # ------------------------------------------------------------------------------
#     # Logic Functions
#     # ------------------------------------------------------------------------------

#     def handle_keyboard_input(self, event: KeyboardEvent):
        
#         text = self.text.value
#         result = self.result.value
#         history = self.history.value
#         history_list = self.history_list
#         (
#             self.text.value,
#             self.result.value,
#             self.history.value,
#             self.history_list,
#         ) = handle_keyboard_input(event, text, result, history, history_list)

#         self.update()
class CalculatorApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.text = create_text()
        self.result = ft.Text(
            value="",
            size=20,
            text_align="right",
            color=ft.colors.AMBER_300,
        )
        self.history = ft.Text(
            value="",
            size=20,
            text_align="right",
            color=COLORS["hint_text"],
        )
        self.history_list = []
        self.rows = create_button_rows(self.handle_keyboard_input)

        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[self.history],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        ft.Row(
                            controls=[self.text],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        ft.Row(
                            controls=[self.result],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    scroll="adaptive",
                    alignment=ft.alignment.bottom_right,
                ),
                height=240,
                bgcolor=COLORS["listview_bg"],
                border=ft.border.all(3, COLORS["border"]),
                border_radius=ft.border_radius.all(20),
                padding=5,
                alignment=ft.alignment.bottom_right,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[self.rows[0]]),
                        ft.Row(controls=[self.rows[1]]),
                        ft.Row(controls=[self.rows[2]]),
                        ft.Row(controls=[self.rows[3]]),
                        ft.Row(controls=[self.rows[4]]),
                    ],
                ),
            ),
        ]

        self.bgcolor = COLORS["background"]
        self.border_radius = ft.border_radius.all(20)
        self.padding = ft.padding.all(5)
        self.alignment = ft.alignment.center

    def handle_keyboard_input(self, event: ft.KeyboardEvent):
        text = self.text.value
        result = self.result.value
        history = self.history.value
        history_list = self.history_list
        (
            self.text.value,
            self.result.value,
            self.history.value,
            self.history_list,
        ) = handle_keyboard_input(event, text, result, history, history_list)

        self.update()



# ------------------------------------------------------------------------------
# Main Page Setup
# ------------------------------------------------------------------------------

def main(page: Page):
    """
    Sets up the calculator page
    """

    # Page properties
    page.title = "Calculator"
    page.window_height = 600
    page.window_width = 340
    page.window_min_height = 600
    page.window_min_width = 340
    page.bgcolor = COLORS["background"]
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = MainAxisAlignment.CENTER

    calc_widget = CalculatorApp(page)
    # Set the keyboard event handler for the page, to enable keyboard input
    page.on_keyboard_event = calc_widget.handle_keyboard_input
    page.add(calc_widget)

if __name__ == "__main__":
    app(target=main, assets_dir="assets")