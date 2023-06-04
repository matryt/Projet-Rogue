import random
import tkinter as tk
from tkinter.simpledialog import askinteger, askstring

import Element
import theGame
from utils import getch

root2 = tk.Tk()
root2.withdraw()


def on_closing():
	root2.quit()
	root2.destroy()


def fenetreInput(titre, message, typeInput):
	root2 = tk.Tk()
	root2.withdraw()
	match typeInput:
		case "int":
			val = askinteger(titre, message)
		case "str":
			val = askstring(titre, message)
		case _:
			raise ValueError("Type invalide")
	root2.quit()
	return val

def messageFenetre(message, titre="Entrée"):
	global root2
	root2 = tk.Tk()
	root2.title(titre)
	width = 420
	height = 100
	screen_width = root2.winfo_screenwidth()
	screen_height = root2.winfo_screenheight()
	x = (screen_width - width) // 2
	y = (screen_height - height) // 2
	label = tk.Label(root2, text=message)
	label.pack()
	label.config(font=("Arial", 24))
	root2.protocol("WM_DELETE_WINDOW", on_closing)
	root2.geometry(f"{width}x{height}+{x}+{y}")
	root2.mainloop()


class Shop(Element.Element):
	def __init__(self):
		super().__init__("Shop", "e", "a shop")
		self._items = {}

	def checkItem(self, item):
		return any(item.getName() == i.getName() for i in self._items)

	def __repr__(self):
		return self._abbrv

	def addQuantity(self, item, qty):
		if not self.checkItem(item):
			raise ValueError(f"{item} is not in the shop")
		for e in self._items:
			if e.getName() == item.getName():
				self._items[e]["quantity"] += qty
				return

	def isEmpty(self):
		return len(self._items) == 0

	def description(self):
		if self.isEmpty():
			return
		desc = "La boutique vous propose :"
		for i, item in enumerate(self._items):
			desc += f"\n\t({i}) {item.getName()} ({self._items[item]['quantity']} exemplaire(s)): {self._items[item]['price']} pièce(s)"
		return desc

	def addItem(self, item, qty, price):
		if self.checkItem(item):
			raise ValueError(f"{item} is already in the shop")
		self._items[item] = {"quantity": qty, "price": price}

	def getElementByNumber(self, number):
		if number < 0 or number >= len(self._items):
			raise ValueError(f"{number} is not a valid number")
		return list(self._items.keys())[number]

	def removeItem(self, item):
		if not self.checkItem(item):
			raise ValueError(f"{item} is not in the shop")
		self._items[item]["quantity"] -= 1
		if self._items[item]["quantity"] == 0:
			del self._items[item]

	def getElem(self, item):
		cle = None
		for elem in self._items:
			if elem.getName() == item.getName():
				cle = elem
		if cle:
			return self._items[cle]

	def meetAffichage(self, elem):
		choix = ""
		while choix != "f":
			choix = fenetreInput("Choix", f"{self.description()} \nQue voulez-vous faire ? (a)cheter, (v)endre, (f)inir : ", "str")
			if choix == "a":
				if len(theGame.theGame().getHero().getInventory()) > 9:
					continue
				item = fenetreInput("Choix", f"{self.description()} \nQuel item voulez-vous acheter ? ", "int")
				try:
					item = self.getElementByNumber(int(item))
				except:
					messageFenetre("Cet item n'existe pas", "Erreur")
					continue
				if theGame.theGame().getHero().getGoldCount() < self._items[item]["price"]:
					messageFenetre("Vous n'avez pas assez d'\nargent pour acheter cet item", "Erreur")
					continue
				theGame.theGame().getHero().addGold(-self.getElem(item)["price"])
				theGame.theGame().getHero().addItem(item)
				self.removeItem(item)
				messageFenetre(f"Vous avez acheté \n{item.getName()}", "Achat")
			if choix == "v":
				inventory = "".join([f"({i}) {item.getName()}\n" for i, item in enumerate(theGame.theGame().getHero().getInventory())])
				item = fenetreInput("Choix", "Here is your inventory : \n" + inventory + "\n" + "Quel item voulez-vous vendre ? ", "int")
				try:
					item = theGame.theGame().getHero().getInventory()[int(item)]
				except:
					messageFenetre("Cet item n'existe pas", "Erreur")
					continue
				if not self.checkItem(item):
					try:
						price = int(random.expovariate(theGame.theGame().getRarety(item) + 1))+1
					except:
						messageFenetre("Cet item n'est pas vendable", "Erreur")
						continue
					self.addItem(item, 1, price)
					theGame.theGame().getHero().addGold(price)
				else:
					theGame.theGame().getHero().addGold(self.getElem(item)["price"])
					self.addQuantity(item, 1)
				theGame.theGame().getHero().removeItem(item)
				messageFenetre(f"Vous avez vendu \n{item.getName()}", "Vente")
		messageFenetre("Merci beaucoup, \net à bientôt j'espère !", "Au revoir")

	def meet(self, elem):
		choix = ""
		while choix != "f":
			theGame.theGame().addMessage(self.description())
			theGame.theGame().addMessage(f"Vous avez {theGame.theGame().getHero().getGoldCount()} pièces d'or")
			theGame.theGame().addMessage("Que voulez-vous faire ? (a)cheter, (v)endre, (f)inir : ")
			print(theGame.theGame().readMessages())
			choix = getch()
			if choix == "a":
				theGame.theGame().addMessage("Quel item voulez-vous acheter ? ")
				print(theGame.theGame().readMessages())
				item = getch()
				try:
					item = self.getElementByNumber(int(item))
				except:
					theGame.theGame().addMessage("Cet item n'existe pas")
					print(theGame.theGame().readMessages())
					continue
				if theGame.theGame().getHero().getGoldCount() < self._items[item]["price"]:
					theGame.theGame().addMessage("Vous n'avez pas assez d'argent pour acheter cet item")
					print(theGame.theGame().readMessages())
					continue
				theGame.theGame().getHero().addGold(-self.getElem(item)["price"])
				theGame.theGame().getHero().addItem(item)
				self.removeItem(item)
				theGame.theGame().addMessage(f"Vous avez acheté {item}")
				print(theGame.theGame().readMessages())
			if choix == "v":
				inventory = "".join([f"({i}) {item.getName()}\n" for i, item in enumerate(theGame.theGame().getHero().getInventory())])
				theGame.theGame().addMessage("Here is your inventory : \n" + inventory)
				theGame.theGame().addMessage("Quel item voulez-vous vendre ? ")
				print(theGame.theGame().readMessages())
				item = getch()
				try:
					item = theGame.theGame().getHero().getInventory()[int(item)]
				except:
					theGame.theGame().addMessage("Cet item n'existe pas")
					print(theGame.theGame().readMessages())
					continue
				if not self.checkItem(item):
					try:
						price = int(random.expovariate(theGame.theGame().getRarety(item) + 1))+1
					except:
						theGame.theGame().addMessage("Cet item n'est pas vendable")
						print(theGame.theGame().readMessages())
						continue
					self.addItem(item, 1, price)
					theGame.theGame().getHero().addGold(price)
				else:
					theGame.theGame().getHero().addGold(self.getElem(item)["price"])
					self.addQuantity(item, 1)
				theGame.theGame().getHero().removeItem(item)
				theGame.theGame().addMessage(f"Vous avez vendu {item.getName()}")
				print(theGame.theGame().readMessages())
		theGame.theGame().addMessage("Merci beaucoup, et à bientôt j'espère !")
