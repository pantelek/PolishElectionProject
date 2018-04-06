import csv
from copy import copy
from jinja2 import Template


candidates = ('Dariusz Maciej GRABOWSKI', 'Piotr IKONOWICZ', 'Jarosław KALINOWSKI',
              'Janusz KORWIN-MIKKE', 'Marian KRZAKLEWSKI', 'Aleksander KWAŚNIEWSKI',
              'Andrzej LEPPER', 'Jan ŁOPUSZAŃSKI', 'Andrzej Marian OLECHOWSKI',
              'Bogdan PAWŁOWSKI', 'Lech WAŁĘSA', 'Tadeusz Adam WILECKI')

stats = ('Obwody', 'Uprawnieni', 'Karty wydane',
         'Głosy oddane', 'Głosy nieważne', 'Głosy ważne')

clean_slate = {}
for cand in candidates:
    clean_slate[cand] = 0
for stat in stats:
    clean_slate[stat] = 0
votes = {'Polska': copy(clean_slate)}
subareas = {'Polska': []}
mother_area = {'Polska': []}
types = {'Polska': 'country'}
commune_name = {}


with open('./election_data/pkw2000.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Województwo'] not in votes:
            votes[row['Województwo']] = copy(clean_slate)
            subareas['Polska'].append(row['Województwo'])
            subareas[row['Województwo']] = []
            types[row['Województwo']] = 'voivodeship'

        if row['Nr okręgu'] not in votes:
            votes[row['Nr okręgu']] = copy(clean_slate)
            subareas[row['Województwo']].append(row['Nr okręgu'])
            subareas[row['Nr okręgu']] = []
            types[row['Nr okręgu']] = 'district'

        if row['Kod gminy'] not in votes:
            votes[row['Kod gminy']] = copy(clean_slate)
            subareas[row['Nr okręgu']].append(row['Kod gminy'])
            subareas[row['Kod gminy']] = []
            types[row['Kod gminy']] = 'commune'
            commune_name[row['Kod gminy']] = row['Gmina']

        for cand in candidates:
            votes[row['Kod gminy']][cand] += int(row[cand])
        for stat in stats:
            votes[row['Kod gminy']][stat] += int(row[stat])


def count_votes_and_mother_areas(area):
    if types[area] == 'commune':
        return
    else:
        for subarea in subareas[area]:
            mother_area[subarea] = copy(mother_area[area])
            mother_area[subarea].append(area)
            count_votes_and_mother_areas(subarea)
            for cand in candidates:
                votes[area][cand] += votes[subarea][cand]
            for stat in stats:
                votes[area][stat] += votes[subarea][stat]


def generate_sites(area):
    with open('./templates/' + types[area] + '.html', 'r') as f:
        template = Template(f.read())
        generated = template.render(candidates=candidates, stats=stats, votes=votes[area],
                                    commune_name=commune_name, subareas=subareas[area],
                                    mother_area=mother_area[area], area=area, types=types)
        if types[area] == 'country':
            name = './generated/index.html'
        else:
            name = './generated/' + types[area] + '/' + area + '.html'
        with open(name, 'w+') as f2:
            f2.write(generated)
    for subarea in subareas[area]:
        generate_sites(subarea)


count_votes_and_mother_areas('Polska')
generate_sites('Polska')
