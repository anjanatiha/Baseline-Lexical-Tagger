
# coding: utf-8

# In[3]:



# coding: utf-8

# In[1]:


'''
* Author           : Anjana Tiha
* Assignment No    : #3 
* Course           : Natural Language Processing (COMP 8780)
* Semester         : Spring 2018
* Course Instructor: Professor Visali Rus
* University       : University of Memphis 
* Deadline         : Due Mar. 1, 2018.
*
* Description      : 1. Builds a baseline statistical tagger by using the assignment#2's hash of hashes.
*                    2. Train baseline lexicalized statistical tagger on the entire BROWN corpus.
*                    3. Uses the baseline lexicalized statistical tagger to tag all the words in the SnapshotBROWN.pos.all.txt file.
*                    4. Evaluates and reports the performance of this baseline tagger on the Snapshot file.
*                    5. Adds rules for unknown word tagging.
*                    6. Tests on new text collected from article.
*
* Description      : 1. Maps each parse tree in the BROWN.pos.all file into one-line sentences.
* (Detailed)         2. Each sentence span a single line in the output file.
*                    3. Generates the hash of hashes from the clean file BROWN-clean.pos.txt in word:pos:freq format. 
*                    4. Takes the most frequent tag and use it to tag the words in all the sentences from the SnapshotBROWN-clean.pos.txt file. 
*                    5. Report the performance (Accuracy, error, percentile not prensent in tagset) of this tagger.
*
* Comments         : Please use Anaconda editor for convenience.
* Tools Requirement: Anaconda, Python 
* Current Version  : v1.0.2.1
* Version History  : v1.0.0.0.0 (Coppied Assignment 2)
*                  : v1.0.0.0.1 (Completed lexicalized statistical tagger for full corpus and tested on snapshot)
*                  : v1.0.4.2 (Completed adding unknown word rules and tested on new text)      
* Last Update      : 02.28.2018 (Time : 06:22am)
*
'''         


# In[2]:


'''
Question 

Assignment #3: Due March 1.
-----------------------------------------------------------------------
Instructor Instruction:

Remember that the homework is due by midnight on the due date. You must 
turn in a soft copy via email to TA. Your submission should have a cover page 
and one or more summary pages where you provide for each problem the
answer. You should not submit the data you use if the data is too
large. You must submit your code.


1. Build a baseline statistical tagger.

(i) [10 points] Use the assignment#2's hash of hashes to train a
baseline lexicalized statistical tagger on the entire BROWN corpus.

(ii) [20 points] Use the baseline lexicalized statistical tagger to tag 
all the words in the SnapshotBROWN.pos.all.txt file. Evaluate and report the
performance of this baseline tagger on the Snapshot file.

(iii) [20 points] add few rules to handle unknown words for the tagger
   in (ii). The rules can be morphological, contextual, or of other
   nature. Use 25 new sentences to evaluate this tagger (the (ii) tagger +
   unknown word rules). You can pick 25 sentences from a news article
   from the web and report the performance on those.

NOTE: You should only consider the 45 proper tags from Penn Treebank
tagset (available in the slides). You should disregard tags such as
-NONE-, etc.

-----------------------------------------------------------------------
'''


# In[3]:

import re
import os
import operator
from collections import OrderedDict


# removes file
def remove_file(filename):
    try:
        os.remove(filename)
        return 1
    except OSError:
        return 0
    

# In[5]:


# reads file
def read_file(filename):             
    with open(filename, 'r', encoding="utf8") as content_file:
        content = content_file.read()
    return content


# read file line by line/ splits by line
def read_file_line_by_line(filename):             
    with open(filename, 'r', encoding="utf8") as content_file:
        content = content_file.readlines()
    return content


# writes file whole content
def write(filename, content):
    fh = open(filename,"w+", encoding="utf8")
    fh.write(content)
    fh.close()
    return filename


# In[6]:


# print file in one pass
def print_complete_file(filename):             
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content


# print file line by line/ splits by line
def print_file_line_by_line(filename):             
    with open(filename, 'r') as content_file:
        content = content_file.readlines()
    return content


# In[7]:

# prints dictionary
def print_dict(dict_s):
    for i in dict_s:
        print(i)


# In[8]:


# converts text to lowercase
def to_lower(text):
    return text.lower()

