from collections import Counter

from .template import templater, inside_page
from .player import Player
from .murder import Murder

def stats_template(game_id, players, murders, **kwargs) -> str:
	stats = templater.load('stats.html').generate(game_id=game_id, murders=murders, players=players, **kwargs)
	return inside_page(stats, game_id=game_id)

def stats(response, game_id=None):
	players = list(Player.iter(game=game_id))
	murders = list(Murder.iter(game=game_id))
	wanted = most_wanted(murders)

	response.write(stats_template(game_id, players, murders, most_wanted=wanted))

def most_wanted(murders):
	murder_counts = Counter(murder.murderer for murder in murders)
	if murders:
		murderer_id, count = max(murder_counts.items(), key=lambda t: t[1])
		most_wanted = Player.find(id=murderer_id)
		most_wanted.murders = count
	else:
		most_wanted = None

	return most_wanted
