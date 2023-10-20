import time
import pyautogui
import cv2
import pygetwindow as gw
import ctypes

msg_history = ''


def adjust_screen(menu):
    def is_app_running():
        app_titles = ["Phone", "phone"]

        # Find the window with a matching title
        app_is_running = None
        # Test all title
        for title in app_titles:
            try:
                app_is_running = gw.getWindowsWithTitle(title)[0]
                break
            except IndexError:
                pass

        if app_is_running:
            return app_is_running
        else:
            return None

    app_window = is_app_running()

    if app_window is None:
        def app_not_found(menu):
            menu["row1"].update("Error :(", text_color="red", font=("Helvetica", 16, "bold"),
                                background_color="#f0f0f0")
            menu["row2"].update("Unable to detect Emulator", text_color="red",
                                font=("Helvetica", 12, "bold"),
                                background_color="#f0f0f0")

            menu.refresh()

        app_not_found(menu)
        return

    # Resize the window
    app_window.resizeTo(400, 1025)

    # Get Screen Center
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    window_width = app_window.width
    window_height = app_window.height

    screen_center_x = screen_width - window_width - 80
    screen_center_y = (screen_height - window_height) // 2

    app_window.activate()

    # Select app
    time.sleep(1)
    # Move the window to the center of the screen
    app_window.moveTo(screen_center_x, screen_center_y)

    menu["row1"].update("Screen Adjusted!!", text_color="#509296", font=("Helvetica", 16, "bold"),
                        background_color="#f0f0f0")
    menu["row2"].update("Try again if screen dont move to center", text_color="#509296", font=("Helvetica", 12, "bold"),
                        background_color="#f0f0f0")
    menu.refresh()


def update_gui_msg(msg, menu):
    global msg_history

    msg_history += msg
    menu.Element('_Multiline_').Update(msg_history, font=("Helvetica", 10, "bold"))
    menu.refresh()


def click(coordinate, msg, menu):
    update_gui_msg(msg, menu)
    menu.refresh()
    pyautogui.click(coordinate[0], coordinate[1], button="left")
    time.sleep(1)


def get_icon_coordinate(icon_path):
    screenshot = pyautogui.screenshot()
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"
    screenshot = cv2.imread(screenshot_path)

    # Load template image
    template = cv2.imread(icon_path)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.06

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val)

    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0], center[1])
        print(click_coordinate)
        return click_coordinate
    else:
        return None

if __name__ == '__main__':
    coordinate = get_icon_coordinate("img/joystick.png")
