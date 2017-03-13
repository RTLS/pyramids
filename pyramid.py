import sys, getopt
import timing
from PIL import Image

def main(argv):
	""" Main Function """

	## Defaults sim size ##
	iterate = False
	DEFAULT_WIDTH = 150
	width = DEFAULT_WIDTH
	steps = DEFAULT_WIDTH>>1
	## Defaults rule ##
	rule = 30
	rules = [0x01&(rule>>(x)) for x in range(8)]

	try:
		opts, args = getopt.getopt(argv,"hir:w:s:sd:",["help","iterate","rule=","width=","steps=","start-distribution="])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print_help()
			print("\nDefault args: [Iterate: {}, Rule: {}, Width: {}, Height: {}]".format(iterate, rule, width, steps))
			sys.exit()
		elif opt in ("-i", "--iterate"):
			iterate = True
		elif opt in ("-r", "--rule"):
			if int(arg) not in range(256):
				print("Rule must be an integer in [0,255]")
				sys.exit()
			else:
				rules = [0x01&(int(arg)>>(x)) for x in range(8)]
		elif opt in ("-w", "--width"):
			width = int(arg)
			steps = width>>1
		elif opt in ("-s", "--steps"):
			steps = int(arg)
		elif opt in ("-sd", "--start-distribution"):
			steps = int(arg)

	## Defaults starting condition ##
	data = [[0 for e in range(width)]]
	data[0][width>>1] = 1

	if iterate:
		iterate_all_rules(width, steps)
	else:
		## Save and print specific rule ###
		implement_rules(data,rules,steps)
		save2image(data, rules)
		print2image(data, rules)


def iterate_all_rules(width, steps):
	""" Iterate through all rule combinations, saving to JPEG files """
	for x in range(258):
		data = [[0 for element in range(width)]]
		data[0][width>>1] = 1
		rules = [0x1&(x>>(7-y)) for y in range(8)]
		implement_rules(data,rules,steps)
		save2image(data, rules)


def print_help():
	print("This script simulates elementary (1 dimensional) cellular automata.")
	print("-r specifies a rule number.  Interesting rules can be found at https://en.wikipedia.org/wiki/Elementary_cellular_automaton")
	print("-w specifies a simulation width, and automatically sets steps to width / 2.")
	print("-s overrides default step length")
	print("-i sets to 'iterate mode'.  This iterates and saves-to-image all 256 rules.")
	print("\nSome examples:")
	print("pyramid.py -i (iterate all rules) -w <width>")
	print("pyramid.py -r <rule # (integer)> -w <width> -s <steps>")


def save2image(ptr, rules):
	""" Saves 2D list to JPEG in current folder """
	im = Image.new("1", (len(ptr[0]), len(ptr)))
	sequence = [ptr[x][y] for x in range(len(ptr)) for y in range(len(ptr[0]))]
	im.putdata(sequence)
	rule = 0
	for i,e in enumerate(rules):
		rule += e<<i
	path = "images/"
	name = "pyramid_{}x{}_{}".format(len(ptr[0]),len(ptr), rule)
	ext = ".jpeg"
	im.save(path+name+ext)


def print2image(ptr, rules):
	""" Prints  2D list as JPEG  """
	im = Image.new("1", (len(ptr[0]), len(ptr)))
	sequence = [ptr[x][y] for x in range(len(ptr)) for y in range(len(ptr[0]))]
	im.putdata(sequence)
	im.show()

def map(row, indices):
	""" Computes integer value of three  'overhead' blocks as binary """
	num = 0
	width = len(row)
	for i,index in enumerate(indices):
		if index[1] < 0 or index[1] >= width:
			continue
		else:
			num += row[index[1]]<<(2-i)
	return num


def implement_rules(data, rules, steps):
	""" Carries out rules on data, appending new data """
	""" data is a list of lists of desired width """
	""" rules is list where the nth element """
	""" corresponds to binary interpretation of the three overhead values. """
	""" For example:	"""
	"""	0 1 0 1 1	"""
	"""	    x		"""
	""" x will be replaced by rules[hex2int('101')] """

	width = len(data[0])
	for row in xrange(steps):
		newRow = []
		for col in xrange(width):
			indices = [[row,col+x] for x in range(-1,2)]
			rule = map(data[row], indices)
			newRow.append(rules[rule])
		data.append(newRow)

	return data


if __name__ == '__main__':
	main(sys.argv[1:])
