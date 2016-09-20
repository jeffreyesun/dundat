#This is a whole lot of spaghetti, and I apologize to anyone trying to figure out how it works, which is probably going to be myself in the future. The basic deal is that your character can be in one of many numbered locations, stored as "shared.pos".

#(This code may be deprecated, but at least it's self-deprecated)

#The game runs by iterating the step() function until the win conditions are met.

#Each command the user types is split by parse() into a "verb" and an optional "noun. Each verb has a corresponding function, and each noun has a corresponding object. So typing "examine poster", for example, sets noun=poster, and calls climb().

#The verbs are all defined in the main files because python doesn't allow imported functions to access the global variables of the parent module. Don't do this! Set up a shared namespace at the get-go!

#import some data
from generators import question
from generators import poster
from generators import prop
from generators import poster1
from objects import objects
surroundings=objects("surroundings")
dialogues=objects("dialogues")
descriptions=objects("descriptions")
intros=objects("intros")
nouns=objects("nouns")
mapp=objects("map")

#set locations as traversable or untraversable
traversable=['24out','20door','18door','11house','8bar','4cw','5cw','6cw','7cw','4ws','5ws','6ws','7ws','3stairs','4stairs','6stairs','8w','8east','8south','9north','9south','9east','9west','10east','10west','10south','11west','11south','11e','12north','13north','14north','15out','16.1door','17out','17door','18cw','18ws','19out','24out','20cw','21cw','21ws','22cw','22ws','23ws','20w','23booth']
untraversable=['8n','10n','11n','12e','12s','12w','13e','13s','13w','14s','14e','14w','20ws','23cw','23w','19w','19n','19s','21w']


pos = 1			#start on square 1
path = []		#records where you've been
inv = []		#inventory
noun=[]			#current noun
winconditions='notmet'	#you still have some work to do
splitentry=[]		#the user input, split into words
verb=''			#current verb


#########################
#Verbs Begin, Forgive Me#
#########################

def help():
	print('''	Though this game is designed to understand whatever you might want to do, sometimes an action will be too... eccentric, or worded in a way that confuses us.
	Serving both as tutorial and hint section, here is a list of the verbs necessary to the game:
	plug in
	use (either a single object, or one object with another)
	talk to
	help
	wear
	make
	cut
	take
	inventory (i)
	look around (look) (commands such as "look east" and "look clockwise" are understood)
	examine
	move
	open (not needed for doors)
	enter
	exit
	go
	wake up
	map (Displays a high-res map of your location, with an x marking you current position)
	Everything can be accomplished with these verbs, and whatever nouns you might find lying around. Good luck!"''')

def plug():
	global noun
	global descriptions
	global splitentry
	if noun in ['24mixing','24cord']:
		if 'pluggedin' not in path:
			print("\tYou plug it in. Nothing happens.")
			path.append('pluggedin')
			descriptions['24mixing']="The mixing table has a socket for a microphone and a socket for power. A power cord is plugged into the latter."
			descriptions['24cord']="The cord is plugged into the mixing table."
		else: print("\tIt's already plugged in.")
	elif ('microphone' in splitentry) or ('mike' in splitentry):use()
	else:print("\tWhat?")

def sit():
	if noun in ["17couch","19chair","24chair"]:use()
	else:print("\tYou sit down, for whatever reason.")
		