# removes all spaces 
# replaces " " with ""
def remove_all_space(text):
    return re.sub(r' +', '', text)

# removes multiple spaces with single space
def remove_multi_space(text):
    return re.sub(r' +', ' ', text)


# add space before and after the punctuation
def add_space_punc(text):
    return re.sub("([^a-zA-Z0-9])", r' \1 ', text)

# remove all the characters except alphabetical
# removes special characters and numerical charcharters
def remove_non_alpha(text):
    return re.sub(r'[^a-zA-Z]', ' ', text)


# check if substring present in text
def text_contains(text, substr):
    if(substr in text): 
        return 1
    else:
        return 0


# splits stiong by space or " "
def split_string(text):
    return text.split()


# In[9]:


# Removes all blank lines
def remove_extra_blank_lines(content):   
    return re.sub(r'\n\s*\n', '\n', content)
    return txt



# get word frequency from word list
def get_word_freq(word_tokens):
    word_freq = {}
    for w in word_tokens:
        if w in word_freq:
            word_freq[w] +=1
        else:
            word_freq[w] = 1
    return word_freq


# sort dictionary by key or value
def sort_dict(dict_x, type_s):
    if type_s == "key":
        return sorted(dict_x.items(), key=operator.itemgetter(0))
    elif type_s == "val":
        return OrderedDict(sorted(dict_x.items(), key=operator.itemgetter(1), reverse=True))
    else:
        return OrderedDict(sorted(dict_x.items(), key=operator.itemgetter(0), reverse=True))
    
# prints first num number of dictionary key and valye pair
def print_most_dict(dict_map, num):
    count = 0
    print("*********************************************")
    for tag in dict_map:
        print(tag, " : ", dict_map[tag])
        count +=1
        if count >= num:
            break
    print("*********************************************")
    print("\n\n")


# In[10]:


# read annotated file with pos
# clean file and save text in pos: word format 
def get_pos_word(text, output_file):
    blacklist = ["-NONE-", "-LRB-", "-RRB-"]  
    eof_txt = "(TOP END_OF_TEXT_UNIT)"
    i = 0
    current_line = ""
    remove_file(output_file)
    
    with open(output_file, 'a') as the_file:
        for line in text:
            if eof_txt in line:
                current_line = current_line.strip()
                if current_line != "":
                    the_file.write(current_line + "\n")
                current_line = ""
                continue
            else:
                temp = line.rsplit('(')
                temp = temp[len(temp)-1] 
                temp = temp.rsplit(')')
                temp = temp[0]
                #temp = temp.strip()
                pass_iter = 0
                for item in blacklist:
                    if item in temp:
                        pass_iter = 1
                        break
                if pass_iter == 1:
                    continue
                else:
                    #temp_test = re.sub(r'[^a-zA-Z0-9]', ' ', temp) 
                    #temp_test = remove_all_space(temp_test)
                    temp_test  = temp
                    if temp_test == "":
                        continue
                    else:
                        temp_vocab = temp.split() 
                        if len(temp_vocab) == 2:
                            temp = temp.strip()
                            current_line += temp + " "  


# In[11]:



# get pos and frequency of each word in a document map={word:{pos:freq}} format
def get_has_word_pos_freq(text):
    pos = ""
    word_pos = {}
    curr_pos_word_freq = {}
    for line in text:
        line = line.strip()
        temp = line.split(" ")
        for i in range(len(temp)):
            if temp[i] == "\n":
                pos = ""
                continue
            if i%2 == 0:
                pos = temp[i]
            else:
                vocab = temp[i]
                vocab = to_lower(vocab)
                if vocab in word_pos:
                    curr_pos_word_freq = word_pos[vocab]
                    if pos in curr_pos_word_freq:
                        curr_pos_word_freq[pos] = curr_pos_word_freq[pos] + 1 
                    else:
                        curr_pos_word_freq[pos] = 1
                else:
                    curr_pos_word_freq[pos] = 1
                    word_pos[vocab] = curr_pos_word_freq

                curr_pos_word_freq = {}   
    return word_pos


# In[12]:


# get frequency of each tag
def get_tag_freq(word_pos):
    tag_dict_freq = {}
    for word in word_pos:
        word_tags = word_pos[word]
        for tag in word_tags:
            if tag in tag_dict_freq:
                tag_dict_freq[tag] = tag_dict_freq[tag] + word_tags[tag]
            else:
                tag_dict_freq[tag] = word_tags[tag]
    return tag_dict_freq


