import os
import random
import re
import sys

DAMPING = 0.85   #阻尼系数
SAMPLES = 10000   #采样次数


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
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
    if corpus[page] == set():
        tmp = dict()
        for key in corpus:
            tmp[key] = 1 / len(corpus)
        return tmp
    else:
        tmp = dict()
        for key in corpus:
            if key in corpus[page]:
                tmp[key] = (damping_factor / len(corpus[page])) + (1 - damping_factor) / len(corpus)
            else:
                tmp[key] = (1 - damping_factor) / len(corpus)
        return tmp


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = dict()
    for key in corpus:
        ranks[key] = 0
    current_page = random.choice(list(corpus.keys()))
    ranks[current_page] += 1
    for i in range(n - 1):
        current_prob = transition_model(corpus, current_page, damping_factor)
        points = list(current_prob.keys())
        probs = list(current_prob.values())
        selected_point = random.choices(points, weights=probs, k=1)[0]
        ranks[selected_point] += 1
        current_page = selected_point
    for key in ranks:
        ranks[key] = ranks[key] / n
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = dict()
    for key in corpus:
        ranks[key] = 1 / len(corpus)
    while True:
        tmp = dict()
        for key in corpus:
            tmp[key] = (1 - damping_factor) / len(corpus)
            for page in corpus:
                if key in corpus[page]:
                    tmp[key] += damping_factor * ranks[page] / len(corpus[page])
                if corpus[page] == set():
                    tmp[key] += damping_factor * ranks[page] / len(corpus)
        diff = 0
        for key in tmp:
            diff += abs(tmp[key] - ranks[key])
        if diff < 0.001:
            break
        ranks = tmp
    return ranks


if __name__ == "__main__":
    main()