def use():
	global winconditions
	global spaced
	global pos
	global inv
	global path
	global noun
	global splitentry
	global descriptions
	global surroundings
	global nouns
	global intros
	global dialogues
	if pos == 2:
		if noun == "invsack":
			pos = 3
		else: print("\tYou decide to file that away under \"if I survive.\"")
	elif "scissors" in splitentry:
		cut()
	elif (noun == "invpen") and (pos != 21):
		print("\tYou sign your name on a piece of paper. That'll be worth a lot someday, you think.")
	elif noun in ["invsack","invbackpack"]:
		if ("make" in splitentry) and ("eyepatch" in splitentry):make()
		else:inventory()
	elif noun in ["4stairs","6stairs","9door","11hole",'16door']:go()
	elif noun == "12radio":	print("\tYou approach the radio, and put a hand towards it. \"Touchin' Nikola's the last thin' ye'll e'er do, boy.\" Growls the pirate.")
	elif noun == "12hammock": print("\tYou climb into the hammock, and awake an hour later, well rested.")
	elif noun == "inveyepatch":wear()
	elif noun in ['invrum','15rum']:print("\tYou take a swig of the cask-strength rum. The world gets slightly fuzzier.")
	elif (('tap' in splitentry) or ('button' in splitentry)) and (pos==17):
		if 'glass' in splitentry:
			if 'condiment' not in path:
				print("\tYou pour the butter-like condiment flavored spread into the glass, leaving the glass filled with a mixture of corrosive butteresque oils and residual hard liquor.")
				nouns["condiment"]="invglass"
				nouns["acid"]="invglass"
				nouns["oil"]="invglass"
				nouns["oils"]="invglass"
				path.append("condiment")
				descriptions["invglass"]="The glass is a sizzling cauldron of butter-inspired acid and hard liquor."
			else:
				print("\tYou pour more of the butter-reminiscent liquid into the glass, overfilling it and dripping onto the floor where it leaves a widening bald spot in the carpet.")
			descriptions["17carpet"]="A hole in the carpet widens and sizzles where the butter-like condiment flavored spread dissolves it into oblivion."
		else:
			print("\tYou push the button, and butter-like condiment flavored spread drips onto the floor, where is sizzles for a moment before leaving a bald patch in the carpet.")
			descriptions["17carpet"]="A hole in the carpet widens and sizzles where the butter-like condiment flavored spread dissolves it into oblivion."
	elif noun in["17couch","19chair","24chair"]:
		print("\tYou sit in it. It's comfy.")
	elif ('flashlight' in splitentry) and ('flashlight' in inv) and ('door' not in splitentry):
		if 'battery' in splitentry:
			if 'battery' in inv:
				print ("\tYou install the batteries in the flashlight. It bursts on, filling the room with light. You retract any doubts you had as to the quality of this portable lighthouse.")
				spaced = 1
				pos = 16.1
				inv.remove('battery')
			else: print("\tYou don't have any batteries.")
		elif pos==16:print("\tYou try to turn it on, but it doesn't work. This was not a nice reward, you think. You begin to distrust the ethical roadmap of the average pirate.")
		elif 'condiment' not in path:print("\tThe flashlight is already on, and shines with at least 3 digits of watts.")
		else: print("\tYou don't know quite how to use this pot of vegetable oil and battery acid")
	elif ('door' in splitentry) and (pos==17):
		if (('glass' in splitentry) or ('condiment' in splitentry) or ('spread' in splitentry) or ('oil' in splitentry)) and ("glass" in inv):
			if 'condiment' in path:
				print("\tYou splash the butter-like condiment flavored spread onto the door. After a few seconds, a hole big enough to climb through is eaten out of it. The shell of the glass crumbles in your hand.")
				inv.remove("glass")
				path.append("splashed")
				nouns['17hole']="17door"
				descriptions["17door"]="The door quietly sizzles as the spread eats away at it."
			else:print("\tYou bash the glass against the door to no avail.")
		elif 'splashed' not in path:
			print("\tYou try to open the door, but it is firmy and heavily locked.")
		else:go()
	elif ('box' in splitentry) and ('pen' in splitentry) and ('pen' in inv) and (pos == 21):
			print("\tYou place the pen between the two electrodes.")
			descriptions["21box"]="A steel pen is fit snugly into a socket in the fusebox."
			surroundings[21]="There is a fuse-box here, in which one fuse has been replaced by a steel pen. The master lever is in the off position."
			path.append('fused')
			inv.remove('pen')
	elif noun == '21lever':
		if 'fused' not in path: print("\tYou clunk it to \"on\", but it just snaps back.")
		elif 'levered' not in path:
			print(dialogues['leveredd'])
			path.append("levered")
			surroundings[21]="There is a fuse-box here in which one fuse has been replaced by a steel pen. The master lever is in the on position."
			descriptions["21lever"]="It is locked in the \"on\"position."
			descriptions["21box"]="The pen in the fuse box crackles slightly as electricity runs through it."
			descriptions["21pen"]="The pen crackles slightly with electricity."
			surroundings[24]="The booth is transparent, and sits directly on the grass. There are two rolling chairs at a desk facing onto the field, and a mixing table tucked underneath it. The man is standing in the middle of the room, look up at the sky."
			intros[24]="You walk into the announcer's booth. The booth pushes out onto the field slightly, and the eerily empty stands are completely visible from here. There are two rolling chairs at a desk facing onto the field, and a mixing table tucked underneath it. The man is standing in the middle of the room, look up at the sky."
			nouns['24man']='24man'
			nouns['24guy']='24man'
			nouns['24dude']='24man'
			nouns['24him']='24man'
			nouns['24them']='24man'
		else: print("It is locked in the \"on\" position.")
	elif noun == '24cord':
		if 'pluggedin' not in path:
			print("\tYou plug it in. Nothing happens.")
			path.append('pluggedin')
			descriptions['24mixing']="The mixing table has a socket for a microphone. A power cord is plugged into it."
			descriptions['24cord']="The cord is plugged into the mixing table."
		else: print("It's already plugged in.")
	elif noun == 'invmicrophone':
		if pos == 24:
			if ("levered" in path) and ("pluggedin" in path):
				winconditions = 'met'
			else:print("\tYou plug it in. Nothing happens. You try to rest the microphone on the mixing table, but it just rolls off, so you unplug it and put it back in your backpack.")
		else:print("\tYou say \"Hallo?\" into the microphone. Nothing happens.")
	elif noun=='invpaper':
		if "hat" in splitentry:make()
	else:print("\tYou can't use that")

