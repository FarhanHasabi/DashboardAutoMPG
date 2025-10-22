import panel as pn
import holoviews as hv
import hvplot.pandas
import pandas as pd
from ucimlrepo import fetch_ucirepo

# Inisialisasi Panel
pn.extension(template='fast', theme='dark', sizing_mode='stretch_width')

# Ambil dataset
auto_mpg = fetch_ucirepo(id=9)
X = auto_mpg.data.features
y = auto_mpg.data.targets

# Gabungkan features dan targets
df = X.copy()
df['mpg'] = y.values
df['origin'] = df['origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
df['origin'] = df['origin'].astype('category')
df['model_year'] = df['model_year'] + 70  # Ubah ke tahun sebenarnya

# Widget
origin_picker = pn.widgets.Select(name='Asal Mobil', options=['All'] + list(df['origin'].cat.categories), value='All')
cylinders_selector = pn.widgets.MultiSelect(
    name='Silinder (Scatter)', 
    options=list(df['cylinders'].unique()), 
    value=[4, 6, 8]
)

# Fungsi update plot
def update_plots(origin, cylinders):
    if origin != 'All':
        filtered_df = df[df['origin'] == origin]
    else:
        filtered_df = df

    # Plot 1: Distribusi MPG
    dist_plot = filtered_df.hvplot.hist('mpg', bins=30, title='Distribusi MPG', color='skyblue', alpha=0.7)

    # Plot 2: Rata-rata MPG per Silinder
    avg_mpg_by_cyl = filtered_df.groupby('cylinders')['mpg'].mean().reset_index()
    bar_plot = avg_mpg_by_cyl.hvplot.bar(x='cylinders', y='mpg', title='Rata-rata MPG Berdasarkan Silinder', color='orange')

    # Plot 3: Scatter Weight vs MPG
    scatter_df = filtered_df[filtered_df['cylinders'].isin(cylinders)]
    scatter_plot = scatter_df.hvplot.scatter(x='weight', y='mpg', by='origin', title='Hubungan Weight vs MPG', size=8, alpha=0.7)

    # Plot 4: Tren MPG per Tahun
    yearly_mpg = df.groupby('model_year')['mpg'].mean().reset_index()
    line_plot = yearly_mpg.hvplot.line(x='model_year', y='mpg', title='Tren Rata-rata MPG per Tahun', color='green', line_width=2)

    # Kembalikan plot dalam format Tabs
    tabs = pn.Tabs(
        ("Distribusi MPG", dist_plot),
        ("MPG per Silinder", bar_plot),
        ("Weight vs MPG", scatter_plot),
        ("Tren MPG Tahunan", line_plot),
    )
    return tabs

# Interaktivitas
interactive_plot = pn.bind(update_plots, origin=origin_picker, cylinders=cylinders_selector)

# Sidebar
sidebar = pn.Column(
    pn.pane.Markdown("### Filter Data", styles={'color': 'white'}),
    origin_picker,
    cylinders_selector,
    width=300,
    sizing_mode='stretch_height'
)

# Main layout
main = pn.Column(
    pn.pane.Markdown("# Dashboard Eksplorasi Data Auto MPG", styles={'font-size': '1.8em', 'color': '#00d0ff'}),
    pn.Row(sidebar, interactive_plot, sizing_mode='stretch_width'),
    sizing_mode='stretch_width'
)

# Jadikan servable untuk dijalankan di browser
main.servable(title="Auto MPG Dashboard")