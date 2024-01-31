import os
import json
import time
import requests


targets = ['https://chat.openai.com/public-api/gizmos/discovery/trending',
'https://chat.openai.com/public-api/gizmos/discovery/research',
'https://chat.openai.com/public-api/gizmos/discovery/dalle',
'https://chat.openai.com/public-api/gizmos/discovery/writing',
'https://chat.openai.com/public-api/gizmos/discovery/productivity',
'https://chat.openai.com/public-api/gizmos/discovery/programming',
'https://chat.openai.com/public-api/gizmos/discovery/education',
'https://chat.openai.com/public-api/gizmos/discovery/lifestyle']

def get_trending_data(url):
    time.sleep(5)
    params = {
        'cursor': '0',
        'limit': '10',
        'locale': 'global'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return None



raw_data = []


# generate folder :yyyy-mm-dd
today_date = time.strftime("%Y-%m-%d", time.localtime())
folder = today_date
os.mkdir(folder)

content = f"# Today's Trending -- {today_date}\n\n"

# Navigate to yesterday
yesterday_folder = os.path.join("..", yesterday_date)
yesterday_file_path = os.path.join(yesterday_folder, "README.md")
content += "[yesterday](" + os.symlink(os.path.relpath(file_path, os.path.dirname(yesterday_file_path)), yesterday_file_path) + ")"
content += "\n"

# Navigate to tomorrow
tomorrow_folder = os.path.join("..", tomorrow_date)
tomorrow_file_path = os.path.join(tomorrow_folder, "README.md")
content += "[tomorrow](" + os.symlink(os.path.relpath(file_path, os.path.dirname(tomorrow_file_path)), tomorrow_file_path) + ")"
content += "\n\n"

for target in targets:
    time.sleep(10)
    data = get_trending_data(target)

    if not data:
        print(f"error in get {target}")
        continue 
    json_data = json.loads(data)
    gpt_type = json_data['info']['display_group']

    # maintain raw data
    json_data['type'] = gpt_type
    raw_data.append(json_data)

    # tranfsorm to markdown format
    content += '## ' + gpt_type + '\n'
    for item in json_data['list']['items']:
        name = item['resource']['gizmo']['display']['name']
        url = f"https://chat.openai.com/g/{item['resource']['gizmo']['short_url']}" 
        description = item['resource']['gizmo']['display']['description']
        content += f'- [{name}]({url}) {description}\n'
    content += '\n'

# save markdown file
with open(folder + '/README.md', 'w', encoding='utf-8') as f:
    f.write(content)
    

# save raw data
with open(folder + '/raw_data.json', 'w', encoding='utf-8') as f:
    json.dump(raw_data, f, ensure_ascii=False, indent=4)
