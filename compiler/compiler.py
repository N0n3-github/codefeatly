#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import subprocess
import os
import re
from platform import system


def process_threading_function(timeout=1):
    from psutil import Process as psutil_Process
    from signal import SIGTERM

    def outer(func):
        def wrapper(*args, **kwargs):
            def thread_children_proc_pids():
                children = psutil_Process().children(recursive=True)
                return [child.pid for child in children]

            def target():
                thread.result = func(*args, **kwargs)

            thread = threading.Thread(None, target=target)
            thread.result = None
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
                for pid in thread_children_proc_pids():
                    os.kill(pid, SIGTERM)
            return thread.result
        return wrapper
    return outer


def compile_file(lang, path, outputpath):  # Refactor this
    from shutil import copyfile, SameFileError as shutil_SameFileError
    from time import sleep as wait_for_compilng
    compile_commands = {
        'c++11': 'g++ -std=c++11 -o {} {}',
        'c++14': 'g++ -std=c++14 -o {} {}',
        'gcc': 'gcc -o {} {}',
        'java': 'javac {}',
        'pascalabc.net': '..{0}pascal{0}pabcnetc.exe'.format(os.sep) + ' {}',
        'nasm': 'nasm -o {} -f {} {}',
    }
    if lang in ('c++11', 'c++14', 'gcc'):
        subprocess.call(compile_commands[lang].format(outputpath, path), shell=True)
    elif lang == 'java':
        try:
            with open(path, 'r') as file:
                public_class_name = re.findall(r'public class .*', file.read())[0][13:]
        except IndexError:
            public_class_name = 'Error_public_name:::none'
        try:
            copyfile(path, 'codes'+os.sep+public_class_name+'.java')
        except shutil_SameFileError:
            pass
        subprocess.call(compile_commands[lang].format('codes'+os.sep+public_class_name+'.java'), shell=True)
        if 'codes'+os.sep+public_class_name+'.java' != path:
            os.remove('codes'+os.sep+public_class_name+'.java')
    elif lang == 'pascalabc.net':
        os.chdir('codes')
        mono_tool = 'mono' if system() != 'Windows' else ''
        compile_command = mono_tool + ' ' + compile_commands[lang].format(path[path.find(os.sep) + 1:])
        devnull = open(os.devnull, 'w')
        subprocess.call(compile_command, shell=True, stdout=devnull)
        os.chdir('..')
    elif lang == 'nasm':  # fix and clarify NASM support
        if system() != 'Windows':
            output = path[:-4] + '.o'
            devnull = open(os.devnull, 'w')
            # 32 arc
            subprocess.call(compile_commands[lang].format(output, 'elf32', path), shell=True, stderr=devnull)
            subprocess.call('ld -m elf_i386 -o {} {}'.format(outputpath, output), shell=True, stderr=devnull)
            if not os.path.exists(outputpath):
                # 64 arc
                subprocess.call(compile_commands[lang].format(output, 'elf64', path), shell=True,
                                stderr=devnull)
                subprocess.call('ld -o {} {}'.format(outputpath, output), shell=True, stderr=devnull)
    wait_for_compilng(2.5)


@process_threading_function(1)  # replace later with sys.argv[<index of timeout>]
def return_output(lang, path, input_expr):
    run_commands = {
        'java': 'java -cp codes {}',
        'python': 'python {}',
        'python2': 'python2 {}',
        'python3': 'python3 {}',
        'php': 'php -f {}',
        'c++11': '{}',
        'c++14': '{}',
        'gcc': '{}',
        'nasm': '{}',
        'pascalabc.net': '{}',
    }
    command = 'echo ' + input_expr + ' | ' + run_commands[lang].format(path)
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, errors = [str(x.strip())[2:-1] for x in process.communicate()]
        process.terminate()
    return output


def delete_compiled_files():
    output = os.listdir('codes')
    for fname in output:
        if fname[-fname[::-1].find('.') - 1:] not in ('.asm', '.c', '.cpp', '.java', '.pas', '.py', '.php'):
            os.remove('codes{}'.format(os.sep + fname))


if __name__ == '__main__':
    # TEMP CONFIGS
    prog_input = ['1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2', '1 2', '1 3', '5 4', '3 2']
    expecting_output = ['3', '4', '9', '5', '3', '4', '9', '5', '3', '4', '9', '5']
    paths = [
        r'codes/for_testing.py',
        r'codes/main.cpp',
        r'codes/hello_world.java',
        r'codes/hello_world.pas',
        r'codes/print_input.asm',
    ]  # make only one path as sys.argv[2]
    # TEMP CONFIGS
    compiling_langs = 'pascalabc.net', 'c++11', 'c++14', 'gcc', 'nasm', 'java'
    compile_extensions = {
        'java': '.class',
        'c++11': '.exe',
        'c++14': '.exe',
        'gcc': '.exe',
        'pascalabc.net': '.exe',
        'nasm': '.exe',
    }
    sys_argv_path = paths[2].replace('/', os.sep).replace('\\', os.sep)  # write sys.argv[2] instead pf paths[2] instead
    sys_argv_lang = 'java'  # write sys.argv[<index of language>] here instead
    # COMPILE FILE
    if sys_argv_lang in compiling_langs:
        opt_path = sys_argv_path[:-sys_argv_path[::-1].find('.') - 1] + compile_extensions[sys_argv_lang]
        compile_file(sys_argv_lang, sys_argv_path, opt_path)
        if sys_argv_lang == 'java':
            sys_argv_path = [x for x in os.listdir('codes') if x[-6:] == compile_extensions['java']][0][:-6]
        else:
            sys_argv_path = opt_path
    # COMPILE FILE

    # TODO: refactor compile function
    # TODO: All exit types as (CE; RE; TLE; ME; WA; OK;) and make json response, sys.argv
    # TODO: NASM support, MySQL bind
    # TODO: Do something with errors
    # TODO: Test that all
    for i in range(len(prog_input)):
        print(sys_argv_lang.upper()+':', return_output(sys_argv_lang, sys_argv_path, prog_input[i]))
    delete_compiled_files()
