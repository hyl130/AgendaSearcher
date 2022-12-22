# Agenda Searcher

### Import Agenda
This program imports the schedule of an event into a local SQLite database.

This program will
1. Open an Agenda excel file
2. Design a SQLite Database table schema allowing to store agenda information
3. Parse the content of the excel file and store the content in the table you designed

To run the program:
$> ./import_agenda.py agenda.xls


### Lookup Agenda
This program finds agenda sessions in the data you imported.

This program will
1. Parse the command line arguments to retrieve the conditions that the sessions we are looking for must match.
2. Lookup the data you imported for the matching records
3. Print the result onto the screen

To run the program:
$> ./lookup_agenda.py column value

Where:
* column can be one of {date, time_start, time_end, title, location, description, speaker}
* value is the expected value for that field

For example, if I got the following simplified rows:
Title	     Location 	  Description		    Type
===========================================================================
Breakfast    Lounge	  Fresh fruits and pastries Session
Hangout	     Beach	  Have fun		    Subsession of Breakfast
Lunch	     Price Center Junk food    	   	    Session
Dinner	     Mamma Linnas Italien handmade pasta    Session
Networking   Lounge	  Let's meet		    Subsession of Dinner

Then the expected behavior is as follow:
$> ./lookup_agenda.py location lounge
Breakfast   Lounge    	  Fresh fruits and pastries Session	  # Returned because its location is lounge 
Hangout	    Beach	  Have fun		    Subsession    # Returned because its parent session location is lounge
Networking  Lounge	  Let's meet   	   	    Subsession	  # Returned because its location is lounge

Please note:
* This program looks for sessions and subsessions.
* If one of the matched session has any subsession, the program returns all the subsessions belonging to that session as well.
* This program looks for an exact match for date, time_start, time_end, title, location and description.
* For speaker, even though they may not be the only speaker in the session, the program will return all sessions where we can find this speaker.



### agenda.xls
This is the file we import for the "Import Agenda" program.
