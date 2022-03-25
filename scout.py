#!/usr/bin/env python3

"""
Reads a CSV with team numbers as headers and notes in the column and
returns a dictionary with team numbers as keys and a list of notes
as the values. Returns an empty dictionary on error.
"""
def import_from_csv(path):
    all_team_information = dict()
    with open(path, "w") as csv_file:
        pass
    with open(path) as csv_file:
        rows = csv_file.readlines()
        for row in rows:
            data = row.strip().split(",")
            team_number = data[0]
            notes = data[1:]
            all_team_information[team_number] = notes
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
    contents = str()
    for (team_number, notes) in all_team_information.items():
        team_text = f"{team_number}\n"
        for note in notes:
            unescaped_note = note.replace(";;", ",")
            team_text += f" • {unescaped_note}\n"
        team_text += "\n"
        contents += team_text
    with open(path, "w") as text_file:
        text_file.write(contents)
    return True


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
    contents = str()
    for (team_number, notes) in all_team_information.items():
        escaped_notes = [note.replace(",", ";;") for note in notes]
        csv_notes = ",".join(escaped_notes)
        contents += f"{team_number},{csv_notes}\n"
    with open(path, "w") as csv_file:
        csv_file.write(contents)
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

        # Force-ensure that the dictionary is capable of storing the note for the team.
        # If the team is not in the dictionary already, initialize an empty list
        # for the note to be appended to. If the data within the team's entry is
        # corrupted, overwrite the data with an empty list.
        # TODO: Implement a more elegant method for ensuring the dictionary is
        # capable of storing the note.
        if (team_number not in all_team_information.keys() or
            type(all_team_information[team_number]) != list):
            all_team_information[team_number] = list()
        team_information = all_team_information[team_number]
        team_information.append(text)
        all_team_information[team_number] = team_information

        export_success = export_as_csv(all_team_information, "data.csv")
        is_accepting_input = export_success


if __name__ == "__main__":
    app()
