from multiprocessing import Process, Pipe
import subprocess

def start_key_press_handler(pipe_end):
    subprocess.run(["python", "key_press_handler.py"], check=True)

def start_print_number(pipe_end):
    subprocess.run(["python", "print_number.py"], check=True)

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    
    p1 = Process(target=start_key_press_handler, args=(child_conn,))
    p2 = Process(target=start_print_number, args=(parent_conn,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
