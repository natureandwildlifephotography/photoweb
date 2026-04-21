
def compare_columns():
    audited_names = set()
    english_names = set()

    with open('Master-PhotoList - BirdPhotos.tsv', 'r', encoding='latin-1') as f:
        header = f.readline().split('\t')
        audited_idx = header.index('AuditedName')
        english_idx = header.index('English Name')

        for line in f:
            parts = line.split('\t')
            if len(parts) > max(audited_idx, english_idx):
                audited = parts[audited_idx].strip()
                english = parts[english_idx].strip()
                
                if audited: audited_names.add(audited)
                if english: english_names.add(english)

    print(f"AuditedName count: {len(audited_names)}")
    print(f"English Name count: {len(english_names)}")

    missing_in_english = audited_names - english_names
    missing_in_audited = english_names - audited_names

    if not missing_in_english and not missing_in_audited:
        print("Perfect match!")
    else:
        if missing_in_english:
            print(f"\nMissing in English Name ({len(missing_in_english)}):")
            for name in sorted(list(missing_in_english)):
                print(f"  {name}")
        
        if missing_in_audited:
            print(f"\nMissing in AuditedName ({len(missing_in_audited)}):")
            for name in sorted(list(missing_in_audited)):
                print(f"  {name}")

if __name__ == "__main__":
    compare_columns()
