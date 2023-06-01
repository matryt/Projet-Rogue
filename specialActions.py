import random
import copy
import importlib
import Creature
from utils import getch
import tkinter as tk
from tkinter.simpledialog import askinteger, askstring

theGame = importlib.import_module("theGame")
root2 = tk.Tk()

def heal(creature):
    """
    Soigne une créature

    Parameters
    ----------
    creature : Creature.Creature
            La créature à soigner

    Returns
    -------
    bool
            True

    """
    creature.heal()
    return True


def teleport(creature, unique):
	"""
	Téléporte une créature dans une salle vide

	Parameters
	----------
	creature : Creature.Creature
		La créature à téléporter
	unique : bool

	Returns
	-------
	bool

	"""
	m = theGame.theGame().getFloor()
	numberRooms = len(m.getRooms())
	i = 0
	p = m.pos(creature)
	roomsAvailable = copy.deepcopy(m.getRooms())
	random.shuffle(roomsAvailable)
	moved = False
	while not moved and i < numberRooms:
		room = roomsAvailable[i]
		r = room.randEmptyCoord(m)
		if r is not None and r != p:
			m.move(creature, r-p)
			moved = True
		i += 1
	return unique

def equip(creature,outfit):
	"""
	equipe une créature d'une arme ou tenue et lui applique ses effets 

	Parameters
	----------
	creature : Creature.Creature
		La créature à equiper
	outfit : Wearable.Wearable
		l'objet à equiper

	Returns
	-------
	bool
		True

	"""
	for key in outfit.effect:
		if key == 'strength':
			if creature._arme_equipee:
				creature._inventory.append(creature._arme_equipee)
			creature._arme_equipee = outfit
			#if creature.strengthMax != creature._strength + outfit.effect[key]:
			#	theGame.theGame().equiped_outfits.append(outfit)
			#	return True 
			#JE SAIS PAS PUTAIN
			creature._strength += outfit.effect.get('strength', 0)
 		
			if outfit.durability > 0:
					#while outfit.durability > 0:
						#creature._strength = creature._strength
						creature.strengthMax += outfit.effect[key]
						#outfit.durability -= 1
					#creature._strength -= outfit.effect.get('strength', 0)
					#pass
			else:
		
				return True

		if key == 'armor':
			creature.armor += outfit.effect[key]
			creature._inventory.remove(outfit)

		return False

def recover(creature, unique):
	"""
	Soigne une créature

	Parameters
	----------
	creature : Creature.Creature
		La créature à soigner
	unique : bool

	Returns
	-------
	bool

	"""
	creature.recover()
	return unique

def fireballThrow(creature, map, levelsUsed = []):
	"""
	Lance une boule de feu dans une direction
	Parameters
	----------
	creature : Creature.Creature
		La créature qui lance la boule de feu
	map : Map.Map
		La carte sur laquelle la boule de feu est lancée
	levelsUsed : list
		La liste des niveaux auxquels la boule de feu a déjà été lancée
	"""
	if theGame.theGame().getLevel() in levelsUsed:
		theGame.theGame().addMessage("You can't use this power again on this level")
		return
	print("In which direction do you want to throw the fireball ?")
	d = getch()
	while d not in ['z', 'q', 's', 'd']:
		theGame.theGame().addMessage("Please enter a valid direction")
		fireballThrow(creature, map)
	direction = theGame.theGame().getFloor().dir[d]
	pos = map.pos(creature)
	casesConcernees = [(pos+direction*i, 10-2*i) for i in range(1, 5)]
	for case in casesConcernees:
		g = map.get(case[0])
		if isinstance(g, Creature.Creature):
			g._hp -= case[1]
			theGame.theGame().addMessage(
				f"The fireball hits the {g._name} and causes him {case[1]} damage"
			)
	return levelsUsed

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

def fireballThrowAffichage(creature, map, levelsUsed = []):
	"""
	Lance une boule de feu dans une direction
	Parameters
	----------
	creature : Creature.Creature
		La créature qui lance la boule de feu
	map : Map.Map
		La carte sur laquelle la boule de feu est lancée
	levelsUsed : list
		La liste des niveaux auxquels la boule de feu a déjà été lancée
	"""
	if theGame.theGame().getLevel() in levelsUsed:
		theGame.theGame().addMessage("You can't use this power again on this level")
		return
	fenetreInput("Direction", "In which direction do you want to throw the fireball ?", "str")
	d = getch()
	while d not in ['z', 'q', 's', 'd']:
		messageFenetre("Please enter a valid direction")
		fireballThrow(creature, map)
	direction = theGame.theGame().getFloor().dir[d]
	pos = map.pos(creature)
	casesConcernees = [(pos+direction*i, 10-2*i) for i in range(1, 5)]
	for case in casesConcernees:
		g = map.get(case[0])
		if isinstance(g, Creature.Creature):
			g._hp -= case[1]
			messageFenetre(f"The fireball hits the {g._name} and causes him {case[1]} damage")
	return levelsUsed

def blind(hero):
	if theGame.theGame().range == 2:
		return
	theGame.theGame().range = 2
	theGame.theGame().addMessage(f"The {hero.conciseDescription()} is blind")
	theGame.theGame().turn = 1

def supervision(*args):
	if theGame.theGame().getLevel() in theGame.theGame().levelsUsed[1]:
		theGame.theGame().addMessage("You can't use this power again on this level")
		return
	theGame.theGame().addMessage("You have now a super-vision for 10 turns")
	theGame.theGame().range = 10
	theGame.theGame().turn = 1
	return True

def revive(creature):
	"""
	réanime le héro 

	Parameters
	----------
	creature : Creature.Creature
		La créature à revive 

	Returns
	-------
	bool

	"""
	creature.revive = True
	return True