from flask import flash
import os
import re


def count_filter_logs(path_to_file: str,
                      num_of_log_lines: int, *,
                      message_type='ALL'):
    path = os.path.abspath(path_to_file)
    """Функция, осуществляющая фильтрацию логов по количеству и типу сообщения.
    Тип сообщения необязательный аргумент, по умолчанию ALL, возвращает все логи
    Возвращает список с обработанными логами в порядке убывания по времени
    
    Parameters
    -------------
    path_to_file: str
        Путь до файла, из которого требуется считать логи
    num_of_log_lines: int
        Требуемое количество логов (при вызове функции со значением параметра
        num_of_log_lines равным 0, функция вернет все логи из файла)
    message_type
        Требуемый тип сообщения: {Info, Warning, Error}
    """

    if os.path.isfile(path):
        # Обрабатываем PermissionError, исключение возбуждается, если нет прав на чтение файла
        try:
            with open(path, 'r') as logs:
                # Переводим указатель в конец файла, чтобы узнать количество символов
                # Поскольку наша цель считать файл с конца не перегружая память,
                # а встроенных способов считывания определенных строк нет, воспользуемся указателем
                # и предположим, что в каждой строке примерно 200 символов
                count_symbol = logs.seek(0, 2)
                read_characters = count_symbol
                log_count = 0
                type_mes_list = dict()
                # Сдвигаем указатель назад, 200 символов на количество требуемых логов
                count_symbol -= 200 * num_of_log_lines
                # Попытаемся сдвинуть указатель, если достигнуто начало файла, обработаем исключение
                try:
                    logs.seek(count_symbol)
                except ValueError:
                    count_symbol = 0
                    logs.seek(0, 0)
                # Главный цикл, работающий до тех пор, пока мы не получим требуемое количество логов,
                # или не достигнем начала докумена
                while True:
                    # Случай, когда в качестве num_of_log_lines был передан 0, хотим получить все логи
                    if num_of_log_lines == 0:
                        num_of_log_lines = count_symbol
                    # Если переместились в позицию, не соответствующую началу строки, просто уберем эту строку
                    if count_symbol != 0:
                        logs.readline()
                    tmp_read = logs.tell()
                    tmp_cur = count_symbol
                    # Второстепенный цикл, предназаначенный для считывания только тех строк логов,
                    # которые еще не были считаны и записаны в словарь. Для этого используется
                    # переменная read_characters, перемещающаяся каждый раз, как мы прочитали какой то блок символов
                    while count_symbol < read_characters:
                        count_symbol = logs.tell()
                        line = logs.readline()
                        # Предполагаем, что лог имеет время, если строка не имеет времени, не учитываем ее
                        if not islog(line):
                            continue
                        # Блок if - else для обработки типа сообщения, если передан message_type,
                        # то заносим в словарь только логи, которые имеют нужный тип сообщения
                        if message_type != 'ALL':
                            if message_type in line[15:30]:
                                # Если лог уже записан в словарь, повторно не записываем
                                if count_symbol not in type_mes_list.keys():
                                    # В качестве ключа словаря укажем положение строки в файле
                                    # Удовлетворяет условию индивидуальности,
                                    # значение, сам лог
                                    type_mes_list[count_symbol] = line
                                    log_count += 1
                                else:
                                    break
                        else:
                            if count_symbol not in type_mes_list.keys():
                                type_mes_list[count_symbol] = line
                                log_count += 1
                    read_characters = tmp_read
                    count_symbol = tmp_cur
                    # Если мы считали логов больше чем нужно, просто удалим ненужные(более ранние),
                    # и выйдем из цикла обработки логов
                    if log_count > num_of_log_lines:
                        keys_sort = sorted(type_mes_list)
                        keys_sort.reverse()
                        for delete in keys_sort[num_of_log_lines:]:
                            type_mes_list.pop(delete)
                        break
                    # Если же логов в словаре недостаточно, переместим указатель на 120 символов назад,
                    # и считаем еще раз, дойдя только до блока, который мы уже считали
                    if log_count < num_of_log_lines:
                        try:
                            count_symbol -= 120
                            logs.seek(count_symbol)
                        # Если логов все еще недостаточно, но достигнуто начало файла,
                        # значит запрошено логов больше, чем есть в файле, и мы вернем все, что есть
                        except ValueError:
                            logs.seek(0, 0)
                            line = logs.readline()
                            if message_type == 'ALL':
                                type_mes_list[0] = line
                            else:
                                if message_type in line[15:30]:
                                    type_mes_list[0] = line
                            break
                    if log_count == num_of_log_lines:
                        break
        except PermissionError:
            flash('Ошибка доступа к файлу', 'error')
            return []

        sorted_keys = sorted(type_mes_list)

        ready_make_logs = []
        # Из всего словаря мы получаем значения по отсортиврованным ключам,
        # разбиваем каждый лог на время, тип сообщения, источник, сооющение
        # и возвращаем лист (указатель на строки нужен для последующего удаления)
        for keys in sorted_keys:
            one_log = split_line(keys, type_mes_list[keys])
            ready_make_logs.append(one_log)
        ready_make_logs.reverse()
        return ready_make_logs


