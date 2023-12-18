from threading import Thread
from time import sleep

# 如何使用使用ctrl+c强制终止程序
    
def f():
    """
    目标函数
    """
    sleep(100)

p = Thread(target=f,daemon=True)  # 将线程设置为守护线程，主线程结束即终止  
p.start()

# 子线程开始后，主线程进入死循环，直到子线程结束或者用ctrl+c强制打断主线程，守护线程也会终止。
while 1:
    if not p.is_alive():
        break
    sleep(1)

print('done')