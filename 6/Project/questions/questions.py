import nltk
import sys
import os
import math
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), encoding="utf8") as f:
            files[filename] = f.read()
    return files
    


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #Filter and tokenize the document
    filteredDoc = document.lower()
    tokens = nltk.word_tokenize(filteredDoc)
    filteredTokens = []
    #Save lists as sets to increase speed
    punctuation = set(string.punctuation)
    stopwords = set(nltk.corpus.stopwords.words("english"))
    for word in tokens:
        if word not in punctuation and word not in stopwords:
            filteredTokens.append(word)
    return filteredTokens
    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    #Create a list of all words found in the documents
    words = []
    for doc in documents:
        for word in documents[doc]:
            if word not in words:
                words.append(word)
    #Calculate an  idf for each word
    idfs = {}
    for word in words:
        docsWithWords = 0
        for doc in documents:
            if word in documents[doc]:
                docsWithWords += 1
        idfs[word] = math.log(len(documents)/docsWithWords)
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    docSums = {}
    for doc in files:
        docSum = 0
        for word in query:
            #Add the tf-idf value for each word in the query
            docSum += files[doc].count(word) * idfs[word]
        #Store the documents tf-idf score
        docSums[doc] = docSum
    #Sort the documents by descending tf-idf score
    top_files = sorted(docSums.keys(), key = lambda doc: docSums[doc], reverse = True)
    return top_files[:n]




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentenceSums = {}
    for sentence in sentences:
        sentenceSum = 0
        for word in query:
            #If the query word is in the sentence, add its idf value to the sentence's score
            if word in sentences[sentence]:
                sentenceSum += idfs[word]
        #Store the sentence's idf score
        sentenceSums[sentence] = sentenceSum
    #Sort the sentences by descending idf score
    top_sentences = sorted(sentenceSums.keys(), key = lambda sentence: sentenceSums[sentence], reverse = True)
    #If sentences have matching idf scores, sort by query term density
    for i in range(len(top_sentences) - 1):
        curSentence = top_sentences[i]
        nextSentence = top_sentences[i+1]
        if sentenceSums[curSentence] == sentenceSums[nextSentence]:
            words_in_query = 0
            for word in sentences[curSentence]:
                if word in query:
                    words_in_query += 1
            cur_qtd = words_in_query/len(sentences[curSentence])

            words_in_query = 0
            for word in sentences[nextSentence]:
                if word in query:
                    words_in_query += 1
            next_qtd = words_in_query/len(sentences[nextSentence])
            if next_qtd > cur_qtd:
                top_sentences[i] = nextSentence
                top_sentences[i+1] = curSentence

    return top_sentences[:n]


if __name__ == "__main__":
    main()
