'''This file will contain utility functions which are required
in the project.'''

from django.core.mail import send_mail

MAIL_ID = 'something@smvdu.ac.in'
PASS = 'HaveAGoodDayBro!'

def checkmail(mailid):
	'''It checks whether a mail ID is university's valid email ID
	or not. If not it returns False otherwise it will return the
	entry number parsed from that email ID.'''

	#TODO: Improve the following email Id parser
	if mailid.endswith('@smvdu.ac.in'):
		return mailid[:-12]
	return False

def send_confirm_email(fname, lname, mailid):
	'''This handles everything related to confirmation
	email which is send to the users email ID.'''

	message = prepare_message(fname, lname, mailid)
	subject = 'Confirm your email ID | Rocket'
	send_mail(subject, message, MAIL_ID, mailid, False, MAIL_ID, PASS)


def prepare_message(fname, lname, mailid):
	'''This prepares the message which is sent to the user
	for confirming the email. This also includes preparing a
	random hash which will be given as an url.'''
	pass