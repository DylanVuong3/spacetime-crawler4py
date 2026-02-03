import sys

# Code Disclosure: Adapted parts of code from https://www.sqlpey.com/python/python-efficient-large-file-reading/
# Time Complexity: O(n)
# Explanation: This method iterates through each line of the txt file ONCE, in each iteration, each character is iterated ONCE and thus would mean that the total time complexity is dependent on the number of tokens as the operations in each iteration take a O(1) time complexity, thus the overall is O(n)

def tokenize(path):
	try:
		token_list = []
		alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

		with open(path, "r") as file:
			for line in file:
				token = ""
				for char in line:
					if char in alphanumeric:
						token += char.lower()
					else:
						if token:
							token_list.append(token)
							token = ""
				if token:
					token_list.append(token)

		return token_list

	except FileNotFoundError:
		print(f"Error: the file '{path}' was not found.")
		sys.exit(1)

	except Exception as e:
		print(f"An unexpected error has occured: {e}")
		sys.exit(1)

# Time Complexity: O(n)
# Explanation: This program iterates through each elment of a <list> parameter only once, since the operations of searching through a dictionary takes O(1) time complexity, the overall time complexity is dependent on the size of the parameter, or O(n)
def computeWordFrequencies(tokens):
	frequency = {}

	for token in tokens:
		if token in frequency:
			frequency[token] += 1
		else:
			frequency[token] = 1

	return frequency

# Code Disclosure: Adapted parts of code from: https://www.geeksforgeeks.org/python/sort-dictionary-by-value-python-descending/
# Time Complexity: O(nlogn)
# Explanation: The sorted functionality used has a documented time complexity of O(nlogn), after the sorting, the program then iterates through each pair in the dictionary, which takes O(n) time, this means that the total time complexity of this program is O(nlogn)
def printFrequencies(freq):
	sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
	for token, count in sorted_freq:
		print(f"{token} = {count}")

def main():

	if len(sys.argv) != 2:
		print("Error: Expected only one input")
		sys.exit(1)

	arg1 = sys.argv[1]
	tokens = tokenize(arg1)
	freq = computeWordFrequencies(tokens)
	printFrequencies(freq)

if __name__ == "__main__":
	main()

