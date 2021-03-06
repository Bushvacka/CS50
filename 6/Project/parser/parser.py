import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Det NP | AP NP | N PP
VP -> V | V NP | V NP PP | V PP | AVP VP | VP AVP
AP -> Adj | Adj AP
PP -> P NP
AVP -> Adv | Adv AVP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    ALPHABET = ['a', 'b', 'c' ,'d', 'e', 'f', 'g' ,'h', 'i', 'j', 'k' ,'l', 
        'm', 'n', 'o' ,'p', 'q', 'r', 's' ,'t', 'u', 'v', 'w' ,'x', 'y', 'z']
    tokenized = nltk.word_tokenize(sentence.lower())
    for token in tokenized:
        alpha = False
        for char in token:
            if char in ALPHABET:
                alpha = True
                break
        if not alpha:
            tokenized.remove(token)
    return tokenized


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    subs = tree.subtrees()
    for sub in subs:
        if sub.label() == "NP":
            npc = True
            subsubs = sub.subtrees()
            for subsub in subsubs:
                #Ignoring the original tree, check for subtrees with a NP label
                if subsub != sub and subsub.label() == "NP":
                    #If there is a subtree with a NP, this sub is not a chunk
                    npc = False
            if npc:
                chunks.append(sub)
            #print(f"{sub} Label:{sub.label()}")
    #print(tree.pos())
    return chunks


if __name__ == "__main__":
    main()
