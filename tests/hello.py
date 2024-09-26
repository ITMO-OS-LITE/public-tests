import tests.base

def __test1():
	# -- Task 1 --
	print('-- Testing task 1...')
	tests.base.run_once('hello.bash', answer = 'Hello, world!')
	print('   ... OK')

def run_tests():
	__test1()
