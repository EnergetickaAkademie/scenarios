from Enak import *

building_consumptions = {
	#these numbers define the (day, night) consumption of the specific buildings
	Building.CITY_CENTER_A: (575, 200),
	Building.CITY_CENTER_B: (600, 200),
	Building.CITY_CENTER_C: (620, 200),
	Building.CITY_CENTER_D: (550, 200),
	Building.CITY_CENTER_E: (625, 200),
	Building.CITY_CENTER_F: (550, 200),
	
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

	#FÁZE 1 - prezentace
	sr = SlideRange(1, 5) #starting index is 1
	script.addRound(sr)
	#same for the other teams

	#FÁZE 2 - umístění dvou uhelek a jedné budovy, jednoduché vyrovnání soustavy
	d = Day()
	script.addRound(d)

	n = Night()
	script.addRound(n)

	#FÁZE 3 - spotřeba města roste o 60MW ve dne, o 120MW v noci
	script.changeBuildingsConsumptions(CITY_CENTERS, (60, 120))

	d = Day()
	script.addRound(d)

	n = Night()
	script.addRound(n)



	n = Windy(Night())
	script.addRound(n)

	sl = Slide(6)
	script.addRound(sl)
	script.changeBuildingConsumption(Building.CITY_CENTER, 750, 300)

	d = Sunny(Windy(Day("Koná se mistrovství světa v ledním hokeji")))
	d.outage(Source.GAS) #there is a gas outage in this round
	d.addBuildingModifier(Building.STADIUM, 100)  #increase stadium consumption because of a specific event
	script.addRound(d)

	return script

if __name__ == "__main__":
	s = getScript()