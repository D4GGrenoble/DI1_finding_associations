import os
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from textwrap import dedent
import pandas as pd
import glob

with open('figures/20191105_nb_asso_per_dep.html', 'r') as f:
    map_departements = f.read()
with open('figures/20191105_nb_asso_per_dep_per10000.html', 'r') as f:
    map_departements_hab = f.read()

root = '/home/myriam/DataScience/dataforgoodgrenoble/data'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
repartition = pd.read_csv(os.path.join(root, 'processed/repartition_obj.csv'))
image_directory = 'figures'
static_image_route = '/static/'
pics = [pic.split('/')[-1] for pic in glob.glob('%s/*.png' % image_directory)]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Data For Good Grenoble'),

    html.H2('Discovering French associations'),

    html.H3('Context'),

    dcc.Markdown(dedent('''
    The first analysis of the Data For Good Grenoble team has been to analyse
    the "Répertoire National des Associations". Our goal was to get familiar
    with associations in France and more specifically around Grenoble,
    before offering them our services.
    ''')),
    html.H3('Datasets'),
    dcc.Markdown(dedent('''
    We used the open data portal of the French government to get the
    ["Répertoire National des Associations"](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/)
    (RNA). This gives a insight into the association's landscape in France.

    The city of Grenoble offers a portal to search for associations registered
    in Grenoble. We contacted them to know if the database behind this
    portal was available. It wasn't at that time, but it is now ! Big thanks !
    [Annuaire des associations de Grenoble](http://data.metropolegrenoble.fr/ckan/dataset/les-associations-de-l-annuaire-des-associations-de-grenoble-fr)
    ''')),
    html.H3('Associations in France'),
    html.P('Now, here is a short presentation of our insights.'),
    # How many? 1531245 active associations
    dcc.Markdown(dedent('''
    **How many ?** 1 531 245 active associations in France (on 01/11/2019).

    **When was the first association created ? What does this group do ?**
    The oldest association in the RNA is the "Congrégation des sœurs trinitaires" created on July 16th 1810.
    Its social object is _Soin des malades et des vieillards - instruction et éducation aussi bien en France qu'à l'étranger et notamment dans le tiers monde_.

    **Where are the associations located ?**
    We first notice that the departments hosting the most associations are Paris,
    Nord, Rhône and Bouches-du-Rhône corresponding respectively to Lille, Lyon and
    Marseille.
    To get a more representative view, we also plotted a map normalized by the
    number of inhabitants. The results are stinkingly different.
    The 3 departments in white in the north-east correspond to a region that was
    not part of France when the law defining associations was voted in 1901.
    Thus there exists associations there but with another status. The few that
    appears in our data have a headquarter out of those departments.
    Paris has a high number of associations per inhabitants but it is by far not
    the most dense area. The top departments are quite a surprise as most of them
    are not densely populated and have a low count of associations.
    ''')),
    html.Iframe(
        srcDoc=map_departements,
        height='1050px',
        width='100%'
    ),
    html.Iframe(
        srcDoc=map_departements_hab,
        height='1050px',
        width='100%'
    ),

    html.H5('Type of associations'),
    dcc.Markdown(dedent('''
    We grouped the associations by their activity : Culture and hobbies,
    Social action, Sport, Education, Networking, Healthcare, Environment,
    Public services, Other fields.
    We compare the repartition of the associations across those categories at
    different scales : nationwide, in Grenoble's department and in Grenoble Alpes
    Métropole.
    The numbers are quite similar except 1.5 times more associations in Environment
    and Networking in Grenoble than in France and slightly less educational associations.
    ''')),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in repartition.columns],
        data=repartition.to_dict('records'),
    ),
    html.H6('Description of the associations'),
    dcc.Markdown(dedent('''
    Another way of picturing the association landscape is to create a wordcloud
    from the free text description of each association. This data is given by the
    associations themselves.
    The wordcloud represent the words with the most occurences in those descriptions.
    We can find the same pattern as in the above table but we can also see the
    cultural associations are oriented around art and music while the social associations
    are about helping one another.
    ''')),
    html.Img(src='/static/wordcloud.png'),

    html.H5('History of creation in Grenoble'),
    dcc.Markdown(dedent('''
    Finally, we had a look on the history of creation of associations in Grenoble.
    We notice an explosion of the creations after 2006 that is now stable at more
    than 200 associations created each year.
    ''')),
    html.Img(src='/static/year_grenoble.png')
])

@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in pics:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)


if __name__ == '__main__':
    app.run_server(debug=True)
