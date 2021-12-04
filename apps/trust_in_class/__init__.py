from otree.api import *


doc = """
Hello 
"""

# MODELS
class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1

    multiplier = 3
    initial_endowment = Currency(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(label="Please tell us how much you'd like to transfer to Player B",
                                       min= 0,
                                       max= Constants.initial_endowment,
                                       )
    returned_amount = models.CurrencyField(label="Please tell us how much you'd like to transfer back to Player A",
                                       min= 0)


class Player(BasePlayer):
    pass


# FUNCTIONS
def returned_amount_max(group):
    return group.sent_amount * Constants.multiplier


def set_payoffs(group):
    player1 = group.get_player_by_id(1)
    player2 = group.get_player_by_id(2)

    player1.payoff = Constants.initial_endowment - group.sent_amount + group.returned_amount
    player2.payoff = group.sent_amount * Constants.multiplier - group.returned_amount


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(player):
        return player.id_in_group == 1



class WaitForP1(WaitPage):
    pass


class Return(Page):
    form_model = 'group'
    form_fields = ['returned_amount']

    def vars_for_template(player):
        transferable_amount = player.group.sent_amount * Constants.multiplier

        return dict(ta = transferable_amount)


    def is_displayed(player):
        return player.id_in_group == 2



class WaitForP2(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Send, WaitForP1, Return, WaitForP2, Results]

