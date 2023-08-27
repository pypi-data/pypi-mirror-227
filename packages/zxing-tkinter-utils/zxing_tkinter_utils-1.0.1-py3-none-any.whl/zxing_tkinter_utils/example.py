from tkinter import *

from zxing_tkinter_utils.core import App, place

class MyApp(App):
	def __init__(self):
		super().__init__("这是标题。", 400, 300)
	def UI(self, root):
		btn = Button(root, text="这是一段文字。")
		place(btn, 0, 0, 100, 100)
if __name__ == "__main__":
	MyApp()