def gowhat():
	print("\tYou can't go any further in that direction.")

def talk():
	global dialogues
	global pos
	global noun
	global spaced
	global path
	global inv
	if pos<8:#before the Pirate Bay
		if noun == "5man":
			if '5man' in path: print("\t"+dialogues['5man2'])
			else:
				print("\t"+dialogues['5man'])
				path.append('5man')
				inv.extend(['scissors','pen'])
		elif noun == "7man":
			if '7man' not in path:
				print("\t"+dialogues['7man'])
				path.append('7man')
			elif 'weareyepatch' in path:
				if 'hat' in inv:
					print("\tThe man looks you up and down, and mutters that it will have to do. He pulls out a length of blue chain from a fold of his surprisingly puffy shirt. \"Get close,\" He grumbles, \"Wouldn't want half of you left behind.\" You step nearer him, and he starts doing something with the chain.\n\t\"Wait.\" You say, \"Where are w-\"\n\n\tYou are blind and deaf. The sounds of the crowd and the soft illumination of the indirect sunlight are replaced by silence and darkness.")
					spaced = 1
					poo=raw_input(">>")
					pos = 8
				else: print('\tThe man turns to you and looks at your eyepatch. He shakes his head. "The eyepatch be fine, but yer not ready yet, matey." He says, and turns back to look over the railing.')
			elif 'hat' in inv: print('''\tThe man turns to you and looks at your hat. He shakes his head. "The hat be fine, but yer not ready yet, matey." He says, and turns back to look over the railing.''')
			else: print("\t"+dialogues['7man2'])
		elif noun == "4person":
			if "4person" in path: print("\tAgain, nobody seems to notice you. They seem completely unaware of you and even, you almost imagine, of each other.")
			else:
				print("\tYou try to get someone's attention, but the crowd churns quickly, and nobody seems to notice you.")
				path.append("4person")
		else: print("\tWhat?")
	elif noun == '14man':
		if 'giverum' in path:
			if 'getkey' in path: print("\tHe is sleeping deeply on the table, enjoying your present.")
			elif 12 in path:
				print("\tYou poke him out of his sleep. \"You said something about encryption keys?\" You ask.\n\t\"Arr. So the best of the besht of ush could get the content firsht. It be worthlesh fer me now. Let that be a leshon fer ya, boy. When ya-\"\n\t\"I might be able to use it,\" You hint.\n\t\"What? Ah, aye, what the hell,\" He winks, \"Maybe ye ken teach 'em shomethin' about lookin' after they eldersh. I'll tell ya tha key we used.\" He leans forward conspiratorially.\n\t\"A.\"\n\tYou nod.\n\t\"B.\"\n\tNod.\n\t\"C.\"\n\tYou raise an eyebrow.\n\t\"D.\"\n\tYou open your mouth to question this, when you notice that you are holding a physical key.\n\t\"Where did this come from?\" You ask.\n\tThe old man frowns at you, confused. Then, with a bewildered condescension, \"You musht be new here,\" He says, \"Now go make shum mishchief,\" He grins, and turns his affections back toward the bottle.")
				inv.append("key")
				path.append("getkey")
			else: print("\t\"Usedtobesomebodymatey\" He burbles, three-quarters asleep.")
		elif 'rum' in inv:
			inv.remove("rum")
			print("\tYou sigh, and charitably hand over your bottle of rum. Receiving it, the man springs back to life as if given 20 years and 8 hours of sleep. \"Thish be good rum,\" He smiles, taking a quarter of the bottle in a sip. \"I ushed to get thish, back when thish old man was in tha game. Rum, shcreenersh, encryption keysh. It be a dangeroush game, now.\" He looks scared for a second, \"Too dangeroush fer thish old drunken landlubber. I losht a lot o' me friends to that...\"  He pauses, and continues to suck on the bottle, momentarily at peace with his fall from grace.")
			path.append("giverum")
			if 12 in path:
				print("\t\"Encryption keys?\" You ask.\n\t\"Arr. So the best of the besht of ush could get the content firsht. It be worthlesh fer me now. Let that be a leshon fer ya, boy. When ya-\"\n\t\"I might be able to use it,\" You hint.\n\t\"What? Ah, aye, what the hell,\" He winks, \"Maybe ye ken teach 'em shomethin' about lookin' after they eldersh. I'll tell ya tha key we used.\" He leans forward conspiratorially.\n\t\"A.\"\n\tYou nod.\n\t\"B.\"\n\tNod.\n\t\"C.\"\n\tYou raise an eyebrow.\n\t\"D.\"\n\tYou open your mouth to question this, when you notice that you are holding a physical key.\n\t\"Where did this come from?\" You ask.\n\tThe old man frowns at you, confused. Then, with a bewildered condescension, \"You musht be new here,\" He says, \"Now go make shum mishchief,\" He grins, and turns his affections back toward the bottle.")
				inv.append("key")
				path.append("getkey")
		else:
			print("\t\"Usedtobesomebodymatey\" He burbles, three-quarters asleep.")
	elif noun == '12man':
		if 'key' not in inv: print("\t\"How are ya, boy?\" He thunders, \"If ya've come fer somethin' I'm afraid yer out o' luck. What ya see is what I got.\"")
		else:
			print("\t\"Haha! That'll do nicely!\" He takes the key and inserts it into the radio. \"Aright scallywags,\" He says into the microphone, \"I got The Avengers in Bluray, and the first one two miles offshore gets it. Do it fer tha party!\" He turns off the machine and chuckles. \"That'll get 'em.\" He says, \"Here's a little somethin' fer yer help.\" He hands you a flashlight.")
			path.append("called")
			inv.append("flashlight")
	elif noun == '13hawker': print("\t\"Hallo There!\" You shout at a hawker, \"What are you selling?\"\n\t\"We aren't sellin' nothin', matey.\" He shouts back, \"We're supplyin'!\"")
	elif noun == '19man':
		if 'tropetalk' not in path:
			print("\t\"How did you get that thing in here?\" You ask groggily, pointing at the TV, \"The door's not-\"\n\tHe stands up and turns around. \"I really am sorry about knocking you out,\" He says, \"But you can't be too careful.\"\n\t\"Don't suppose I could go home now?\" You ask, more weary than hopeful or scared.\n\t\"Not yet,\" He says. \"We might need you.\"\n\t\"Me? Need me? That's more than unlikely.\"\n\t\"You're new here.\" He says, \"I can tell. You seem unusually... aware.\"\n\t\"Really. See that's weird because I've spend the last few...\" Hours? Days? \"...I've been feeling quite spectacularly unaware.\"\n\t\"Yeah. Don't worry about it?\" He says unsurely. He stops to think. \"Look, right now, unaware is good. Unaware is very good. You just need to trust me. I'll explain when it's done. What I need you to do, right now, is go out, and somehow get the power on outside. Then I need you to turn on the PA system. It will just play static, but that's enough. I'll be there as soon as you do that.\"\n\t\"But I have questions...\" You sigh.\n\t\"All in good time,\" He says urgently, \"But now is not a good time. Hurry.\"\n\n\tThe door swings open.")
			path.append('tropetalk')
		else: print("\t\"Hurry, man!\" He urges, \"We might not have much time.\"")
	elif noun == '24man':print("\tHe stares upward. You stand in silence for a while. \"Are you sure there's nothing we can do?\" You ask.\n\t\"Not yet,\" He says. \"It's not safe outside.\"")
	else: print("\tWhat?")

