import threading
import subprocess
from platform import system


def process_threading_function(timeout=2):
    """
    This function wraps a function that calls a process in a thread.
    You should give a process name as the first argument of your function.
    It can be useful if you want to run your processes parallel.
    Also there is a timeout argument if you want to kill your process after some period of time.
    """
    from psutil import process_iter as get_all_processes
    from os import kill, getpid as main_pid
    from signal import SIGTERM

    def outer(func):
        def wrapper(*args, **kwargs):
            def get_processes(name):
                if name.startswith('python'):
                    name = 'python'
                processes = [proc for proc in get_all_processes() if proc.name().startswith(name)]
                return processes

            def target():
                thread.result = func(*args, **kwargs)
            thread = threading.Thread(None, target=target)
            thread.result = None
            thread.start()
            thread.join(timeout)
            thread.alive_pids = [process.pid for process in get_processes(args[0])]
            if thread.is_alive():
                for pid in thread.alive_pids:
                    if pid != main_pid():
                        kill(pid, SIGTERM)
            return thread.result
        return wrapper
    return outer


@process_threading_function()
def return_output(lang, path, input_expr):
    if lang in ('c++', 'g++', 'gcc'):
        from os.path import exists as file_exsists
        exec_file = None
        if system() == 'Windows':
            exec_file = path[:-4] + '.exe'
        elif system() == 'Linux':
            exec_file = path[:-4] + '.o'

        if not file_exsists(exec_file):
            command = lang + ' ' + path + ' -o ' + exec_file
            subprocess.call(command, shell=True)
        lang = ''
        path = exec_file
    command = None
    if system() == 'Windows':
        command = (lang + ' ' + path).split()
    elif system() == 'Linux':
        command = 'echo ' + input_expr + ' | ' + lang + ' ' + path
    with subprocess.Popen(command,
                          shell=True,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as process:
        output, errors = [str(x.strip())[2:-1] for x in process.communicate(input=input_expr.encode())]
        process.terminate()
        # do something with errors
    return output

# delete .exe file after json response


if __name__ == '__main__':
    prog_input = ['1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2']
    expecting_output = ['3', '4', '9', '5', '3', '4', '9', '5', '3', '4', '9', '5']
    for i in range(len(prog_input)):
        print(return_output('python3', r'codes\for_testing.py', prog_input[i]))
        print(return_output('c++', r'codes\main.cpp', prog_input[i]))
