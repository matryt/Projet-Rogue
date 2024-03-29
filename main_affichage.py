import pygame
import theGame
import Equipment
import Wearable
import Hero
import contextlib
import specialActions
import tkinter as tk
from pygame.locals import *
from tkinter.simpledialog import askstring, askinteger
from tkinter import ttk
import sys
import Coord
import Chest

import random

root2 = tk.Tk()
root2.withdraw()

def findTresor():
	for i in range(len(theGame.theGame().getFloor())):
		for j in range(len(theGame.theGame().getFloor())):
			elem = theGame.theGame().getFloor().get(Coord.Coord(i, j))
			if isinstance(elem, Chest.Tresor) and elem.chestopened:
				return True
	return False

def endWin():
	if theGame.theGame()._level == 25 and findTresor():
		global game
		game = False
		screen = pygame.display.set_mode(res, pygame.RESIZABLE)
		screen = pygame.display.set_mode(res, pygame.RESIZABLE)
		win = pygame.transform.scale(pygame.image.load("assets/win.png").convert_alpha(), (1000, 1000))
		screen.fill((89, 177, 187))
		screen.blit(win, ((screen.get_width() - 1000)//2, (screen.get_height() - 1000)//2))
		pygame.display.flip()
		global running
		running = False
		pygame.time.wait(5000)
		pygame.quit()
		sys.exit(0)

def on_closing():
	root2.quit()
	root2.destroy()

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

def is_digit_key(key):
	return key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]


def play_final():
	level = theGame.theGame()._level
	if event.type == KEYDOWN :
		num=pygame.key.name(event.key)
		if num in theGame.theGame()._actionsAffichage:
			theGame.theGame()._actionsAffichage[num](theGame.theGame()._hero)
	if theGame.theGame()._level != level:
		screen2.fill("white")
	theGame.theGame()._hero.checkPoison()
	theGame.theGame()._floor.moveAllMonsters()
	theGame.theGame()._hero.unlockSkillsAffichage()
	theGame.theGame().resetVision()
	endWin()


listEmplacements = {"0": [(60, 227),False],
					  "1": [(216, 227),False],
					"2": [(60, 353),False],
					"3": [(216, 353),False],
					"4": [(60, 477),False],
					"5": [(216, 477),False],
					"6": [(60, 605),False],
					"7": [(216, 607),False],
					"8": [(60, 729),False],
					"9": [(216, 729),False]}

def displayInventory(screen):
	for i, elem in enumerate(theGame.theGame()._hero._inventory):

		with contextlib.suppress(Exception):
			img = dict_item[elem.get_abbrv()]
			screen.blit(img, listEmplacements[str(i)][0])
			listEmplacements[str(i)][1] = True


def textInput(titre, message, typeInput):
	root2 = tk.Tk()
	root2.withdraw()
	ttk_style = ttk.Style(root2)
	ttk_style.configure('TEntry')
	match typeInput:
		case "int":
			val = askinteger(titre, message)
		case "str":
			val = askstring(titre, message)
		case _:
			raise ValueError("Type invalide")
	root2.quit()
	return val

def update_all(surface):
	update_health(surface)
	update_xp(surface)
	update_strength(surface)
	update_gold(surface)
	update_armor(surface)
	update_floor(surface)


def update_health(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 160, 400, 50])
	varHP = f"HP : {str(theGame.theGame().getHero().getHP())}/{str(theGame.theGame().getHero().hpMax)}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varHP, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width()-170, 175)
	screen2.blit(text, textRect)
	percent = 230 * (theGame.theGame().getHero().getHP() / theGame.theGame().getHero().hpMax)
	bar_position=[surface.get_width()-290,195,percent,60]
	back_bar_position=[surface.get_width()-290,195,230,60]
	pygame.draw.rect(surface,(80, 88, 94),back_bar_position)
	pygame.draw.rect(surface,("green"),bar_position)

