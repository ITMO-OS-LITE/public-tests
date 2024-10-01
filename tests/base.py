import os
import subprocess
import random

from typing import Iterable, List, Union

SOURCE_DIR = 'src'

def verify_file(needed: str) -> str:
	current_working_directory = os.getcwd()
	src = os.path.join(current_working_directory, SOURCE_DIR)
	p = os.path.join(src, needed)
	if not os.path.exists(p):
		raise FileNotFoundError("File \"%s\" is not found for testing. Abort." % (needed))
	return p

def verify_files(needed: Iterable[str]) -> List[str]:
	l = []
	for need in needed:
		l.append(verify_file(need))
	return l

def args_to_strs(args: list) -> List[str]:
	argv: List[str] = [str(x) for x in args]
	return argv

def escape(s: str) -> str:
	e = ''
	for c in s:
		if c == '\t':
			e += '\\t'
		elif c == '\n':
			e += '\\n'
		elif c == '\r':
			e += '\\r'
		elif c == '\\':
			e += '\\\\'
		else:
			e += c
	return e

def contains_only_chars_from(text: str, allowed_chars: str) -> bool:
	for char in text:
		if char not in allowed_chars:
			return False
	return True

def get_random_elements(container: Iterable, percent: int) -> Iterable:
	n = int((percent / 100) * len(container))
	return random.sample(container, n)

def check_fail(results: subprocess.CompletedProcess[str], file_output: str):
	# CASE: Stderr should not be empty.
	if results.stderr == '':
		raise ValueError('On failure, stderr should not be empty.')

	# CASE: Stdout should be empty.
	if results.stdout != '':
		raise ValueError('On failure, stdout should be empty.')

	# Skip, when there is no file output.
	if file_output is None:
		return

	# CASE: File should not be created.
	if os.path.exists(file_output):
		raise ValueError('On failure, output file should not be created.')

def check_pass(results: subprocess.CompletedProcess[str], answer: str, file_output: str, check_output: bool):
	actual: str = None

	if not answer.endswith('\n'):
		answer += '\n'

	# CASE: If it's file output, then file should be created.
	if file_output != None:
		if not os.path.exists(file_output):
			raise ValueError("On successful, there is should be \"%s\" as output file." % (file_output))
		file = open(file_output, 'r')
		actual = file.read()

	# CASE: If it's not file output, then read from stdout.
	if file_output is None:
		actual = results.stdout

	# CASE: Assertion.
	if check_output and actual != answer:
		raise ValueError("Expected \"%s\", but actual is \"%s\"." % (escape(answer), escape(actual)))

def run_once(prog: str, args: list = [], answer: str = "", exitcode: int = 0, file_output: str = None, check_output: bool = True):
	argv = args_to_strs(args)
	executable = verify_file(prog)

	results = subprocess.run([executable] + argv, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)

	# CASE: Exitcode equals to resulting exitcode.
	if results.returncode != exitcode:
		raise ValueError('Asserted at exitcode.')

	# If exitcode is 0, then it's SUCCESS state, check as passing.
	# Otherwise, check as failure.
	if exitcode == 0:
		check_pass(results, answer, file_output, check_output)
	else:
		check_fail(results, file_output)

class interactive_program:
	def __init__(self, prog: str, args: list = [], input_continuously: bool = False):
		self.__prog = verify_file(prog)
		self.__argv = args_to_strs(args)
		self.__input = ''
		self.__answer = ''
		self.__separator = '' if input_continuously else '\n'

	def communicate(self, input: str = '', answer: Union[str, int] = ''):
		if input != '':
			self.__input += input
			self.__input += self.__separator
		if answer != '':
			self.__answer += str(answer)
			self.__answer += self.__separator

	def fork(self, last_input: str = '', last_answer: str = '', exitcode: int = 0):
		self.communicate(last_input, last_answer)

		if not self.__input.endswith('\n'):
			self.__input += '\n'

		results = subprocess.run([self.__prog] + self.__argv, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True, input = self.__input)

		# CASE: Exitcode equals to resulting exitcode.
		if results.returncode != exitcode:
			raise ValueError('Asserted at exitcode.')

		# If exitcode is 0, then it's SUCCESS state, check as passing.
		# Otherwise, check as failure.
		if exitcode == 0:
			check_pass(results, self.__answer, None, True)
		else:
			check_fail(results, None)
