import urllib.request
import json
import datetime

def get_daily_info(id_list):
	url = 'https://api.guildwars2.com/v2/achievements?ids=' + ','.join(str(x) for x in id_list)
	page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
	if '—' in page:
		page = page.replace('—', '-')
	data = json.loads(page)
	quest_name = []
	skipped_counter = 0
	for quest in data:
		if 'Tier' in quest['name'] and '4' not in quest['name']:
			id_list.remove(quest['id'])
			skipped_counter += 1
		else:
			quest_name.append(quest['name'])
	assert len(quest_name) == len(id_list), "Warning: Lists of ID, name, requirements not all same length"
	print (str(datetime.datetime.now().strftime('%A %m/%d/%y'))+" Dailies ("+str(len(id_list))+") [Valid until 16:00 EST]:")
	print (str(skipped_counter)+" dailies removed due to tier level <> 4.")
	for i in range(len(id_list)):
		while len(str(id_list[i])) <4:
			id_list[i] = str(id_list[i])+' '
	counter = 0
	while counter < min(len(quest_name), len(id_list)):
		print ('ID: '+str(id_list[counter])+'\t'+quest_name[counter])
		counter += 1
	
def get_dailies():
	dailies = json.loads(urllib.request.urlopen('https://api.guildwars2.com/v2/achievements/daily').read().decode('utf-8'))
	id_list = []
	for x in dailies:
		for y in sorted(dailies[x], key = lambda x: x['id']):
			if y['id'] not in id_list:
				id_list.append(y['id'])
	id_list.sort()
	return id_list
	
get_daily_info(get_dailies())

