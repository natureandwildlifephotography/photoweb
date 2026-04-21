import re

filenames = [
    "Turdus migratorius - American Robin.jpg",
    "Passer domesticus.jpg",
    "Some photo.png"
]

def extract_species(filename):
    # Try to extract "Scientific Name" or "Common Name"
    # Looking at the pattern: "Species name - Common Name.jpg" or just "Species name.jpg"
    
    # Remove extension
    name_no_ext = os.path.splitext(filename)[0]
    
    # If it contains " - ", take everything before it
    if " - " in name_no_ext:
        return name_no_ext.split(" - ")[0].strip()
    
    # Otherwise return the whole name
    return name_no_ext.strip()

import os
for f in filenames:
    print(f"{f} -> {extract_species(f)}")
