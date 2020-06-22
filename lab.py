import os
import re


def date_search(path_to_file: str, start_date: str, end_date: str):
    path_to_file = os.path.abspath(path_to_file)
    find_logs = []
    with open(path_to_file) as log:
        end_file = log.seek(0, 2)
        log.seek(0, 0)
        while True:
            line = log.readline()
            date_log = get_log_date(line)
            if date_log:
                if start_date <= date_log <= end_date:
                    find_logs.append(line)
            if log.tell() == end_file:
                break
    return find_logs[::-1]


def count_search(path_to_file: str, count_log: int, *, type_log='ALL'):
    path_to_file = os.path.abspath(path_to_file)
    find_logs_type = []
    with open(path_to_file) as log:
        end_file = log.seek(0, 2)
        log.seek(0, 0)
        if type_log == 'ALL':
            log.seek(end_file - 350 * count_log)
            find_logs = log.readlines()
            find_logs = find_logs[::-1]
            find_logs = find_logs[:count_log:]
            return find_logs
        else:
            tell = end_file
            flag = False
            while len(find_logs_type) < count_log:
                last_pos = tell
                tell = tell - 1000
                try:
                    log.seek(tell)
                    log.readline()
                except ValueError:
                    log.seek(0, 0)
                    flag = True
                tell = log.tell()
                tmp = []
                while log.tell() < last_pos:
                    line = log.readline()
                    if type_log in line[20:40]:
                        tmp.append(line)
                tmp = tmp[::-1]
                find_logs_type += tmp
                if flag:
                    break
            print(find_logs_type)
            return find_logs_type[:count_log:]


def get_log_date(line):
    found = re.search(r'\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}', line)
    return found[0] if found else False
