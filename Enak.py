#create date types enum

from enum import Enum
from typing import Optional, override, List

class ReadableEnum(Enum):
    def __str__(self):
        return self.name.replace('_', ' ').title()

class Source(ReadableEnum):
	PHOTOVOLTAIC = 1
	WIND = 2
	NUCLEAR = 3
	GAS = 4
	HYDRO = 5
	HYDRO_STORAGE = 6
	COAL = 7
	BATTERY = 8

class RoundType(ReadableEnum):
	DAY = 1
	NIGHT = 2
	SLIDE = 3 #show a presentation slide
	SLIDE_RANGE = 4

class WeatherType(ReadableEnum):
	SUNNY = 1
	RAINY = 2
	CLOUDY = 3
	SNOWY = 4
	FOGGY = 5
	WINDY = 6
	CALM = 7
	BREEZY = 8
	PARTLY_CLOUDY = 9

class Building(ReadableEnum):
	CITY_CENTER = 1
	CITY_CENTER_A = 2
	CITY_CENTER_B = 3
	CITY_CENTER_C = 4
	CITY_CENTER_D = 5
	CITY_CENTER_E = 6
	CITY_CENTER_F = 7
	FACTORY = 8
	STADIUM = 9
	HOSPITAL = 10
	UNIVERSITY = 11
	AIRPORT = 12
	SHOPPING_MALL = 13
	TECHNOLOGY_CENTER = 14

	FARM = 15
	LIVING_QUARTER_SMALL = 16
	LIVING_QUARTER_LARGE = 17
	SCHOOL = 18

CITY_CENTERS = [Building.CITY_CENTER_A, Building.CITY_CENTER_B, Building.CITY_CENTER_C,
				Building.CITY_CENTER_D, Building.CITY_CENTER_E, Building.CITY_CENTER_F]

class Round:
	def __init__(self, comment: Optional[str] = None):
		self.type = None
		self.comment = comment

	def getRoundType(self) -> RoundType:
		return self.type

	def setRoundType(self, round_type: RoundType):
		self.type = round_type

	def getType(self) -> RoundType:
		return self.type
		
	def __str__(self):
		return f"Round(type={self.type}, comment={self.comment})"