def wear():
	global inv
	global noun
	global path
	if noun == "inveyepatch":
		if "weareyepatch" not in path:
			print('\tYou fit the strap around your head, and manage to cover one eye with it.\n\n\t"Arr," You reassure yourself.')
			path.append("weareyepatch")
		else: print("\tYou're already wearing it.")
	elif noun == "invhat":
		print("\tYou're already wearing it.")
	else: print("\tWhat?")

def make():
	global inv
	global noun
	global splitentry
	if "hat" in splitentry:
		if "paper" in inv:
			print("\tYou don't know how to fold a hat, but you remember making a boat once. You fold a boat and casually slip it atop your head. You feel silly.")
			inv.append("hat")
			inv.remove("paper")
		else: print("\tYou don't have anything to fold a hat out of.")
	elif noun=="invpaper":
		newentry=raw_input("\n\tFold it into what? ")
		newsplit=newentry.split()
		if "hat" in newsplit:
			print("\tYou don't know how to fold a hat, but you remember making a boat once. You fold a boat and casually slip it atop your head. You feel silly.")
			inv.append("hat")
			inv.remove("paper")
		else: print("\tYou don't know how to fold that")
	elif "eyepatch" in splitentry:cut()
	else: print("\tWhat?")

def cut():
	global inv
	global noun
	global splitentry
	if noun in ['invscissors','invbag','invsack','invpaper']:
		if 'scissors' in inv:
			if 'sack' in inv:
				if 'bag' in splitentry:
					print("\tYou manage to cut a strip of fabric from your sack, in the process accidentally making a backpack out of the rest of it.")
					inv.append('eyepatch')
					inv.append('backpack')
					inv.remove('sack')
				elif 'sack' in splitentry:
					print("\tYou manage to cut a strip of fabric from your sack, in the process accidentally making a backpack out of the rest of it.")
					inv.append('eyepatch')
					inv.append('backpack')
					inv.remove('sack')
				elif 'paper' in splitentry: print ("\tYou cut the paper into two. Curiously, both are the same size as the original. You discard one sheet.")
				else: print("\tCut what?")
			else: print("\tCut what?")
		else: print("\tYou don't have anything to cut it with.")
	else: print("\tWhat?")

