import stop
#POSTIVE WORDS
file_path = "MasterDictionary/positive-words.txt"

with open(file_path, "r") as file:
    #reading contents
    file_contents = file.read().split()

file_contents=[x.lower() for x in file_contents]
# print(file_contents)
file_contents= list(set(file_contents))
# print(len(file_contents))
#THERE ARE 2006 UNIQUE POSITIVE WORDS IN TOTAL

#POSITIVE WORDS THAT ARE NOT IN STOP WORDS 
positive_words=[]
for w in file_contents:
    if w not in stop.stop_words_array:
        positive_words.append(w)

# print(len(positive_words))

# THERE REMAINS 1906 POSITIVE WORDS WHICH MEANS OUT OF 2006 TOTAL POSITIVE WORDS 100 POSITIVE WORDS ARE PRESENT IN THE STOP WORDS LIST.

# print(len(stop.stop_words_array))



#NEGATIVE WORDS
file_path_n = "MasterDictionary/negative-words.txt"

with open(file_path_n, "r") as file:
    #reading contents
    file_contents_n = file.read().split()

file_contents_n=[x.lower() for x in file_contents_n]
# print(file_contents_n)
file_contents= list(set(file_contents_n))
# print(len(file_contents_n))
#THERE ARE 2006 UNIQUE POSITIVE WORDS IN TOTAL

#SIMIALRLY WITH NEGATIVE WORDS
#NEGATIVE WORDS THAT ARE NOT IN STOP WORDS 
negative_words=[]
for w in file_contents_n:
    if w not in stop.stop_words_array:
        negative_words.append(w)
negative_words= list(set(negative_words))
# print(len(negative_words))
#THERE REMAINS 4693 NEGATIVE WORDS WHICH MEANS OUT OF 4783 TOTAL NEGATIVE WORDS 90 WORDS ARE PRESENT IN THE STOP WORDS LIST.
