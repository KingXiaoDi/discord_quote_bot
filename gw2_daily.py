import urllib.request
import json
'''To Do:
	-find dictionary with quest IDs and quest names
	-implement dynamnic sorting?
'''

def request_dailies():
	with open('gw2.json', 'r') as f:
		dailies = json.loads(f.read())
		return dailies
	#commented out due to firewall issues, comment in for real use. Code was tested once and worked, but not sure if this is the correct URL
	url = "https://api.guildwars2.com/v2/achievements/daily"
	#page = urllib.request.urlopen(url)
	#dailies = json.loads(page.read().decode('utf-8'))

#tell quotebot your level, the category of daily you want, if you want to see all dailies, and how to sort the dailies
def quote_bot_line(level, cat='', showall=False, sortby=''):
	'''Accepts an integer level, and three optional parameters: a category of daily, a showall boolean, and a 'sort by' string [yet to be implemented].
	Checks inputs for errors then calls get_dailies() for the category passed (or all types).'''
	try:
		int(level)
	except (ValueError, SyntaxError):
		print ("You entered '{}' as your level. Please enter an integer level.".format(level))
		quit()
	if level not in range(1,101):
		print ("Warning: unacceptable level ('{}'). Please enter an integer between 0 and 100.".format(level))
	dailies = request_dailies()
	if cat == '' or showall == True:
		for cat in dailies:
			get_dailies(level, cat, showall, dailies)
	else:
		try:
			c = cat.lower()
			get_dailies(level, c, showall, dailies)
		except KeyError:
			print ("You entered an invalid category! Acceptable categories: pve, pvp, wvw, fractals, special")
			quit()

def get_dailies(level, cat, showall, dailies):
	'''Accepts integer level, type string, and showall booelan from quote_bot_line(). Prints sorted dailies matching input criteria.'''
	print (cat.upper())
	sorted_dailies = sorted(dailies[cat], key = lambda x: x['level']['min'])
	for x in sorted_dailies:
		if showall == True:
			print ('ID: {0}\tLevel: [{1},{2}]\tNeeded: {3}'.format(x['id'], x['level']['min'], x['level']['max'], x['required_access']))
		else:
			if level in range(int(x['level']['min']), int(x['level']['max'])):
				print ('ID: {0}\tLevel: [{1},{2}]\tNeeded: {3}'.format(x['id'], x['level']['min'], x['level']['max'], x['required_access']))
	print ()
	
def make_id_list(daily_list, idlist):
	idlist.append(daily_list['id'])
	return idlist

quote_bot_line(1, showall=True)
