import copy
import time
import random

import Stairs
import Chest
import Wearable
from utils import getch
from specialActions import heal, teleport, equip, recover
import Equipment
import Creature
import Hero
import Map
import Coord
import Shop
import importlib
import tkinter as tk
from tkinter.simpledialog import askinteger, askstring
import hashlib

theGame = importlib.import_module("theGame")
root2 = tk.Tk()
root2.withdraw()


class Game(object):
	"""
	La classe de jeu

	...
	Attributes
	----------
	equipments : list
			Equipements qui peuvent être positionnées sur la carte
	monsters : list
			Monstres pouvant être positionnées sur la carte
	equiped_outfits : list
			tenues et armes equipés

	_hero
	_messages
	_level
	_floor : Map.Map
	_actions : dict
			Actions possibles du jeu
	_idMonsters : int
			Identifiant des monstres
	"""

	equipments = {
		0: [
			Equipment.Equipment("potion", "p", usage=lambda self, hero: heal(hero)),
			Wearable.Wearable("broken sword",abbrv="n",durability=1, place="right hand", effect={"strength": 1}, usage=lambda self, hero: equip(hero, self)),
			Wearable.Wearable("trident", place="right hand", durability=7, effect={"strength": 3}, usage=lambda self, hero: equip(hero, self)),
			Wearable.Wearable(
				"double_epee", place="right hand", durability=5, effect={"strength": 2}, usage=lambda self, hero: equip(hero, self)
			),
			Equipment.Equipment("gold", "o"),
		],
		1: [Equipment.Equipment("potion de tp", "!", usage=lambda self, hero: teleport(hero, True))],
		2: [
			Wearable.Wearable(
				"sword", place="right hand", effect={"strength": 2}, usage=lambda self, hero: equip(hero, self)
			),
			Equipment.Equipment("bow"),
			Wearable.Wearable("leather vest", place="torso", effect={"armor": 1}, usage=lambda self, hero: equip(hero, self)),
			Equipment.Equipment("antidotal", usage=lambda self, hero: recover(hero, True)),
		],
		3: [
			Equipment.Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False)),
			Equipment.Equipment("invisibility potion", "i", usage=lambda self, hero: hero.becomeInvisible()),
		],
		4: [Wearable.Wearable("chainmail", place="torso", durability=7, effect={"armor": 2}, usage=lambda self, hero: equip(hero, self))],
	}
	monsters = {
		0: [Creature.Creature("Goblin", 4), Creature.Creature("Bat", 2, "W")],
		1: [Creature.Creature("Ork", 6, strength=2), Creature.Creature("Blob", 10)],
		6: [Creature.Creature("Witch", 12, "X", isBlinding=True)],
		15: [Creature.Creature("Dragon", 15, strength=3), Creature.Creature("Spider", 8, isPoisoning=True, strength=2)],
	}

	_actions = {
		"z": lambda hero: theGame.theGame().getFloor().move(hero, Coord.Coord(0, -1)),
		"s": lambda hero: theGame.theGame().getFloor().move(hero, Coord.Coord(0, 1)),
		"q": lambda hero: theGame.theGame().getFloor().move(hero, Coord.Coord(-1, 0)),
		"d": lambda hero: theGame.theGame().getFloor().move(hero, Coord.Coord(1, 0)),
		"i": lambda hero: theGame.theGame().addMessage(hero.fullDescription()),
		"k": lambda hero: hero.__setattr__("_hp", 0),
		" ": lambda hero: None,
		"u": lambda hero: hero.opendescription(theGame.theGame().select(hero._inventory), theGame.theGame().getFloor()),
		"p": lambda hero: theGame.theGame().addMessage(f"Seed: {theGame.theGame().seed}"),
		"f": lambda hero: theGame.theGame().floorInfos(),
		"c": lambda hero: hero.useSkills(),
	}

	_actionsAffichage = {
		"z": lambda hero: theGame.theGame().getFloor().moveAffichage(hero, Coord.Coord(0, -1)),
		"s": lambda hero: theGame.theGame().getFloor().moveAffichage(hero, Coord.Coord(0, 1)),
		"q": lambda hero: theGame.theGame().getFloor().moveAffichage(hero, Coord.Coord(-1, 0)),
		"d": lambda hero: theGame.theGame().getFloor().moveAffichage(hero, Coord.Coord(1, 0)),
		"i": lambda hero: theGame.theGame().addMessage(hero.fullDescription()),
		"k": lambda hero: hero.__setattr__("_hp", 0),
		" ": lambda hero: None,
		#"u": lambda hero: hero.opendescription(theGame.theGame().select(hero._inventory), theGame.theGame().getFloor()),
		"p": lambda hero: theGame.theGame().addMessage(f"Seed: {theGame.theGame().seed}"),
		"f": lambda hero: theGame.theGame().floorInfos(),
		"c": lambda hero: hero.useSkillsAffichage(),
		"t": lambda hero: theGame.theGame().cheatAffichage(),
	}

	def __init__(self, hero=None, level=1, floor=None, messages=None, equiped_outfits=None):
		"""
		Parameters
		----------
		hero : Hero | None
				Le héros à insérer dans la carte
		level : int | None
				Le niveau du jeu
		floor : Map.Map | None
				La carte
		messages : list | None
				La liste des messages à afficher au joueur
		"""
		if equiped_outfits is None:
			equiped_outfits = []
		self._hero = hero or Hero.Hero()
		if not messages:
			messages = []
		self._level = level
		self._floor = floor
		self._messages = messages
		self._idMonsters = 0
		self.seed = None
		self.equiped_outfits = equiped_outfits
		self.allMonsters = []
		self.levelsUsed = {}
		self.range = 5
		self.authenticated = False
		self.turn = 1

	def getRarety(self, equipment, i=0):
		if i > 4:
			raise KeyError("Equipment not found")
		for equip in Game.equipments[i]:
			if equip.getName() == equipment.getName():
				return i
		return self.getRarety(equipment, i + 1)

	def buildFloor(self, s=False):
		"""Construit la carte"""
		self._hero._invisible = False
		self.allMonsters = []
		self._floor = Map.Map(hero=self._hero, simulation=s)
		self._level += 1
		self.range = 5
		escalierPlace = False
		if self._level < 24:
			while not escalierPlace:
				try:
					self._floor.put(self._floor.randRoomfromRooms().randEmptyCoord(self._floor), Stairs.Stairs())
				except:
					pass
				else:
					escalierPlace = True
		nbRooms = len(self._floor.getRooms())
		if nbRooms >= 2 and self._level >= 5 and self._level <= 15:
			self._floor.put(
				self._floor.getRooms()[random.randint(0, nbRooms - 1)].randEmptyCoordNotCorridor(self._floor), Chest.Chest()
			)
		if self._level >= 15:
			randomValue = random.randint(1, 4)
			if randomValue == 1:
				self._floor.put(
					self._floor.getRooms()[random.randint(0, nbRooms - 1)].randEmptyCoordNotCorridor(self._floor),
					Chest.Chest(size="big"),
				)
		if self._level == 25:
			self._floor.put(
				self._floor.getRooms()[random.randint(0, nbRooms - 1)].randEmptyCoordNotCorridor(self._floor),
				Chest.Tresor(),
			)
		self.createShop()
		self.special_id = random.choice(self.allMonsters).getID()

	def getHero(self):
		"""
		Returns
		-------
		Hero.Hero
				Le héros du jeu
		"""
		return self._hero

	def getFloor(self):
		"""
		Returns
		-------
		Map.Map
				La carte du jeu
		"""
		return self._floor

	def addMessage(self, msg):
		"""
		Ajoute un message dans la liste des messages à afficher
		Parameters
		----------
		msg : str
				Message à afficher
		"""
		self._messages.append(msg)

	def readMessages(self):
		"""
		Renvoie une chaîne de caractère composée de tous les messages enregistrés
		et les supprime de la liste
		Returns
		-------
		str
				Concaténation des messages en question
		"""
		if not self._messages:
			return ""
		msg = "\n".join(self._messages)
		self._messages = []
		return msg

	def cheatAffichage(self):
		"""
		Permet d'exécuter une commande entrée par input, tout en vérifiant que la commande utilise theGame
		Returns
		-------
		"""
		if not self.authenticated:
			mdp = fenetreInput("mdp", "Mot de passe: ", "str")
			if hashlib.md5(mdp.encode()).hexdigest() != "b114c6627f97611de60963965a05d541":
				print("Wrong password !")
				return
			self.authenticated = True
		c = fenetreInput("Cmd","Commande de test: ", "str")
		exec(c)

	def randElement(self, collection):
		"""
		Renvoie un élément au hasard parmi la collection passée en paramètre

		Parameters
		----------
		collection : dict
				Ensemble des éléments associés par niveau

		Returns
		-------
		Element.Element
				L'élément tiré au hasard
		"""
		x = int(random.expovariate(1 / self._level))
		while not collection.get(x):
			x -= 1
		return copy.copy(random.choice(collection[x]))

	def resetVision(self):
		"""Reset la vision du joueur"""
		if self.turn % 10 == 0 and self.range != 5:
			self.range = 5
			theGame.theGame().addMessage("Your vision is reset")

	def randEquipment(self):
		"""
		Renvoie un équipement au hasard

		Returns
		-------
		Equipment.Equipment
				L'équipement tiré au hasard
		"""
		return self.randElement(Game.equipments)

	def randMonster(self):
		"""
		Renvoie un monstre au hasard et incrémente une liste de tout les monstres

		Returns
		-------
		Creature.Creature
				Le monstre tiré au hasard
		"""
		s = self.randElement(Game.monsters)
		s.setID(self._idMonsters)
		self._idMonsters += 1
		self.allMonsters.append(s)
		return s

	def createShop(self):
		s = Shop.Shop()
		items = 0
		while items < 5:
			level = random.randint(0, 4)
			item = random.choice(Game.equipments[level])
			if s.checkItem(item):
				continue
			price = int(random.expovariate(1 / self._level)) + 1
			number = int(random.expovariate(1 / self._level)) + 1
			s.addItem(copy.copy(item), number, price)
			items += 1
		element = ""
		coord = None
		while element != Map.Map.ground:
			r = self._floor.randRoomfromRooms()
			coord = r.randEmptyCoordNotCorridor(self._floor)
			element = self._floor.get(coord)
		self._floor.put(coord, s)

	@staticmethod
	def select(listeChoix):
		"""
		Sélectionne un élément dans une liste

		Parameters
		----------
		listeChoix : list
				La liste dans laquelle sélectionner

		Returns
		-------
		Equipment.Equipment | Wearable.Wearable
				L'élément sélectionné
		"""
		if not listeChoix:
			print("Nothing is in the inventory !")
			return None
		c = "Choose item> ["
		for i, choice in enumerate(listeChoix):
			c += f"'{i}: {choice.getName()}', "
		c = f"{c[:-2]}]"
		print(c)
		n = getch()
		while not n.isdigit() or int(n) < 0 or int(n) >= len(listeChoix):
			c = "Choose item> ["
			for i, choice in enumerate(listeChoix):
				c += f"'{i}: {choice.getName()}', "
			c = f"{c[:-2]}]"
			print(c)
			n = getch()
		itemdescription = "\t Choose action>  [0: 'use' , 1: 'description', 2: 'drop', 3: 'destroy']"
		print(itemdescription)
		return listeChoix[int(n)]

	def play(self):
		"""Main game loop"""
		self.seed = setSeed()
		self.buildFloor()
		self.resetVision()
		print("--- Welcome Hero! ---")
		while self._hero.getHP() > 0:
			print()
			print(self._floor)
			print(self._hero.description())
			print(self.readMessages())
			c = getch()
			if c in Game._actions:
				Game._actions[c](self._hero)
			self._hero.checkPoison()
			self._floor.moveAllMonsters()
			self._hero.unlockSkills()
		print("--- Game Over ---")



	def getchSimulation(self):
		"""
		Renvoie une touche au hasard parmi les touches possibles

		Returns
		-------
		str
				La touche sélectionnée
		"""
		roomsVisited = self._floor.getVisitedRooms()
		if len(self._floor.getRooms()) == len(roomsVisited):
			self._floor.setVisitedRooms([])
			self._floor.shuffleRooms()
		for m in self._floor.getRooms():
			if m not in self._floor.getRoomsVisited():
				s = self._floor.getElem()[self._hero].direction(m.center(), self._floor)
				if s:
					return self.dir[s]
		return random.choice(list(self.dir.values()))

	def getLevel(self):
		"""
		Renvoie le niveau actuel

		Returns
		-------
		int
				Le niveau actuel
		"""
		return self._level

	def playSimulation(self):
		self.dir = {Coord.Coord(0, -1): "z", Coord.Coord(0, 1): "s", Coord.Coord(1, 0): "d", Coord.Coord(-1, 0): "q"}
		"""Main game loop"""
		self.seed = setSeed()
		self.buildFloor(True)
		print("--- Welcome Hero! ---")
		i = 0
		while self._hero.getHP() > 0:
			print()
			print(self._floor)
			print(self._hero.description())
			print(self.readMessages())
			if i % 10 == 0:
				print("Entrez i pour jouer vous même !")
				t = getch()
				if t.lower() == "i":
					print("OK ! Entrez l'action à effectuer : ")
					c = getch()
				else:
					c = self.getchSimulation()
					print("Touche choisie : ", c)
					time.sleep(0.5)
					i += 1
			else:
				c = self.getchSimulation()
				print("Touche choisie : ", c)
				time.sleep(0.5)
				i += 1
			if c in Game._actions:
				Game._actions[c](self._hero)
			self._hero.checkPoison()
			self._floor.moveAllMonsters()
			self._hero.unlockSkills()
		print("--- Game Over ---")

	def floorInfos(self):
		"""
		Affiche l'étage actuel
		"""
		theGame.theGame().addMessage(f"You are at floor {self._level}")


def setSeed():
	"""
	Définit une graine aléatoire pour le jeu
	Returns
	-------
	int
			La graine aléatoire
	"""
	r = random.randint(0, 1000000000)
	# r = 102781142
	random.seed(r)
	return r

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
