import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '17SY2T7CvlO5zO_vR0RuVogWyZd5IJI_KWzHKedFoy1g'
RANGE_NAME = 'BirdPhotos!A1'

def get_sheets_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        try:
            with open('token.json', 'rb') as token:
                creds = pickle.load(token)
        except Exception:
            # If pickle fails, maybe it's not a pickle file or outdated
            pass

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

def generate_file_list():
    source_dir = 'New-photos'
    output_file = 'Files_In_New-photos.txt'
    
    if not os.path.exists(source_dir):
        print(f"Error: Directory '{source_dir}' not found.")
        return

    # Get all files, excluding hidden files like .DS_Store
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and not f.startswith('.')]
    files.sort()

    if not files:
        print("No new photos found in New-photos/.")
        return

    try:
        # 1. Create Files_In_New-photos.txt
        with open(output_file, 'w', encoding='utf-8') as f:
            for filename in files:
                f.write(filename + '\n')
        print(f"Successfully created {output_file} with {len(files)} files.")

        # 2. Append new entries to FilesInPhotos.txt
        master_output_file = 'FilesInPhotos.txt'
        with open(master_output_file, 'a', encoding='utf-8') as f:
            for filename in files:
                f.write(filename + '\n')
        print(f"Successfully appended {len(files)} entries to {master_output_file}.")

        # 3. Append to Google Sheet
        print("Connecting to Google Sheets...")
        service = get_sheets_service()
        
        # Extract species name (before " - " or the whole name if not present)
        # Strips trailing numbers (and preceding dashes/spaces) from filename first.
        import re
        def extract_species(filename):
            name_no_ext = os.path.splitext(filename)[0]
            name_no_ext = re.sub(r'[-\s]*\d+$', '', name_no_ext)
            if " - " in name_no_ext:
                return name_no_ext.split(" - ")[0].strip()
            return name_no_ext.strip()
            
        values = [[f, extract_species(f)] for f in files]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption='RAW', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended to Google Sheet.")

    except Exception as e:
        print(f"Error: {e}")
    
    print("\nOpen Master-PhotoList (Google Sheet) copy the missing formulas in the added rows, and to verify that the English Names in columns C and D are matching.  Non matching names reveal inconsistencies in the naming of the species.  Correct before proceeding. Also, sort the entire sheet on Column A by alphabetical order.")
    print("Check the results")

if __name__ == "__main__":
    generate_file_list()
