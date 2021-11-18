from otree.api import *
import random

doc = """
This is a survey created by Ali Seyhun Saral
for the oTree crash course in CEREB.
"""


class Constants(BaseConstants):
    name_in_url = 'my_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(blank=True, label="Your name (optional)")

    age = models.IntegerField(min=18,
                              max=118,# Kane Tanaka, Japan 1903
                              initial=30)

    mood = models.StringField(choices=['bad',
                                        'okay',
                                        'wonderful'],
                                    label="How do you feel today?",
                                    widget = widgets.RadioSelect,
                                    )

    wants_feedback = models.BooleanField(label="Would you like to be contacted about survey results.")

    picked_number = models.IntegerField()

    comments = models.LongStringField()

def mood_choices(player):
    choices = ['bad', 'okay', 'wonderful']
    random.shuffle(choices)
    return choices

# PAGES
class Survey(Page):
    form_model = "player"
    form_fields = ['name', 'age', 'mood', 'wants_feedback']

class Results(Page):
    pass

page_sequence = [Survey, Results]
