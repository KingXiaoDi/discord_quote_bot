import urllib.request
import json
import datetime
import time

def get_daily_info(*styles, show_all=False):
	id_dict = get_dailies(*styles)
	quest_name = {}
	skipped_id = {}
	skipped_quest_name = {}
	ordered = ['pve','pvp','wvw','fractals','special']
	print ("GW2 Dailies\t"+check_time())
	for style in ordered:
		skipped_id[style] = []
		skipped_quest_name[style] = []
		quest_name[style] = []
		if id_dict[style] != []:
			url = 'https://api.guildwars2.com/v2/achievements?ids=' + ','.join(str(x) for x in id_dict[style])
			page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
			page = page.replace('—', '-')
			data = json.loads(page)
			for quest in data:
				if 'Tier' in quest['name'] and '4' not in quest['name']:
					skipped_id[style].append(id_dict[style].pop())
					skipped_quest_name[style].append(quest['name'])
				else:
					quest_name[style].append(quest['name'])
	
			assert len(quest_name[style]) == len(id_dict[style]), "Warning: Lists of ID and name are not the same length. Type: "+style+"\tlen(ID): "+str(len(quest_name[style]))+"\t len(Name): "+str(len(id_dict[style]))
			assert len(skipped_quest_name[style]) == len(skipped_id[style]), "Warning: Lists of skipped ID and skipped name are not the same length. Type: "+style+"\t len(Skipped Name): "+str(len(skipped_name[style])) + "\t len(Skipped ID): "+str(len(skipped_id[style]))
			if len(skipped_id[style]) > 0:
				print ("\t{} ({}) [{} skipped]".format(style.capitalize(), len(id_dict[style]), len(skipped_id[style])))
			else:
				print ("\t{} ({})".format(style.capitalize(), len(id_dict[style])))
			for id, quest in zip(id_dict[style], quest_name[style]):
				print ('ID: '+'{:4d}\t {}'.format(id, quest))
			print ()
			if style == 'fractals':
				if show_all == True:
					print ("{} {} dailies separated due to tier level <> 4.".format(len(skipped_id[style]), style.capitalize()))
					for x, y in zip(skipped_id[style], skipped_quest_name[style]):
						print ('ID: '+'{:4d}\t {}'.format(x, y))
					print ()
				else:
					print ("{} dailies removed due to tier level <> 4. Include 'show_all=True' to show all dailies.".format(len(skipped_id[style])))
					print ()
					
def get_dailies(*styles):
	dailies = json.loads(urllib.request.urlopen('https://api.guildwars2.com/v2/achievements/daily').read().decode('utf-8'))
	daily_id_dict = {'pvp': [], 'pve': [], 'wvw': [], 'fractals': [], 'special': []}
	if styles == ():
		return empty_search(dailies, daily_id_dict)
	else:
		maxlength = 0
		for style in styles:
			if style.lower() in daily_id_dict.keys():
				for x in dailies[style]:
					if x['id'] not in daily_id_dict[style]:
						daily_id_dict[style].append(x['id'])
					daily_id_dict[style].sort()
				maxlength = max(maxlength, len(daily_id_dict[style]))
			else:
				print ("Sorry, I didn't understand '{}'".format(style))
		if maxlength == 0:
			print ("Sorry, I couldn't understand any of the quest type(s) you entered: "+', '.join(x for x in styles))
			print ("Since you didn't pass me a useable quest type ("+', '.join(x for x in daily_id_dict.keys())+"), I will return all dailies.")
			print ()
			return empty_search(dailies, daily_id_dict)	
		else:
			return daily_id_dict
			
def empty_search(dailies, daily_id_dict):
	for style in daily_id_dict.keys():
			for x in dailies[style]:
				if x['id'] not in daily_id_dict[style]:
					daily_id_dict[style].append(x['id'])
					daily_id_dict[style].sort()
	return (daily_id_dict)
		
def check_time():
	diff = int(time.strftime('%z'))
	hours_diff = diff/100
	return " [Valid until 0:00 UTC (20:00 EST/17:00 PST) on {}]".format(datetime.datetime.utcnow().date().strftime('%A %m/%d/%y'))

get_daily_info()
