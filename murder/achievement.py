from .db import Model, DoesNotExistError
from .template import templater, inside_page

class Achievement(Model):
	_table = 'achievement'
	
	def __init__(self, id, name, description, points, goal=None, unit=None):
		super(Achievement, self).__init__()
		self.id, self.name, self.description, self.points, self.goal, self.unit = id, name, description, points, goal, unit

	@classmethod
	def init_db(cls):
		CREATE = """CREATE TABLE IF NOT EXISTS achievement (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name STRING NOT NULL,
			description STRING NOT NULL,
			points INTEGER,
			goal INTEGER,
			unit STRING,
			UNIQUE (name)
		)"""
		cls._sql(CREATE)
		
		for achievement in Achievement.achievements:
			try:
				achievement.get(name=achievement.name)
			except DoesNotExistError:
				achievement.add(**achievement.__dict__)

Achievement.achievements = [
	Achievement(None, 'A taste of blood', 'Got your first kill', 5, 1, 'murder'),
	Achievement(None, 'Double kill', 'Kill two people within 10 minutes', 10, 2, 'successive kills'),
	Achievement(None, 'Innocent victim', 'Died without killing', 5),
	Achievement(None, 'Mafia talk', 'Kill during the night (after 8pm)', 5, 1, 'nighttime hit'),
]

class PlayerAchievement(Model):
	_table = 'player_achievement'

	def __init__(self, achievement, game, player, progress):
		super(PlayerAchievement, self).__init__()
		self.id, self.achievement, self.game, self.player, self.progress = id, achievement, game, player, progress

	def increment_progress(self, amount=1):
		self.progress = amount if pa.progresss == None else self.progress+amount
		self.update(progress=self.progress)

	@classmethod
	def find_achievements(cls, player):
		achievements = list(Achievement.iter())
		for achievement in achievements:
			pa = PlayerAchievement.find_or_create(achievement=achievement.id, player=player)
			achievement.progress = pa.progress

		return achievements

	@classmethod
	def init_db(cls):
		CREATE = """CREATE TABLE IF NOT EXISTS player_achievement (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			achievement INTEGER NOT NULL references achievement (id),
			player INTEGER NOT NULL references player (id),
			progress INTEGER DEFAULT 0,
			UNIQUE (player, achievement)
		)"""
		cls._sql(CREATE)

def achievements_template(game_id, achievements) -> str:
	template = templater.load('achievements.html').generate(game_id=game_id, achievements=achievements, profile=False)
	return inside_page(template, game_id=game_id)

def achievements(response, game_id=None):
	achievements = list(Achievement.iter())
	response.write(achievements_template(game_id, achievements))