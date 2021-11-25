from otree.api import *

doc = """
Your app description
"""

# MODELS
class Constants(BaseConstants):
    name_in_url = 'guessing'
    players_per_group = 3
    num_rounds = 1
    multiplier = 2/3   # 2/3 of the averages
    bonus_points = Currency(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    average_guess = models.FloatField()
    target_number = models.FloatField()
    minimum_distance = models.FloatField()

class Player(BasePlayer):
    guess = models.IntegerField(label= "Please select a number between 0 and 100", min=0, max=100)
    distance = models.FloatField()
    is_winner = models.BooleanField()

# FUNCTIONS
def set_payoffs(group):
    # Get players in group
    players = group.get_players()

    # Get guesses in group
    guesses = [p.guess for p in players]

    # Calculate the average and the target number
    group.average_guess = sum(guesses) / Constants.players_per_group
    group.target_number = group.average_guess * Constants.multiplier

    # Calculate the distances
    distances = []
    for p in players:
        p.distance = abs(p.guess - group.target_number) # This is for my data
        distances.append(p.distance) # For the calculation

    # Get the minimum distance in group
    group.minimum_distance = min(distances)

    for p in players:
        # if the player is the winner
        if p.distance == group.minimum_distance:
            p.is_winner = True
            p.payoff = Constants.bonus_points

        # if the player is not the winner
        else:
            p.is_winner = False
            p.payoff = 0

# PAGES
class Welcome(Page):
    pass

class Guessing(Page):
    form_model = "player"
    form_fields = ['guess']



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        guesses = [p.guess for p in player.group.get_players()]

        return dict(
            guesses=guesses,
        )


page_sequence = [Welcome, Guessing, ResultsWaitPage, Results]
