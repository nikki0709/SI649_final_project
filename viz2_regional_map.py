"""
Visualization 2: Regional Preference Map
Creates an interactive US map showing states with the most devoted dog owners
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

# Load data from CSV
df = pd.read_csv('datasets/data-VJH4o.csv')

# Clean up percentage columns - remove % sign and convert to float
df['Breakup_Percent'] = df['Percentage of dog owners who broke up with a significant other who didn\'t like their dog'].str.rstrip('%').astype(float)
df['Moved_Percent'] = df['Percentage of dog owners who moved from an apartment to a house so their dog would have a yard'].str.rstrip('%').astype(float)

# Create the choropleth map
fig = go.Figure(data=go.Choropleth(
    locations=df['State Abbreviations'],  # State abbreviations
    z=df['Score'],  # Data to be color-coded
    locationmode='USA-states',  # Set to plot as US states
    colorscale='YlOrRd',  # Yellow-Orange-Red color scale
    text=df.apply(lambda row: f"{row['State']}<br>" +
                  f"Devotion Score: {row['Score']:.2f}<br>" +
                  f"Rank: #{row['Rank']}<br>" +
                  f"Moved for dog: {row['Moved_Percent']:.1f}%<br>" +
                  f"Broke up over dog: {row['Breakup_Percent']:.1f}%", axis=1),
    hovertemplate='%{text}<extra></extra>',
    colorbar=dict(
        title=dict(text="Devotion<br>Score", font=dict(size=12, weight='bold')),
        tickfont=dict(size=11),
        thickness=15,
        len=0.5,
        x=1.02,
        xpad=5
    ),
    marker_line_color='white',
    marker_line_width=1
))

# Update layout
fig.update_layout(
    title={
        'text': 'Dog Owner Devotion by State',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 16, 'color': '#2c3e50', 'weight': 'bold'}
    },
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
        bgcolor='rgba(0,0,0,0)'
    ),
    width=800,
    height=600,
    margin=dict(l=0, r=0, t=50, b=0),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Configure the modebar to match Visualization 1's interactive style
config = {
    'modeBarButtonsToAdd': ['downloadImage'],
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'dog_owner_devotion_map',
        'height': 600,
        'width': 900,
        'scale': 1
    }
}

# Get HTML string
html_string = fig.to_html(include_plotlyjs='cdn', config=config)

# Prepare state data for JavaScript
state_data = df.to_dict('records')
for record in state_data:
    record['Score'] = float(record['Score'])
    record['Breakup_Percent'] = float(record['Breakup_Percent'])
    record['Moved_Percent'] = float(record['Moved_Percent'])

# Add comparison panel CSS and JavaScript
comparison_panel_html = """
<style>
.comparison-panel {
    position: absolute;
    top: 60px;
    right: 20px;
    background: white;
    border: 2px solid #2c3e50;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    min-width: 280px;
    max-width: 320px;
    z-index: 1000;
    font-family: Arial, sans-serif;
    font-size: 12px;
    display: none;
}

.comparison-panel.active {
    display: block;
}

.comparison-panel h3 {
    margin: 0 0 15px 0;
    color: #2c3e50;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 2px solid #3498db;
    padding-bottom: 8px;
}

.comparison-instruction {
    color: #7f8c8d;
    font-size: 11px;
    font-style: italic;
    margin-bottom: 15px;
    padding: 8px;
    background: #f8f9fa;
    border-radius: 4px;
}

.state-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin-bottom: 15px;
}

.state-box {
    border: 2px solid #ecf0f1;
    border-radius: 6px;
    padding: 10px;
    background: #f8f9fa;
}

.state-box.selected {
    border-color: #3498db;
    background: #ebf5fb;
}

.state-name {
    font-weight: bold;
    font-size: 13px;
    color: #2c3e50;
    margin-bottom: 8px;
    text-align: center;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    font-size: 11px;
}

.metric-label {
    color: #7f8c8d;
}

.metric-value {
    font-weight: bold;
    color: #2c3e50;
}

.comparison-diff {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #ecf0f1;
    font-size: 11px;
}

.diff-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.diff-positive {
    color: #27ae60;
}

