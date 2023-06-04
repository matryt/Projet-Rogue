import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk



class CustomDialog(simpledialog.Dialog):
	def __init__(self, parent, title=None, image_path=None):
		self.image_path = image_path
		super().__init__(parent, title)

	def body(self, master):
		if self.image_path:
			image = Image.open(self.image_path)
			photo = ImageTk.PhotoImage(image)
			image_label = tk.Label(master, image=photo)
			image_label.image = photo  # Conserver une référence à l'image pour éviter la suppression par le garbage collector
			image_label.pack()

		self.entry = tk.Entry(master)
		self.entry.pack()
		return self.entry

	def apply(self):
		self.result = self.entry.get()
