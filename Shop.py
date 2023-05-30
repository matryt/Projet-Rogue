import random

import Element
import theGame
from utils import getch


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

	def changePrice(self, item, price):
		if not self.checkItem(item):
			raise ValueError(f"{item} is not in the shop")
		self._items[item]["price"] = price

	def getElem(self, item):
		cle = None
		for elem in self._items:
			if elem.getName() == item.getName():
				cle = elem
		if cle:
			return self._items[cle]

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