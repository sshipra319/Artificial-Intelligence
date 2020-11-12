import sys

input_value = sys.argv[1]
len_input_value = len(input_value)

p_h = []
for i in range(0, len_input_value + 1):
	column = {}
	for j in range(1, 6):
		column[j] = 0
	p_h.append(column)

# Initial probability of h1, h2, h3, h4, h5
p_h[0][1] = 0.1
p_h[0][2] = 0.2
p_h[0][3] = 0.4
p_h[0][4] = 0.2
p_h[0][5] = 0.1	

# Initial probability of cherry
p_c = {}
p_c[1] = 1
p_c[2] = 0.75
p_c[3] = 0.50
p_c[4] = 0.25
p_c[5] = 0

# Initial probability of lime
p_l = {}
p_l[1] = 0
p_l[2] = 0.25
p_l[3] = 0.50
p_l[4] = 0.75
p_l[5] = 1

p_q_c = {}
p_q_l = {}

# Initial probability of observation sequence for cherry and lime
p_q_c[0] = p_h[0][1] * p_c[1] + p_h[0][2] * p_c[2] + p_h[0][3] * p_c[3] + p_h[0][4] * p_c[4] + p_h[0][5] * p_c[5]
p_q_l[0] = p_h[0][1] * p_l[1] + p_h[0][2] * p_l[2] + p_h[0][3] * p_l[3] + p_h[0][4] * p_l[4] + p_h[0][5] * p_l[5]

file = open('result.txt', 'w')

#print("Observation sequence Q: " + input_value + "\n")
#print("Length of Q: " + str(len_input_value) + "\n")
file.write ("Observation sequence Q: " + input_value + "\n")
file.write ("Length of Q: " + str(len_input_value) + "\n")

i = 1

for alphabet in input_value:
	file.write ("After Observation " + str(i) + " = " + alphabet + "\n\n")
	#print("After Observation " + str(i) + " = " + alphabet + "\n\n")
	if alphabet == "L":
		p_q_l[i] = 0
		for j in range(1, 6):
			p_h[i][j] = (p_l[j] * p_h[i-1][j]) / p_q_l[i-1]
			p_q_l[i] = p_q_l[i] + (p_h[i][j] * p_l[j])

			file.write ("P(h" + str(j) + "| Q) = " + str(round(p_h[i][j], 5)) + "\n")
			#print("P(h" + str(j) + "| Q) = " + str(round(p_q_c[i], 5)) + "\n")

		p_q_c[i] = 1 - p_q_l[i]

		file.write("Probability that next candy we pick will be C, given Q: %.5f\n" % round(p_q_c[i], 5))
		file.write("Probability that next candy we pick will be L, given Q: %.5f\n" % round(p_q_l[i], 5))
		#print("Probability that next candy we pick will be C, given Q: %.5f\n" % round(p_q_c[i], 5))
		#print("Probability that next candy we pick will be L, given Q: %.5f\n" % round(p_q_l[i], 5))

	elif alphabet == "C":
		p_q_c[i] = 0
		for j in range(1, 6):
			p_h[i][j] = (p_c[j] * p_h[i-1][j]) / p_q_c[i-1]
			p_q_c[i] = p_q_c[i] + (p_h[i][j] * p_c[j])

			file.write ("P(h" + str(j) + "| Q) = " + str(round(p_h[i][j], 5)) + "\n")
			#print("P(h" + str(j) + "| Q) = " + str(round(p_q_l[i], 5)) + "\n")

		p_q_l[i] = 1 - p_q_c[i]

		file.write("Probability that next candy we pick will be C, given Q: %.5f\n" % round(p_q_c[i], 5))
		file.write("Probability that next candy we pick will be L, given Q: %.5f\n" % round(p_q_l[i], 5))
		#print(round(p_q_c[i], 5))
		#print(round(p_q_l[i], 5))

	i = i + 1

file.close()
