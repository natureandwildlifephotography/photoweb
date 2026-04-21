import os
import re

def extract_species(filename):
    # Remove extension
    name_no_ext = os.path.splitext(filename)[0]
    
    # Remove trailing numbers (including leading "-")
    # This regex matches " - " followed by digits at the end, or just digits at the end
    # Specifically, the user said "stripped from all numbers appearing at the end"
    
    # Let's test: "Turdus migratorius - American Robin-1.jpg" -> "Turdus migratorius - American Robin"
    # Wait, the user said "strip from ... filename ... at the end".
    # Previous logic extracted species name first.
    # Should I strip from the filename BEFORE extracting species, or just the species name part?
    
    # Re-reading: "strip from all numbers appearing at the end of the initial filename"
    
    # 1. Clean trailing numbers/dashes from filename
    name_no_ext = re.sub(r'[-\s]*\d+$', '', name_no_ext)
    
    # 2. Extract species name
    if " - " in name_no_ext:
        return name_no_ext.split(" - ")[0].strip()
    return name_no_ext.strip()

filenames = [
    "Turdus migratorius - American Robin-1.jpg",
    "Passer domesticus-22.jpg",
    "Some photo-123.png"
]

for f in filenames:
    print(f"{f} -> {extract_species(f)}")
