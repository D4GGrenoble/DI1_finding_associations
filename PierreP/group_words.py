import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv('small_data_shipped/clean_data_small.csv', engine='python', sep=',', nrows=1000)

# Those are some constants for the greater good
sep = {',', ';', '(', "'", ')', ';', '\\', ' ', '’'}
unwanted = {'association', 'club', 'activite', 'organisation', 'groupement', 'pratique', 'plein', 'pour', 'autre'}
replacements = {'éèêë':'e', 'àâä':'a', 'ùûü':'u', 'ôö':'o', 'îï':'i'}

def clean_word(word):
    """
    Clean the word given.
    The word is lowered, all accents are replaced by the original letter.
    return the cleaned word.
    """
    cleaned_word = word.lower()
    for accents in replacements:
        for a in accents:
            cleaned_word = cleaned_word.replace(a, replacements[accents])

    return cleaned_word

def iter_clean_words(text):
    """
    Detect all words in the given text.
    All detected words are then cleaned
    before yielding.
    """
    w = ''
    for c in text:
        if c in sep:
            detected_word = clean_word(w)
            yield detected_word
            w = ''
        else:
            w += c

#### Start reading all words and storing the useful one in a dict ####
count_words = dict() # count every occurences of each word
for obj in df.objet_social1_desc.dropna():
    for word in iter_clean_words(obj):
        if word not in unwanted and len(word) >= 4 and word[:-1] not in unwanted:
            # We only keep the wanted word, 'word[:-1] not in unwanted' is for the plurial version of the unwanted
            # The words that are not long enought are ignored, so we don't get all the 'le', 'la', 'les', 'un' french words.
            if word not in count_words.keys(): # init the entry
                count_words[word] = 0
            count_words[word] += 1


#### Sort by number of times a word appear ####
group_by_count = dict() # inverse the dict count_words
for w in count_words.keys():
    if count_words[w] not in group_by_count:
        group_by_count[count_words[w]] = [w] # Init the entry
    else:
        group_by_count[count_words[w]].append(w)

sorted_keys = sorted(group_by_count, reverse=True)

print("Most common words found (in order) :")
for count in sorted_keys[:20]:
    print("{}: {}".format(count, ", ".join(group_by_count[count])))
print("\n\n")

#### Show a nice WordCloud picture ####
freq_words = dict() # For the 'generate_from_frequencies' method
for w in count_words:
    freq_words[w] = count_words[w]/len(count_words)

wc = WordCloud(width=1920, height=1080).generate_from_frequencies(freq_words)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()

#### Detection of the categories by founding the most common word used in the description ####
filtered_titre = df.titre[df.objet_social1_desc.notna()] # We only keep the titles where the description is not null

categories = []
first_keys = sorted_keys[:30]
for k in first_keys:
    categories += group_by_count[k]

titre_categories = {}
for titre, obj in zip(filtered_titre, df.objet_social1_desc.dropna()):
    for word in iter_clean_words(obj):
        if word in categories:
            if titre not in titre_categories.keys():
                titre_categories[titre] = set() # Init the entry

            titre_categories[titre] |= {word}

print("Number of categories : {}".format(len(categories)))
print(", ".join(categories))
print("\n\n")

i = 0
for titre in titre_categories:
    if i >= 30:
        break

    print("{} : {}".format(titre, ", ".join(titre_categories[titre])))
    i += 1

