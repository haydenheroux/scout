#!/usr/bin/env python3
"""
Reads a CSV with team numbers as headers and notes in the column and
returns a dictionary with team numbers as keys and a list of notes
as the values. Returns an empty dictionary on error.
"""
def import_from_csv(path):
    pass


"""
Wraps Python's input() function with special functionality; namely,
an adaptive prompt and checking for empty lines. Returns the line the
user entered.
"""
def get_user_input():
    prompt = ">"
    if prompt[-1] != " ":
        prompt = prompt + " "
    text = input(prompt)
    if len(text) == 0:
        print("err?: empty line")
    return text


"""
Returns any special operations which may be associated with a particular line.
Special operations are returned as an upper-cased string if found. If the line is
empty, None is returned. If the line contains no special operations and the line 
is not empty, then the string is returned.
"""
def get_execution_type(read_line):
    pass


"""
Exports a text file containing a formatted report of all information
recorded. All teams share the same report. Returns False if writing fails,
otherwise returns True.
"""
def export_as_formatted_text(all_team_information, path):
    pass


"""
Breaks a line of text into a team number and textual information. Presumes
that a team number is the first word of the line and the remainder of the line
contains text information (e.g. a note). Returns team_number, text.
"""
def text_process_line(read_line):
    pass


"""
Exports a CSV containing information about all teams. Teams numbers are stored
in the header of the CSV, and information (e.g. notes) about the team is contained
within the columns following the corresponding team number. Returns False if writing
fails, otherwise returns true.
"""
def export_as_csv(all_team_information):
    pass


"""
The primary method of the application; contains the processing loop. 
"""
def app():
    all_team_information = import_from_csv("data.csv")
    is_accepting_input = True 
    while is_accepting_input:
        read_line = get_user_input()
        execution_type = get_execution_type(read_line)

        if execution_type == None:
            is_accepting_input = False
            continue
        elif execution_type == "EXPORT":
            export_success = export_as_formatted_text(all_team_information, "output.txt")
            is_accepting_input = export_success
            continue

        team_number, text = text_process_line(read_line)

        team_information = all_team_information[team_number]
        updated_team_information = team_information.append(text)
        all_team_information[team_number] = updated_team_information

        export_success = export_as_csv(all_team_information)
        is_accepting_input = export_success


if __name__ == "__main__":
    app()