# In[13]:



# set maximum frequent pos to word
def set_max_pos(word_pos):
    word_pos_ch = {}

    for word in word_pos:
        cur_pos = ""
        curr_word_pos_freq = 0
        curr_word_pos = word_pos[word]
        for pos in curr_word_pos:
            if curr_word_pos_freq < curr_word_pos[pos]:
                curr_word_pos_freq = curr_word_pos[pos]
                cur_pos = pos
        word_pos_ch[word] = cur_pos
    return word_pos_ch


# In[14]:



# get accuracy of adjusted tag in tagged text
def get_tagger_performance(text, word_tag_max):
    pos = ""
    total_count = 0
    correct_tag_count = 0
    word_unspecified = 0
    for line in text:
        line = line.strip()
        temp = line.split(" ")
        for i in range(len(temp)):
            if temp[i] == "\n":
                pos = ""
                continue
            if i%2 == 0:
                pos = temp[i]
            else:
                vocab = temp[i]
                vocab = to_lower(vocab)
                if vocab in word_tag_max:
                    curr_pos_word = word_tag_max[vocab]
                    if pos == curr_pos_word:
                        correct_tag_count +=1 
                    total_count += 1
                else:
                    word_unspecified +=1

    return total_count, correct_tag_count, word_unspecified

# calculate accuracy
# calculate error, and percentile not present in tagset for tagging
def accuracy_tag(total_count, correct_tag_count, word_unspecified):
    accuracy = (float(correct_tag_count) / float(total_count)) * 100
    error = 100 - accuracy
    word_unspecified_percentile = (float(word_unspecified) / float(total_count)) * 100
    return accuracy, error, word_unspecified_percentile


# In[15]:


# all the task in assignment 2
def assignment2(input_file, output_file, num):
    print("\n ______________________________________________Begin_____________________________________________________\n")
    print(" Processing File:  \"", input_file, "\" ..............................\n")
    text = read_file_line_by_line(input_file)
    get_pos_word(text, output_file)
    text = read_file_line_by_line(output_file)
    word_pos = get_has_word_pos_freq(text)
    tag_dict_freq = get_tag_freq(word_pos)
    tag_dict_freq = sort_dict(tag_dict_freq, "val")
    
    print(" Most Frequent 20 Tags/POS of File - ", input_file, " : ")
    print(" ___________________________________________________________________")
    print_most_dict(tag_dict_freq, num)
    word_tag_max = set_max_pos(word_pos)
    total_count, correct_tag_count, word_unspecified = get_tagger_performance(text, word_tag_max)
    accuracy, error, word_unspecified_percentile = accuracy_tag(total_count, correct_tag_count, word_unspecified)
    print("\n     Performance Report of File - %s %s "% (test_file, " : "))
    print(" ___________________________________________________________________")
    print(" ***********************************************************************************")
    print("     Accuracy Percentile                    : %s%s" % (accuracy,"%"))
    print("     Error Percentile                       : %s%s" % (error,"%"))
    print("     Unspecified Word in Tagset(percentile) : %s%s" % (word_unspecified_percentile,"%"))
    print(" ***********************************************************************************")
    print("\n ______________________________________________END_____________________________________________________\n\n\n")
    return word_tag_max

# In[16]:



# baseline_lexical_tagger trained on full brown corpus and tested on snapshot brown corpus 
def baseline_lexical_tagger(input_file, output_file, test_file, test_file_out):
    print("\n ______________________________________________Begin_____________________________________________________\n")
    print(" Processing File: \"%s\"%s" % (input_file, "\n"))
    text = read_file_line_by_line(input_file)
    get_pos_word(text, output_file)
    text = read_file_line_by_line(output_file)
    word_pos = get_has_word_pos_freq(text)
    word_tag_max = set_max_pos(word_pos)
    print("\n______________________________________________Ending Taining_____________________________________________\n")
    print("\n______________________________________________Begin_____________________________________________________\n")
    print(" Processing File: \"%s\"%s" % (test_file, "\n"))
    text = read_file_line_by_line(test_file)
    get_pos_word(text, test_file_out)
    text = read_file_line_by_line(test_file_out)
    total_count, correct_tag_count, word_unspecified = get_tagger_performance(text, word_tag_max)
    accuracy, error, word_unspecified_percentile = accuracy_tag(total_count, correct_tag_count, word_unspecified)
    print("\n     Performance Report of File - \"%s\" %s "% (test_file, " : "))
    print(" ___________________________________________________________________")
    print(" ***********************************************************************************\n")
    print("     Accuracy Percentile                    : %.2f%s" % (accuracy,"%"))
    print("     Error Percentile                       : %.2f%s" % (error,"%"))
    print("     Unspecified Word in Tagset(percentile) : %.2f%s" % (word_unspecified_percentile,"%\n"))
    print(" ***********************************************************************************")
    print("\n ______________________________________________END_____________________________________________________\n\n\n")
    return word_tag_max


