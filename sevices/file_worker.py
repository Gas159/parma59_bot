import os

# Define the directory and file name
directory = 'files'
file_name = 'text_raw.txt'

# Construct the full file path
file_path = os.path.join(directory, file_name)

file_path = '../files/text_raw.txt'
absolute_path = os.path.abspath(file_path)
print(absolute_path)
print(file_path)



def refact(file_path):
	try:
		with open(file_path, 'r') as file:
			print("Opening file...")
			text = file.read()
			lst = text.split('\n\n')
			print(lst)
			with open('../files/text_modified', 'w') as file:
				modified_text = [i.strip() for i in lst if i.strip()]
				print(modified_text)
				file.write('\n\n'.join(modified_text))
			print("Reading file...")
	except FileNotFoundError:
		print(f"File '{file_path}' not found.")
	except Exception as e:
		print(f"An error occurred: {e}")


refact(absolute_path)
print(2)
