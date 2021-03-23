import socket
import time
import os
import os.path
import socket
import threading
import time
import utils
import micDataProcess

""" 读取麦克风阵列发送的数据，以文本保存。
"""

BUFSIZE = 2000
read_time_duration = 5 # save data time duration.
end_flag = False 

start_time = time.time()

def task(host, port,root_dir):
    global end_flag
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议
    server.bind((host, port))

    # dir_name = 'dataset/'
    # f_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +'.txt'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    f_name = root_dir+'rawdata.txt'

    print('start listening...')
    count = 0
    with open(f_name,'wb') as f:
        while time.time()-start_time < read_time_duration:
            data, _ = server.recvfrom(BUFSIZE)
            print('recv %d' %count)
            f.write(data)
            count += 1
    print('write finish')
    server.close()
    end_flag = True


def main():
    # ip = '10.20.3.219'
    # port = (ip, 8089)  # 10.20.3.219  # static ip: 192.168.1.104
    host, port,root_dir,*_ = utils.get_config()

    t = threading.Thread(target=task, args=(host, port,root_dir))
    t.daemon = True
    t.start()

    while not end_flag and time.time()-start_time < read_time_duration:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('keyboard interrupt')
            exit(0)
    micDataProcess.transfer_and_plot(root_dir)

if __name__ == "__main__":
    main()
    print('done')