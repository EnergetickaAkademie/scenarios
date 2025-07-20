#create date types enum

from enum import Enum
from typing import Optional, override, List

class Source(Enum):
	PHOTOVOLTAIC = "photovoltaic"
	WIND = "wind"
	NUCLEAR = "nuclear"
	GAS = "gas"
	HYDRO = "hydro"
	HYDRO_STORAGE = "hydro_storage"
	COAL = "coal"

class RoundType(Enum):
	DAY = "day"
	NIGHT = "night"
	SLIDE = "slide" #show a presentation slide
	SLIDE_RANGE = "slide_range"

class WeatherType(Enum):
	SUNNY = "sunny"
	RAINY = "rainy"
	CLOUDY = "cloudy"
	SNOWY = "snowy"
	FOGGY = "foggy"
	WINDY = "windy"
	CALM = "calm"

class Building(Enum):
	CITY_CENTER = "city_center"
	FACTORY = "factory"
	STADIUM = "stadium"
	HOSPITAL = "hospital"
	UNIVERSITY = "university"
	AIRPORT = "airport"
	SHOPPING_MALL = "shopping_mall"
	TECHNOLOGY_CENTER = "technology_center"

	FARM = "farm"
	LIVING_QUARTER_SMALL = "living_quarter_small"
	LIVING_QUARTER_LARGE = "living_quarter_large"
	SCHOOL = "school"

class Round:
	def __init__(self, comment: Optional[str] = None):
		self.type = None
		self.comment = comment

	def getRoundType(self) -> RoundType:
		return self.type

	def setRoundType(self, round_type: RoundType):
		self.type = round_type

	def __str__(self):
		return f"Round(type={self.type}, comment={self.comment})"

class PlayRound(Round):
	def __init__(self, comment: Optional[str] = None):
		super().__init__(comment)
		self.production_coefficients = {
			Source.PHOTOVOLTAIC: 0.0,
			Source.WIND: 0.0,
			Source.NUCLEAR: 1.0,
			Source.GAS: 1.0,
			Source.HYDRO: 1.0,
			Source.HYDRO_STORAGE: 1.0,
			Source.COAL: 1.0
		}

		# production modifiers are added to the default building consumption defined in the script
		# eg. if a building of type BuildingType.FACTORY has a default production of 1000 (MW)
		# a value of -200 here would make the consumption 800 (MW)
		self.building_modifiers = {}

		for building in Building:
			self.building_modifiers[building] = 0.0

		self.weather = []

	def setWeather(self, weather: WeatherType):
		if weather == WeatherType.SUNNY:
			self.weather.append(WeatherType.SUNNY)
			self.setPVCoefficient(1.0)
		
		elif weather == WeatherType.RAINY:
			self.weather.append(WeatherType.RAINY)
		
		elif weather == WeatherType.CLOUDY:
			self.weather.append(WeatherType.CLOUDY)
			self.setPVCoefficient(0.5)
		
		elif weather == WeatherType.SNOWY:
			self.weather.append(WeatherType.SNOWY)

		elif weather == WeatherType.FOGGY:
			self.weather.append(WeatherType.FOGGY)

		elif weather == WeatherType.WINDY:
			self.weather.append(WeatherType.WINDY)
			self.setWindCoefficient(1.0)

		elif weather == WeatherType.CALM:
			self.weather.append(WeatherType.CALM)

	def getWeather(self) -> Optional[List[WeatherType]]:
		return self.weather

	def setRoundType(self, round_type: RoundType):
		self.type = round_type
		if round_type == RoundType.DAY:
			self.setPVCoefficient(0.8) # by default its not really sunny, so we set to some smaller value than exact 1.0

		elif round_type == RoundType.NIGHT:
			self.setPVCoefficient(0.0)

	def setPVCoefficient(self, coefficient: float):
		self.production_coefficients[Source.PHOTOVOLTAIC] = coefficient

	def setWindCoefficient(self, coefficient: float):
		self.production_coefficients[Source.WIND] = coefficient

	def setNuclearCoefficient(self, coefficient: float):
		self.production_coefficients[Source.NUCLEAR] = coefficient

	def setGasCoefficient(self, coefficient: float):
		self.production_coefficients[Source.GAS] = coefficient

	def setHydroCoefficient(self, coefficient: float):
		self.production_coefficients[Source.HYDRO] = coefficient

	def setHydroStorageCoefficient(self, coefficient: float):
		self.production_coefficients[Source.HYDRO_STORAGE] = coefficient

	def setCoalCoefficient(self, coefficient: float):
		self.production_coefficients[Source.COAL] = coefficient

	def outage(self, source: Source):
		if source in self.production_coefficients:
			self.production_coefficients[source] = 0.0
		else:
			raise ValueError(f"Unknown energy source: {source}")
		
	def addBuildingModifier(self, building: Building, modifier: float):
		if building in self.building_modifiers:
			self.building_modifiers[building] += modifier
		else:
			raise ValueError(f"Unknown building type: {building}")

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

class Day(PlayRound):
	def __init__(self, comment: Optional[str] = None):
		super().__init__(comment)
		self.setRoundType(RoundType.DAY)

class Night(PlayRound):
	def __init__(self, comment: Optional[str] = None):
		super().__init__(comment)
		self.setRoundType(RoundType.NIGHT)

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

class WeatherRound(PlayRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		# use the comment from the wrapped round if no new comment is provided
		effective_comment = comment if comment is not None else (round.comment if hasattr(round, 'comment') else None)
		
		super().__init__(effective_comment)

		self.setRoundType(round.type)

		if hasattr(round, 'production_coefficients'):
			for key, value in round.production_coefficients.items():
				self.production_coefficients[key] = value

		if hasattr(round, 'weather') and round.weather:
			self.weather = round.weather.copy()

class Windy(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.WINDY)

class Rainy(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.RAINY)

class Sunny(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.SUNNY)

class Cloudy(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.CLOUDY)

class Foggy(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.FOGGY)

class Snowy(WeatherRound):
	def __init__(self, round: Round, comment: Optional[str] = None):
		super().__init__(round, comment)
		self.setWeather(WeatherType.SNOWY)

class Script:
	def __init__(self, building_consumptions: dict):
		self.rounds : List[Round] = []
		self.pdf : str = None
		self.building_consumptions = building_consumptions

	def addRound(self, round: Round):
		self.rounds.append(round)

	def getRounds(self):
		return self.rounds
	
	def setPDF(self, pdf):
		self.pdf = pdf

	def getPDF(self):
		return self.pdf
	
	def getBuildingConsumption(self, building: Building) -> Optional[tuple]:
		return self.building_consumptions.get(building, None)