class PlayRound(Round):
	def __init__(self, comment: Optional[str] = None):
		super().__init__(comment)
		self.production_coefficients = {source: 0.0 for source in Source}
		self.production_changes = set()

		# production modifiers are added to the default building consumption defined in the script
		# eg. if a building of type BuildingType.FACTORY has a default production of 1000 (MW)
		# a value of -200 here would make the consumption 800 (MW)
		self.building_modifiers = {}

		for building in Building:
			self.building_modifiers[building] = 0.0

		self.weather = []

	def setProductionCoefficients(self, coefficients: dict):
		self.production_coefficients = coefficients
		print(f"setting production coefficients")

	def addWeather(self, weather: WeatherType):
		if weather == WeatherType.SUNNY:
			self.weather.append(WeatherType.SUNNY)
			self.setProductionCoefficient(Source.PHOTOVOLTAIC, 1.0)

		elif weather == WeatherType.PARTLY_CLOUDY:
			self.weather.append(WeatherType.PARTLY_CLOUDY)
			self.setProductionCoefficient(Source.PHOTOVOLTAIC, 0.5)
		
		elif weather == WeatherType.CLOUDY:
			self.weather.append(WeatherType.CLOUDY)
			self.setProductionCoefficient(Source.PHOTOVOLTAIC, 0.0)
		
		elif weather == WeatherType.RAINY:
			self.weather.append(WeatherType.RAINY)
		
		elif weather == WeatherType.SNOWY:
			self.weather.append(WeatherType.SNOWY)
			self.setProductionCoefficient(Source.PHOTOVOLTAIC, 0.0)
			self.setProductionCoefficient(Source.BATTERY, 0.5)

		elif weather == WeatherType.FOGGY:
			self.weather.append(WeatherType.FOGGY)

		elif weather == WeatherType.CALM:
			self.weather.append(WeatherType.CALM)
			self.setProductionCoefficient(Source.WIND, 0.0)

		elif weather == WeatherType.BREEZY:
			self.weather.append(WeatherType.BREEZY)
			self.setProductionCoefficient(Source.WIND, 0.5)

		elif weather == WeatherType.WINDY:
			self.weather.append(WeatherType.WINDY)
			self.setProductionCoefficient(Source.WIND, 1.0)

	def getWeather(self) -> Optional[List[WeatherType]]:
		return self.weather

	def setRoundType(self, round_type: RoundType):
		self.type = round_type
		# if round_type == RoundType.DAY:
		# 	self.setPVCoefficient(0.8) # by default its not really sunny, so we set to some smaller value than exact 1.0

		# elif round_type == RoundType.NIGHT:
		# 	self.setPVCoefficient(0.0)

	def setProductionCoefficient(self, source: Source, coefficient: float):
		if source in self.production_coefficients:
			self.production_coefficients[source] = coefficient
			self.production_changes.add(source)
		else:
			print(f"Warning: Source '{source}' not found in production coefficients.")

	def outage(self, source: Source):
		if source in self.production_coefficients:
			self.setProductionCoefficient(source, 0.0)
		else:
			raise ValueError(f"Unknown energy source: {source}")
		
	def addBuildingModifier(self, building: Building, modifier: float):
		if building in self.building_modifiers:
			self.building_modifiers[building] += modifier
		else:
			raise ValueError(f"Unknown building type: {building}")
		
	def addBuildingModifiers(self, buildings: List[Building], modifier: float):
		for building in buildings:
			self.addBuildingModifier(building, modifier)

	def __str__(self):

		res = f"PlayRound"
		res += f"\n{self.comment if self.comment else ''},"
		res += f"\n{self.type.name},"

		res += "\n--weather--"
		
		for w in self.weather:
			res += f"\n{w.name}"

		res += "\n--production coefficients--"

		for key, value in self.production_coefficients.items():
			res += f"\n{key}={value}"

		#print all of the building modifiers
		res += "\n--building modifiers--"
		for key, value in self.building_modifiers.items():
			res += f"\n{key}={value}"

		return res
		#return f"Round(type={self.type}, weather={self.weather}, production_coefficients={self.production_coefficients}, comment={self.comment})"

class Day(): #create a day builder class
	def __init__(self):
		self.round = PlayRound()
		self.round.setRoundType(RoundType.DAY)

	def sunny(self):
		self.round.addWeather(WeatherType.SUNNY)
		return self
	
	def windy(self):
		self.round.addWeather(WeatherType.WINDY)
		return self
	
	def rainy(self):
		self.round.addWeather(WeatherType.RAINY)
		return self
	
	def cloudy(self):
		self.round.addWeather(WeatherType.CLOUDY)
		return self
	
	def foggy(self):
		self.round.addWeather(WeatherType.FOGGY)
		return self
	
	def snowy(self):
		self.round.addWeather(WeatherType.SNOWY)
		return self
	
	def calm(self):
		self.round.addWeather(WeatherType.CALM)
		return self
	
	def partly_cloudy(self):
		self.round.addWeather(WeatherType.PARTLY_CLOUDY)
		return self
	
	def breezy(self):
		self.round.addWeather(WeatherType.BREEZY)
		return self

	def setCoefficient(self, source: Source, coefficient: float):
		self.round.setProductionCoefficient(source, coefficient)
		return self
	
	def outage(self, source: Source):
		self.round.outage(source)
		return self
	
	def addBuildingModifier(self, building: Building, modifier: float):
		self.round.addBuildingModifier(building, modifier)
		return self
	
	def addBuildingModifiers(self, buildings: List[Building], modifier: float):
		self.round.addBuildingModifiers(buildings, modifier)
		return self

	def build(self) -> PlayRound:
		return self.round

