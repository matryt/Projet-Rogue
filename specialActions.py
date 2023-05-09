import Game
import random
import copy

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
    m = Game.theGame().getFloor()
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
