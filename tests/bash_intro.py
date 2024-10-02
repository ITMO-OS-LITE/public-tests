import re
import os
import random
import string

import tests.base

from typing import Dict, List, Tuple

def __get_prefix(a: int, b: int) -> str:
	test_list = list(range(a, b + 1))
	prefix = [sum(test_list[ : i + 1]) for i in range(len(test_list))]
	res = '\n'.join(str(x) for x in prefix)
	return res

def __test1():
	# -- Task 1 --
	print('-- Testing task 1...')
	for i, ab in enumerate([(1, 5), (1, 10), (10, 50), (100, 200)]):
		print("     Run test #%d" % (i + 1))
		a = ab[0]
		b = ab[1]
		tests.base.run_once('prefix.bash', [a, b], __get_prefix(a, b))
	print('   ... OK')

def __test2():
	# -- Task 2 --
	print('-- Testing task 2...')
	for i, n_lines in enumerate([1, 5, 10, 50, 100]):
		print("     Run test #%d" % (i + 1))
		tty = tests.base.interactive_program('strings.bash')
		for _ in range(n_lines):
			only_letters = bool(random.getrandbits(1))
			selected_alphabet = string.ascii_letters
			if not only_letters:
				selected_alphabet += string.digits
				selected_alphabet += string.punctuation
			generated_string = ''.join(random.choice(selected_alphabet) for _ in range(random.randint(10, 100)))
			if not only_letters:
				only_letters = tests.base.contains_only_chars_from(generated_string, string.ascii_letters)
			escaped_string = ""
			for c in generated_string:
				if c == '`':
					escaped_string += "\\"
					escaped_string += "`"
				else:
					escaped_string += c
			tty.communicate(escaped_string, len(escaped_string))
			tty.communicate(answer = ('true' if only_letters else 'false'))
		tty.fork('q')
	print('   ... OK')

def __msg(x: int, y: int) -> str:
	return "x=%d;y=%d" % (x, y)

def __w(x: int, y: int) -> Tuple[str, int, int]:
	x1 = x
	y1 = y + 1
	return __msg(x1, y1), x1, y1

def __a(x: int, y: int) -> Tuple[str, int, int]:
	x1 = x - 1
	y1 = y
	return __msg(x1, y1), x1, y1

def __s(x: int, y: int) -> Tuple[str, int, int]:
	x1 = x
	y1 = y - 1
	return __msg(x1, y1), x1, y1

def __d(x: int, y: int) -> Tuple[str, int, int]:
	x1 = x + 1
	y1 = y
	return __msg(x1, y1), x1, y1

def __test3():
	# -- Task 3 --
	print('-- Testing task 3...')
	tty = tests.base.interactive_program('robot.bash', args = [6, 6], input_continuously = True)
	x = 3
	y = 3
	tty.communicate(answer = __msg(x, y))
	# Up, up.
	m, x, y = __w(x, y)
	tty.communicate('W', m)
	m, x, y = __w(x, y)
	tty.communicate('w', m)
	# Down, down.
	m, x, y = __s(x, y)
	tty.communicate('s', m)
	m, x, y = __s(x, y)
	tty.communicate('S', m)
	# Left, right.
	m, x, y = __a(x, y)
	tty.communicate('a', m)
	m, x, y = __d(x, y)
	tty.communicate('d', m)
	# Left, right.
	m, x, y = __a(x, y)
	tty.communicate('A', m)
	m, x, y = __d(x, y)
	tty.communicate('D', m)
	# Run.
	tty.fork('q')
	print('   ... OK')

def __walk_with_level(some_dir: str, level: int = 1):
	some_dir = some_dir.rstrip(os.path.sep)
	num_sep = some_dir.count(os.path.sep)
	for root, dirs, files in os.walk(some_dir):
		yield root, files
		num_sep_this = root.count(os.path.sep)
		if num_sep + level <= num_sep_this:
			del dirs[:]

def __test7_solution() -> List[str]:
	email_pattern = r"[a-zA-Z.+-]+@[a-zA-Z-]+\.[a-zA-Z.-]+"
	emails = set()
	for root, files in __walk_with_level('/etc', 3):
		for file in files:
			p = os.path.join(root, file)
			try:
				f = open(p, 'r')
				s = f.read()
				for e in re.findall(email_pattern, s):
					emails.add(e)
			except Exception as _:
				pass
	return sorted(emails)

def __test7():
	# -- Task 7 --
	print('-- Testing task 7...')
	file_output = 'etc_emails.lst'
	tests.base.run_once('emails.bash', file_output = file_output, check_output = False)
	expected = __test7_solution()
	f = open(file_output, 'r')
	actual = set(f.read().split(','))
	NUMBER_OF_RANDOM_ELEMENTS = 10
	for i in range(NUMBER_OF_RANDOM_ELEMENTS):
		expected_single = random.choice(expected)
		print("     Random pickup #%d" % (i + 1))
		if expected_single in actual:
			continue
		raise ValueError("Random picked up \"%s\" is not in actual solution." % (expected_single))
	print('     Good enough.')
	print('   ... OK')

def __test8_solution() -> str:
	read: Dict[int, str] = {}
	with open('/etc/passwd', 'r') as file:
		lines = [line.rstrip() for line in file]
		for line in lines:
			arr = line.split(':')
			read[int(arr[2])] = arr[0]
	res = '\n'.join(f"{key} {value}" for key, value in sorted(read.items()))
	return res

def __test8():
	# -- Task 8 --
	print('-- Testing task 8...')
	tests.base.run_once('users.bash', answer = __test8_solution())
	print('   ... OK')

def __test9():
	# -- Task 9 --
	print('-- Testing task 9...')
	tests.base.run_once('frequently.bash', answer = ['shell', 'command', 'with', 'value'])
	print('   ... OK')

def run_tests():
	__test1()
	__test2()
	__test3()
	__test7()
	__test8()
	__test9()
