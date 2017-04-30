'''This file will contain utility functions which are required
in the project.'''

def checkmail(mailid):
	'''It checks whether a mail ID is university's valid email ID
	or not. If not it returns False otherwise it will return the
	entry number parsed from that email ID.'''

	#TODO: Improve the following email Id parser
	if mailid.endswith('@smvdu.ac.in'):
		return mailid[:-12]
	return False