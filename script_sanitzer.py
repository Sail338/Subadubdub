import fileinput
import re


def santize(script_path:str,delims:list):
    characters= {}
    list_sentences = []
    with open(script_path) as f:
        for line in f:
            for delim in delims:
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
    return (characters,list_sentences)