.diff-negative {
    color: #e74c3c;
}

.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 18px;
    color: #95a5a6;
    cursor: pointer;
    padding: 0;
    width: 20px;
    height: 20px;
    line-height: 20px;
}

.close-btn:hover {
    color: #2c3e50;
}

.plotly-container {
    position: relative;
}
</style>

<div class="comparison-panel" id="comparison-panel">
    <button class="close-btn" onclick="closeComparison()">×</button>
    <h3>State Comparison</h3>
    <div class="comparison-instruction" id="comparison-instruction">
        Click two states on the map to compare them
    </div>
    <div class="state-comparison" id="state-comparison" style="display: none;">
        <div class="state-box" id="state1-box">
            <div class="state-name" id="state1-name">-</div>
            <div class="metric-row">
                <span class="metric-label">Devotion Score:</span>
                <span class="metric-value" id="state1-score">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Rank:</span>
                <span class="metric-value" id="state1-rank">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Moved for dog:</span>
                <span class="metric-value" id="state1-moved">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Broke up over dog:</span>
                <span class="metric-value" id="state1-breakup">-</span>
            </div>
        </div>
        <div class="state-box" id="state2-box">
            <div class="state-name" id="state2-name">-</div>
            <div class="metric-row">
                <span class="metric-label">Devotion Score:</span>
                <span class="metric-value" id="state2-score">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Rank:</span>
                <span class="metric-value" id="state2-rank">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Moved for dog:</span>
                <span class="metric-value" id="state2-moved">-</span>
            </div>
            <div class="metric-row">
                <span class="metric-label">Broke up over dog:</span>
                <span class="metric-value" id="state2-breakup">-</span>
            </div>
        </div>
        <div class="comparison-diff" id="comparison-diff" style="display: none;">
            <div class="diff-row">
                <span>Score Difference:</span>
                <span id="diff-score">-</span>
            </div>
            <div class="diff-row">
                <span>Moved % Difference:</span>
                <span id="diff-moved">-</span>
            </div>
            <div class="diff-row">
                <span>Breakup % Difference:</span>
                <span id="diff-breakup">-</span>
            </div>
        </div>
    </div>
</div>

<script>
var stateData = """ + json.dumps(state_data) + """;

var selectedStates = [];
var originalColors = null;
var originalLineWidths = null;

function getStateByAbbr(abbr) {
    return stateData.find(function(s) { return s['State Abbreviations'] === abbr; });
}

function closeComparison() {
    document.getElementById('comparison-panel').classList.remove('active');
    selectedStates = [];
    resetMapHighlight();
}

function resetMapHighlight() {
    var gd = document.querySelector('.plotly-graph-div');
    if (!gd || !gd.data) return;
    
    // Reset to original colors
    if (originalColors) {
        Plotly.restyle(gd, {
            'marker.line.color': [originalColors],
            'marker.line.width': [originalLineWidths || 1]
        }, [0]);
    }
}

function highlightStates(stateAbbrs) {
    var gd = document.querySelector('.plotly-graph-div');
    if (!gd || !gd.data) return;
    
    // Get current line colors and widths
    var currentData = gd.data[0];
    var locations = currentData.locations;
    
    // Store original if not already stored
    if (!originalColors) {
        originalColors = currentData.marker.line.color || 'white';
        originalLineWidths = currentData.marker.line.width || 1;
    }
    
    // Create new line colors and widths
    var newLineColors = locations.map(function(abbr) {
        return stateAbbrs.indexOf(abbr) >= 0 ? '#3498db' : 'white';
    });
    
    var newLineWidths = locations.map(function(abbr) {
        return stateAbbrs.indexOf(abbr) >= 0 ? 3 : 1;
    });
    
    Plotly.restyle(gd, {
        'marker.line.color': [newLineColors],
        'marker.line.width': [newLineWidths]
    }, [0]);
}

