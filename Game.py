import copy
import math
import random

from Equipment import Equipment
from Creature import Creature
import Hero
import Map
import Stairs
from Wearable import Wearable
from utils import getch
import Coord
from specialActions import heal, teleport


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
	_hero
	_messages
	_level
	_floor : Map
	_actions : dict
		Actions possibles du jeu
	_idMonsters : int
		Identifiant des monstres
	"""
	equipments = {0: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
	                  Equipment("gold", "o")],
	              1: [Equipment("potion", "!", usage=lambda self, hero: teleport(hero, True))],
	              2: [Wearable("sword", place='right hand', effect={'strength': 2}),
	                  Equipment("bow"),
	                  Wearable("leather vest", place='torso', effect={'armor': 1})],
	              3: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False))],
	              4: [Wearable("chaimail", place='torso', effect={'armor': 2})]}
	monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
	            1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}

	_actions = {'z': lambda hero: theGame()._floor.move(hero, Coord.Coord(0, -1)),
	            's': lambda hero: theGame()._floor.move(hero, Coord.Coord(0, 1)),
	            'q': lambda hero: theGame()._floor.move(hero, Coord.Coord(-1, 0)),
	            "d": lambda hero: theGame()._floor.move(hero, Coord.Coord(1, 0)),
	            "i": lambda hero: theGame().addMessage(hero.fullDescription()),
	            "k": lambda hero: theGame()._hero.__setattr__('_hp', 0),
	            " ": lambda hero: None,
	            "u": lambda hero: hero.use(theGame().select(hero.getInventory()))
	            }

	def __init__(self, hero = None, level = 1, floor = None, messages = None):
		"""
		Parameters
		----------
		hero : Hero | None
			Le héros à insérer dans la carte
		level : int | None
			Le niveau du jeu
		floor : int | None
			La carte
		messages : list | None
			La liste des messages à afficher au joueur
		"""
		self._hero = hero or Hero.Hero()
		if not messages:
			messages = []
		self._level = level
		self._floor = floor
		self._messages = messages
		self._idMonsters = 0

	def buildFloor(self):
		"""
		Construit la carte
		"""
		self._floor = Map.Map(hero=self._hero)
		self._level += 1
		self._floor.put(self._floor.getRooms()[-1].center(), Stairs.Stairs())

	def getHero(self):
		"""
		Renvoie le héros du jeu

		Returns
		-------
		Hero.Hero
			Le héros du jeu
		"""
		return self._hero

	def getFloor(self):
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
		msg = ". ".join(self._messages)+"."
		self._messages = []
		return msg

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
		x = random.expovariate(1/self._level)
		x = math.floor(x)
		while not collection.get(x):
			x -= 1
		return copy.copy(random.choice(collection[x]))

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
		Renvoie un monstre au hasard

		Returns
		-------
		Creature.Creature
			Le monstre tiré au hasard
		"""
		s = self.randElement(Game.monsters)
		s.setID(self._idMonsters)
		self._idMonsters += 1
		return s

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
		c = "Choose item> ["
		for i, choice in enumerate(listeChoix):
			c += f"\'{i}: {choice.getName()}\', "
		c = f"{c[:-2]}]"
		print(c)
		n = getch()
		while not n.isdigit() or int(n) < 0 or int(n) >= len(listeChoix):
			c = "Choose item> ["
			for i, choice in enumerate(listeChoix):
				c += f"\'{i}: {choice.getName()}\', "
			c = f"{c[:-2]}]"
			print(c)
			n = getch()
		return listeChoix[int(n)]

	def play(self):
		"""Main game loop"""
		self.buildFloor()
		print("--- Welcome Hero! ---")
		while self._hero.getHP() > 0:
			print()
			print(self._floor)
			print(self._hero.description())
			print(self.readMessages())
			c = getch()
			if c in Game._actions:
				Game._actions[c](self._hero)
			self._floor.moveAllMonsters()
		print("--- Game Over ---")


def theGame(game = Game()):
	"""
	Retourne l'instance Game du programme en cours
	Parameters
	----------
	game : Game, optional
		L'instance de Game pour ce run

	Returns
	-------
	Game
	"""
	return game
