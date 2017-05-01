import urllib.request
import datetime
import json

'''need to update to version 1.01 from home PC'''

def get_daily_info(id_list):
	base_url = 'https://api.guildwars2.com/v2/achievements?ids='
	url = base_url + ','.join(str(x) for x in id_list)
	page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
	if '—' in page:
		page = page.replace('—', '-')
	data = json.loads(page)
	quest_name = []
	to_complete = []
	bits = []
	for quest in data:
		tier = ''
		quest_name.append(quest['name'])
		if '  ' in quest['requirement']:
			for y in quest['tiers']:
				tier += str(y['count']) + '/'
				tier = tier[:-1]
			req = quest['requirement'].split('  ')
			merged = str(req[0]+" "+tier+" "+req[1])
			to_complete.append(merged)
		else:
			to_complete.append(quest['requirement'])
		if 'bits' in quest:
			quest_bits = []
			for each in quest['bits']:
				quest_bits.append(each['text'])
			bits.append(quest_bits)
		else:
			bits.append(' ')
	assert len(quest_name) == len(to_complete) == len(id_list), "Warning: Lists of ID, name, requirements not all same length"
	min_length = min(len(quest_name), len(to_complete), len(id_list))
	i = 0
	print (str(datetime.datetime.now().strftime('%A %m/%d/%y')+" Dailies:")
	while i < min_length:
		print ('ID: '+str(id_list[i])+' '+quest_name[i]+': '+to_complete[i])
		print (bits[i])
		print ()
		i += 1
			
def get_dailies():
	dailies_url = 'https://api.guildwars2.com/v2/achievements/daily'
	page = urllib.request.urlopen(dailies_url)
	dailies = json.loads(page.read().decode('utf-8'))
	idlist = []
	for x in dailies:
		sorted_dailies = sorted(dailies[x], key = lambda x: x['id'])
		for y in sorted_dailies:
			idlist.append(y['id'])
	idlist.sort()
	return idlist

get_daily_info(get_dailies())
