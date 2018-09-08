import fileinput
import re


print("Add start and end delimeters for non-verbal parts of the script")
print("Example:")
print("Delims: *,*[ENTER][,][ENTER]()[ENTER][ENTER]")
print("Make sure to hit Enter with no input to define when you've finished!")
delims = ["X","X"]
list_delims = []

while len(delims) != 0:
    delimsText = input("Delims: ")
    delims = []
    if len(delimsText) == 0:
        continue
    delims = delimsText.split(",")
    list_delims.append(delims[:])

characters= {}
list_sentences = []
with open("../data/script.txt") as f:
    for line in f:
        for delim in list_delims:
            regex = "\\"+str(delim[0])+".*\\"+str(delim[1])
            line = re.sub(r""+regex,"",line)
        line = re.sub(r"\n","",line)
        line_split = line.split(":")
        if len(line_split) > 1:
            character = line_split[0]
            sentence = line_split[1]
        else:
            continue
        if character not in characters:
            characters[character] = True
        list_sentences.append((sentence,character))


print(characters)
print(list_sentences)



