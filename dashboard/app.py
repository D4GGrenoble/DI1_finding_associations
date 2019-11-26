import dash
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent

with open('figures/20191105_nb_asso_per_dep.html', 'r') as f:
    map_departements = f.read()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Data For Good Grenoble'),

    html.H2(children='''
        Data analysis for charities
    '''),

    dcc.Markdown(dedent('''
    The first analysis of the Data For Good Grenoble team has been to analyse
    the "Répertoire National des Associations". Our goal was to get familiar
    with associations in France and more specifically around Grenoble,
    before offering them our services.
    
    **The datasets**

    We used the open data portal of the French government to get the
    ["Répertoire National des Associations"](https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/)
    (RNA)

    The city of Grenoble offers a portal to search for associations registered
    in Grenoble. We contacted them to know if the database behind this
    portal was available. It wasn't at that time, but it is now ! Big thanks !
    [Annuaire des associations de Grenoble](http://data.metropolegrenoble.fr/ckan/dataset/les-associations-de-l-annuaire-des-associations-de-grenoble-fr)
    ''')),
    html.H3('Associations in France'),
    # How many? 1531245 active associations
    dcc.Markdown(dedent('''
    **How many ?** 1 531 245 active associations in France (on 01/11/2019).

    **When was the first association created ? What does this group do ?** The oldest association in the RNA is the "Congrégation des sœurs trinitaires" created on July 16th 1810.
    Its social object is _Soin des malades et des vieillards - instruction et éducation aussi bien en France qu'à l'étranger et notamment dans le tiers monde_.

    **Where are the associations located ?**


    ''')),
    html.Iframe(
        srcDoc=map_departements,
        height='1050px',
        width='100%'
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
