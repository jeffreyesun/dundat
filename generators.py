from random import random
def question():
	string=''
	subjects=["hat","budgie","pineapple","shirt","celebrity","church","ship","fruit","vase","lamp","clock","belt","banana","book","chair"]
	scenes=["landscape","dining room table","writing desk","forest","harbor","statue of lincoln","park","highrise apartment complex"]
	operators=["divide","multiply","add","subtract"]
	randomnum=random()
	if randomnum<0.4:
		string="You pick up a single card from the thousands. It asks you to "+operators[int(random()*4)]+" "+str(int(random()*100))+" and "+str(int(random()*100))+"."
	elif randomnum<0.7:
		string="You pick up a single card from the thousands. The card has the picture of a "+scenes[int(random()*8)]+" on it. It asks you if the picture contains a "+subjects[(int(random()*15))]+". "
	if randomnum>=0.7:
		string="You pick up a single card from the thousands. The card asks you to identify the variety of "+subjects[int(random()*15)]+" in a picture provided."
	return(string)
def poster():
	string = ''
	pre=['North','South','East','West','future','ancient','modern','postmodern','the football club of','a post-neo-rock band from','a funk-grunge collective from','the Armenian population of','the architecture of','a notable philosopher from','the adult entertainment industry of']
	post=['America','Ethiopia','Chicago','Prague','Vienna','Mostar','Newcastle','Finland','Hong Kong','Taiwan','Vietnam','Sydney','Algeria','Manhattan','Pakistan','South Dakota']
	pre=pre[int(random()*15)]
	post=post[int(random()*16)]
	string="You approach a poster and see that it is a collection of scraps of paper and notes with information about "+pre+" "+post+' pasted together onto a large sheet of paper. People are continually pasting on new notes and pulling off old ones to throw them onto the great pile in the center.'
	return(string)
def prop():
	string = ''
	pre=['fake beard','prosthetic nose','hat','glove','cup','window frame','car door','stuffed falcon','model spaceship','newspaper','toothbrush','telephone','wax papaya','inhaler','box of tissues']
	post=['Firefly','the TV show Dexter','The Shawshank Redemption','the movie Romeo+Juliet','The TV show Soap','The movie Sexmission','Driving Miss Daisy','The movie Sideways','the movie Sucker Punch','the movie Some Like it Hot','The TV show Jupiter Moon','American Pie','Doctor Who','Arrested Development']
	string="You see a "+pre[int(random()*15)]+" that was used in "+post[int(random()*14)]+'.'
	return(string)

def poster1():
	shows =['Firefly','the TV show Dexter','The Shawshank Redemption','the movie Romeo+Juliet','The TV show Soap','The movie Sexmission','Driving Miss Daisy','The movie Sideways','the movie Sucker Punch','the movie Some Like it Hot','The TV show Jupiter Moon','American Pie','Doctor Who','Arrested Development']
	string="You see a poster for "+shows[int(random()*14)]+'.'
	return(string)