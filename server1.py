import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 53210))
serv_sock.listen(10)
#inputefile = 'dism.txt'
#myfile = open(inputefile, 'r')
print("<Timestap>           <Message Type>            <Source of message>:Log message itself>")
while True:
    # Бесконечно обрабатываем входящие подключения
    client_sock, client_addr = serv_sock.accept()  #принимаем входящие подключения
    print('Connected by', client_addr)

    while True:
        # Пока клиент не отключился, читаем передаваемые
        # им данные и отправляем их обратно
      data = client_sock.recv(1024)
      if data.decode() == '1':  #если принимаемое сообщение сервером равно 1 то отправляем бд клиенту
        #client_sock.sendall(data)
        inputefile = 'dism.txt'  #объявляем наш файл
        myfile = open(inputefile, 'r')  #открываем наш файл
        for num, line in enumerate(myfile, 1):  #далее узнаем сколько в файле строк с enumerate
            number = num
        # print(number)
        number = num - 2
        #client_sock.sendall(data)
        lines_index = []
        with open("dism.txt", 'r', buffering=1, encoding="utf8") as file:
            while file.readline():
                lines_index.append(file.tell())
                # with open("dism.txt", 'r', buffering=1, encoding="utf8") as file:
            while number > 0:  #до тех пор пока число строк не закончилось отправляем их клиенту
                myfile.seek(lines_index[number])
                data = myfile.readline()
                data = str(data).encode("utf-8")  #отправляем в виде str т.к myfile.readline метод sendall обработать не может
                print(data)  # Прочитать шестую строку
                client_sock.sendall(data)  #сама отправка
                #client_sock.sendall(myfile.readline(), end='')
                number = number - 1
      if data.decode() == '2':  #если полученное сообщение от клиента 2 то начинаем обработку файла и поиск данных
          inputefile = 'dism.txt'
          myfile = open(inputefile, 'r')
          #data = input("Введите поисковое слово:")
          data = client_sock.recv(1024) #прослушиваем клиента на получение от него поискового слова
          data1 = data.decode()
          for num1, line1 in enumerate(myfile, 1):  #проверяем каждую строку на результат вхождений данного поискового запроса
              if data1 in line1:
                  data = line1
                  data = str(data).encode("utf-8")  #также присваем data значение str для отправки
                  client_sock.sendall(data)  #отправляем данные
                  print(str(num1) + " " + line1)
    client_sock.close()