def date_filter_logs(path_to_file: str, *,
                     date_start='1970-01-01 00:00:00',
                     date_end='3000-12-31 23:59:59',
                     message_type='ALL'):
    """Функция, предназначенная для сортировки по времени и типц сообщения.
    Возвращает список с обработанными логами в порядке убывания по времени

    Parameters
    -------------
    path_to_file: str
        Путь до файла, из которого требуется считать логи
    date_start
        Дата, котоая задает нижнюю границу для фильтрации по времени
    date_end
        Дата, которая задает верхнюю границу для сортировки по времени
    message_type
        Требуемый тип сообщения: {Info, Warning, Error}
    """

    if date_start > date_end:
        '''flash(f'Вы неправильно ввели дату: '
              f'начальная дата поиска [{date_start}] больше '
              f'конечной даты [{date_end}]', 'error')'''
        return []
    path = os.path.abspath(path_to_file)
    if os.path.isfile(path):
        # Обработка исключения при нехватке прав доступа
        try:
            with open(path, 'r') as logs:
                count_symbol = logs.tell()
                jump_flag = True
                # В функции сортивровки по времени, мы хотим найти указатель на 1ый подходящий
                # по времени лог и последний подходящий по времени лог.
                # Предполагаем, что логи отсортированы по времени

                # Здесь, с начала документа мы отыскиваем позицию первого подходящего лога
                # при этом, мы не просматриваем каждую строку, мы просматриваем примерно каждую десятую,
                # если нужная строка достигнута, возращаемся в предыдущее положение,
                # и оттуда построчно ищем первый подходящий (ситуация, когда перепрыгнули несколько подходящих)
                end_file = logs.seek(0, 2)
                logs.seek(0, 0)
                while True:
                    line = logs.readline()
                    if islog(line):
                        date_log = islog(line, mode='r')
                        if date_log < date_start:
                            if jump_flag:
                                tmp = logs.tell()
                                count_symbol += 3000
                                if count_symbol >= end_file:
                                    tmp = end_file
                                    break
                                try:
                                    logs.seek(count_symbol)
                                except ValueError:
                                    logs.seek(0, 0)
                                    jump_flag = False
                                    continue
                                logs.readline()
                            else:
                                tmp = logs.tell()
                                continue
                            continue
                        if (date_log >= date_start) and jump_flag:
                            if count_symbol == 0:
                                tmp = 0
                                break
                            logs.seek(tmp)
                            jump_flag = False
                            continue
                        logs.seek(tmp)
                        break

                start_position = tmp

                count_symbol = logs.seek(0, 2)
                logs.seek(count_symbol - 500)
                flag = True
                # Логика та же, что и с первым подходящим логом, однако здесь мы ищем
                # последний подходящий по времени лог, проходим файл с конца
                while True:
                    line = logs.readline()
                    if not line:
                        tmp = logs.seek(0, 2)
                        break
                    if islog(line):
                        date_log = islog(line, mode='r')
                        if (date_log > date_end) and flag:
                            count_symbol -= 3000
                            try:
                                logs.seek(count_symbol)
                            except ValueError:
                                logs.seek(0, 2)
                                break
                            logs.readline()
                            continue
                        if date_log <= date_end:
                            flag = False
                            tmp = logs.tell()
                            continue
                        break
                end_position = tmp

                ready_make_logs = []
                logs.seek(start_position)
                # Перешли в позицию start_position, и считываем логи до end_position
                # Если указан message_type, то просматриваем каждый подходящий по времени лог
                # на тип сообщения
                while True:
                    tell = logs.tell()
                    if tell >= end_position:
                        break
                    line = logs.readline()
                    # Проверка, если вдруг среди подходящих по времени логов, оказался неподходящий по времени
                    check_date = islog(line, mode='r')
                    if (check_date > date_end) or (check_date < date_start):
                        continue
                    if not islog(line):
                        continue
                    if message_type == 'ALL':
                        ready_make_logs.append(split_line(tell, line))
                    else:
                        if line[20:30].strip() == message_type:
                            ready_make_logs.append(split_line(tell, line))
                ready_make_logs.reverse()
                return ready_make_logs
        except PermissionError:
            flash('Ошибка доступа к файлу', 'error')
            return []


