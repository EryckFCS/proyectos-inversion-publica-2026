import requests
import json

TOKEN = 'f4dd70dfbc9497d25d834ec2fbeebfa132562b46'
BASE_URL = 'https://kf.kobotoolbox.org'
headers = {'Authorization': f'Token {TOKEN}', 'Content-Type': 'application/json'}
headers_dep = {'Authorization': f'Token {TOKEN}', 'Accept': 'application/json'}

res = requests.get(f'{BASE_URL}/api/v2/assets/a2BAHpQdZRvJy7vb8NndDU/', headers=headers)
content = res.json().get('content', {})
survey = content.get('survey', [])
choices = content.get('choices', [])

for idx in range(28, 35):
    sub_survey = [dict(x) for x in survey[:idx]]
    list_names = {q.get('select_from_list_name') for q in sub_survey if q.get('select_from_list_name')}
    sub_choices = [c for c in choices if c.get('list_name') in list_names]
    bg_count = sum(1 for q in sub_survey if q.get('type') == 'begin_group')
    eg_count = sum(1 for q in sub_survey if q.get('type') == 'end_group')
    while bg_count > eg_count:
        sub_survey.append({'type': 'end_group', 'name': f'close_{bg_count}'})
        eg_count += 1
    p = {'name': f'Test {idx}', 'asset_type': 'survey', 'content': json.dumps({'schema':'1','survey':sub_survey,'choices':sub_choices,'settings':{}})}
    r = requests.post(f'{BASE_URL}/api/v2/assets/', headers=headers, json=p)
    uid = r.json().get('uid')
    rd = requests.post(f'{BASE_URL}/api/v2/assets/{uid}/deployment/', headers=headers_dep, data={'active': 'true'})
    name_q = survey[idx-1].get('name')
    print(f"Item {idx} ({name_q}): status = {rd.status_code}")
