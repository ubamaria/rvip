from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

# фактическое время на машине, выполняющей процессы.
def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())

# новая отметка времени, когда процесс получает сообщение,
# Функция берет максимум полученной временной метки и ее локального счетчика и увеличивает ее на единицу.
def calc_timestamp(receive_time_stamp, counter):
    return max(receive_time_stamp, counter) + 1

# возвращать обновленную метку времени для процесса, где происходит событие.
def event(pid, counter):
    counter += 1
    print('Something happened in {} !'.format(pid) + local_time(counter))
    return counter

# Отправка сообщения. pipe - кортеж из объектов соединений
def send_message(pipe, pid, counter):
    counter += 1
    pipe.send([counter, 'hello', None])
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

def receive_message(pipe, pid, counter):
    timestamp = pipe.recv()
    counter = calc_timestamp(timestamp, counter)
    print('Message received at ' + str(pid) + local_time(counter))
    return counter

# определение процесса
def process_one(ab, ba):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(ab, pid, counter)
    counter = event(pid, counter)
    counter = receive_message(ba, pid, counter)
    counter = event(pid, counter)

if __name__ == '__main__':
    a, b = Pipe()
    process1 = Process(target=process_one, args=(a, b))
    process1.start()
    process1.join()