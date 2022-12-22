from db_table import db_table
import sys
import xlrd

# This is the 'row number where the agenda starts from in the excel file subtract by 1'.
# Subtract 1 because the list index starts with 0 in python.
# This program assumes that the actual agenda data 
# starts at row 16 just like the given 'agenda.xls' file.
# 16 - 1 = 15
AGENDA_START_ROW = 15 

# 
# Imports the event schedule into a local SQLite database 
# by storing the content into a table
#
class import_agenda:

    # create a db_table
    def __init__(self):
        # table that stores the information about each session
        self.table = db_table("agenda", { "id": "integer PRIMARY KEY",
                                          "date": "text NOT NULL", 
                                          "time_start": "text NOT NULL",
                                          "time_end": "text NOT NULL", 
                                          "session_type":"text NOT NULL",
                                          "title":"text NOT NULL",
                                          "location": "text",
                                          "description":"text",
                                          "speaker": "text",
                                          "subsession_id": "text" })
                                          
        # table that stores the information about each speaker
        self.speaker_table = db_table("speaker_list", { "speaker_name": "text NOT NULL",
                                                        "session_id": "integer NOT NULL" })

    #
    # IMPORT the content of excel file into the db_table
    #
    def import_agenda(self):

        # grab data from the excel file
        file_name = sys.argv[1]
        event_list = xlrd.open_workbook(file_name).sheet_by_index(0)

        # insert all the events into the table
        for row in range(AGENDA_START_ROW, event_list.nrows):

            curr_row = event_list.row_values(row)

            # replace "'" with "`" because "'" means end of the string
            for x in range( len(curr_row) ):
                if "'" in curr_row[x] :
                    curr_row[x] = curr_row[x].replace("'","`")

            # attach the subsession to the previous session
            if (row+1 < event_list.nrows):
                if event_list.row_values(row+1)[3] == "Sub":
                    subsessions = row - AGENDA_START_ROW + 1
                else:
                    subsessions = None
            # no subsession
            else:
                subsessions = None

            # Insert current row into the table. 
            # If no input for location, description, speaker, subsession, then insert None
            self.table.insert({ "id": row-AGENDA_START_ROW, 
                                "date": curr_row[0],
                                "time_start": curr_row[1],
                                "time_end": curr_row[2],
                                "session_type": curr_row[3],
                                "title": curr_row[4],
                                "location": curr_row[5] if len(curr_row[5])>0 else None,
                                "description": curr_row[6] if len(curr_row[6])>0 else None,
                                "speaker": curr_row[7] if len(curr_row[7])>0 else None,
                                "subsession_id": subsessions})

            # Insert each speaker with their participating session to the speaker_table
            if len(curr_row[7]) > 0:
                speaker_list = curr_row[7].split("; ")
                for speaker in speaker_list:
                    self.speaker_table.insert({ "speaker_name": speaker,
                                                "session_id": row-AGENDA_START_ROW})

        # close the database connection
        self.table.close()

if __name__ == "__main__":
    import_agenda().import_agenda()