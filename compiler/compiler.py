#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import subprocess
from platform import system
import os


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
    interpreting_langs = 'python, python3, python2, php'
    compiling_langs = 'pascalabc.net', 'c++11', 'c++14', 'gcc', 'nasm', 'java'
    if lang not in interpreting_langs and lang not in compiling_langs:
        return
    compile_commands = {
        'pascalabc.net': '../pascal/pabcnetc.exe {}',
        'c++11': 'g++ -std=c++11 -o {} {}',
        'c++14': 'g++ -std=c++14 -o {} {}',
        'gcc': 'gcc -o {} {}',
        'nasm': 'nasm -o {} -f {} {}',
        'java': 'javac {}',
    }
    output_extenstions = {
        'pascalabc.net': '.exe',
        'c++11': '.exe',
        'c++14': '.exe',
        'gcc': '.exe',
        'nasm': '.exe',
        'java': '.class',
    }

    if lang in compiling_langs:
        exec_file = path[:path.find('.')] + output_extenstions[lang]
        if not os.path.exists(exec_file):
            if lang in ('c++11', 'c++14', 'gcc'):
                subprocess.call(compile_commands[lang].format(exec_file, path), shell=True)
            elif lang == 'java':
                subprocess.call(compile_commands[lang].format(path), shell=True)
            elif lang == 'pascalabc.net':
                os.chdir('codes')
                mono_tool = 'mono' if system() != 'Windows' else ''
                split = '/' if system() != 'Windows' else '\\'
                compile_command = mono_tool + ' ' + compile_commands[lang].format(path[path.find(split) + 1:])
                subprocess.call(compile_command, stdout=subprocess.PIPE, shell=True)
                os.chdir('../')
            elif lang == 'nasm':
                arc = 'elf32' if system() != 'Windows' else 'win32'
                output = path[:-4] + '.o'
                subprocess.call(compile_commands[lang].format(output, arc, path), shell=True)
                compiled_fname = output[:-2] + '.exe'
                subprocess.call('ld -m elf_i386 -o {} {}'.format(compiled_fname, output), shell=True)

        if lang != 'java':
            path = path[:path.find('.')] + output_extenstions[lang]
            lang = ''
        else:
            split = '/' if system() != 'Windows' else '\\'
            path = path[path.find(split) + 1:path.find('.')]

    if system() != 'Windows' and lang != 'java':
        path = './' + path
    if lang == 'java':
        os.chdir('codes')
    command = 'echo ' + input_expr + ' | ' + lang + ' ' + path
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, errors = [str(x.strip())[2:-1] for x in process.communicate()]
        process.terminate()
        if lang == 'java':
            os.chdir('..')
        # do something with errors
    return output

# delete compiled files after json response


if __name__ == '__main__':
    prog_input = ['1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2']
    expecting_output = ['3', '4', '9', '5', '3', '4', '9', '5', '3', '4', '9', '5']
    paths = [
        r'codes\for_testing.py',
        r'codes\main.cpp',
        r'codes\hello_world.java',
        r'codes\hello_world.pas',
        r'codes\print_input.asm',
    ]  # make only one path as sys.argv[2]
    if system() != 'Windows':
        for i in range(len(paths)):
            paths[i] = paths[i].replace('\\', r'/')  # do this with only sys.argv[2] when add it
    for i in range(len(prog_input)):
        print('Python3:', return_output('python3', paths[0], prog_input[i]))
        print('C++:', return_output('c++14', paths[1], prog_input[i]))
        print('Java:', return_output('java', paths[2], prog_input[i]))
        print('PascalABC.NET:', return_output('pascalabc.net', paths[3], prog_input[i]))
        print('NASM:', return_output('nasm', paths[4], prog_input[i]))
        print()
