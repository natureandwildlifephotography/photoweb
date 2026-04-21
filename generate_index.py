import os
import csv

# Configuration
PHOTOS_DIR = 'Photos'
MASTER_LIST = 'Master-PhotoList - BirdPhotos.tsv'
OUTPUT_FILE = 'index-BirdCards.html'

def load_master_data():
    data = {}
    # Use utf-8 encoding for master data
    with open(MASTER_LIST, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            filename = row['Filename'].strip()
            data[filename] = row
    return data

def generate_html():
    master_data = load_master_data()
    
    # Group photos by species
    species_map = {}
    for photo in sorted(os.listdir(PHOTOS_DIR)):
        if photo.lower().endswith(('.jpg', '.jpeg', '.png')):
            data = master_data.get(photo, {})
            species = data.get('English Name', 'Unknown')
            if species not in species_map:
                species_map[species] = {'photos': [], 'data': data}
            species_map[species]['photos'].append(f"{PHOTOS_DIR}/{photo}")

    # Collect all families, orders, and species
    families = sorted({data.get('Family', 'Unknown') for item in species_map.values() for data in [item['data']]})
    orders = sorted({data.get('Order', 'Unknown') for item in species_map.values() for data in [item['data']]})
    all_species = sorted(species_map.keys())

    # Start HTML template
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Bird Photo Collection</title>
    <style>
        body {{ font-family: sans-serif; background: #f4f4f4; color: #333; margin: 0; padding: 0 20px 20px 20px; }}
        .banner {{ background: url('Banners/Banner_NWPca1.jpg') center/cover no-repeat; width: 100%; height: 313px; display: flex; flex-direction: column; justify-content: flex-end; padding: 20px; margin-bottom: 20px; border-radius: 0; }}
        .nav {{ display: flex; flex-wrap: wrap; gap: 20px; background: #fff; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 20px; }}
        .nav a {{ color: #333; text-decoration: none; font-weight: bold; padding: 8px 20px; border: 1px solid #333; border-radius: 5px; background: #f9f9f9; transition: background 0.2s; }}
        .nav a:hover {{ background: #eee; }}
        .header {{ margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .filters {{ display: flex; gap: 10px; align-items: center; }}
        .filter-element {{ height: 30px; }}
        .gallery {{ display: flex; flex-direction: column; gap: 20px; }}
        .card {{ background: #fff; border-radius: 12px; padding: 15px; border: 1px solid #ddd; display: flex; gap: 20px; }}
        .photo-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; width: 70%; }}
        .card img {{ width: 100%; height: auto; border-radius: 8px; -webkit-touch-callout: none; -webkit-user-select: none; user-select: none; }}
        .info {{ width: 30%; }}
        .name {{ font-weight: bold; font-size: 1.5em; color: #0056b3; margin-bottom: 10px; }}
        .meta {{ font-size: 1em; color: #555; margin-bottom: 5px; }}
        .hidden {{ display: none; }}
        /* Lightbox styles */
        #lightbox {{ display: none; position: fixed; z-index: 999; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); justify-content: center; align-items: center; }}
        #lightbox img {{ max-width: 95%; max-height: 95%; border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.5); }}
        #lightbox .close {{ position: absolute; top: 20px; right: 30px; color: #fff; font-size: 40px; font-weight: bold; cursor: pointer; user-select: none; }}
    </style>
</head>
<body>
    <div id="lightbox" onclick="closeLightbox()">
        <span class="close">&times;</span>
        <img id="lightbox-img" src="" oncontextmenu="return false;" ondragstart="return false;">
    </div>
    <div class="banner">
        <div style="background: rgba(255, 255, 255, 0.3); backdrop-filter: blur(5px); padding: 10px 40px; border-radius: 15px; border: 2px solid rgba(255, 255, 255, 0.4); align-self: flex-start; margin-bottom: auto; margin-top: auto; margin-left: 20px;">
            <h1 style="font-size: 5em; color: black; margin: 0; text-shadow: 1px 1px 5px rgba(255,255,255,0.5);">Gallery</h1>
        </div>
    </div>
    <div class="nav">
        <a href="https://www.natureandwildlifephotography.ca/home">Return to Nature Photography</a>
    </div>
    <div style="padding: 20px; background: #fff; margin-bottom: 20px; border-radius: 8px; border: 1px solid #ddd;">
        <h2>A Lifelong Journey Through the Avian World: 2,035 Species and Counting</h2>
        <p>This collection is more than a dataset; it is the culmination of a lifelong passion that began in the 1960s. Those early years were spent in the company of observation clubs, where the foundations of our birding knowledge were laid. That dedication followed us to Seattle, where we became active members of the local Audubon group, immersing ourselves in the rich birdlife of the Pacific Northwest.</p>
        <p>While the handwritten checklists of those formative decades have long since been lost to time, the spirit of those early observations lives on in our current work. Our "official" digital record began in eBird on August 12, 2005, with a sighting of the Common Ostrich in Tanzania. Since that milestone, we have traversed 20 countries across five continents, documenting a global odyssey through the remarkable diversity of the class Aves.</p>
        <p>The scope of this project is defined by its taxonomic completeness, representing every major lineage of birds currently recognized:</p>
        <ul>
            <li><strong>2,035 Unique Species:</strong> A testament to over twenty years of digital recording and a lifetime of field observation.</li>
            <li><strong>1,500+ Species Photographed:</strong> Our mission has evolved from simple observation to visual documentation, with high-quality photographs now captured for over 75% of our life list.</li>
            <li><strong>174 Families:</strong> A comprehensive look at the avian tree of life, from the tiny Hummingbirds (Trochilidae) to the ancient Cassowaries (Casuariidae).</li>
            <li><strong>41 Orders:</strong> Full representation across every primary branch of bird classification.</li>
        </ul>
        <p>From the lush rainforests of Panama to the rugged coasts of Australia, this page serves as a living record of our history. As we look toward our next expeditions, we invite you to explore the data and the imagery, sharing in a journey that began over sixty years ago and continues to look forward to the next horizon.</p>
    </div>
    <div class="header">
        <div class="filters">
            <div style="display: flex; flex-direction: column;">
                <h1>Bird Photo Collection</h1>
                <div id="stats" style="font-size: 0.9em; color: #555;">
                    <div>Species: <span id="speciesCount">0</span></div>
                    <div>Photos: <span id="photoCount">0</span></div>
                </div>
            </div>
            <button class="filter-element" onclick="resetFilters()">Reset</button>
            <div style="display: flex; flex-direction: column; gap: 5px;">
                <select class="filter-element" id="speciesFilter" onchange="filterGallery()">
                    <option value="">All Species</option>
                    {''.join([f'<option value="{s}">{s}</option>' for s in all_species])}
                </select>
                <select class="filter-element" id="familyFilter" onchange="filterGallery()">
                    <option value="">All Families</option>
                    {''.join([f'<option value="{f}">{f}</option>' for f in families])}
                </select>
                <select class="filter-element" id="orderFilter" onchange="filterGallery()">
                    <option value="">All Orders</option>
                    {''.join([f'<option value="{o}">{o}</option>' for o in orders])}
                </select>
            </div>
            <button class="filter-element" onclick="togglePrivateMode()" style="background: #f0f0f0; border: 1px solid #ccc; color: #333;">LogIn</button>
        </div>
    </div>
    <script>
        let isPrivate = false;
        function togglePrivateMode() {{
            const password = prompt("Enter password:");
            if (password === "123456+++") {{
                isPrivate = !isPrivate;
                alert("Private mode is now " + (isPrivate ? "ON" : "OFF"));
                // Update existing images
                document.querySelectorAll('.photo-grid img').forEach(img => {{
                    if (isPrivate) {{
                        img.style.cursor = 'pointer';
                        img.onclick = () => openLightbox(img.src);
                    }} else {{
                        img.style.cursor = 'default';
                        img.onclick = null;
                    }}
                }});
            }} else {{
                alert("Incorrect password.");
            }}
        }}
        function openLightbox(src) {{
            const lb = document.getElementById('lightbox');
            const lbImg = document.getElementById('lightbox-img');
            lbImg.src = src;
            lb.style.display = 'flex';
        }}
        function closeLightbox() {{
            document.getElementById('lightbox').style.display = 'none';
        }}
    </script>
    <div class="gallery" id="gallery">
"""
    
    # Create cards
    for species in all_species:
        item = species_map[species]
        data = item['data']
        family = data.get('Family', 'Unknown')
        order = data.get('Order', 'Unknown')
        num_photos = len(item['photos'])
        
        img_tags = "".join([f'<img src="{p}" alt="{species}" loading="lazy" oncontextmenu="return false;" ondragstart="return false;">' for p in item['photos']])
        
        html += f"""        <div class="card" data-species="{species}" data-family="{family}" data-order="{order}" data-photos="{num_photos}">
            <div class="info">
                <div class="name">{species}</div>
                <div class="meta">French: {data.get('French Name', 'N/A')}</div>
                <div class="meta">Latin: <i>{data.get('Latin Name', 'N/A')}</i></div>
                <div class="meta">Order: {order}</div>
                <div class="meta">Family: {family}</div>
            </div>
            <div class="photo-grid">
                {img_tags}
            </div>
        </div>
"""
            
    html += """    </div>
    <script>
        function resetFilters() {
            document.getElementById('speciesFilter').value = "";
            document.getElementById('familyFilter').value = "";
            document.getElementById('orderFilter').value = "";
            filterGallery();
        }
        function filterGallery() {
            const speciesFilter = document.getElementById('speciesFilter').value;
            const familyFilter = document.getElementById('familyFilter').value;
            const orderFilter = document.getElementById('orderFilter').value;
            const cards = document.getElementsByClassName('card');
            let speciesCount = 0;
            let photoCount = 0;
            
            for (let card of cards) {
                const matchesSpecies = (speciesFilter === "" || card.getAttribute('data-species') === speciesFilter);
                const matchesFamily = (familyFilter === "" || card.getAttribute('data-family') === familyFilter);
                const matchesOrder = (orderFilter === "" || card.getAttribute('data-order') === orderFilter);
                
                if (matchesSpecies && matchesFamily && matchesOrder) {
                    card.classList.remove('hidden');
                    speciesCount++;
                    photoCount += parseInt(card.getAttribute('data-photos'));
                } else {
                    card.classList.add('hidden');
                }
            }
            document.getElementById('speciesCount').textContent = speciesCount;
            document.getElementById('photoCount').textContent = photoCount;
        }
        // Initial count
        filterGallery();
    </script>
</body>
</html>
"""
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Successfully generated {OUTPUT_FILE}")

    # Also save a duplicate named index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Update for GitHub publishing (replacing local path with R2 URL)
    import subprocess
    subprocess.run(["sed", "-i", "", "s|Photos/|https://pub-4676f40b75f648d9a6625ba16135e8a6.r2.dev/|g", "index.html"])
    subprocess.run(["sed", "-i", "", "s|Banners/|https://pub-4676f40b75f648d9a6625ba16135e8a6.r2.dev/Banners/|g", "index.html"])
    
    # Save index.html again (reading the updated content and writing it back as requested)
    with open('index.html', 'r', encoding='utf-8') as f:
        updated_html = f.read()
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print("Successfully generated and updated index.html for GitHub")

if __name__ == "__main__":
    generate_html()
