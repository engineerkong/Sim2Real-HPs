"""
This file is to run train and test in different threading.
Kong 29.04.2024
"""

import sys
import os
import threading

script_path = 'train_test.py'

def train(additional_args=''):
    command = f'python {script_path} {additional_args}'
    os.system(command)
    
if __name__ == '__main__':
    additional_args = ' '.join(sys.argv[1:])
    threads = []
    for i in range(3):
        thread = threading.Thread(target=train(additional_args))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()