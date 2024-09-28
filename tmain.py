import argparse

import tests.hello
import tests.bash_intro

def test_hello():
	print('-- Started hello task')
	tests.hello.run_tests()

def test_bash_intro():
	print('-- Started bash-intro task')
	tests.bash_intro.run_tests()

SELECTOR = {
	'hello': test_hello,
	'bash-intro': test_bash_intro
}

parser = argparse.ArgumentParser()
parser.add_argument('--suite', help = 'select testing task', type = str, choices = list(SELECTOR.keys()), required = True)

args = parser.parse_args()

runner = SELECTOR[args.suite]
runner()
