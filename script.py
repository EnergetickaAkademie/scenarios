from Enak import *

building_consumptions = {
	#these numbers define the (day, night) consumption of the specific buildings
	Building.CITY_CENTER: (650, 200),
	Building.FACTORY: (400, 400),
	Building.STADIUM: (250, 400),
	Building.HOSPITAL: (350, 250),
	Building.UNIVERSITY: (400, 200),
	Building.AIRPORT: (500, 400),
	Building.SHOPPING_MALL: (350, 200),
	Building.TECHNOLOGY_CENTER: (300, 250),
	Building.FARM: (80, 40),
	Building.LIVING_QUARTER_SMALL: (70, 40),
	Building.LIVING_QUARTER_LARGE: (100, 60),
	Building.SCHOOL: (80, 30)
}

def getScript():
	script = Script(building_consumptions)

	script.setPDF("prednaska.pdf")

	#the presentation beginning
	sr = SlideRange(1, 5) #starting index is 1
	script.addRound(sr)

	d = Sunny(Windy(Day()))
	script.addRound(d)

	n = Windy(Night())
	script.addRound(n)

	sl = Slide(6)
	script.addRound(sl)
	script.changeConsupmtion(Building.CITY_CENTER, 750, 300)

	d = Sunny(Windy(Day("Koná se mistrovství světa v ledním hokeji")))
	d.outage(Source.GAS) #there is a gas outage in this round
	d.addBuildingModifier(Building.STADIUM, 100)  #increase stadium consumption because of a specific event
	script.addRound(d)

	return script

if __name__ == "__main__":
	s = getScript()