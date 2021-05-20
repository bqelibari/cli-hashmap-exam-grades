"""
Implementation of simple course statistics using a custom hash map

Copyright 2021, University of Freiburg.
Chair of Algorithms and Data Structures.

Patrick Brosi <brosi@cs.uni-freiburg.de>

"""

import sys

from hash_map import HashMap


def course_statistics(filepath: str):
    str_list = open_file_and_read_contents()
    sorted_str_list = sort_list(str_list)
    list_of_string_lists = separate_str_at_second_tab(sorted_str_list)

    len_hash_map = determine_hash_map_length(list_of_string_lists)

    mapping = HashMap(len_hash_map)
    insert_data_into_hash_map(mapping, list_of_string_lists)
    sorted_key_value_lists = mapping.key_value_pairs()
    module_name = sorted_key_value_lists[0][0]

    module_grades = []
    for module in sorted_key_value_lists:
        if module[0] == module_name:
            grade = float(module[1])
            module_grades.append(grade)
        else:
            module_name = module[0]
            calculate_module_info(module_grades, module_name)
            module_grades = []


def calculate_module_info(module_grades, module_name):
    participants = len(module_grades)
    sum_of_grades = 0
    failed_exams = module_grades.count(5.0)
    passed_exams = participants - failed_exams

    for grade in module_grades:
        if grade == 5.0:
            break
        sum_of_grades += grade

    median = round((sum_of_grades / passed_exams), 2)
    fail_percentage = round((failed_exams / participants) * 100, 1)
    print_output(module_name, participants, median, fail_percentage)


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


def insert_data_into_hash_map(hashmap, string_list):
    for element in string_list:
        hashmap.insert(element[0], element[1])


def get_key_value_pairs(hashmap):
    return hashmap.key_value_pairs()


def print_output(module_name, participants, median, fail_percentage):
    sys.stdout.write(
        module_name + "\t" + str(participants) + "\t" +
        str(median) + "\t" +
        str(fail_percentage) + "\n")


if __name__ == '__main__':
    sys.argv.append("course_grades.tsv")
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <course grades file>")
        exit(1)
    course_statistics(sys.argv[1])
