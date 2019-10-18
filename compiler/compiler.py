#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import subprocess
import os
from psutil import process_iter as get_all_processes
from signal import SIGTERM
from platform import system


def process_threading_function(timeout=2):
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
                    if pid != os.getpid():
                        os.kill(pid, SIGTERM)
            return thread.result
        return wrapper
    return outer


@process_threading_function(3)
def return_output(lang, path, input_expr):
    interpreting_langs = 'python, python3, python2, php'
    compiling_langs = 'pascalabc.net', 'c++11', 'c++14', 'gcc', 'nasm', 'java'
    if lang not in interpreting_langs and lang not in compiling_langs:
        return
    compile_commands = {
        'c++11': 'g++ -std=c++11 -o {} {}',
        'c++14': 'g++ -std=c++14 -o {} {}',
        'gcc': 'gcc -o {} {}',
        'java': 'javac {}',
        'pascalabc.net': '..{0}pascal{0}pabcnetc.exe'.format(os.sep) + ' {}',
        'nasm': 'nasm -o {} -f {} {}',
    }

    if lang in compiling_langs:
        exec_file = path[:path.find('.')]
        exec_file += '.class' if lang == 'java' else '.exe'
        # if execution file does not exist then compile
        if not os.path.exists(exec_file):
            if lang in ('c++11', 'c++14', 'gcc'):
                subprocess.call(compile_commands[lang].format(exec_file, path), shell=True)
            elif lang == 'java':
                subprocess.call(compile_commands[lang].format(path), shell=True)
            elif lang == 'pascalabc.net':
                os.chdir('codes')
                mono_tool = 'mono' if system() != 'Windows' else ''
                compile_command = mono_tool + ' ' + compile_commands[lang].format(path[path.find(os.sep) + 1:])
                subprocess.call(compile_command, stdout=subprocess.PIPE, shell=True)
                os.chdir('..')
            elif lang == 'nasm':
                if system() != 'Windows':
                    output = path[:-4] + '.o'
                    devnull = open(os.devnull, 'w')
                    # 32 arc
                    subprocess.call(compile_commands[lang].format(output, 'elf32', path), shell=True, stderr=devnull)
                    subprocess.call('ld -m elf_i386 -o {} {}'.format(exec_file, output), shell=True, stderr=devnull)
                    if not os.path.exists(exec_file):
                        # 64 arc
                        subprocess.call(compile_commands[lang].format(output, 'elf64', path), shell=True, stderr=devnull)
                        subprocess.call('ld -o {} {}'.format(exec_file, output), shell=True, stderr=devnull)
                    
        # As java is running through "java" command we don't get any executable, so added some lines of code
        if lang == 'java':
            path = path[path.find(os.sep) + 1:path.find('.')]
            os.chdir('codes')
        else:
            path = path[:path.find('.')] + '.exe'
            lang = ''

    if system() != 'Windows' and lang != 'java':
        path = './' + path
    command = 'echo ' + input_expr + ' | ' + lang + ' ' + path
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, errors = [str(x.strip())[2:-1] for x in process.communicate()]
        process.terminate()
    if lang == 'java':
        os.chdir('..')
        # do something with errors
    return output


def delete_compiled_files():
    output = os.listdir('codes')
    for fname in output:
        if fname[-fname[::-1].find('.') - 1:] not in ('.asm', '.c', '.cpp', '.java', '.pas', '.py'):
            os.remove('codes{}'.format(os.sep + fname))


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
    delete_compiled_files()
