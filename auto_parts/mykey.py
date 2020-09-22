from pynput import keyboard
# from pynput.keyboard import Controller
from pynput import mouse
import threading


def on_press(key):
    try:
        if key.char == "s":
            my_key = keyboard.Controller()
            # print('ddsdddddddd')
            my_key.press('1')
            my_key.release('1')

            my_key.press('2')
            my_key.release('2')

            my_key.press('3')
            my_key.release('3')

            my_key.press('4')
            my_key.release('4')

            my_key.press('5')
            my_key.release('5')
    except AttributeError:
        print("按下特殊键！")

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener_key:
#     listener_key.join()

# # ...or, in a non-blocking fashion:
# listener_key = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# # listener_key.start()
# mk = threading.Thread(listener_key.start())
# mk.start()


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))

# # Collect events until released
# with mouse.Listener(
#         on_move=on_move,
#         on_click=on_click,
#         on_scroll=on_scroll) as listener_mouse:
#     listener_mouse.join()

# # ...or, in a non-blocking fashion:
# listener_mouse = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click,
#     on_scroll=on_scroll)
# listener_mouse.start()
#adsfasfd


class myThread1(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程1：" + self.name)
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
                    listener.join()

class myThread2(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("开始线程2：" + self.name)
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener_key:
                listener_key.join()

if __name__ == '__main__':
    # 创建新线程
    thread1 = myThread1(1, "Thread-1")
    thread2 = myThread2(2, "Thread-2")

    # 开启新线程
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()