def take():
	global pos
	global noun
	global inv
	global splitentry
	if noun == "3paper":
		if 'paper' not in inv:
			print("\tYou pick up a sheet of paper, and put it in your sack.")
			inv.append("paper")
	elif noun == "invpaper": print("\tYou already have one of those. It seems silly to take another.")
	elif noun == "15rum":
		print("\tYou pick up the bottle of rum, and lay it lovingly in your backpack.")
		inv.append('rum')
	elif noun == "15spider":
		print("\tYou take a copy of The Amazing Spider Man. Perhaps it will come in handy later, you justify.")
		inv.append('Spider Man')
	elif noun == "20microphone":
		inv.append("microphone")
		print("\tYou reach through the mesh, and manage to pull out of it a professional broadcasting microphone.")
	elif noun == "1sack":move()
	elif noun == "invflashlight":
		print("\tIt's already in your sack")
	elif noun == "invfigure":
		if "battery" in splitentry:open()
		else:print("\tIt's already in your sack")
	elif noun == "1card":examine()
	elif splitentry[1]=="off":
		if noun in ["invhat","inveyepatch"]:
			if pos<19:
				print("\tYou ready yourself to remove it, but you fear the pirates' wrath. You leave it be for the meantime.")
			else:
				print("\tYou're not wearing it any more.")
	else: print("\tWhat?")

def plummet():
	if pos == 2:
		print("\tYou decide to file that away under \"if I survive.\"")
	else:print("\tWhat?")
	
def inventory():
	global inv
	articles=objects("articles")
	statement="\tYou have in your possession: "
	if len(inv)==0: statement="\tNothing here yet."
	for x in inv:
		statement += articles[x]
		statement += x
		if inv.index(x)<len(inv)-1:
			if inv.index(x)==len(inv)-2:statement += " and "
			else:statement += ", "
	print(statement+".")

def lookaround():
	global pos
	global surroundings
	if pos == 3:
		if 'look3' in path: print("\tThere are a staircase leading up to the first floor and a great mountain of paper here.")
		else:
			path.append('look3')
			print("\t"+surroundings[3])
	elif pos == 4:
		if 'look4' in path: print("\tYou are back at the top of the stairs to the floor below.")
		else:
			path.append('look4')
			print("\t"+surroundings[4])
	elif pos == 8:
		if 'look8' in path: print("\tYou are standing at the west end of a boardwalk. To the north crowd ships and to the south crowd bars and taverns.")
		else:
			print("\t"+surroundings[pos])
			path.append('look8')
	else: print("\t"+surroundings[pos])

def map():
	global pos
	global mapp
	print(mapp[pos])

def intro():
	global pos
	global intros
	print("\t"+intros[pos])

def examine():
	global pos
	global noun
	global path
	global descriptions
	if (noun == '16.1poster')and('movieposter' not in path):
		print("\tYou examine a poster for the movie Singin' in the Rain, and find a door behind it.")
		path.append('movieposter')
	elif noun == "1card":print("\t"+question())
	elif noun == "4poster":print("\t"+poster())
	elif noun == "16.1prop":print("\t"+prop())
	elif noun == "16.1poster":print("\t"+poster1())
	else: print("\t"+descriptions[noun])

def nonsense(): print("\tWhat?")

def whatdear(): print("\tLook at what, dear?")
	
def emptystr(): pass

def move():
	global pos
	global noun
	if noun == '1table': print("\tYou push the table as hard as you can, but it is immobile under the weight of the sack.")
	elif noun == '1.2table': print("\tYou try, but have been too weakened from moving it the first time.")
	elif noun == '1.3table': print("\tYou're standing on it.")
	elif noun=="1sack":
		pos=1.1
		inv.append("sack")
	elif noun=="1.1table": pos=1.2
	elif noun=='17button':
		noun = '17tap'
		use()
	elif noun=='21lever': use()
	else:go()

def open():
	global pos
	global inv
	global path
	global descriptions
	if noun=="1sack":
		pos=1.1
		inv.append("sack")
	elif pos == 2:
		if noun == "invsack":
			pos = 3
		else: print("\tYou decide to file that away under \"if I survive.\"")
	elif noun == "15chest":
		if 'rum' in inv: print("\tYou open the chest to find it stacked with hundreds of DVD copies of The Amazing Spider Man.")
		else: print("\tYou open the chest to find it stacked with hundreds of DVD copies of The Amazing Spider Man. In the same chest, labeled \"Director's Cut\" is a bottle of rum\"")
	elif noun == 'invfigure':
		if "openbatt" not in path:
			print("\tYou pop open Gordon's battery compartment, and take out a D battery.")
			inv.append("battery")
			path.append("openbatt")
			descriptions['invfigure']="Gordon is unenergetic in your backpack."
		else: print ("\tThere's nothing else inside Gordon.")
	else: print("\tThere's nothing openable around here like that")

