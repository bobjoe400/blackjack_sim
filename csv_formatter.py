input = open("strategy.txt")
output = open("strategy.csv", "w")
lines = input.readlines()
output.write(",".join(['PC'] + lines[0].strip().split('\t')) + "\n")
for line in lines[1:]:
	output.write(",".join(line.strip().split('\t')) + "\n")
input.close()
output.close()