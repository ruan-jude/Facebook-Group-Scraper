import pandas as pd
import gspread
import gspread_dataframe as gd
from oauth2client.service_account import ServiceAccountCredentials
from FacebookScraper import FacebookScraper

# Login info
payload = {
	'email': ''' Insert FB email ''',
	'pass': ''' Insert FB password '''   
}

# Data frame of scraped data
facebookData = pd.DataFrame(columns = ['First Name', 'Last Name', 'Join Date', 'Other Info'])

# Write data collected to Google Sheet through Google API
def dataToGoogleSheet(data):
    scope = [
        'https://spreadsheets.google.com/feeds', 
        'https://www.googleapis.com/auth/spreadsheets', 
        'https://www.googleapis.com/auth/drive.file', 
        'https://www.googleapis.com/auth/drive'
    ]

    # Create JSON on Google Cloud Services website
    creds = ServiceAccountCredentials.from_json_keyfile_name(''' Insert API credentials json ''', scope)
    client = gspread.authorize(creds)
    sheet = client.open(''' Insert sheets title ''').worksheet(''' Insert page title ''')
    gd.set_with_dataframe(sheet, facebookData)

    # Formats column headers
    sheet.format('A1:D1', {
        'horizontalAlignment': 'CENTER',
        'textFormat': {
            'fontSize': 14,
            'bold': True
        }
    })


# Start of runnable code
try:
    scraper = FacebookScraper(
        payload.get('email'), 
        payload.get('pass'), 
        ''' Insert FB group members URL '''
    )
    scraper.login()
    scraper.getMemberDetails()

    # Extracting data scraped and puts it in the DataFrame      
    for row in range(scraper.countMembers()):
        name = scraper.getName(row)
        firstName = name[ : name.find(' ')] if name.find(' ') >= 0 else name
        lastName = name[name.find(' ') + 1 : ] if name.find(' ') >= 0 else ''
        facebookData.loc[row] = [firstName, lastName, scraper.getJoined(row), scraper.getOther(row)]

    dataToGoogleSheet(facebookData)
finally:
    scraper.quit()