def update_xp(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 270, 280, 400, 50])
	varLevel = f"Level {str(theGame.theGame().getHero().getLevel())}"
	fontText = pygame.font.Font("freesansbold.ttf", 30)
	text = fontText.render(varLevel, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width() - 170, 295)
	screen2.blit(text, textRect)
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 325, 400, 50])
	varXP = f"XP : {str(theGame.theGame().getHero().xp)}/{str(theGame.theGame().getHero().xpMax)}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varXP, True, "black")
	textRect2 = text.get_rect()
	textRect2.center = (screen2.get_width() - 170, 325)
	screen2.blit(text, textRect2)
	if theGame.theGame().getHero().xp > 0 and theGame.theGame().getHero().xpMax > 0:
		percent = 230 * (theGame.theGame().getHero().xp / theGame.theGame().getHero().xpMax)
	else:
		percent = 0
	bar_position = [surface.get_width() - 290, 345, percent, 60]
	back_bar_position = [surface.get_width() - 290, 345, 230, 60]
	pygame.draw.rect(surface, (80, 88, 94), back_bar_position)
	pygame.draw.rect(surface, ("blue"), bar_position)

def update_strength(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 405, 400, 75])
	varStrength = f"Strength : {str(theGame.theGame().getHero()._strength)}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varStrength, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width() - 170, 425)
	surface.blit(text, textRect)
	surface.blit(epeeIcon, (screen2.get_width() - 310, 410))

def update_armor(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 465, 400, 50])
	varArmor = f"Armor : {str(theGame.theGame().getHero().armor)}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varArmor, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width() - 170, 480)
	surface.blit(text, textRect)
	surface.blit(bouclier, (screen2.get_width() - 315, 465))

def update_floor(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 580, 400, 50])
	varFloor = f"Floor : {theGame.theGame().getLevel()}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varFloor, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width() - 170, 595)
	surface.blit(text, textRect)
	surface.blit(floor, (screen2.get_width() - 320, 570))

def update_gold(surface):
	pygame.draw.rect(surface, "white", [screen2.get_width() - 300, 525, 400, 50])
	varHP = f"Gold(s) : {str(theGame.theGame().getHero().getGoldCount())}"
	font = pygame.font.Font("freesansbold.ttf", 30)
	text = font.render(varHP, True, "black")
	textRect = text.get_rect()
	textRect.center = (screen2.get_width() - 170, 545)
	surface.blit(text, textRect)
	surface.blit(gold, (screen2.get_width() - 315, 525))


pygame.init()
running = True
game = False
aide = False
fin_=False
flags = pygame.FULLSCREEN | pygame.RESIZABLE
clock = pygame.time.Clock()
pygame.display.set_caption("DONGEON MASTER")
res = (1440, 810)
screen = pygame.display.set_mode(res, pygame.RESIZABLE)
sol = pygame.transform.scale(pygame.image.load("assets/sol.png").convert(), (66, 66))
mur1 = pygame.transform.scale(pygame.image.load("assets/mur1.png").convert(), (66, 66))
mur2 = pygame.transform.scale(pygame.image.load("assets/mur2.png").convert(), (66, 66))
inventaire = pygame.transform.scale(pygame.image.load("assets/inventaireV2_r.png").convert_alpha(), (320, 840))
hero = pygame.transform.scale(pygame.image.load("assets/hero.png").convert_alpha(), (150, 150))
nuage = pygame.transform.scale(pygame.image.load("assets/sol/nuage_sol.png").convert_alpha(), (66, 66))
bouclier = pygame.transform.scale(pygame.image.load("assets/shield_icon.png").convert_alpha(), (35, 35))
epeeIcon = pygame.transform.scale(pygame.image.load("assets/strength_icon.png").convert_alpha(), (26, 43))
gold = pygame.transform.scale(pygame.image.load("assets/coin.png").convert_alpha(), (35, 35))
floor = pygame.transform.scale(pygame.image.load("assets/floor2_icon.png").convert_alpha(), (40, 40))


