import importlib
Game = importlib.import_module("Game")


def theGame(game = Game.Game()):
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