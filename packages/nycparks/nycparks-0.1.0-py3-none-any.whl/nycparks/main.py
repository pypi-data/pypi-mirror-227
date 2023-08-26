
import click
import pandas as pd
import os

from nycparks.utils.reserver import TennisReserver
from nycparks.utils.texter import Texter



locations = ["central", "mccarren", "mill pond", "119", "riverside clay", "randall", "sutton east"]


@click.command()
@click.option("-locations", '-l', type=click.Choice(locations), default=locations, multiple=True, help='Name of parks to check')
@click.option("-number", '-n', type=str, help='Receiving number e.g. +11234567890')
def cli(locations, number):

    previous_availability = pd.DataFrame()
    if os.path.isfile("data/availability.csv"):
        previous_availability = pd.read_csv("data/availability.csv")

    tr = TennisReserver()
    texter = Texter()

    current_availability = tr.reserve(locations=locations)
    current_availability.to_csv("data/availability.csv")

    if previous_availability.empty == False:
        new_availability = tr.find_new(new=current_availability, old=previous_availability, locations=locations)
    else:
        new_availability = tr.make_bool_df(current_availability, label="new", locations=locations)

    if new_availability.empty == False:
        texter.send(number=number, df=new_availability)


    

