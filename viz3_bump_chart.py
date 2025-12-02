"""
Visualization 3: Bump Chart
Creates an interactive bump chart showing how dog breed rankings have changed from 2015-2024
"""

import pandas as pd
import altair as alt

# Load data from CSV
df = pd.read_csv('datasets/dog_breeds_2015_2024.csv')

# Normalize breed names to handle variations
breed_mapping = {
    'French Bulldogs': 'French Bulldog',
    'French Bulldog': 'French Bulldog',
    'Labrador Retrievers': 'Labrador Retriever',
    'Retrievers (Labrador)': 'Labrador Retriever',
    'Labrador Retriever': 'Labrador Retriever',
    'Golden Retrievers': 'Golden Retriever',
    'Retrievers (Golden)': 'Golden Retriever',
    'Golden Retriever': 'Golden Retriever',
    'German Shepherd Dogs': 'German Shepherd Dog',
    'German Shepherd Dog': 'German Shepherd Dog',
    'Poodles': 'Poodle',
    'Poodle': 'Poodle',
    'Bulldogs': 'Bulldog',
    'Bulldog': 'Bulldog',
    'Beagles': 'Beagle',
    'Beagle': 'Beagle',
    'Rottweilers': 'Rottweiler',
    'Rottweiler': 'Rottweiler',
    'Dachshunds': 'Dachshund',
    'Dachshund': 'Dachshund',
    'German Shorthaired Pointers': 'German Shorthaired Pointer',
    'Pointers (German Shorthaired)': 'German Shorthaired Pointer',
    'German Shorthaired Pointer': 'German Shorthaired Pointer',
    'Yorkshire Terriers': 'Yorkshire Terrier',
    'Yorkshire Terrier': 'Yorkshire Terrier',
    'Pembroke Welsh Corgis': 'Pembroke Welsh Corgi',
    'Boxers': 'Boxer',
    'Boxer': 'Boxer'
}

# Apply normalization
df['Breed_Normalized'] = df['Breed'].map(breed_mapping).fillna(df['Breed'])

# Filter to only include breeds that appear in multiple years (at least 3)
breed_counts = df['Breed_Normalized'].value_counts()
valid_breeds = breed_counts[breed_counts >= 3].index.tolist()
df_filtered = df[df['Breed_Normalized'].isin(valid_breeds)].copy()

# Get unique breeds and assign colors
unique_breeds = sorted(df_filtered['Breed_Normalized'].unique())
color_palette = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
]

# Create color mapping
color_scale = alt.Scale(
    domain=unique_breeds,
    range=color_palette[:len(unique_breeds)]
)

# Create selection for legend click - allows clicking on legend items
legend_selection = alt.selection_point(
    fields=['Breed_Normalized'],
    bind='legend'
)

# Create the line chart (bump chart)
lines = alt.Chart(df_filtered).mark_line(
    strokeWidth=2
).encode(
    x=alt.X('Year:O', 
            title='Year',
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Rank:Q',
            title='Rank',
            scale=alt.Scale(domain=[1, 10], reverse=True),  # Rank 1 at top, 10 at bottom
            axis=alt.Axis(tickCount=10, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
    color=alt.Color('Breed_Normalized:N',
                   scale=color_scale,
                   legend=alt.Legend(
                       title='Breed (click to highlight)',
                       columns=1,
                       symbolLimit=0,
                       labelLimit=200
                   )),
    opacity=alt.condition(
        legend_selection,
        alt.value(1.0),  # Bright when selected
        alt.value(0.15)  # Dim when not selected
    ),
    strokeWidth=alt.condition(
        legend_selection,
        alt.value(3),    # Thicker when selected
        alt.value(1.5)   # Thinner when not selected
    ),
    tooltip=[
        alt.Tooltip('Year:O', title='Year'),
        alt.Tooltip('Breed_Normalized:N', title='Breed'),
        alt.Tooltip('Rank:Q', title='Rank', format='d')
    ],
    order='Year'
).add_params(
    legend_selection
).properties(
    width=540,
    height=570
)

# Add points on the lines
points = alt.Chart(df_filtered).mark_circle(
    size=60
).encode(
    x=alt.X('Year:O'),
    y=alt.Y('Rank:Q', scale=alt.Scale(domain=[1, 10], reverse=True)),
    color=alt.Color('Breed_Normalized:N', scale=color_scale, legend=None),
    opacity=alt.condition(
        legend_selection,
        alt.value(1.0),  # Bright when selected
        alt.value(0.2)   # Dim when not selected
    ),
    tooltip=[
        alt.Tooltip('Year:O', title='Year'),
        alt.Tooltip('Breed_Normalized:N', title='Breed'),
        alt.Tooltip('Rank:Q', title='Rank', format='d')
    ]
).add_params(
    legend_selection
)

# Combine lines and points
chart = (lines + points).properties(
    title='Dog Breed Popularity Rankings (2015-2024)'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14,
    titleFontWeight='bold'
).configure_title(
    fontSize=16,
    fontWeight='bold',
    anchor='start'
).configure_legend(
    labelFontSize=11,
    titleFontSize=12,
    titleFontWeight='bold'
)

# Save as HTML
chart.save('viz3_bump_chart.html')

print("Visualization 3 saved to viz3_bump_chart.html")

