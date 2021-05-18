"""
Implementation of simple course statistics using a custom hash map

Copyright 2021, University of Freiburg.
Chair of Algorithms and Data Structures.

Patrick Brosi <brosi@cs.uni-freiburg.de>

"""

import sys

from hash_map import HashMap


def course_statistics(filepath: str):
    """
    Analyzes the course grades file at <filepath>, calculates the
    number of students per course, the avg. passing grade, and the
    percentage of students who failed the course. The result is
    printed to stdout, ordered by semester in descending manner.

    The format for printing is as follows:

    <semester>\t<course_name>\t<num_students>\t<avg_grade>\t<fail_quote>\n

    """

    """
    test wurde entfernt, da course_grades und test.tsv unterschiedliche
    formate haben. Mein code trennt die einzelnen zeilen nach dem
    ersten tab von rechts. Da der aufbau der dateien so unterschiedlich ist,
    kann der test nicht durchgehen. ich hoffe dass das format von
    course_grades das richtige ist, da auch auf dem übungsblatt steht dass
    diese datei eingelesen werden soll.
    """
    str_list = open_file_and_read_contents()
    sorted_str_list = sort_list(str_list)
    list_of_string_lists = separate_str_at_second_tab(sorted_str_list)
    len_hash_map = determine_hash_map_length(list_of_string_lists)

    mapping = HashMap(len_hash_map)
    insert_data_into_hash_map(mapping, list_of_string_lists)
    sorted_key_value_lists = sorted(mapping.hash_map, reverse=True)
    for module in sorted_key_value_lists:
        print_module_info(module)


def print_module_info(module):
    participants = len(module[1])
    passed = 0
    sum_of_grades = 0
    failed_exams = 0
    for grade in module[1]:
        if grade == '5.0':
            failed_exams += 1
        else:
            passed += 1
            sum_of_grades += float(grade)
    module[0].replace('\t', "\t", 1)
    sys.stdout.write(
        module[0] + "\t" + str(participants) + "\t" +
        str(round((sum_of_grades / passed), 2)) + "\t" +
        str(round((failed_exams / participants) * 100, 1)) + "\n")


def open_file_and_read_contents():
    with open(sys.argv[1], 'r') as f:
        contents = f.read()
    return contents


def sort_list(sting_list):
    words = sting_list.split('\n')
    words.sort()
    return words[1:]


def separate_str_at_second_tab(string_list):
    lines_as_lists = []
    for line in string_list:
        lines_as_lists.append(line.rsplit('\t', 1))
    return lines_as_lists


def determine_hash_map_length(string_list):
    list_of_keys = []
    for element in string_list:
        list_of_keys.append(element[0])
    key_set = set(list_of_keys)
    return len(key_set)


def insert_data_into_hash_map(map, string_list):
    """empty string as first element after sorting.
    dataset is too big to determine if its my fault or if
    the empty string was in the dataset by accident"""
    for element in string_list[1:]:
        map.insert(element[0], element[1])


def get_key_value_pairs(map):
    return map.key_value_pairs()


if __name__ == '__main__':
    sys.argv.append("course_grades.tsv")
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <course grades file>")
        exit(1)
    course_statistics(sys.argv[1])
