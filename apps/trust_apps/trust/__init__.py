from otree.api import *
from otree.settings import POINTS_CUSTOM_NAME
from otree.settings import REAL_WORLD_CURRENCY_CODE
from otree.currency import RealWorldCurrency

doc = """
Your app description
"""

# MODELS
class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    multiplier = 3
    initial_endowment = Currency(10)

    P1_role = "A"
    P2_role = "B"

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(label="Please tell us how much you would like to send to Player B.",
                                      min=Currency(0), max=Constants.initial_endowment)

    returned_amount = models.CurrencyField(label="Please tell us how much would you like to send to the other person.", min=Currency(0))

def returned_amount_max(group):
    return group.sent_amount * Constants.multiplier

class Player(BasePlayer):
    pass

# FUNCTIONS
def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    p1.payoff = Constants.initial_endowment - group.sent_amount + group.returned_amount
    p2.payoff = group.sent_amount * Constants.multiplier - group.returned_amount

# PAGES
class GroupingWait(WaitPage):
    group_by_arrival_time = True

class Instructions(Page):
    pass

class Send(Page):
    form_model = "group"
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class WaitForA(WaitPage):
    pass

class Return(Page):
    form_model = "group"
    form_fields = ['returned_amount']

    def vars_for_template(player: Player):
        returnable_amount = player.group.sent_amount * Constants.multiplier
        return dict(returnable_amount = returnable_amount)

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2


class WaitForB(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass

page_sequence = [GroupingWait, Instructions, Send, WaitForA, Return, WaitForB, Results]