equipments = {
		0: [
			Equipment.Equipment("potion", "p", usage=lambda self, hero: specialActions.heal(hero)),
			Wearable.Wearable(
				"broken sword", place="right hand", effect={"strength": 1}, usage=lambda self, hero: specialActions.equip(hero, self)
			),
			Wearable.Wearable(
				"trident", place="right hand", effect={"strength": 3}, usage=lambda self, hero: specialActions.equip(hero, self)
			),
			Wearable.Wearable(
				"double_epee", place="right hand", effect={"strength": 2}, usage=lambda self, hero: specialActions.equip(hero, self)
			),
			Equipment.Equipment("gold", "o"),
		],
		1: [Equipment.Equipment("potion de tp", "!", usage=lambda self, hero: specialActions.teleport(hero, True))],
		2: [
			Wearable.Wearable(
				"sword", place="right hand", effect={"strength": 2}, usage=lambda self, hero: specialActions.equip(hero, self)
			),
			Equipment.Equipment("bow"),
			Wearable.Wearable("leather vest", place="torso", effect={"armor": 1}, usage=lambda self, hero: specialActions.equip(hero, self)),
			Equipment.Equipment("antidotal", usage=lambda self, hero: specialActions.recover(hero, True)),
		],
		3: [
			Equipment.Equipment("portoloin", "w", usage=lambda self, hero: specialActions.teleport(hero, False)),
			Equipment.Equipment("invisibility potion", "i", usage=lambda self, hero: hero.becomeInvisible()),
		],
		4: [Wearable.Wearable("chainmail", place="torso", durability=7, effect={"armor": 2}, usage=lambda self, hero: specialActions.equip(hero, self))],
	}

dict_sol ={
		"G": pygame.transform.scale(pygame.image.load("assets/sol/goblinsol.png").convert(), (66, 66)),
		"E":pygame.transform.scale(pygame.image.load("assets/sol/escalier_sol.png").convert(), (66, 66)),
		"W":pygame.transform.scale(pygame.image.load("assets/sol/bat_sol.png").convert(), (66, 66)),
		"O": pygame.transform.scale(pygame.image.load("assets/sol/orksol.png").convert(), (66, 66)),
		"B":pygame.transform.scale(pygame.image.load("assets/sol/blobsol.png").convert(), (66, 66)),
		"S":pygame.transform.scale(pygame.image.load("assets/sol/spider_sol.png").convert(), (66, 66)),
		"D":pygame.transform.scale(pygame.image.load("assets/sol/dragonsol.png").convert(), (66, 66)),
		"p":pygame.transform.scale(pygame.image.load("assets/sol/potion_hp_sol.png").convert(), (66, 66)),
		"n":pygame.transform.scale(pygame.image.load("assets/sol/brokensword_sol.png").convert(), (66, 66)),
		"t":pygame.transform.scale(pygame.image.load("assets/sol/trident_sol.png").convert(), (66, 66)),
		"d":pygame.transform.scale(pygame.image.load("assets/sol/double_epee_sol.png").convert(), (66, 66)),
		"o":pygame.transform.scale(pygame.image.load("assets/sol/gold_sol.png").convert(), (66, 66)),
		"!":pygame.transform.scale(pygame.image.load("assets/sol/teleport_potion_sol.png").convert(), (66, 66)),
		"s":pygame.transform.scale(pygame.image.load("assets/sol/epeesol.png").convert(), (66, 66)),
		"b":pygame.transform.scale(pygame.image.load("assets/sol/arcsol.png").convert(), (66, 66)),
		"l":pygame.transform.scale(pygame.image.load("assets/sol/leathervestsol.png").convert(), (66, 66)),
		"a":pygame.transform.scale(pygame.image.load("assets/sol/antidote_sol.png").convert(), (66, 66)),
		"w":pygame.transform.scale(pygame.image.load("assets/sol/portoloin_sol.png").convert(), (66, 66)),
		"i":pygame.transform.scale(pygame.image.load("assets/sol/invisibility_potion_sol.png").convert(), (66, 66)),
		"c":pygame.transform.scale(pygame.image.load("assets/sol/chainmail_sol.png").convert(), (66, 66)),
		"@":pygame.transform.scale(pygame.image.load("assets/sol/herosol.png").convert(), (66, 66)),
		"e":pygame.transform.scale(pygame.image.load("assets/sol/shopsol.png").convert(), (66, 66)),
		"M":pygame.transform.scale(pygame.image.load("assets/sol/coffre_ferme_sol.png").convert(), (66, 66)),
		"Mo":pygame.transform.scale(pygame.image.load("assets/sol/coffre_ouvert_sol.png").convert(), (66, 66)),
		"X":pygame.transform.scale(pygame.image.load("assets/sol/witchsol.png").convert(), (66, 66)),
		"k":pygame.transform.scale(pygame.image.load("assets/sol/clesol.png").convert(), (66, 66))
		}

