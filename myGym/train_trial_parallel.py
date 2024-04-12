import os
import threading

script_path = 'train_hydra.py'

def train():
    os.system('python {script_path}'.format(script_path=script_path))
    
    

if __name__ == '__main__':
    threads = []
    for i in range(5):
        thread = threading.Thread(target=train)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()