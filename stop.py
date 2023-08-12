import os
folder_path = "StopWords"
#empty list to store the words
stop_words_array = []

#Read the contents of all files in the folder and extract words
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    with open(filepath, "r") as file:
        # Read the content of the file and split it into words
        words = file.read().split()
        stop_words_array.extend(words)

stop_words_array=[x.lower() for x in stop_words_array]

#list to a set to remove duplicate words
stop_words_array = list(set(stop_words_array))
# print(len(stop_words_array))