# cleans input file and rewrites whole file
# rempoves extra empty lines
def clean_file(filename):
    content = read_file(filename)
    content = remove_extra_blank_lines(content)
    filename = write(filename, content)
    content = read_file_line_by_line(filename)
    return filename, content


# Preprocesses content to seperate words and punctuations
def preprocess_content(content, IGNORE_):
    count = 0
    content_modified = ""
    for line in content:
        line = line.strip()
        if line not in IGNORE_:
            count +=1
            line = add_space_punc(line)
            line = remove_multi_space(line)
            content_modified = content_modified + line  + "\n" 
        else:
            pass
    return content_modified


# tags unknown words for supplementing baseline lexical tagger
def tag_unknown_words(line, pos, word, word_tag_max):
    text = word.strip()
    
    modals = ["can", "could", "may", "might", "will", "would", "shall", "should", "must"]
    wh_determiner = ["what", "which", "whose", "whatever", "whichever"]
    articles = ["a", "an", "the"]
    personal_pronoun = ["I","me", "you", "he", "him", "she", "her", "it", "we", "us", "you", "they", "them"]
    possessive_pronoun = ["mine", "yours", "his", "hers", "ours", "yours", "theirs"]
    
    if text.lower() in modals:
        return "MD"
    elif text.lower() in wh_determiner:
        return "WDT"
    elif text.lower() in articles:
        return "DT"
    elif text.lower() in personal_pronoun:
        return "PP"
    elif text.lower() in possessive_pronoun:
        return "PP$"
    elif text[len(text)-2:] == "ss":
        return "NN"
    elif text[len(text)-2:] == "ed":
        return "VBN"
    elif text[len(text)-3:] == "ing":
        return "VBG"
    elif text[len(text)-2:] == "ly":
        return "BB"
    elif text+"ly" in word_tag_max:
        return "JJ"
    elif text[len(text)-2:] == "us":
        return "JJ"
    elif text[len(text)-3:] == "ble":
        return "JJ"
    elif text[len(text)-2:] == "ic":
        return "JJ"
    elif ((text[:2] == "un") and (text[2:] in word_tag_max)):
        return "JJ"
    elif text[len(text)-3:] == "ive":
        return "JJ"
    elif text[len(text)-1:] == "s":
        return "NNS"
    elif text.isdigit():
        return "CD"
    elif text_contains(text, ".") and (text.strip()!="."):
        return "CD"
    elif text_contains(text,"-") and (text.strip()!="-"):
        return "JJ"
    elif text == "+" or text == "%" or text == "&":
        return "SYM"
    elif text == "{" or text == "(" or text == "[" or text == "<":
        return "("
    elif text == "}" or text == ")" or text == "]" or text == ">":
        return ")"
    elif text == "," or text == ";" or text == "-" or text == "-":
        return ","
    elif text == "." or text == "!" or text == "?":
        return "."
    elif text == '$' or text == '#' or text == ',':
        return text
    elif len(text) == 1 and (text == "\"" or text == "\"" or text == "'" or text == "'" or text == '`' or text == '""' or text == "''"):
        return text
    elif (text.isupper() and len(text)>2):
        return "NNP"
    elif (text[:1]).isupper() and len(text)>1 and to_lower(text[:2])!="wh" and to_lower(text[:2])!="th":
        return "NNP"
    else:
        return "<NONE>"



