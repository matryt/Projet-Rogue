import random
import copy
import importlib

theGame = importlib.import_module("theGame")


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
			creature._strength += outfit.effect[key] + 100
			theGame.theGame().equiped_outfits.append(outfit)
			outfit.durability -= 1
			if outfit.durability == 0:
				theGame.theGame().equiped_outfits.remove(outfit) 
				return True
			return False 
			
		if key == 'armor':
			creature._hp += outfit.effect[key]
			theGame.theGame().equiped_outfits.append(outfit)
			return True


