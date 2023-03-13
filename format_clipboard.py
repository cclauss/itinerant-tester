#!/usr/bin/env python3
#
# from https://github.com/cclauss/itinerant-tester
#
# Copy the Travis CI output from the macOS Clipboard
# Clean up the test output based on simple readability rules
# Pastes the resulting text back onto macOS Clipboard to be pasted into a pull request

import subprocess

EXPLANATION = """
https://flake8.pycqa.org/en/latest/user/error-codes.html

On the flake8 test selection, this PR does _not_ focus on "_style violations_" (the majority of flake8 error codes that [__psf/black__](https://github.com/psf/black) can autocorrect).  Instead these tests are focus on runtime safety and correctness:
* E9 tests are about Python syntax errors usually raised because flake8 can not build an Abstract Syntax Tree (AST).  Often these issues are a sign of unused code or code that has not been ported to Python 3.  These would be compile-time errors in a compiled language but in a dynamic language like Python they result in the script halting/crashing on the user.
* F63 tests are usually about the confusion between identity and equality in Python.  Use ==/!= to compare str, bytes, and int literals is the classic case.  These are areas where __a == b__ is True but __a is b__ is False (or vice versa).  Python >= 3.8 will raise SyntaxWarnings on these instances.
* F7 tests logic errors and syntax errors in type hints
* F82 tests are almost always _undefined names_ which are usually a sign of a typo, missing imports, or code that has not been ported to Python 3.  These also would be compile-time errors in a compiled language but in Python a __NameError__ is raised which will halt/crash the script on the user.
"""  # noqa: E501


def osx_clipboard_get():  # Only works for data types: {txt | rtf | ps}
    p = subprocess.Popen(["pbpaste"], stdout=subprocess.PIPE)
    _ = p.wait()  # noqa
    return p.stdout.read().decode()


def osx_clipboard_set(data):
    p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
    p.stdin.write(bytes(data, encoding="utf-8"))
    p.stdin.close()
    return p.wait()


def cleanup(text):
    START_TEXT = "\nflake8 testing of https://github.com/"
    END_TEXT = "\nreal	"
    FLAKE8_LINK = "[flake8](http://flake8.pycqa.org)"
    text = ("\n" + text).split(START_TEXT)[-1].split(END_TEXT)[0]
    lines = [line for line in text.splitlines() if line.strip()]
    lines[0] = START_TEXT.replace("\nflake8", FLAKE8_LINK) + lines[0]
    lines[1] = ""
    lines[2] = f'$ __{lines[2].split("$ time ")[-1]}__\n```'
    return "\n".join(lines) + "\n```" + EXPLANATION


def main():
    text = osx_clipboard_get()
    if not text:
        print("Nothing found on the Mac OS X Clipboard.")
        return -1  # signal error
    osx_clipboard_set(cleanup(text))
    print(osx_clipboard_get())
    return 0  # noError


def test(text):
    print("Testing...")
    osx_clipboard_set(text)
    text = osx_clipboard_get()
    if not text:
        print("Nothing found on the Mac OS X Clipboard.")
        return -1  # signal error
    osx_clipboard_set(cleanup(osx_clipboard_get()))
    print(osx_clipboard_get())
    return 0  # noError


PAYLOAD = """The command "echo stop the build if there are Python syntax errors or undefined names" exited with 0.
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
"""  # noqa: E501

if __name__ == "__main__":
    # test(PAYLOAD)
    main()
