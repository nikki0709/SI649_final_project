"""
Generate all visualizations for the SI649 Narrative Visualization Project
Run this script to regenerate all three visualizations from the datasets
"""

import subprocess
import sys

print("Generating all visualizations...")
print("-" * 50)

# Generate Visualization 1
print("\n1. Generating Pet Ownership Bar Chart...")
try:
    subprocess.run([sys.executable, "viz1_pet_ownership.py"], check=True)
    print("   ✓ Visualization 1 created successfully")
except subprocess.CalledProcessError as e:
    print(f"   ✗ Error generating Visualization 1: {e}")
    sys.exit(1)

# Generate Visualization 2
print("\n2. Generating Regional Devotion Map...")
try:
    subprocess.run([sys.executable, "viz2_regional_map.py"], check=True)
    print("   ✓ Visualization 2 created successfully")
except subprocess.CalledProcessError as e:
    print(f"   ✗ Error generating Visualization 2: {e}")
    sys.exit(1)

# Generate Visualization 3
print("\n3. Generating Breed Rankings Bump Chart...")
try:
    subprocess.run([sys.executable, "viz3_bump_chart.py"], check=True)
    print("   ✓ Visualization 3 created successfully")
except subprocess.CalledProcessError as e:
    print(f"   ✗ Error generating Visualization 3: {e}")
    sys.exit(1)

print("\n" + "-" * 50)
print("All visualizations generated successfully!")
print("\nOpen index.html in a web browser to view the article with visualizations.")

