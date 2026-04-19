
def get_files_from_photos():
    with open('FilesInPhotos.txt', 'r') as f:
        return {line.strip() for line in f if line.strip()}

def get_files_from_master():
    files = set()
    with open('Master-FotoList.txt', 'r', encoding='latin-1') as f:
        next(f)  # Skip header
        for line in f:
            parts = line.split('\t')
            if parts and parts[0].strip():
                files.add(parts[0].strip())
    return files

def compare():
    photos_files = get_files_from_photos()
    master_files = get_files_from_master()

    print(f"FilesInPhotos.txt count: {len(photos_files)}")
    print(f"Master-FotoList.txt count: {len(master_files)}")

    missing_in_master = photos_files - master_files
    missing_in_photos = master_files - photos_files

    if not missing_in_master and not missing_in_photos:
        print("Perfect match!")
    else:
        if missing_in_master:
            print(f"\nMissing in Master-FotoList.txt ({len(missing_in_master)}):")
            for f in sorted(list(missing_in_master)):
                print(f"  {f}")
        
        if missing_in_photos:
            print(f"\nMissing in FilesInPhotos.txt ({len(missing_in_photos)}):")
            for f in sorted(list(missing_in_photos)):
                print(f"  {f}")

if __name__ == "__main__":
    compare()