def go():
	global pos
	global path
	global spaced
	global inv
	global descriptions
	if pos<8:#before the Pirate Bay
		if noun=="1.2table": pos=1.3
		elif noun=="1.3table":
			print("\tYou climb down from the table")
			spaced = 1
			pos=1.2
		elif noun in ['1window','1.1window','1.2window']:print("\tThe window is too high.")
		elif noun=="1.3window": pos=2
		elif noun=='3stairs': pos=4
		elif noun=='4stairs':
			print("\tYou go down the stairs.")
			spaced = 1
			pos=3
		elif noun=="4cw": pos=5
		elif noun=="5cw": pos=6
		elif noun=="6cw": pos=7
		elif noun=="7cw": pos=4
		elif noun=="4ws": pos=7
		elif noun=="7ws": pos=6
		elif noun=="6ws": pos=5
		elif noun=="5ws": pos=4
		elif noun=="6stairs":print('''\tAs you step toward the first stair, the little man calls out from just widdershins of you. "I'm sorry, you can't go up there!", He shouts. You query this with an eyebrow. He reassures you, "That's semi-protected, I'm afraid!"\n\tWhen in Rome, you mutter and step away, Or wherever...''')
		else: print("\tI don't understand where you're trying to go.")
	elif pos<16:
		if noun=="8east": pos=9
		elif noun=="8w":print("\tA feeling of dread pours into your bones as you look west. You couldn't possibly bring yourself to go that way.")
		elif noun in ["8south",'8bar']:
			pos=14
			inv.append("glass")
		elif noun=="9west": pos=8
		elif noun=="9east": pos=10
		elif noun=="9north":
			if 'party' in path: print("\tThe Swedish gentleman smiles at you from the pirate yacht. \"Ve a hea olvays!\" He shouts, possibly in English")
			else:
				print("\tYou walk onto the deck. A tall, blonde man approaches you and says, \"Vi har en fest! Vill du vara med?\"\n\tYou blink.\n\t\"I'm sorry?\" You ask.\n\t\"Ve are having a party!\" He says, \"You vill join us, ja?\"\n\t\"Look,\" you say, \"I would very much like to know what is going on around here.\"\n\t\"Ve are doing very vell at ze moment. Zey told us ve vere not allowed in ze UK, but ve get zere anyvay.\"\n\t\"You're about as helpful as the rest of them,\" You resign.\n\t\"Senk you! Ve see you around, ja. You are velcome to join, but you must dress not so... like zat.\"\n\t\"Ja, ja.\" You say, and step back onto the boardwalk. You feel self-conscious.")
				path.append('party')
		elif noun=="9south": print("\tYou try to open the door but find it locked. Nailed to the door is a note reading \"To pass this door please complete one of the following surveys: There are 0 surveys available.\"")
		elif noun=="10west": pos=9
		elif noun=="10east": pos=11
		elif noun=="10south": pos=13
		elif noun=="11west": pos=10
		elif noun=="11e":print("\tA feeling of dread pours into your bones as you look east. You couldn't possibly bring yourself to go that way.")
		elif noun in ["11south",'11house']: pos=12
		elif noun=="12north": pos=11
		elif noun=="13north": pos=10
		elif noun=="13door":
			if 'key' in inv:
				if "selfportrait" not in path:
					print("\tYou fit the key into the door and open it. A curly-haired boy sits in a swiveling chair in the middle, looking at a few dozen monitors organized into a grid over one wall.\n\t\"Hi!\" He says. \"My name's Jeffrey. I made this game. I hope you like it so far. I'm sorry if you tried getting in here without decrypting it first. Junk data can be... disturbing in its pataphysical form.\"\n\t\"I don't suppose you're going to tell me what's going on yet?\" You ask.\n\t\"Well, don't get your hopes up.\" He says, \"You're already between a third and halfway through it, though. This was really just a summer/getting over a girl project that I made in my spare time. Eventually it became quite important to me, became the glue that held the pieces of my day together and filled in the cracks through which I could see slivers of the black and indifferent void. Unfortunately, even in my loneliness, I still had things I had to do, so it didn't end up as long as I had hoped. Still, like a filleted fish, I tried to include the best bits for this half-hour-or-two. If I get a good enough response about this one, I will definitely do something else, though. Bye!.\"\n\n\tYou blink, and find yourself back at the market, and nothing but wall where the door was.")
					path.append("selfportrait")
					descriptions['13e']="You see the outside of a tavern. A sign nailed to it reads: \"Specials today: Beer.\"."
				else:print("\tThere is no door here.")
			else:
				print("\tYou open the door, and choke in astonisment. The inside of the room appears to consist of cubes of material floating in thin air. Bright colors and jagged edges seem to physically jerk around, sometimes jumping from one location to another without occupying the intervening space. You shut the door in shock.")
		elif noun=="14north": pos=8
		elif noun=="15stairs":print("\tYou climb the stairs, but the trap door is covered by something heavy above. It doesn't budge.")
		elif noun in ['11hole','11ship']:
			if 'called' not in path:
				pos=15
			else:
				pos=16
		elif noun=='15out': pos=11
		else: print("\tI don't understand where you're trying to go.")
	elif pos<19:
		if pos==16:
			if 'figure' not in inv:
				print("\tYou try to walk, and almost trip over something. You pick it up and find it to be a Gordon Gekko action figure. It squeaks, \"Let's trade derivatives!\"")
				inv.append("figure")
		elif noun=='16.1door':
			if 'movieposter' in path:
				pos = 17
			else: print("\tYou don't see a way out of this basement of lost miscellania.")
		elif noun in ['17door','17out']:
			if 'splashed' in path:
				pos = 18
			else:
				print("\tThe door is locked from the outside.")
		elif noun=='18door': pos=17
		elif noun in ['18cw','18ws']:
			print("\tYou walk, and see a door handle jiggle next to you. A skinny young man walks out. \"Boy, that was good.\" He says to you. \"You know The Matrix is a perfect example of the hero's journey? It was all defined in The Hero with a Thousand Faces by Joseph Campbell.\"\n\tYou nod, strangely bewitched by this little man.\n\t\"You see,\" He continues, \"After the Call to Adventure, he goes from practically an Ridiculously Average Guy to a Badass Longcoat after about 20 minutes with the Chooser of the One, who I suppose could be considered the Supernatural Aid, though I prefer to think of his first successful alterations of reality as the Supernatural Aid.\n\tYou have no idea what he's talking about, but somehow you can't look away.\n\t\"And they're playing Alice in Wonderland next, which is great because it's really not a hero's journey. It's just a girl being jerked from one place to another. It's a great Trope Namer, though, and the Matrix uses Down the Rabbit Hole, even though for a change the lead actually takes initiative. That's the bit with the pills.\"\n\t\"Jerked from one place to another...\" You murmur empathetically.\n\tYou are so enchanted by his gibberish that you haven't noticed the little man leading you into a small, bare, dark room by the side of the corridor, and closing the door.\n\t\"Just to be safe, you know,\" He says, \"Sorry about this.\" You notice your flashlight in his hand.")
			poo=raw_input("")
			print("\tVague images float around your head.\n\tA dog wearing glasses asking \"Why is it hard to do calculus with black people? Because they're hard to integrate and they're hard to differentiate.\"\n\tA raccoon telling you, \"I have two pieces of string, one untied, and one not.\"\n\tA boy with orange hair squinting and saying, \"Not sure if dream or distorted memory.\"")
			splitentry=''
			inv.remove("eyepatch")
			inv.remove("hat")
			inv.remove("flashlight")
			while ('wake' not in splitentry) and ('awake' not in splitentry):
				print("\n\tYou are asleep.")
				splitentry=raw_input(">>").split()
			spaced = 1
			pos=19
		else: print("\t I don't understand where you're trying to go.")
	elif noun == '19out':
		if 'tropetalk' in path:
			pos=20
		else: print("\tThe door is locked.")
	elif noun == '20cage':print("\tThe cage is locked, but you can push your hands in a little ways.")
	elif noun == '20cw':pos=21
	elif noun == '21cw':pos=22
	elif noun == '22cw':pos=23
	elif noun == '21ws':pos=20
	elif noun == '22ws':pos=21
	elif noun == '23ws':pos=22
	elif noun == '20w' :pos=19
	elif noun == '23booth':pos=24
	elif noun == '24out':pos=23
	else: print("\t I don't understand where you're trying to go.")

