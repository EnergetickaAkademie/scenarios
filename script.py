from Enak import *

def getScript():
	script = Script()

	script.setPDF("prednaska.pdf")

	#the presentation beginning
	sr = SlideRange(1, 5) #starting index is 1
	script.addRound(sr)

	d = Sunny(Windy(Day()))
	script.addRound(d)

	n = Windy(Night())
	script.addRound(n)

	sl = Slide(1)
	script.addRound(sl)

	return script

if __name__ == "__main__":
	s = getScript()