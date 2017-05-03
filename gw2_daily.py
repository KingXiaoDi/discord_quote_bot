import urllib.request
import json

def get_daily_info(id_list):
	base_url = 'https://api.guildwars2.com/v2/achievements?ids='
	url = base_url + ','.join(str(x) for x in id_list)
	page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
	if '—' in page:
		page = page.replace('—', '-')
	data = json.loads(page)
	quest_name = []
	for quest in data:
		if 'Tier' in quest['name'] and '4' not in quest['name']:
			id_list.remove(quest['id'])
		else:
			quest_name.append(quest['name'])
	assert len(quest_name) == len(id_list), "Warning: Lists of ID, name, requirements not all same length"
	for i in range(len(id_list)):
		while len(str(id_list[i])) <4:
			id_list[i] = str(id_list[i])+' '
	i = 0
	while i < min(len(quest_name), len(id_list)):
		print ('ID: '+str(id_list[i])+' '+quest_name[i])
		i += 1
			
def get_dailies():
	dailies_url = 'https://api.guildwars2.com/v2/achievements/daily'
	page = urllib.request.urlopen(dailies_url)
	dailies = json.loads(page.read().decode('utf-8'))
	id_list = []
	for x in dailies:
		sorted_dailies = sorted(dailies[x], key = lambda x: x['id'])
		for y in sorted_dailies:
			if y['id'] not in id_list:
				id_list.append(y['id'])
	id_list.sort()
	return id_list

get_daily_info(get_dailies())
