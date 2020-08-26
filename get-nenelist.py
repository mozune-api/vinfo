from apiclient.discovery import build
import config
import json
import os
from datetime import datetime


def max_date(str_date0, str_date1):
        dt0 = datetime.fromisoformat(str_date0)
        dt1 = datetime.fromisoformat(str_date1)
        if dt0 > dt1:
                return 0
        else:
                return 1
def init_list():
        return {'v1':[], 'last_update':"2020-08-12"}

def main():
        youtube = build('youtube', 'v3', developerKey=config.api_key)
        response = youtube.activities().list(
                part='snippet,contentDetails',
                channelId='UCAWSyEs_Io8MtpY3m-zqILA',
                maxResults=1000 
                ).execute()
        path_json = 'json/api.json'
        if os.path.isfile(path_json):
                with open(path_json) as f:
                        info_list = json.loads(f.read())
                if not('v1' in info_list):
                        info_list = init_list()
        else:
                info_list = init_list()
                
        for item in response['items']:
                s = item['snippet']
                if max_date(s['publishedAt'][0:10], info_list['last_update'][0:10]) == 1:
                        break
                c = item['contentDetails']['upload']
                info_list['v1'].append({'id': c['videoId'], 'publishedAt':s['publishedAt'], 'title':s['title']})
                #print({'id': c['videoId'], 'publishedAt':s['publishedAt'], 'title':s['title']})
        info_list['last_update'] = response['items'][0]['snippet']['publishedAt']
        text = json.dumps(info_list, sort_keys=True, ensure_ascii=False, indent=2)
        with open(path_json, 'w', encoding='utf-8') as f:
                f.write(text)

if __name__ == '__main__':
        main()