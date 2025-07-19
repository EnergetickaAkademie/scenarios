#create date types enum

from enum import Enum
from typing import Optional, override, List


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

class Round:
	def __init__(self):
		self.type = None

	def getRoundType(self) -> RoundType:
		return self.type

	def setRoundType(self, round_type: RoundType):
		self.type = round_type

	def __str__(self):
		return f"Round(type={self.type})"

class PlayRound(Round):
	def __init__(self):
		super().__init__()
		self.production_coefficients = {
			"photovoltaic": 0.0, 	#photovoltaic
			"wind": 0.0, 			#wind
			"nuclear": 1.0, 		#nuclear
			"gas": 1.0, 			#gas
			"hydro": 1.0, 			#water
			"hydro_storage": 1.0, 	#hydroelectric storage
			"coal": 1.0 			#coal
		}

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
		self.production_coefficients["photovoltaic"] = coefficient

	def setWindCoefficient(self, coefficient: float):
		self.production_coefficients["wind"] = coefficient

	def setNuclearCoefficient(self, coefficient: float):
		self.production_coefficients["nuclear"] = coefficient

	def setGasCoefficient(self, coefficient: float):
		self.production_coefficients["gas"] = coefficient

	def setHydroCoefficient(self, coefficient: float):
		self.production_coefficients["hydro"] = coefficient

	def setHydroStorageCoefficient(self, coefficient: float):
		self.production_coefficients["hydro_storage"] = coefficient

	def setCoalCoefficient(self, coefficient: float):
		self.production_coefficients["coal"] = coefficient

	def __str__(self):
		return f"Round(type={self.type}, weather={self.weather}, production_coefficients={self.production_coefficients})"

class Day(PlayRound):
	def __init__(self):
		super().__init__()
		self.setRoundType(RoundType.DAY)

class Night(PlayRound):
	def __init__(self):
		super().__init__()
		self.setRoundType(RoundType.NIGHT)

class Slide(Round):
	def __init__(self, slide_number: Optional[int] = None):
		super().__init__()
		self.type = RoundType.SLIDE
		self.slide_number = slide_number

	def setSlideNumber(self, slide_number: int):
		self.slide_number = slide_number

	def getSlideNumber(self) -> Optional[int]:
		return self.slide_number
	
	def __str__(self):
		return f"Slide(slide_number={self.slide_number})"
	
class SlideRange(Round):
	def __init__(self, start: int, end: int):
		super().__init__()
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
	def __init__(self, round: Round):
		super().__init__()

		self.setRoundType(round.type)
		for key, value in round.production_coefficients.items():
			self.production_coefficients[key] = value

		self.setWeather(round.weather)

class Windy(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.WINDY)

class Rainy(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.RAINY)

class Sunny(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.SUNNY)

class Cloudy(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.CLOUDY)

class Foggy(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.FOGGY)

class Snowy(WeatherRound):
	def __init__(self, round: Round):
		super().__init__(round)
		self.setWeather(WeatherType.SNOWY)

class Script:
	def __init__(self):
		self.rounds : List[Round] = []
		self.pdf : str = None

	def addRound(self, round: Round):
		self.rounds.append(round)

	def getRounds(self):
		return self.rounds
	
	def setPDF(self, pdf):
		self.pdf = pdf

	def getPDF(self):
		return self.pdf