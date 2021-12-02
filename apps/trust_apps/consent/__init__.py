from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    timed_out = models.BooleanField(initial=False)

# By convention, these imports should normally be at the top
from otree.settings import POINTS_CUSTOM_NAME
from otree.settings import REAL_WORLD_CURRENCY_CODE

# PAGES
class Consent(Page):
    timeout_seconds = 30

    @staticmethod
    def vars_for_template(player):
        session = player.session
        rate = session.config['real_world_currency_per_point']
        units = POINTS_CUSTOM_NAME
        rwc_code =  REAL_WORLD_CURRENCY_CODE
        rwc_symbol = "€"
        return dict(units=units, rate=rate, rwc_code=rwc_code, rwc_symbol=rwc_symbol)


    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timed_out = True

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.timed_out:
            return "timeout"



page_sequence = [Consent]
