# CyberRoam-Login
#This is a basic command line application to login into the Cyberroam server of DAIICT.
#Requires Python 3.6 and Selenium
#It uses the IDs in the ids.ht and logins in the order provided.
#'ids.ht' is not provided. Add your own ids :P
#'ids.ht' should contain the ids, passwords and names in the following format:
#(For the first ID)<id> <password> <name>
#(For the rest of the IDs)#<id> <password> <name>
#
#Features:
#	->Basic Login
#	->Report on all the ids (Logins in automatically after report if previously logged in)
#	->Add id
#	->Logout
#	->Login as from the set of names
#	->logout as from the set of names
#	->custom login, logout and report
#	->List of all available IDs
#	->Change priority order
#	->Help menu

#Coming up features:
#	->Login in automatically on waking up
#	->BlackList IDs
#	->Change Passwords (noobie work)
