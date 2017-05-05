import urllib.request
import json
import datetime
import time

def get_daily_info(*styles, show_all=False):
	id_list = get_dailies(*styles)
	url = 'https://api.guildwars2.com/v2/achievements?ids=' + ','.join(str(x) for x in id_list['IDs'])
	page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
	if '—' in page:
		page = page.replace('—', '-')
	data = json.loads(page)
	quest_name = []
	skipped_id = []
	skipped_name = []
	skipped_counter = 0
	for quest in data:
		if 'Tier' in quest['name'] and '4' not in quest['name']:
			skipped_id.append(id_list['IDs'].pop())
			skipped_name.append(quest['name'])
			skipped_counter += 1
		else:
			quest_name.append(quest['name'])
	assert len(quest_name) == len(id_list['IDs']), "Warning: Lists of ID and name are not the same length. len(ID): "+str(len(id_list))+"\t len(Name): "+str(len(quest_name))
	assert len(skipped_name) == len(skipped_id), "Warning: Lists of skipped ID and skipped name are not the same length. len(Skipped ID): "+str(len(skipped_id))+"\t len(Skipped Name): "+str(len(skipped_name))
	print ("GW2 Dailies ("+str(len(id_list['IDs']))+")"+check_time()+":")
	for id, quest in zip(id_list['IDs'], quest_name):
		print ('ID: '+'{:4d}\t {}'.format(id, quest))
	print ()
	if show_all == True:
		print (str(skipped_counter)+" dailies separated due to tier level <> 4.")
		for x, y in zip(skipped_id, skipped_name):
			print ('ID: '+'{:4d}\t {}'.format(x, y))
	else:
		print ({}+" dailies removed due to tier level <> 4. Include 'show_all=True' to show all dailies.".format(skipped_counter))

def get_dailies(*styles):
	dailies = json.loads(urllib.request.urlopen('https://api.guildwars2.com/v2/achievements/daily').read().decode('utf-8'))
	id_list = {'IDs': []}
	quest_types = {'pvp': [], 'pve': [], 'wvw': [], 'fractals': [], 'special': []}
	accepted = ['pvp', 'pve', 'wvw', 'fractals', 'special']
	if styles == ():
		order = ["pve", 'pvp', 'wvw', 'fractals', 'special']
		for x in order:
			for y in sorted(dailies[x], key = lambda x: x['id']):
				if y['id'] not in id_list:
					id_list['IDs'].append(y['id'])
		id_list['IDs'].sort()
		print (len(id_list))
		return (id_list)
#need a way to reject bad input'''
	else:
		try:
			for style in styles:
				if style.lower() in quest_types.keys():
					for x in dailies[style]:
						if x['id'] not in quest_types[style]:
							quest_types[style].append(x['id'])
					quest_types[style].sort()
			print (quest_types)
		except:
			print ("fail")

def check_time():
	diff = int(time.strftime('%z'))
	hours_diff = diff/100
	return " [Valid until 0:00 UTC (20:00 EST/17:00 PST) on {}]".format(datetime.datetime.utcnow().date().strftime('%A %m/%d/%y'))

get_daily_info(show_all=True)