# Tags content with POS for new content 
# Handles unknown words
def tag_pos_content(content, word_tag_max, IGNORE_):
    count_total = 0
    count_un = 0
    count_tagged = 0
    count_tagged_un = 0
    count_not_tagged_un = 0

    content_modified = ""
    print("-------------------------Some taggging for new text shown below--------------------")
    print("-----------------------------------------------------------------------------------")
    for line in content:
        line = line.strip()
        words = line.split(" ")

        if line not in IGNORE_:
            pos = 0
            for word in words:
                word = word.strip()
                if word in word_tag_max:
                    content_modified = content_modified + word_tag_max[word] + " " + word + " "
                    count_tagged +=1
                    if pos % 20 == 0:
                        print("Word (Known-Tagged)      : %5s   %s"% (word_tag_max[word], word))
                else:
                    tag = tag_unknown_words(line, pos, word, word_tag_max)
                    
                    if tag != "<NONE>":
                        content_modified = content_modified + tag + " " + word + " "
                        if pos % 10 == 0:
                            print("Word (New-Tagged)        : %5s   %s"% (tag, word))
                        count_tagged_un +=1
                    else:
                        if pos % 10 == 0:
                            print("Word (New-Not Tagged)    : %5s  %s"% (tag, word))
                        content_modified = content_modified + "<NONE>" + " " + word + " "
                        count_not_tagged_un +=1
                    count_un +=1

                count_total +=1
                pos +=1
            content_modified = content_modified + "\n"
        else:
            pass
    print(" _____________________________________________________________________________________________")
    return content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un


# main baseline_lexical_tagger for new file
def tagger_unknown_corpus(word_tag_max, test_article, test_article_prep, test_article_tag, IGNORE_):
    filename, content = clean_file(test_article)
    content = preprocess_content(content, IGNORE_)
    write(test_article_prep, content)
    content = read_file_line_by_line(test_article_prep)
    content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un = tag_pos_content(content, word_tag_max, IGNORE_)
    write(test_article_tag, content_modified)
    return content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un

# baseline lexical tagger performance for new content
def tagger_unknown_corpus_performance(content_modified, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un):	
    count_total = float(count_total)
    count_un = float(count_un)
    count_tagged = float(count_tagged)
    count_tagged_un = float(count_tagged_un)
    count_not_tagged_un = float(count_not_tagged_un)


    count_un_prct = (count_un/count_total)*100
    count_tagged_prct = (count_tagged/count_total)*100
    count_tagged_un_prct = (count_tagged_un/count_un)*100
    count_not_tagged_un_prct = (count_not_tagged_un/count_un)*100
    print("\n______________________________________________Begin_____________________________________________________\n")
    print("\n                           Performance Report of New Content                                              ")
    print(" ___________________________________________________________________________________________________________")
    print(" *********************************************************************************************************\n")
    print(" Total Number of Words                          : %s         " % (int(count_total)))
    print(" Tagged Words Known (percentile among all words): %s (%.2f%s)" % (int(count_tagged), count_tagged_prct, "%"))
    print(" New Words(percentile among all words)          : %s (%.2f%s)" % (int(count_un), count_un_prct, "%"))
    print(" Words Tagged(percentile among all new words)   : %s (%.2f%s)" % (int(count_tagged_un), count_tagged_un_prct, "%"))
    print(" Words Could Not Tag (percentile in new words)  : %s (%.2f%s)" %(int(count_not_tagged_un), count_not_tagged_un_prct, "%"))
    print(" *********************************************************************************************************")
    print("\n ______________________________________________END_____________________________________________________\n\n\n")


#Assignment 3
input_file = "data/BROWN.pos.all"
output_file = "out/BROWN-clean.pos.txt"

test_file = "data/SnapshotBROWN.pos.all.txt"
test_file_out = "out/SnapshotBROWN-clean.pos.txt"

test_article = "data/article.txt"
test_article_prep = "out/article_prep.txt"
test_article_tag = "out/article_tag.txt"

IGNORE_ = ["", "\n","\r", "\r\n", "\n\r"]

word_tag_max = baseline_lexical_tagger(input_file, output_file, test_file, test_file_out)
content, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un = tagger_unknown_corpus(word_tag_max, test_article, test_article_prep, test_article_tag, IGNORE_)
tagger_unknown_corpus_performance(content, count_total, count_un, count_tagged, count_tagged_un, count_not_tagged_un)

