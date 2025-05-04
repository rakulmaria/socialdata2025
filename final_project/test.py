import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os

# Load dataset
cols_to_keep = ['family', 'genus', 'species', 'locality', 'decimalLatitude',
                'decimalLongitude', 'coordinateUncertaintyInMeters', 'eventDate',
                'month', 'year']
df = pd.read_csv('./resources/DOF-observations-threathened-and-rare-species-1998-2025.csv',
                 usecols=cols_to_keep, sep='\t', on_bad_lines='skip')

species_to_keep = set([
    "Ichthyaetus melanocephalus",
    "Ciconia ciconia",
    "Ciconia nigra",
    "Circus pygargus",
    "Pandion haliaetus",
    "Aquila chrysaetos",
    "Haliaeetus albicilla",
    "Aegolius funereus",
    "Asio flammeus",
    "Falco peregrinus",
    "Anthus campestris"
])

df_novama = df[df["species"].isin(species_to_keep)]

species_to_commonname = {
    'Aegolius funereus': 'Boreal owl',
    'Anthus campestris': 'Tawny pipit',
    'Asio flammeus': 'Short-eared owl',
    'Aquila chrysaetos': 'Golden eagle',
    'Ciconia ciconia': 'White stork',
    'Ciconia nigra': 'Black stork',
    'Circus pygargus': "Montagu's harrier",
    'Falco peregrinus': 'Peregrine falcon',
    'Haliaeetus albicilla': 'White-tailed eagle',
    'Ichthyaetus melanocephalus': 'Mediterranean gull',
    'Pandion haliaetus': 'Osprey',
}

# add a new column commonName with the english commonName of the birds
# fillna handles unknown species, if there are any
df_novama['commonName'] = df_novama['species'].map(species_to_commonname).fillna('Unknown species')
df_novama.head()


# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H2("Threatened Bird Species in Denmark (1998–2024)"),
    
    dcc.Dropdown(
        id='species-dropdown',
        options=[{'label': name, 'value': name} for name in sorted(df_novama['commonName'].unique())],
        value='White-tailed Eagle'  # You can set your preferred default
    ),
    
    dcc.Graph(id='population-graph'),
    
    html.Div([
        html.Img(id='bird-image', style={'height': '300px', 'margin-top': '20px'})
    ])
])

# Callback for updating plot and image
@app.callback(
    [Output('population-graph', 'figure'),
     Output('bird-image', 'src')],
    Input('species-dropdown', 'value')
)
def update_species(selected_common_name):
    # Filter by selected common name
    filtered = df_novama[df_novama['commonName'] == selected_common_name]
    
    # Group by year and count observations
    yearly_counts = filtered.groupby('year').size().reset_index(name='observations')
    
    # Plotting population trend
    fig = px.line(yearly_counts, x='year', y='observations',
                  title=f"Population Trend for {selected_common_name}",
                  markers=True)
    
    # Generate image file path
    safe_name = selected_common_name.lower().replace(' ', '-')
    image_path = f'resources/{safe_name}.png'
    
    # Check if image exists
    if os.path.exists(image_path):
        # Serve local file as base64 image
        import base64
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('ascii')
        img_src = f'data:image/png;base64,{encoded_image}'
    else:
        # Fallback image or empty placeholder
        img_src = ''

    return fig, img_src

if __name__ == '__main__':
    app.run(debug=True)