dict_item ={
		"p":pygame.transform.scale(pygame.image.load("assets/potion_hp.png").convert_alpha(), (66, 66)),
		"n":pygame.transform.scale(pygame.image.load("assets/brokensword.png").convert_alpha(), (66, 66)),
		"t":pygame.transform.scale(pygame.image.load("assets/trident.png").convert_alpha(), (66, 66)),
		"d":pygame.transform.scale(pygame.image.load("assets/double_epee.png").convert_alpha(), (66, 66)),
		"o":pygame.transform.scale(pygame.image.load("assets/gold.png").convert_alpha(), (66, 66)),
		"!":pygame.transform.scale(pygame.image.load("assets/teleport_potion.png").convert_alpha(), (66, 66)),
		"s":pygame.transform.scale(pygame.image.load("assets/epee.png").convert_alpha(), (66, 66)),
		"b":pygame.transform.scale(pygame.image.load("assets/arc.png").convert_alpha(), (66, 66)),
		"l":pygame.transform.scale(pygame.image.load("assets/leathervest.png").convert_alpha(), (66, 66)),
		"a":pygame.transform.scale(pygame.image.load("assets/antidote.png").convert_alpha(), (66, 66)),
		"w":pygame.transform.scale(pygame.image.load("assets/portoloin.png").convert_alpha(), (66, 66)),
		"i":pygame.transform.scale(pygame.image.load("assets/invisible_potion.png").convert_alpha(), (66, 66)),
		"c":pygame.transform.scale(pygame.image.load("assets/chainmail.png").convert_alpha(), (66, 66)),
		"M":pygame.transform.scale(pygame.image.load("assets/coffre_ferme.png").convert_alpha(), (66, 66)),
		"Mo":pygame.transform.scale(pygame.image.load("assets/coffre_ouvert.png").convert_alpha(), (66, 66)),
		"k":pygame.transform.scale(pygame.image.load("assets/cle.png").convert_alpha(), (66, 66))
		}

