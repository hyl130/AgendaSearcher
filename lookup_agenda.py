from db_table import db_table
import sys

# 
# Finds agenda session in the data from the import
#
class lookup_agenda:

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
    # Lookup the agenda session using the user's specified conditions
    #
    def lookup(self):

        # querty the database by applying the specified condition
        column = sys.argv[1] 
        value = sys.argv[2]
        
        # if user's look up condition was to look for a specific speaker
        if column == 'speaker':
            # get all the session ids where this speaker participates in
            speakers_session = self.speaker_table.select(where = { 'speaker_name': value })
            participating_session_ids = [session['session_id'] for session in speakers_session]

            # select the event that is associated with this selected session id
            selected_row = []
            for session_id in participating_session_ids:
                selected_row += self.table.select(where = { 'id': session_id })
        
        # if condition is not a speaker
        else:
            selected_row = self.table.select(where = { column: value })

        results = []
        # go through all the sessions including the subsessions
        # and append all the matching events into the 'results' list.
        for row in selected_row:
            self.retrieve_session(self.table, row['id'], results)

        # if there is no query result, there is no matching session in the agenda
        if len(results) == 0:
            print("There is no matching session in the agenda.")
            self.table.close()
            return

        # print the result onto the screen
        for result in results:
            self.print_result(result)

        # close the database connection
        self.table.close()

    #
    # Retrieve the matching events that the user is looking for
    #
    # \param table      db_table        the database table that we want to search from
    # \param id         integer         the id number of the event
    # \param results    array<string>   list of agenda sessions that matches the conditions 
    #
    def retrieve_session(self, table, id, results):

        # the current row that matches the condition
        row = table.select(where={ "id": id })[0]

        # avoid adding duplicate events
        if( row not in results):
            results.append(row)

        # if the session has subsession,
        # also return all the subsessions that belongs to the current session
        if row['subsession_id'] != 'None':
            self.retrieve_session(table, row['subsession_id'], results)

    #
    # Prints the matching session in a well-formated string
    #
    # \param result    dict<string, string>   agenda information that we want to print
    #
    # Example: This function will print the matching agenda session in the following format:
    #          id | date | time_start | time_end | session_type | title | location | speaker | description
    #
    def print_result(self, result):

        # the string that we want to print
        output_text = (str)(result['id']) + " | " + result['date'] + " | " + result['time_start'] + " | "
        output_text += result['time_end'] + " | " + result['session_type'] + " | " + result['title'] + " | "

        # Adding location to the output
        # If location was not specified in the database, output '-' as the location
        if result['location'] == 'None':
            output_text += "-" + " | "
        else:
            output_text += result['location'] + " | "

        # Adding speaker to the output
        # If speaker was not specified in the database, output '-' as the speaker
        if result['speaker'] == 'None':
            output_text += "-" + " | "
        else:
            output_text += result['speaker'] + " | "

        # Adding description to the output
        # If description was not specified in the database, output '-' as the description
        # For a cleaner format, new line characters are replaced by a space
        # in order to maintain a single line input per session
        if result['description'] == 'None':
            output_text += "-" + " | "
        else:
            result['description'] = result['description'].replace('\n', ' ')
            output_text += result['description']

        print(output_text)

if __name__ == "__main__":
    lookup_agenda().lookup()