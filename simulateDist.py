import sys
import math
import random

def check_probability_range(p):
	p = float(p)
	if p < 0.0 or p > 1.0:
		print "Probability should be between 0 and 1."
		exit()

def uniform(a, b):
	random_num = float(random.random())
	return random_num * (b - a) + a

def geometric(p):
	count = 0
	while not float(random.random()) <= float(p):
		count += 1
	return count

def neg_binomial(k, p):
	count = 0
	random_num = random.random()
	while float(random_num) > float(p) and (count + 1) != k:
		count += 1
	return count

def normal(mu, sigma):
	random_num_1 = float(random.random())
	random_num_2 = float(random.random())
	z = math.sqrt(float(-2) * math.log(random_num_1)) * (math.cos(float(2) * math.pi * random_num_2))
	return (z * sigma) + mu

def poisson(frequency):
	count = 1
	random_num = 1
	e_frequency = math.exp(-1.0 * frequency)
	while count < 1000:
		random_num = random_num * random.random()
		if random_num <= e_frequency:
			return count
		count += 1

def bernoulli(p):
	random_num = random.random()
	if float(random_num) <= float(p):
		return 1
	else:
		return 0

def binomial(n, p):
	count = 1
	for i in range(n):
		random_num = random.random()
		if float(random_num) <= float(p):
			count += 1
		return count

def exponential(e_lambda):
	random_num = float(random.random())
	return (float(-1) / e_lambda) * (math.log(float(1) - random_num))

def gamma(alpha, g_lambda):
	a = float(0.0)
	for x in range(alpha):
		random_num = float(random.random())
		a += ((float(-1) / g_lambda) * (math.log(float(1) - random_num)))
	return a

def arb_discrete(p):
	random_num = random.random()
	count = 0
	min_prob = float(0.0)
	for prob in p:
		if float(min_prob) < float(random_num) <= (float(min_prob) + float(prob)):
			return count
		count += 1
		min_prob += float(prob)

def distributions(n, distribution, params):
	result = []
	if distribution == "bernoulli":
		probability = params[0]
		check_probability_range(probability)
		for i in range(n):
			sample = bernoulli(probability)
			result.append(sample)
		print result

	elif distribution == "binomial":
		n = int(params[0])
		p = params[1]
		check_probability_range(p)
		if n < 1:
			print "Value of n should be greater than 0."
			exit()
		else:
			for i in range(n):
				sample = binomial(n, p)
				result.append(sample)	
			print result

	elif distribution == "geometric":
		probability = params[0]
		check_probability_range(probability)
		for i in range(n):
			sample = geometric(probability)
			result.append(sample)
		print result

	elif distribution == "neg-binomial":
		k = int(params[0])
		probability = params[1]
		check_probability_range(probability)
		if k < 1:
			print 'Value of k should be greater than 0'
			exit()
		for i in range(n):
			sample = neg_binomial(k, probability)
			result.append(sample)
		print result

	elif distribution == "poisson":
		frequency = float(params[0])
		if not frequency > 0.0:
			print "Frequency should be greater than 0."
			exit()
		for i in range(n):
			sample = poisson(frequency)
			result.append(sample)
		print result

	elif distribution == "uniform":
		a = float(params[0])
		b = float(params[1])
		if a > b:
			print "Value of a should be less than value of b."
			exit()
		elif a <= 0.0 or b <= 0.0:
			print "Values of a and b both should be greater than 0."
			exit()
		else:
			for i in range(n):
				sample = uniform(a, b)
				result.append(sample)
			print result

	elif distribution == "exponential":
		e_lambda = float(params[0])
		if not e_lambda > 0.0:
			print "Value of lambda should be greater than 0."
			exit()
		else:
			for i in range(n):
				sample = exponential(e_lambda)
				result.append(sample)
			print result

	elif distribution == "gamma":
		alpha = int(params[0])
		g_lambda = float(params[1])
		if not alpha >= 1 or not g_lambda >= 0.0:
			print "Value of alpha and lambda should be greater than 0."
			exit()
		else:
			for i in range(n):
				sample = gamma(alpha, g_lambda)
				result.append(sample)
			print result

	elif distribution == "normal":
		mu = float(params[0])
		sigma = float(params[1])
		if sigma <= 0.0:
			print "Value of sigma should be greater than 0."
			exit()
		else:
			for i in range(n):
				sample = normal(mu, sigma)
				result.append(sample)
			print result

	elif distribution == "arb-discrete":
		prob_sum = float(0.0)
		for probability in params:
			check_probability_range(probability)
			prob_sum += float(probability)
		if prob_sum != float(1):
			print "Sum of probabilities should be 1."
			exit()
		else:
			for i in range(n):
				sample = arb_discrete(params)
				result.append(sample)
			print result



if __name__ == '__main__':
	result = []
	try:
		n = int(sys.argv[1])
		distrib = sys.argv[2]
		params = sys.argv[3:]

		distributions(n, distrib, params)

	except IndexError, e:
		print e
		print "Please enter 3 parameters."
	except TypeError, te:
		print te
		print "Enter proper integer and float values."