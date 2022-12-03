import pandas as pd
import json,requests,time,pickle


with open('git_token.json') as f:
    cred = json.load(f)

user = cred.get('user')
token = cred.get('token')
json_file = 'responses.json'

required_repos = 200000
repos = list()
len_repos = len(repos)
since = 0
header = {
    'Authorization': f'Token {token}'
}

while len_repos < required_repos:
    x = requests.get(f'https://api.github.com/repositories?since={since}',headers=header)
    if 'message' in x.json():
        print('sleeping for 1 hour...........')
        time.sleep(3600)
        continue
    repos.extend(x.json())
    len_repos = len(repos)
    print(since,len_repos)
    since += 1
    if not (len_repos % 10000):
        with open(json_file, 'w') as f:
            json.dump(repos, f)
        print('saved..........')

df = pd.read_json(json_file)

languages_url = df['languages_url']
all_language_responses = list()

for idx,i in enumerate(df['languages_url']):
    x = requests.get(i,headers=header)
    all_language_responses.append(x)
    print(idx,i,x)

with open('languages.pkl','w') as f:
    pickle.dump(all_language_responses,f)
    print('pickle saved')

languages = [i.json() for i in all_language_responses]
df['languages'] = languages
df.to_csv('responses.csv')