def islog(line: str,
          mode='f'):
    """Функция, обрабатывающая строку для извлечения даты с помощью регулярных выражений

    Parameters
    -------------
    line: str
        Строка для обработки
    mode
        found mode находит дату, и возвращает True, если дата найдена, False иначе
        return mode находит и возвращает дату
    """

    found = re.search(r'\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}', line)
    if mode == 'f':
        return True if found else False
    if mode == 'r':
        return found[0] if found else 'not date'


def split_line(tell,
               log_line: str):
    """Функция, предназанченная для разбиения строки на <log_date>  <message_type> <source> <message_text>
    Возвращает либо Bool, либо дату в зависимости от параметра mode

    Parameters
    -------------
    tell
        Указатель на позицию строки в файле
    log_line: str
        Строка для обработки
    """

    log_date = islog(log_line, mode='r')
    if 'Warning' in log_line[:30]:
        message_type = 'Warning'
    elif 'Info' in log_line[:30]:
        message_type = 'Info'
    else:
        message_type = 'Error'

    source = log_line[43:50]
    source = source.strip()
    message_text = log_line[50:]
    message_text = message_text.strip()
    list_with_log = [tell, log_date, message_type, source, message_text]
    return list_with_log


def log_delete(path_to_log,
               deleted_items: list):
    """Функция удаления выбранных логов. Принимает путь до файла и лист с позициями строк
    в файле, возвращает True или False в зависимости от результата выполнения функции

    Parameters
    -------------
    path_to_log
        Путь до файла с логами, которые требуется удалить
    deleted_items: list
        Список позиций удаляемых строк в файле
    """

    deleted_items = [int(i) for i in deleted_items]
    # Пытаемся открыть файл на чтение и дозапись
    # Поскольку в python нет встроенных способов удалить какую либо строку из файла,
    # а в интернете есть только способ с записью нужных строк в новый файл с последующим
    # переименованием, мы придумали следующий путь решения:
    # по значениям из листа с удаляемыми позициями, находим минимальную позицию,
    # последующие нужные строки заносим в лист, встроенной функцией truncate()
    # вырезаем из файла все строки с конца файла до минимального значения указателя, и
    # дозаписываем заранее сохраненные нужные строки обратно файл
    try:
        point = min(deleted_items)
    except ValueError:
        flash('Вы не выбрали логи для удаления', 'error')
        return False
    saved_lines = []
    path_to_log = os.path.abspath(path_to_log)
    try:
        with open(path_to_log, 'a+') as logs:
            end_pos = logs.seek(0, 2)
            logs.seek(point)
            while True:
                tell = logs.tell()
                if tell == end_pos:
                    break
                if tell not in deleted_items:
                    line = logs.readline()
                    saved_lines.append(line)
                    continue
                else:
                    logs.readline()
                    continue
            logs.truncate(point)
            for line in saved_lines:
                logs.write(line)
            flash('Логи успешно удалены', 'info')
            return True
    except PermissionError:
        flash('Нет прав на изменение файла', 'error')
        return False
