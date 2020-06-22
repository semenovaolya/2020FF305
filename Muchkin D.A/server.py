import socket

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('', 53210))
serv_sock.listen(10)
#inputefile = 'log1.txt'
#myfile = open(inputefile, 'r')
print("<Timestap>           <Message Type>            <Source of message>:Log message itself>")
while True:

    client_sock, client_addr = serv_sock.accept()  #Принимаем входящие подключения
    print('Connected by', client_addr)

    while True:
        #Пока клиент находится в сети, читаем передаваемые им данные и отправляем их обратно
      data = client_sock.recv(1024)
      if data.decode() == '1':                  #Если принимаемое сообщение сервером равно 1, то отправляем log клиенту
        
        inputefile = 'log1.txt'                 #Объявляем наш файл
        myfile = open(inputefile, 'r')          #Открываем файл
        for num, line in enumerate(myfile, 1):  #Узнаем сколько в файле строк с enumerate
            number = num
       
        number = num - 2
       
        lines_index = []
        with open("log1.txt", 'r', buffering=1, encoding="utf8") as file:
            while file.readline():
                lines_index.append(file.tell())
               
            while number > 0:                     #Пока количество строк не закончилось, отправляем их клиенту
                myfile.seek(lines_index[number])
                data = myfile.readline()
                data = str(data).encode("utf-8")  #Отправляем в виде str т.к myfile.readline 
                print(data) 
                client_sock.sendall(data)  #отправка
                #client_sock.sendall(myfile.readline(), end='')
                number = number - 1
      if data.decode() == '2':  #Если полученное сообщение от клиента 2 то начинаем обработку файла
          inputefile = 'log1.txt'
          myfile = open(inputefile, 'r')
          #data = input("Введите поисковое слово:")
          data = client_sock.recv(1024)             #Прослушиваем клиента на получение от него поискового слова
          data1 = data.decode()
          for num1, line1 in enumerate(myfile, 1):  #Проверяем каждую строку на результат данного поискового запроса
              if data1 in line1:
                  data = line1
                  data = str(data).encode("utf-8")  #Присваиваем data значение str для отправки
                  client_sock.sendall(data)         #Отправляем данные
                  print(str(num1) + " " + line1)
    client_sock.close()