class Night():
	def __init__(self):
		self.round = PlayRound()
		self.round.setRoundType(RoundType.NIGHT)
	
	def windy(self):
		self.round.addWeather(WeatherType.WINDY)
		return self
	
	def rainy(self):
		self.round.addWeather(WeatherType.RAINY)
		return self
	
	def cloudy(self):
		self.round.addWeather(WeatherType.CLOUDY)
		return self
	
	def foggy(self):
		self.round.addWeather(WeatherType.FOGGY)
		return self
	
	def snowy(self):
		self.round.addWeather(WeatherType.SNOWY)
		return self
	
	def calm(self):
		self.round.addWeather(WeatherType.CALM)
		return self
	
	def partly_cloudy(self):
		self.round.addWeather(WeatherType.PARTLY_CLOUDY)
		return self
	
	def breezy(self):
		self.round.addWeather(WeatherType.BREEZY)
		return self
	
	def setCoefficient(self, source: Source, coefficient: float):
		self.round.setProductionCoefficient(source, coefficient)
		return self
	
	def outage(self, source: Source):
		self.round.outage(source)
		return self
	
	def addBuildingModifier(self, building: Building, modifier: float):
		self.round.addBuildingModifier(building, modifier)
		return self
	
	def addBuildingModifiers(self, buildings: List[Building], modifier: float):
		self.round.addBuildingModifiers(buildings, modifier)
		return self
	
	def build(self) -> PlayRound:
		return self.round

class Slide(Round):
	def __init__(self, slide_number, comment: Optional[str] = None):
		super().__init__(comment)
		self.setRoundType(RoundType.SLIDE)
		self.slide_number = slide_number

	def setSlideNumber(self, slide_number: int):
		self.slide_number = slide_number

	def getSlideNumber(self) -> Optional[int]:
		return self.slide_number
	
	def __str__(self):
		return f"Slide(slide_number={self.slide_number})"
	
class SlideRange(Round):
	def __init__(self, start: int, end: int, comment: Optional[str] = None):
		super().__init__(comment)
		self.setRoundType(RoundType.SLIDE_RANGE)
		self.start = start
		self.end = end

	def getStart(self) -> int:
		return self.start
	
	def getEnd(self) -> int:
		return self.end
	
	def getRange(self) -> tuple:
		return (self.start, self.end)
	
	def setRange(self, start: int, end: int):
		self.start = start
		self.end = end

	def __str__(self):
		return f"SlideRange(start={self.start}, end={self.end})"

