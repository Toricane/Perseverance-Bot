from apiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyAwsUxCA0P_SGoHiVVk3Bmva9hGEg3v4j0'
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

ids = '5rC0qpLGciU,LgbuxTfJFr0'
results = youtube.videos().list(id=ids, part='snippet').execute()
for result in results.get('items', []):
    print(result['id'])
    print(result['snippet']['description'])
    print(result['snippet']['title'])