###########
#Verbs End#
###########


#Parses user input
def parse():
	global verb
	global noun
	global pos
	global splitentry
	global nouns
	global traversable
	global untraversable
	global inv
	noun = "unrecognized"		#This is changed iff an entered noun is recognized
	entry=raw_input(">>")		#The text prompt
	splitentry=entry.split()
	if splitentry==[]:splitentry=['emptystr']
	if splitentry[0]=="nikolaisgreat":	#Cheat code for my friend Nikola
		pos=8
		inv.append("scissors")
		inv.append("pen")
		inv.append("eyepatch")
		inv.append("backpack")
		inv.append("hat")
		print("\tKittens and rainbows! You've cheated!")
	for x in range(len(splitentry)): splitentry[x]=splitentry[x].lower()#Lowercase
	for x in range(len(splitentry)):
		if str(pos)+splitentry[x] in nouns:
			noun = nouns[str(pos)+splitentry[x]]
			splitentry[x] = nouns[str(pos)+splitentry[x]].replace(str(pos),'')
		if "inv"+splitentry[x] in nouns:
			if nouns["inv"+splitentry[x]].replace('inv','') in inv:
				noun = nouns["inv"+splitentry[x]]
				splitentry[x] = nouns['inv'+splitentry[x]].replace('inv','')
	if splitentry[0]=='get':#Get
		if len(splitentry)==1:splitentry=['nonsense']
		elif splitentry[1] in ["on","off","to","over","onto","out"]: splitentry[0]="go"
		else: splitentry[0]="take"
	if splitentry[0]=='look':#Look
		if len(splitentry)==1: splitentry=['lookaround']
		elif splitentry[1]=='around':
			splitentry.pop(1)
			splitentry[0]='lookaround'
		elif splitentry[1] in ['at','over']:
			if noun != "unrecognized": splitentry[0]='examine'
			else: splitentry[0]='whatdear'
		elif noun != "unrecognized": splitentry[0]='examine'
		else: splitentry=['nonsense']
	if splitentry[0] not in verbs: splitentry=["nonsense"]
	verb=verbs[splitentry[0]]
	if noun in traversable:
		if verb not in [examine,use,lookaround,inventory,talk,make,wear]: verb = go
	elif noun in untraversable:
		if verb not in [examine,use,lookaround,inventory,talk,make,wear]: verb = gowhat
	if pos == 2:
		if verb not in [open,inventory,nonsense,emptystr,use,help,map]: verb = plummet#use
	if verb in transitive:
		if noun=="unrecognized": verb=nonsense

	
