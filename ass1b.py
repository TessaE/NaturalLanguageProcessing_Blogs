import os
import re
import operator
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

path_blogs = r"C:\Users\TessaElfrink\Documents\Uni\NaturalLanguageProcessing\dataset\blogs\train"
path_twitter = r"C:\Users\TessaElfrink\Documents\Uni\NaturalLanguageProcessing\dataset\twitter\train"
out_file = open(r"C:\Users\TessaElfrink\Documents\Uni\NaturalLanguageProcessing\dataset\output.txt", 'w')
all_words = []

def process_text(text_file):
    """Return a list of all the words in the given text, stripped of punctuation marks and in lower case, POS-tagged."""
    # word_tokenize(text) maakt een lijst waarin elk woord of leesteken uit de tekst een element is
    f = open(text_file, encoding="utf8", errors="ignore")
    word_list = word_tokenize(f.read().strip())
    new_word_list = []
    # filter op tekstelementen die bestaan uit letters, een apostrof of een streepje (zoals binnen een woord kan voorkomen)     
    r = re.compile("[a-z'-]+")
    for word in word_list:
        word = word.lower()
        if r.match(word):
            # in de nieuwe woordenlijst komen alleen woorden, geen leestekens
            new_word_list.append(word)
    all_words.extend(new_word_list)
    return new_word_list

def process_files(path_blogs, path_twitter):
    files_blogs = os.listdir(path_blogs)
    files_twitter = os.listdir(path_twitter)

    f_word_list = []
    m_word_list = []
    r = re.compile("^F")
    
    print("started processing...")
    for file in files_blogs:
        p = path_blogs + "\\" + file       
        if r.match(file):
            f_word_list.extend(process_text(p))         
        else:
            m_word_list.extend(process_text(p))
    
#     for file in files_twitter[3:8]:
#         p = path_twitter + "\\" + file       
#         if r.match(file):
#             f_word_list.extend(process_text(p))           
#         else:
#             m_word_list.extend(process_text(p))
    print("finished processing...")   
    return f_word_list, m_word_list
    
def count_words(word_list):
    """Count the words that occur in one class."""
    new_list = {}
    print("started counting..")
    for word in word_list:
        if word in new_list:
            new_list[word] += 1
        else:
            new_list[word] = 1
    print("finished counting..")
    return new_list

def compare_words(class1_list, class1_counts, class2_list, class2_counts):
    """Check which words occur more often in class1 than in class2, return the n most distinguishing words from the list."""
    word_probs = {}
    print("started comparing..")
#   P(w|class1)/P(w|class2)
    for word in all_words:
        count1 = 0
        count2 = 0
        if word in class1_list:
            count1 = class1_counts[word]
        if word in class2_list:
            count2 = class2_counts[word]
            
            prob = (count1 + 1/ len(class1_list) + 2) / (count2 + 1/ len(class2_list) + 2)
            word_probs[word] = prob
    
    print("started sorting..")
    # sorteer woordlijst op scores (van laag naar hoog)   
    sorted_word_probs = sorted(word_probs.items(), key=operator.itemgetter(1))
    # selecteed x aantal hoogste scores in de lijst
    best = sorted_word_probs[-100:]
    
    print("started tagging..")
    tag_list = []
    for item in best:
        tag_list.append(item[0])
    #print(best)
    tagged_list = dict(pos_tag(tag_list))
    
    print("started writing..")
    for item in best:
        out_file.write(item[0] + "\t" + str(item[1]) + "\t" + tagged_list[item[0]] + "\n")
    
    print("done!")
    return word_probs

f_word_list, m_word_list = process_files(path_blogs, path_twitter)
f_count_list = count_words(f_word_list)
m_count_list = count_words(m_word_list)
#print(f_word_list)
#print(m_word_list)
compare_words(f_word_list, f_count_list, m_word_list, m_count_list)
