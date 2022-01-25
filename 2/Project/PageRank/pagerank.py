import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    N = len(corpus)
    probDist = {}
    if len(corpus[page]) == 0:#If the page has no outgoing links
        for p in corpus:
            probDist[p] = 1 / N#Probability Distribution that chooses randomly among all pages
    else:
        for p in corpus:
            probDist[p] = (1-damping_factor) / N
        for lp in corpus[page]:
            probDist[lp] += damping_factor/len(corpus[page])
    return probDist

#{'1.html': {'2.html'}, '2.html': {'1.html', '3.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}}
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pageRanks = {}
    for page in corpus:
        pageRanks[page] = 0
    curPage = random.choice(list(corpus.keys()))
    pageRanks[curPage] = 1
    for pagesChecked in range(n):
        probDist = transition_model(corpus, curPage, damping_factor)
        curPage = random.choices(list(probDist.keys()), weights = tuple(probDist.values()), k = 1)[0]
        pageRanks[curPage] += 1
    for page in pageRanks:
        pageRanks[page] = pageRanks[page]/n
    return pageRanks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Give each page a starting value
    pageRanks = {}
    N = len(corpus)
    for page in corpus:
        pageRanks[page] = 1/N
    
    greatestChange = 1
    while greatestChange > .001:#Loop until we reach convergence
        #Reset values from the previous loop
        greatestChange = 0
        newRanks = {}

        for page in corpus:#Loop through all pages
            newRank = 0
            linkedPages = getLinkedPages(corpus, page)
            #Formula stuff(Might be wrong, come back here if values dont match)
            newRank = (1 - damping_factor)/N
            for linkedPage in linkedPages:#Loop through linked pages
                numLinks = len(corpus[linkedPage])
                if numLinks == 0:
                    numLinks = N
                newRank += damping_factor*(pageRanks[linkedPage]/numLinks)
            #Update the greatest change if needed
            change = abs(newRank - pageRanks[page])
            if change > greatestChange:
                greatestChange = change
            #Save the new rank of the current page
            newRanks[page] = newRank
        #Update the rank values of all pages with their new ranks
        for page in pageRanks:
            pageRanks[page] = newRanks[page]
    return pageRanks

def getLinkedPages(corpus, curPage):  
    """
    Returns all pages in 'corpus' which link to 'curPage'
    """
    linkedPages = []
    for page in corpus:
        if curPage in corpus[page]:
            linkedPages.append(page)
    return linkedPages

if __name__ == "__main__":
    main()