while running:
	scrrec = screen.get_rect()
	background = pygame.transform.scale(pygame.image.load("assets/background lancement.png").convert(), (scrrec.right, scrrec.bottom))
	screen.blit(background, (0, 0))
	play_button = pygame.image.load("assets/LOGO-PLAY.png")
	play_button_rect = play_button.get_rect()
	play_button_rect.center = screen.get_rect().center
	screen.blit(play_button, play_button_rect)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
		elif event.type == KEYDOWN and event.key == K_ESCAPE:
			pygame.quit()
			running = False
		elif event.type == KEYDOWN and event.key == K_h:
			screen_aide = pygame.display.set_mode((0,0), flags)
			aide = True
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if play_button_rect.collidepoint(event.pos):
				screen2 = pygame.display.set_mode((0, 0), flags)
				screen2.fill("white")
				theGame.theGame().buildFloor()
				theGame.theGame()._hero=Hero.Hero()
				theGame.theGame()._floor.setVisible(theGame.theGame().getFloor().rangeElement(theGame.theGame().getFloor()._hero))
				listEmplacements = {"0": [(60, 227),False],
					  "1": [(216, 227),False],
					"2": [(60, 353),False],
					"3": [(216, 353),False],
					"4": [(60, 477),False],
					"5": [(216, 477),False],
					"6": [(60, 605),False],
					"7": [(216, 607),False],
					"8": [(60, 729),False],
					"9": [(216, 729),False]}
				screen2.blit(inventaire, (10, 15))
				for i in range(13):
					for j in range(13):
						if theGame.theGame().getFloor()._mat[j][i] == theGame.theGame().getFloor().empty:
							screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
						else:
							if theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().ground:
								screen2.blit(sol,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
							elif theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().empty:
								screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)																		
							elif theGame.theGame().getFloor()._visibleMap[j][i] == "~":
								screen2.blit(nuage, ((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
							elif theGame.theGame().getFloor()._visibleMap[j][i]!=theGame.theGame().getFloor().empty:
								elem=theGame.theGame().getFloor()._visibleMap[j][i]
								if not isinstance(theGame.theGame().getFloor()._visibleMap[j][i],str):
									elem=elem.get_abbrv()
								screen2.blit(dict_sol[elem],((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)

				running = False
				game = True

	while aide:
		scrrec_aide = screen_aide.get_rect()
		screen_aide.fill([255, 255, 255])
		background = pygame.transform.scale(pygame.image.load("assets/help.png").convert(), (scrrec_aide.right, scrrec_aide.bottom))
		screen_aide.blit(background, (0, 0))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				aide = False
				screen = pygame.display.set_mode(res, pygame.RESIZABLE)
				screen = pygame.display.set_mode(res, pygame.RESIZABLE)
				background = pygame.transform.scale(pygame.image.load("assets/background lancement.png").convert(), (scrrec.right, scrrec.bottom))
				screen.blit(background, (0, 0))
				running = True

	while game and theGame.theGame().getHero().getHP() > 0:
		screen2.blit(inventaire, (10, 15))
		screen2.blit(hero, (screen2.get_width()-250, 0))
		update_all(screen2)
		displayInventory(screen2)
		for event in pygame.event.get():
			if event.type !=KEYDOWN :
				continue 
			play_final()
			if event.type == KEYDOWN and event.key == K_k:
				pygame.display.set_mode(res, pygame.RESIZABLE)
				pygame.display.set_mode(res, pygame.RESIZABLE)
				game = False
				running = True
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				game = False
				running = False
			#try :
			if is_digit_key(event.key):
				a = pygame.key.name(event.key)
				if len(a)>1:
					a = a[1]
				a = int(a)
				if a >= len(theGame.theGame()._hero._inventory):
					messageFenetre("Vous n'avez pas d'objet \nà cet emplacement", "Erreur")
					continue
				titre = "choose action"
				message = "0 : 'use' \n1: 'drop' \n2: 'destroy'"
				image_path = "assets/chooseaction6.png"
				resultat = int(textInput("Inventaire", message, "int"))
				obj = theGame.theGame()._hero._inventory[a]
				if resultat == 0: 	#"use item"
						theGame.theGame()._hero.use(obj)
				if resultat == 1: 	#"drop item"
					voisins = theGame.theGame().getFloor().pos(theGame.theGame()._hero).voisins(theGame.theGame().getFloor())
					for v in voisins:
						if theGame.theGame().getFloor().get(v) != theGame.theGame().getFloor().ground:    #  Map.Map.empty:
							voisins.remove(v)
					if len(voisins)>0:
						try:
							theGame.theGame()._floor.put(random.choice(voisins), obj) #  cette ligne fait de la D mais tkt dans le try ça rend bien
						except:
							messageFenetre("There is no place \nto drop the item")
						else:
							theGame.theGame()._hero._inventory.remove(obj)
							if obj == theGame.theGame()._hero._arme_equipee:
								theGame.theGame()._hero._arme_equipee = None
								theGame.theGame()._hero._strength -= obj.effect.get('strength', 0)
							if obj == theGame.theGame()._hero._armure_equipee:
								theGame.theGame()._hero._armure_equipee = None
								theGame.theGame()._hero._defense -= obj.effect.get('armor', 0)
					else:
						messageFenetre("There is no place \nto drop the item")
				if resultat == 2:	#  "destroy item"
					obj = theGame.theGame()._hero._inventory[a]
					theGame.theGame()._hero._inventory.remove(obj)
					if obj == theGame.theGame()._hero._arme_equipee:
						theGame.theGame()._hero._arme_equipee = None
						theGame.theGame()._hero._strength -= obj.effect.get('strength', 0)
					if obj == theGame.theGame()._hero._armure_equipee:
						theGame.theGame()._hero._armure_equipee = None
						theGame.theGame()._hero._defense -= obj.effect.get('armor', 0)
				displayInventory(screen2)
			for i in range(13):
					for j in range(13):
						if theGame.theGame().getFloor()._mat[j][i] == theGame.theGame().getFloor().empty:
							screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
						else:
							if theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().ground:
								screen2.blit(sol,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
							elif theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().empty:
								screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)																		
							elif theGame.theGame().getFloor()._visibleMap[j][i] == "~":
								screen2.blit(nuage, ((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
							elif theGame.theGame().getFloor()._visibleMap[j][i]!=theGame.theGame().getFloor().empty:
								elem=theGame.theGame().getFloor()._visibleMap[j][i]
								if not isinstance(theGame.theGame().getFloor()._visibleMap[j][i],str):
									elem=elem.get_abbrv()
								screen2.blit(dict_sol[elem],((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
		pygame.display.update()
		if theGame.theGame().getHero().getHP() <= 0:
			screen_fin = pygame.display.set_mode(res, pygame.RESIZABLE)
			screen_fin = pygame.display.set_mode(res, pygame.RESIZABLE)
			screen_fin.fill("black")
			fin_=True
			game=False
		while fin_ :
			menu_button = pygame.image.load("assets/bouton_menu.png")
			retry_button = pygame.image.load("assets/bouton_retry_.png")
			menu_button_rect = play_button.get_rect()
			retry_button_rect = retry_button.get_rect()
			retry_button_rect.move_ip(350,200)
			menu_button_rect.move_ip(680,200)
			screen_fin.blit(menu_button, menu_button_rect)
			screen_fin.blit(retry_button, retry_button_rect)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.quit()
					running = False
				elif event.type == KEYDOWN and event.key == K_h:
					screen_aide = pygame.display.set_mode((0,0), flags)
					aide = True
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if menu_button_rect.collidepoint(event.pos):
						screen = pygame.display.set_mode(res, pygame.RESIZABLE)
						screen = pygame.display.set_mode(res, pygame.RESIZABLE)
						game=False
						fin_=False
						running=True

					if retry_button_rect.collidepoint(event.pos):
						screen2 = pygame.display.set_mode((0, 0), flags)
						screen2.fill("white")
						theGame.theGame()._level=0
						theGame.theGame().buildFloor()
						theGame.theGame()._hero=Hero.Hero()
						theGame.theGame()._floor.setVisible(theGame.theGame().getFloor().rangeElement(theGame.theGame().getFloor()._hero))
						listEmplacements = {"0": [(60, 227),False],
											"1": [(216, 227),False],
											"2": [(60, 353),False],
											"3": [(216, 353),False],
											"4": [(60, 477),False],
											"5": [(216, 477),False],
											"6": [(60, 605),False],
											"7": [(216, 607),False],
											"8": [(60, 729),False],
											"9": [(216, 729),False]}
						screen2.blit(inventaire, (10, 15))
						for i in range(13):
							for j in range(13):
								if theGame.theGame().getFloor()._mat[j][i] == theGame.theGame().getFloor().empty:
									screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
								else:
									if theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().ground:
										screen2.blit(sol,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
									elif theGame.theGame().getFloor()._visibleMap[j][i] == theGame.theGame().getFloor().empty:
										screen2.blit(mur1,((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)																		
									elif theGame.theGame().getFloor()._visibleMap[j][i] == "~":
										screen2.blit(nuage, ((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
									elif theGame.theGame().getFloor()._visibleMap[j][i]!=theGame.theGame().getFloor().empty:
										elem=theGame.theGame().getFloor()._visibleMap[j][i]
										if not isinstance(theGame.theGame().getFloor()._visibleMap[j][i],str):
											elem=elem.get_abbrv()
										screen2.blit(dict_sol[elem],((screen2.get_width() - 13 * 66) / 2 + i * 66,(screen2.get_height() - 13 * 66) / 2 + j * 66,),)
						game=True
						fin_=False