function updateComparisonPanel() {
    var panel = document.getElementById('comparison-panel');
    var instruction = document.getElementById('comparison-instruction');
    var comparison = document.getElementById('state-comparison');
    var diff = document.getElementById('comparison-diff');
    
    if (selectedStates.length === 0) {
        panel.classList.remove('active');
        return;
    }
    
    panel.classList.add('active');
    
    if (selectedStates.length === 1) {
        instruction.style.display = 'block';
        instruction.textContent = 'Click another state to compare';
        comparison.style.display = 'none';
        diff.style.display = 'none';
    } else if (selectedStates.length === 2) {
        instruction.style.display = 'none';
        comparison.style.display = 'grid';
        diff.style.display = 'block';
        
        var state1 = getStateByAbbr(selectedStates[0]);
        var state2 = getStateByAbbr(selectedStates[1]);
        
        // Update state 1
        document.getElementById('state1-name').textContent = state1.State;
        document.getElementById('state1-score').textContent = state1.Score.toFixed(2);
        document.getElementById('state1-rank').textContent = '#' + state1.Rank;
        document.getElementById('state1-moved').textContent = state1.Moved_Percent.toFixed(1) + '%';
        document.getElementById('state1-breakup').textContent = state1.Breakup_Percent.toFixed(1) + '%';
        document.getElementById('state1-box').classList.add('selected');
        
        // Update state 2
        document.getElementById('state2-name').textContent = state2.State;
        document.getElementById('state2-score').textContent = state2.Score.toFixed(2);
        document.getElementById('state2-rank').textContent = '#' + state2.Rank;
        document.getElementById('state2-moved').textContent = state2.Moved_Percent.toFixed(1) + '%';
        document.getElementById('state2-breakup').textContent = state2.Breakup_Percent.toFixed(1) + '%';
        document.getElementById('state2-box').classList.add('selected');
        
        // Calculate differences
        var scoreDiff = state1.Score - state2.Score;
        var movedDiff = state1.Moved_Percent - state2.Moved_Percent;
        var breakupDiff = state1.Breakup_Percent - state2.Breakup_Percent;
        
        document.getElementById('diff-score').textContent = (scoreDiff >= 0 ? '+' : '') + scoreDiff.toFixed(2);
        document.getElementById('diff-score').className = scoreDiff >= 0 ? 'diff-positive' : 'diff-negative';
        
        document.getElementById('diff-moved').textContent = (movedDiff >= 0 ? '+' : '') + movedDiff.toFixed(1) + '%';
        document.getElementById('diff-moved').className = movedDiff >= 0 ? 'diff-positive' : 'diff-negative';
        
        document.getElementById('diff-breakup').textContent = (breakupDiff >= 0 ? '+' : '') + breakupDiff.toFixed(1) + '%';
        document.getElementById('diff-breakup').className = breakupDiff >= 0 ? 'diff-positive' : 'diff-negative';
        
        // Highlight states on map
        highlightStates(selectedStates);
    }
}

// Wait for Plotly to initialize, then add click handler
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var gd = document.querySelector('.plotly-graph-div');
        if (!gd) return;
        
        gd.on('plotly_click', function(data) {
            if (data.points && data.points.length > 0) {
                var clickedState = data.points[0].location;
                
                // If clicking the same state, deselect it
                var index = selectedStates.indexOf(clickedState);
                if (index >= 0) {
                    selectedStates.splice(index, 1);
                } else {
                    // Add state (max 2)
                    if (selectedStates.length < 2) {
                        selectedStates.push(clickedState);
                    } else {
                        // Replace first state with new one
                        selectedStates[0] = selectedStates[1];
                        selectedStates[1] = clickedState;
                    }
                }
                
                updateComparisonPanel();
            }
        });
    }, 500);
});
</script>
"""

# Insert comparison panel before closing body tag
html_string = html_string.replace('</body>', comparison_panel_html + '</body>')

# Wrap plotly container
html_string = html_string.replace(
    '<div id="',
    '<div class="plotly-container"><div id="'
)
html_string = html_string.replace(
    '</div>\n</body>',
    '</div></div>\n</body>'
)

# Write the modified HTML
with open('viz2_regional_map.html', 'w', encoding='utf-8') as f:
    f.write(html_string)

print("Visualization 2 saved to viz2_regional_map.html with State Comparison Mode")

