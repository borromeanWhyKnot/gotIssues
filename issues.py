import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import os
import sys

Version = "1.3.5 (modifications by y0)"
print("This is Version: "+str(Version))

UserAgent = input("Please enter your main nations name: ")
filename = input("Please enter the puppet list source file. " \
	"Note that this is case sensitive: ")
pulleventmode = input("Would you like to open packs in line " \
	"while you answer issues (yes or no): ")

if(pulleventmode == 'y' or pulleventmode == 'yes'):
	pulleventmode = True
else:
	pulleventmode = False

#Pulleventcard=input("Would you like to pull event a card inline with these packs? (yes or no):")


# if(Pulleventcard == "yes"):
# 	pulleventcardID=input("What is the ID of the card you want to Pull Event: ")
# 	pulleventcardSeason=input("What is the season of the card you want to Pull Event: ")


names = []
password = []
MAX_PACKS = 9

NewListOfIssues = 'link_list.txt'
with open(filename) as csv_file:
	csv_reader = csv.reader(csv_file)
	for row in csv_reader:
		names.append(row[0])
		password.append(row[1])

index=0
Pullcount=0;

if os.path.exists(NewListOfIssues):
  os.remove(NewListOfIssues)

for puppet in names:
	puppet=puppet.replace(" ", "_")
	#####
	# print(puppet)
	# print(password[index])
	#####

	# if(Pullcount>4 and Pulleventcard == 'yes'):
	#
	# 	f.writelines('https://www.nationstates.net/page=deck/card='+pulleventcardID+'/season='+pulleventcardSeason+"/pull_event_card\n")
	# 	Pullcount=0
	# else:
	r = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/',
		headers={'User-Agent': UserAgent,
				'X-Password': password[index].replace(" ","_")},
				params={'nation':puppet, 'q':'issues+packs'})
	sleep(.7)

	#####
	print(f"request for {puppet} made. received ", r)
	#####

	soup = BeautifulSoup(r.content, "xml")
	packs = int(soup.find("PACKS").contents[0])


	if ((pulleventmode and packs == 0) or \
		(not pulleventmode and packs < MAX_PACKS)):
		for ISSUEid in soup.find_all('ISSUE'):
			Pullcount=Pullcount+1

			#####
			print(f"Assigning issue #{ISSUEid.get('id')} " \
			 	   f"option {ISSUEid.OPTION.get('id')}")
			#####

			with open(NewListOfIssues, 'a+') as f:
				# https://www.nationstates.net/nation=PUPPET/page=enact_dilemma/choice-1=1/dilemma=26
				if (ISSUEid.get('id')=='407'):
					if (not pulleventmode):
						f.writelines('https://www.nationstates.net/page=show_dilemma/dilemma=407/template-overall=none'+"/nation="+puppet+"/container="+puppet+"/template-overall=none/pulleventmode=true\n")
					else:
						f.writelines('https://www.nationstates.net/page=show_dilemma/dilemma=407/template-overall=none'+"/nation="+puppet+"/container="+puppet+"/template-overall=none\n")
				else:
					if (not pulleventmode):
						f.writelines('https://www.nationstates.net/page=enact_dilemma/choice-'+ISSUEid.OPTION.get('id')+'=1/dilemma='+ISSUEid.get('id')+"/nation="+puppet+"/container="+puppet+"/template-overall=none\n")
					else:
						f.writelines('https://www.nationstates.net/page=enact_dilemma/choice-'+ISSUEid.OPTION.get('id')+'=1/dilemma='+ISSUEid.get('id')+"/nation="+puppet+"/container="+puppet+"/template-overall=none/pulleventmode=true\n")
	else:
		#####
		print(f"{puppet} has {packs} pack(s) " \
				"and should be cleared before answering issues.")
		#####

	print() # a newline for clarity
index=index+1


print("Done. Thanks for running this!\n")
