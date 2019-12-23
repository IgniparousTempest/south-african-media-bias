import functools
import json
from collections import defaultdict
from pathlib import Path

import datetime as dt
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

import results
from visualisation.area_under_curve import auc


def determine_focus(entry: dict):
    if entry['anc'] == 0 and entry['da'] == 0 and entry['eff'] == 0:
        return None
    elif entry['eff'] >= entry['da'] and entry['eff'] >= entry['anc']:
        return 'eff'
    elif entry['anc'] >= entry['da'] and entry['anc'] >= entry['da']:
        return 'anc'
    else:
        return 'da'


def publication_name(json_file_name: str) -> str:
    return {
        'times_live.json': 'Times Live',
        'iol.json': 'IOL',
        'news24.json': 'News24'
    }[json_file_name]


def save_image(plt, result_name: str, prepend: str):
    name = results.absolute_path(f'{prepend}_{result_name}.png')
    plt.savefig(name, bbox_inches='tight', dpi=200)


def counts(json_path: str, start_year: int) -> Tuple[dict, int]:
    number_of_articles = 0
    results = defaultdict(lambda: defaultdict(lambda: {'anc': 0, 'da': 0, 'eff': 0}))
    with open(json_path, 'r') as f:
        data = json.load(f)
        for entry in data:
            if int(entry['year']) < start_year:
                continue
            focus = determine_focus(entry)
            if focus is None:
                continue
            results[entry['year']][entry['month']][focus] += 1
            number_of_articles += 1
        return results, number_of_articles


def plot_stacked_area(from_year: int):
    # Get data
    raw_data, number_of_articles = counts('../results/times_live.json', from_year)

    xs = []
    anc, da, eff = [], [], []
    for year in sorted(list(raw_data.keys())):
        for month in sorted(list(raw_data[year].keys())):
            xs.append(dt.datetime.fromisoformat(f'{year}-{month}-01'))
            anc.append(raw_data[year][month]['anc'])
            da.append(raw_data[year][month]['da'])
            eff.append(raw_data[year][month]['eff'])

    data = pd.DataFrame({'anc': anc, 'da': da, 'eff': eff, }, index=xs)

    # Seats data
    election_2014 = [249, 89, 25]
    election_2019 = [230, 84, 44]
    elections = np.array([election_2014, election_2014, election_2019, election_2019])
    seats_xs = [xs[0], dt.datetime.fromisoformat('2019-05-07'), dt.datetime.fromisoformat('2019-05-08'), xs[-1]]
    seats = pd.DataFrame({'anc': elections[:,0], 'da': elections[:,1], 'eff': elections[:,2], }, index=seats_xs)
    seats_perc = seats.divide(seats.sum(axis=1), axis=0)
    del seats_perc['anc']
    seats_perc['da'] = seats_perc['da'] + seats_perc['eff']

    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)

    # Make the plot
    pal = sns.color_palette("Set1")
    pal = pal[0:3]
    plt.plot(seats_xs, seats_perc, color='w')
    axes = plt.gca()
    axes.set_ylim([0, 1])

    plt.stackplot(xs, data_perc["eff"], data_perc["da"], data_perc["anc"], labels=['EFF', 'DA', 'ANC'], colors=pal)
    plt.legend(loc='upper left')
    plt.margins(0, 0)
    plt.title(f'Times Live Political Focus (num articles={number_of_articles})')
    plt.show()


def plot_separate_area(json_file_name: str, from_year: int):
    # Get data
    json_path = results.absolute_path(json_file_name)
    raw_data, number_of_articles_in_period = counts(json_path, from_year)

    xs = []
    anc, da, eff = [], [], []
    for year in sorted(list(raw_data.keys())):
        for month in sorted(list(raw_data[year].keys())):
            xs.append(dt.datetime.fromisoformat(f'{year}-{month}-01'))
            anc.append(raw_data[year][month]['anc'])
            da.append(raw_data[year][month]['da'])
            eff.append(raw_data[year][month]['eff'])

    data = pd.DataFrame({'anc': anc, 'da': da, 'eff': eff, }, index=xs)

    # Seats data
    election_2014 = [249, 89, 25]
    election_2019 = [230, 84, 44]
    elections = np.array([election_2014, election_2014, election_2019, election_2019])
    seats_xs = [xs[0], dt.datetime.fromisoformat('2019-05-07'), dt.datetime.fromisoformat('2019-05-08'), xs[-1]]
    seats = pd.DataFrame({'anc': elections[:,0], 'da': elections[:,1], 'eff': elections[:,2], }, index=seats_xs)
    seats_perc = seats.divide(seats.sum(axis=1), axis=0)

    # We need to transform the data from raw data to percentage (fraction)
    data_perc = data.divide(data.sum(axis=1), axis=0)

    # Make the plot
    pub_name = publication_name(json_file_name)
    pal = sns.color_palette("Set1")
    pal = pal[0:3]
    for data, seats, colour, name in zip([data_perc["eff"], data_perc["da"], data_perc["anc"]], [seats_perc["eff"], seats_perc["da"], seats_perc["anc"]], pal, ['EFF', 'DA', 'ANC']):
        ratio, _, _ = auc(data, seats)
        ratio = int(round(ratio * 100))

        plt.plot(seats_xs, seats, label='Vote share', color='k')
        axes = plt.gca()
        axes.set_ylim([0, 1])

        # format the ticks
        years = mdates.YearLocator()  # every year
        months = mdates.MonthLocator()  # every month
        years_fmt = mdates.DateFormatter('%Y')
        axes.xaxis.set_major_locator(years)
        axes.xaxis.set_major_formatter(years_fmt)
        axes.xaxis.set_minor_locator(months)

        plt.stackplot(xs, data, labels=[name], colors=[colour])
        plt.legend(loc='upper left', title=f'{ratio}% Focus')
        plt.margins(0, 0)
        plt.title(f'{pub_name} Political Focus on {name} (num articles={number_of_articles_in_period})')
        save_image(plt, f'{Path(json_file_name).stem}_{name.lower()}', 'results')
        plt.show()


def plot_number_of_articles_a_month(json_file_name: str, from_year: int = 0):
    # Get data
    json_path = results.absolute_path(json_file_name)
    raw_data, number_of_articles_in_period = counts(json_path, from_year)

    xs = []
    ys = []
    for year in sorted(list(raw_data.keys())):
        if int(year) < from_year:
            continue
        for month in sorted(list(raw_data[year].keys())):
            xs.append(dt.datetime.fromisoformat(f'{year}-{month}-01'))
            monthly_articles_count = functools.reduce(lambda acc, value: acc + value, raw_data[year][month].values())
            ys.append(monthly_articles_count)

    # Make the plot
    pub_name = publication_name(json_file_name)
    colour = sns.color_palette("Set1")[3]
    axes = plt.gca()

    plt.stackplot(xs, ys, labels=['articles'], colors=[colour])
    plt.margins(0, 0)
    plt.title(f'{pub_name} articles distribution (total articles={number_of_articles_in_period})')
    save_image(plt, Path(json_file_name).stem, 'articles')
    plt.show()


if __name__ == '__main__':
    # plot_stacked_area(from_year=2016)
    plot_separate_area('times_live.json', from_year=2017)
    plot_separate_area('iol.json', from_year=2015)
    plot_separate_area('news24.json', from_year=2015)

    plot_number_of_articles_a_month('times_live.json')
    plot_number_of_articles_a_month('iol.json')
    plot_number_of_articles_a_month('news24.json')
