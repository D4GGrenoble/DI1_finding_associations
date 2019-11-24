import pandas as pd
import string
import spacy
from collections import defaultdict

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def handle_apostrophe(words):
    """
    Detect words like "l'activité" or "d'un"
    and divide them in "l" "activité" and "d" "un"
    """
    final_words = []
    for w in words:
        start_ind = 0
        for indice, letter in enumerate(w):
            if letter == "'":
                final_words += [w[start_ind:indice]]
                start_ind = indice + 1 # Ignore "'"

        final_words += [w[start_ind:]]

    return final_words

df = pd.read_csv('small_data_shipped/clean_data_small.csv', engine='python', sep=',', nrows=500)
stop_words = set(stopwords.words("french"))
punctuation = string.punctuation + "’"
ignore = {"d\\", "l\\"}
stemmer = SnowballStemmer("french")
lemmer = spacy.load('fr', disable=['parser', 'ner'])


#### Start reading every words and store their stemmed version in a dict ####
count_words = defaultdict(int) # count every occurences of each word
for obj in df.objet_social1_desc.dropna():
    words = word_tokenize(obj, language="french") # Get words from free text
    words = [w for w in words if w not in stop_words] # Ignore stop words
    words = [w for w in words if w not in punctuation] # Ignore punctuation
    words = handle_apostrophe(words) # Divide aprostrophe words
    words = [token.lemma_ for w in words for token in lemmer(w)] # Lemmatize words
    words = [w for w in words if len(w) > 2] # Ignore useless letters
    words = [w for w in words if w not in ignore]

    for w in words:
        count_words[w] += 1


#### Sort by number of times a word appear ####
group_by_count = defaultdict(list) # Inverse the dict count_words
for word in count_words:
    group_by_count[count_words[word]] += [word]

sorted_keys = sorted(group_by_count, reverse=True)

print("Most common words found (in order) :")
for count in sorted_keys[:20]:
    print("{}: {}".format(count, ", ".join(group_by_count[count])))
print("\n\n")


#### Detection of the categories by founding the most common word used in the description ####
filtered_titre = df.titre[df.objet_social1_desc.notna()] # We only keep the titles where the description is not null

categories = set()
first_keys = sorted_keys[:30]
for k in first_keys:
    categories |= set(group_by_count[k])

titre_categories = defaultdict(set)
for titre, obj in zip(filtered_titre, df.objet_social1_desc.dropna()):
    words = word_tokenize(obj, language="french") # Get words from free text
    words = [w for w in words if w not in stop_words] # Ignore stop words
    words = [w for w in words if w not in punctuation] # Ignore punctuation
    words = handle_apostrophe(words) # Divide aprostrophe words
    words = [token.lemma_ for w in words for token in lemmer(w)] # Lemmatize words
    words = [w for w in words if len(w) > 2] # Ignore useless letters
    words = [w for w in words if w not in ignore]

    for w in words:
        if w in categories:
            titre_categories[titre] |= {w}

print("Number of categories : {}".format(len(categories)))
print(", ".join(categories))
print("\n\n")

for count, titre in enumerate(titre_categories):
    print("{} : {}".format(titre, ", ".join(titre_categories[titre])))

    if count >= 30:
        break
