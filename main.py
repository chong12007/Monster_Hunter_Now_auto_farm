import time
import utils
import ctypes
import random
import webbrowser
import PySimpleGUI as sg
import pyautogui

menu = sg.Window("MHNow")


def create_menu_gui():
    # Set a Layout
    layout = [
        [sg.Text("Use Long Sword as Weapon", key="row1", text_color="#509296", font=("Helvetica", 14, "bold"),
                 background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2", text_color="#509296",
                 font=("Helvetica", 12, "bold"), background_color="#f0f0f0")],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],
        [sg.Button("Adjust Screen", key="adjust_screen", button_color="#509296")],
        [sg.Button("Start ", key="start", button_color="#509296")] +
        [sg.Button("How To Use ", key="help", button_color="#509296")],
        [sg.Text("Please leave a star on my github if it helps ><", key="github",
                 enable_events=True, text_color='blue', background_color="#f0f0f0")]
    ]

    # menu setting
    # Get the screen width and height

    screen_resolution_width = ctypes.windll.user32.GetSystemMetrics(0)

    menu_width = screen_resolution_width / 2 + 60
    menu_height = 30

    menu_popup_location = (menu_width, menu_height)  # Specify the desired coordinates of the menu
    menu_size = (400, 350)  # Width, Height
    menu_theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(menu_theme)

    global menu
    menu = sg.Window("MHNow", layout, location=menu_popup_location, keep_on_top=True, size=menu_size)


def menu_function():
    global menu
    # Get screen resolution
    screen_resolution_height = ctypes.windll.user32.GetSystemMetrics(1)

    while True:
        # Read user event
        event, values = menu.read()

        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break

        # Screen resolution only accept 1920x1080
        if screen_resolution_height != 1080:
            utils.update_gui_msg("Only Screen Resolution 1920x1080 Work!!\n", menu)
            time.sleep(3)
            return

        if event == "adjust_screen" and screen_resolution_height == 1080:
            menu["row1"].update("Adjust Screen...")
            menu.refresh()
            utils.adjust_screen(menu)

        if event == "start":
            menu["row1"].update("Mobs Slayed : 0\n")
            menu["row2"].update("", text_color="#509296", font=("Helvetica", 10, "bold"),
                                background_color="#f0f0f0")
            menu.refresh()
            start_process()

        if event == "help":
            sg.popup_no_buttons("", title="Help", keep_on_top=True,
                                image="img/help.png")

        if event == "github":
            webbrowser.open("https://github.com/chong12007/MHNow")


def start_process():
    number_of_mob_killed = 0
    error_count = 0
    global menu
    while True:
        try:
            time.sleep(2)
            mob_coordinate = get_mob_coordinate()
            if mob_coordinate is None:
                raise TypeError

            def start_battle(mob_coordinate):
                global menu
                utils.click(mob_coordinate, "Found mob\n", menu)
                time.sleep(2)
                for i in range(6):
                    pyautogui.doubleClick(mob_coordinate[0], mob_coordinate[1], button="left")
                    time.sleep(0.6)

            start_battle(mob_coordinate)

            number_of_mob_killed += 1
            msg = f"Mob Slayed : {number_of_mob_killed}\n"
            menu["row1"].update(msg)
            menu.refresh()

            error_count = 0

        except TypeError:
            error_count += 1
            back_coordinate = utils.get_icon_coordinate("img/back.png")
            if back_coordinate is not None:
                utils.click(back_coordinate, "Go back\n", menu)
                error_count = 0

            material_go_back_coordinate = utils.get_icon_coordinate("img/material_back.png")
            if material_go_back_coordinate is not None:
                utils.click(material_go_back_coordinate, "Go back\n", menu)
                error_count = 0

            if error_count == 2:
                utils.update_gui_msg("No mobs detected, Moving around...\n", menu)
                walk_around()
                error_count = 0


def walk_around():
    random_number = random.choice([random.randint(-50, 0), random.randint(0, 50)])
    direction_x = random_number

    direction_y = 150

    try:
        joystick_coordinate = utils.get_icon_coordinate("img/joystick.png")

        # Simulate click and hold
        pyautogui.mouseDown(joystick_coordinate[0], joystick_coordinate[1])

        # Move the mouse to the right
        pyautogui.move(direction_x, direction_y, duration=1.2)  # Adjust the distance as needed
        # Release the mouse click
        pyautogui.mouseUp()
    except Exception:
        pass


def get_mob_coordinate():
    my_list = [1, 2, 3, 4, 5]
    for my in my_list:
        icon_path = f"img/monster{my}.png"
        coordinate = utils.get_icon_coordinate(icon_path)
        if coordinate is not None:
            return coordinate

    return None


if __name__ == '__main__':
    create_menu_gui()
    menu_function()

