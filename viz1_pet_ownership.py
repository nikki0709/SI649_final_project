"""
Visualization 1: Pet Ownership Bar Chart
Creates an interactive bar chart showing pet ownership in U.S. households
Bar length shows millions of households, color intensity shows percentages
"""

import pandas as pd
import altair as alt

# Load data from CSV
df = pd.read_csv('datasets/2024_pet_ownership_full.csv')

# Clean up the species name for "Small mammals"
df['Species'] = df['Species'].str.replace('Small mammals (gerbils, hamsters, etc.)', 'Small mammals', regex=False)

# Parse the millions column - remove 'M' and convert to float
df['Millions'] = df['Millions_US_Households_Owning'].str.rstrip('M').astype(float)

# Sort by millions (descending)
df = df.sort_values('Millions', ascending=False)

# Create the bar chart
# Bar length shows millions of households, color intensity shows percentages
chart = alt.Chart(df).mark_bar(
    size=50,
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x=alt.X('Species:N', 
            title='Pet Type',
            axis=alt.Axis(
                labelAngle=-45, 
                labelAlign='right',
                labelFontSize=12,
                labelLimit=150,
                titleFontSize=14,
                titleFontWeight='bold',
                labelPadding=5
            )),
    y=alt.Y('Millions:Q',
            title='Millions of U.S. Households',
            scale=alt.Scale(domain=[0, 65])),
    color=alt.Color('Percent_US_Households_Owning:Q',
                   title='Percentage (%)',
                   scale=alt.Scale(
                       domain=[0, 50],
                       scheme='blues',
                       reverse=False
                   ),
                   legend=alt.Legend(
                       title='Percentage (%)',
                       format='.1f',
                       titleFontSize=12,
                       labelFontSize=11
                   )),
    tooltip=[
        alt.Tooltip('Species:N', title='Pet Type'),
        alt.Tooltip('Millions:Q', title='Millions of Households', format='.1f'),
        alt.Tooltip('Percent_US_Households_Owning:Q', title='Percentage', format='.1f')
    ]
).properties(
    width=600,
    height=390,
    title='Pet Ownership in U.S. Households (2024)'
)

# Add text labels on bars showing millions
text = alt.Chart(df).mark_text(
    align='center',
    baseline='bottom',
    dy=-5,
    fontSize=12,
    fontWeight='bold',
    color='#2c3e50'
).encode(
    x=alt.X('Species:N'),
    y=alt.Y('Millions:Q'),
    text=alt.Text('Millions:Q', format='.1f')
)

# Combine chart and text
final_chart = (chart + text).resolve_scale(color='independent').configure_axis(
    labelFontSize=12,
    titleFontSize=14,
    titleFontWeight='bold'
).configure_title(
    fontSize=16,
    fontWeight='bold',
    anchor='start'
).configure_view(
    strokeWidth=0,
    continuousHeight=500,
    continuousWidth=650
)

# Save as HTML
final_chart.save('viz1_pet_ownership.html')

print("Visualization 1 saved to viz1_pet_ownership.html")