class Script:
	def __init__(self, building_consumptions: dict):
		self.rounds : List[Round] = []
		self.building_changes = {}
		self.pdf : str = None
		self.building_consumptions = building_consumptions.copy()
		self.current_round_index = 0
		self.master_production_coefficients = {source: 0.0 for source in Source}

	def changeMasterProductionCoefficient(self, source: Source, coefficient: float):
		self.master_production_coefficients[source] = coefficient

	#syntactic sugar for setting production coefficient to 1.0
	def allowProduction(self, source: Source):
		self.changeMasterProductionCoefficient(source, 1.0)

	def addRound(self, rnd: Round):
		"""Adds a round to the script and applies current production coefficients."""
		if isinstance(rnd, PlayRound):
			#multiply each of the PlayRound production coefficients by the master production coefficient in the current round
			#if the master coefficient does not exist, is is inherently the last set value

			#if the source master production coefficient does not exist in this round, copy the value from the last round
			print(f"{rnd.getRoundType()} round {len(self.rounds)}")
			print()
			for source in rnd.production_coefficients:
				print(f"{source} round: {rnd.production_coefficients[source]}, master: {self.master_production_coefficients[source]}", end="")

				#if the value was not explicitly set in the round, force a change
				if source not in rnd.production_changes:
					rnd.production_coefficients[source] = self.master_production_coefficients[source]

				#if it was set, multiply it by the current scenario value
				else:
					rnd.production_coefficients[source] *= self.master_production_coefficients[source]

				print(f", result: {rnd.production_coefficients[source]} set: {'T' if source in rnd.production_changes else 'F'}")

		self.rounds.append(rnd)

	def getRounds(self):
		return self.rounds
	
	def setPDF(self, pdf):
		self.pdf = pdf

	def getPDF(self):
		return self.pdf
	
	def changeBuildingConsumption(self, building: Building, day_consumption_increase: int, night_consumption_increase: int):
		#change the building consumption for the given building type by increasing the consumption by a select amount
		if building in self.building_consumptions:
			if self.building_changes.get(len(self.rounds) - 1) is None:
				self.building_changes[len(self.rounds) - 1] = []

			self.building_changes[len(self.rounds) - 1].append((building, day_consumption_increase, night_consumption_increase))

	#change consumption values for multiple buildings with the same value increase
	# a list of buildings will be passed with a value increase tuple for night and day
	# calls changeConsumption for each building, with the original value + the value increase
	def changeBuildingsConsumptions(self, buildings: List[Building], value_increase: tuple):
		for building in buildings:
			if building in self.building_consumptions:
				day_increase, night_increase = value_increase
				self.changeBuildingConsumption(building, day_increase, night_increase)


	def step(self) -> bool:
		if self.rounds:
			if self.current_round_index < len(self.rounds):
				rnd = self.rounds[self.current_round_index]
				self.current_round_index += 1
				
				#update the building_consumptions if there are any building_changes for the current round (add the value from the same Building type)
				if self.building_changes.get(self.current_round_index - 1):
					for change in self.building_changes[self.current_round_index - 1]:
						building, day_consumption, night_consumption = change
						old_day, old_night = self.building_consumptions[building]

						self.building_consumptions[building] = (old_day + day_consumption, old_night + night_consumption)
				
				return True
			
		return False
		
	def getCurrentProductionCoefficients(self) -> dict:
		if self.rounds and self.current_round_index > 0:
			if isinstance(self.rounds[self.current_round_index - 1], PlayRound):
				return self.rounds[self.current_round_index - 1].production_coefficients
			
		return {}

	def getCurrentBuildingConsumption(self, building: Building) -> Optional[tuple]:
		#get the current building consumption with the modifiers from the current PlayRound
		if self.rounds and self.current_round_index > 0:
			if isinstance(self.rounds[self.current_round_index - 1], PlayRound):
				# get the base consumption
				base_consumption = self.building_consumptions.get(building, None)
				if base_consumption is not None:
					# apply the modifier from the current round
					modifier = self.rounds[self.current_round_index - 1].building_modifiers.get(building, 0.0)
					production = (base_consumption[0] + modifier, base_consumption[1] + modifier)

					if self.rounds[self.current_round_index - 1].getRoundType() == RoundType.DAY:
						return production[0]
					
					elif self.rounds[self.current_round_index - 1].getRoundType() == RoundType.NIGHT:
						return production[1]

		return 0.0

	def getCurrentWeather(self) -> Optional[List[WeatherType]]:
		if not isinstance(self.rounds[self.current_round_index - 1], PlayRound):
			print(f"Warning: Current round {self.getCurrentRoundType()} is not a PlayRound, cannot get weather.")
			return None

		if self.rounds and self.current_round_index > 0:
			return self.rounds[self.current_round_index - 1].getWeather()
		
		else:
			print("Warning: No current round available, cannot get current weather.")

		return None
	
	def getCurrentRoundType(self) -> Optional[Round]:
		#return if current round is day, night, or slide (return the type)
		
		if self.rounds and self.current_round_index > 0:
			return self.rounds[self.current_round_index - 1].getType()

		else:
			print("Warning: No current round available, cannot get current round type.")

		return None

	def getCurrentRound(self) -> Optional[Round]:

		if self.rounds and self.current_round_index > 0:
			return self.rounds[self.current_round_index - 1]
		
		else:
			print("Warning: No current round available, cannot get current round.")

		return None
	
	def getCurrentSlideNumber(self) -> Optional[int]:
		if not isinstance(self.rounds[self.current_round_index - 1], Slide):
			print(f"Warning: Current round {self.getCurrentRoundType()} is not a Slide, cannot get slide number.")
			return None
		
		if self.rounds and self.current_round_index > 0:
			return self.rounds[self.current_round_index - 1].getSlideNumber()

		else:
			print("Warning: No current round available, cannot get slide number.")

		return None