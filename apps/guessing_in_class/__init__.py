from otree.api import *

doc = """
Your app description
"""

# MODELS
class Constants(BaseConstants):
    name_in_url = 'guessing'
    players_per_group = 3
    num_rounds = 1
    multiplier = 2/3
    reward = Currency(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    average_guess = models.FloatField()
    target_number = models.FloatField()



def set_payoffs(group):
    players = group.get_players() ### [Player1, Player2, Player3]

    # guesses = [players[0].guess, players[1].guess, players[2].guess]

    # Get guesses in each group
    guesses_in_group=[]
    for p in players:
        guesses_in_group.append(p.guess)

    # Calculate the average guess
    group.average_guess = sum(guesses_in_group) / len(guesses_in_group)

    # Calculate the target number
    group.target_number = group.average_guess * Constants.multiplier

    distances_in_group = []
    for p in players:
        p.distance = abs(p.guess - group.target_number)
        distances_in_group.append(p.distance)

    minimum_distance = min(distances_in_group)

    for p in players:
        if p.distance == minimum_distance:
            p.is_winner = True
            p.payoff = Constants.reward
        else:
            p.is_winner = False
            p.payoff = 0

    print(distances_in_group)

class Player(BasePlayer):
    guess = models.IntegerField(label="Please choose a number between 0 and 100", min=0, max=100)
    distance = models.FloatField()
    is_winner = models.BooleanField()


# PAGES
class Guessing(Page):
    form_model = "player"
    form_fields = ['guess']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoffs"


class Results(Page):

    def vars_for_template(player):
        guesses = [p.guess for p in player.group.get_players()]

        return dict(my_value = guesses)


page_sequence = [Guessing,ResultsWaitPage, Results]
