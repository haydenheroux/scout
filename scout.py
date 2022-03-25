#!/usr/bin/env python3

"""
Reads a CSV with team numbers as headers and notes in the column and
returns a dictionary with team numbers as keys and a list of notes
as the values. Returns an empty dictionary on error.
"""
def import_from_csv(path):
    all_team_information = dict()
    with open(path) as csv_file:
        # Remove newlines at the end of each line
        lines = [line.rstrip() for line in csv_file.readlines()]
        header = lines[0]

        teams_in_order = header.split(",")
        data = lines[1:]

        for row in data:
            notes_in_order = row.split(",")
            for (index, note) in enumerate(notes_in_order):
                corresponding_team = teams_in_order[index]
                # If the team has not been recorded yet, initialize the dictionary
                # with an empty list at the team number.
                if corresponding_team not in all_team_information.keys():
                    all_team_information[corresponding_team] = list()

                corresponding_team_information = all_team_information[corresponding_team]
                # If, for whatever reason, bad data ends up within the dictionary,
                # erase that data with an empty list.
                # TODO: Implement additional checks for "bad data"
                if type(corresponding_team_information) != list:
                    corresponding_team_information = list()
                all_team_information[corresponding_team].append(note)
    return all_team_information


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
    if len(read_line) == 0:
        return None
    words = read_line.split(" ")
    # TODO: Implement aliases
    if words[0] == "export":
        return "EXPORT"
    return read_line


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
    words = read_line.split(" ")
    team_number = words[0]
    if team_number.isdigit() != True:
        print("err?: entered team number is not a number")
    text_words = words[1:]
    text = " ".join(text_words)
    return team_number, text


"""
Exports a CSV containing information about all teams. Teams numbers are stored
in the left-most column of the CSV, and information (e.g. notes) about the team
is stored in the same row, expanding to the right. Returns False is writing fails, otherwise returns True.
"""
def export_as_csv(all_team_information, path):
    with open(path, "a") as csv_file:
        for (team_number, text) in all_team_information.items():
            csv_text = ",".join(text)
            row = team_number + "," + csv_text + "\n"
            csv_file.write(row)
    return True


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
        team_information.append(text)
        all_team_information[team_number] = team_information

        export_success = export_as_csv(all_team_information, "data.csv")
        is_accepting_input = export_success


if __name__ == "__main__":
    app()
