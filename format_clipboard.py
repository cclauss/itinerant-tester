#!/usr/bin/env python
#
# Script: sametimePaste.py
# Author: cclauss
#   Date: Saturday, 29 June 2013 19h43
#
# Copies the Sametime transcript from the Mac OS X Clipboard
# Cleans up the transcript based on simple readability rules
# Pastes the resulting text back onto the Mac OS X Clipboard

import subprocess


def osx_clipboard_get():  # Only works for data types: {txt | rtf | ps}
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    _ = p.wait()  # noqa
    return p.stdout.read().decode()


def osx_clipboard_set(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(bytes(data, encoding='utf-8'))
    p.stdin.close()
    return p.wait()


def cleanup(text):
    START_TEXT = '\nflake8 testing of https://github.com/'
    END_TEXT = '\nreal	'
    FLAKE8_LINK = '[flake8](http://flake8.pycqa.org)'
    text = ('\n' + text).split(START_TEXT)[-1].split(END_TEXT)[0]
    # Workaround for flake8 on Python 3.7
    junk = ("/home/travis/virtualenv/python3.7.0/lib/python3.7/site-packages/"
            "pycodestyle.py:113: FutureWarning: Possible nested set at position 1",
            "EXTRANEOUS_WHITESPACE_REGEX = re.compile(r'[[({] | []}),;:]')")
    for j in junk:
        text = text.replace(j, '')
    lines = [line for line in text.splitlines() if line.strip()]
    lines[0] = START_TEXT.replace('\nflake8', FLAKE8_LINK) + lines[0]
    lines[1] = ''
    lines[2] = f'$ __{lines[2].split("$ time ")[-1]}__\n```'
    return '\n'.join(lines) + '\n```'


def old_cleanup(text):  # modify to meet your requirements
    start_tag = '\nflake8 testing of https://github.com/'
    end_tag = '\n\n'
    temp = '\n{}{}'.format(text, end_tag)
    temp = temp.partition(start_tag)[-1].partition(end_tag)[0]
    assert temp, text
    lines = temp.splitlines()
    lines[1] = ''
    lines = text.splitlines()
    # for i, line in lines:
    #    if line.startswith()
    return 'cleanup({})'.format(text)


def main():
    text = osx_clipboard_get()
    if not text:
        print('Nothing found on the Mac OS X Clipboard.')
        return -1  # signal error
    osx_clipboard_set(cleanup(text))
    print(osx_clipboard_get())
    return 0      # noError


def test(text):
    print('Testing...')
    osx_clipboard_set(text)
    text = osx_clipboard_get()
    if not text:
        print('Nothing found on the Mac OS X Clipboard.')
        return -1  # signal error
    osx_clipboard_set(cleanup(osx_clipboard_get()))
    print(osx_clipboard_get())
    return 0      # noError


PAYLOAD = '''The command "echo stop the build if there are Python syntax errors or undefined names" exited with 0.
0.01s$ echo ; echo -n "flake8 testing of ${URL} on " ; python -V
flake8 testing of https://github.com/vibora-io/vibora on Python 3.6.3
The command "echo ; echo -n "flake8 testing of ${URL} on " ; python -V" exited with 0.
2.71s$ time flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics
./samples/schemas.py:21:55: E999 SyntaxError: invalid syntax
    context = await BenchmarkSchema.load(extra={'db': })
                                                      ^
1     E999 SyntaxError: invalid syntax
1
real	0m2.707s
user	0m4.394s
sys	0m0.192s
'''

if __name__ == '__main__':
    # test(PAYLOAD)
    main()