verbs = {				#Maps commands to functions
	'lookaround':lookaround,
	'nonsense':	nonsense,
	'examine':	examine,
	'view':		examine,
	'inspect':	examine,
	'scrutinize':examine,
	'study':	examine,
	'whatdear':	whatdear,
	'emptystr':	emptystr,
	'empty':	open,
	'open':		open,
	'push':		move,
	'pull':		move,
	'move':		move,
	'lift':		move,
	'turn':		move,
	'go':		go,
	'climb':	go,
	'clamber':	go,
	'walk':		go,
	'enter':	go,
	'mount':	go,
	'talk':		talk,
	'i':		inventory,
	'inventory':inventory,
	'inv':		inventory,
	'backpack':	inventory,
	'take':		take,
	'pick':		take,
	'plummet':	plummet,
	'cut':		cut,
	'fold':		make,
	'make':		make,
	'wear':		wear,
	'don':		wear,
	'gowhat':	gowhat,
	'use':		use,
	'place':	use,
	'insert':	use,
	'put'	:	use,
	'splash':	use,
	'plug':		plug,
	'h':		help,
	'help':		help,
	'm':		map,
	'map':		map,
	'sit':		sit
}

#Verbs that need objects
transitive=[examine,open,cut,talk,take]

#This gets called until you win
def step():
	global spaced
	global pos
	global path
	global verb
	global noun
	spaced = 0				#this gets set to 1 if the user only entered spaces
	path.append(pos)
	poscache=pos
	parse()
	if verb != emptystr:
		print("\n")
	verb()
	if poscache != pos:			#if you've moved
		if spaced == 1: print("\n")	
		if pos in path: lookaround()	#if you've been here before, give a short description
		else: intro()			#if you're in a new place, give a longer description



######################
#The game starts here#
######################



print "\tYou arrive at a suspicious website, with a boldly self-referential prompt. What do you do?"
blahblah=raw_input(">>")
print "\n\tNo sooner do you type these words than the room surrounding you begins to come out of focus. The screen of your monitor seems to grow. Instinctively, you lean back as you feel it draw closer. There is a brilliant FLASH!\n\n\tYou are in a mostly empty room."


#Iterates until you win
while winconditions=='notmet':
	step();


#You win!
print('''You hand him the microphone. "I have an idea," You say, "Start talking."
	"About what?" He asks.
	"About anything."
	"Um. In 1974, Doubleday published Tales of the Black Widowers, a collection of mystery stories by Isaac Asimov, previously best known for science fiction..." The words blare out of the PA speakers in bursting, cracking loudness.
	You look upwards as he talks. You think you can see the cloud sinking a little. Far above you, countless thousands of people stop reading questions, and strain their ears to hear the speakers from below.
	"-Return of the Black Widowers was published posthumously. During his lifetime, Asimov was known for insisting on writing the introductions to his own books, however, this publication featured an introduction by Harlan Ellison, who-" He pauses, seeing the cloud slow down and dip slightly in the sky.
	"Um- was contracted by Warner Brothers to develop a script based on I, Robot, one of Asimov's most well-known and celebrated collections of short stories. The script is entirely unrelated to the 2004 movie starring Will-"
	You stare out of the plexiglass window as one end of the cloud touches onto the field. As it touches the grass it seems to clear, and in the vapor, you can make out the silhouettes of people. The cloud continues to sink, seemingly into the ground, leaving more silhouettes on the green. Thousands of them.
	The little man watches speechlessly. He finally starts, "If that's what brought you here." He says, "It must have found a way to reach your world."
	"The real world." You say.
	"We make that distinction too," He says, "But that's what we call this one. Anyway, the spell is breaking, I think. Time to tap your heels together."
	"What?" You ask too late. The announcer's booth is starting to go fuzzy.

	You are back at your computer. Your hands rest on your keyboard. You glance away from your screen. Haven't I always been here? You think. You're not sure what to do with yourself.

	You decide to drop some coin in the world domination fund, and go for a walk.''')

#Prevents the script from quitting
while True:
	foo=raw_input("")
