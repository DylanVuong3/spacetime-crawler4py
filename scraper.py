import re
from urllib.parse import urlparse, urljoin, urldefrag
from collections import defaultdict
from bs4 import BeautifulSoup

LONGEST_PAGE = {
	"url" : None,
	"wordCount" : 0
}
WORD_FREQUENCIES = defaultdict(int)
SUBDOMAINS = defaultdict(set)
FIFTY_COMMON_WORDS = []
UNIQUE_PAGES = set()	
STOP_WORDS = set([
  "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
  "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
  "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
  "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
  "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", 
  "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", 
  "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", 
  "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", 
  "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", 
  "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", 
  "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", 
  "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", 
  "than", "that", "that's", "the", "their", "theirs", "them", "themselves", 
  "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", 
  "they've", "this", "those", "through", "to", "too", "under", "until", "up", 
  "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", 
  "weren't", "what", "what's", "when", "when's", "where", "where's", "which", 
  "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", 
  "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", 
  "yourself", "yourselves"
])

# Utilized AI to guide the project on the packages that would be useful for the scraper function
# Referenced BeautifulSoup and urllib documentation to help build
# Links: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
#        https://docs.python.org/3/library/urllib.parse.html

def scraper(url, resp):

	links = []
	
	# Do a status check for page response
	if resp.status != 200 or resp.raw_response is None:
		return []
				
	if url in UNIQUE_PAGES:
		return []
	
	UNIQUE_PAGES.add(url)

	# Begin parsing if the status check condition is False
	soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

	text = soup.get_text(separator = "")
	words = re.findall(r"[a-zA-Z0-9]+", text.lower())
	wordCount = len(words)

	if wordCount < 50:
		return []

	if wordCount > LONGEST_PAGE["wordCount"]:
		LONGEST_PAGE["wordCount"] = wordCount
		LONGEST_PAGE["url"] = url
	
	for word in words:
		if word not in STOP_WORDS:
			WORD_FREQUENCIES[word] += 1
	
	parsed = urlparse(url)
	if parsed.netloc.endswith("uci.edu"):
		SUBDOMAINS[parsed.netloc].add(url)

	links = extract_next_links(url, resp)

	valid_links = [link for link in links if is_valid(link)]

	return valid_links

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
   	
	links = []

	if resp.status != 200 or resp.raw_response is None:
		return links

	soup = BeautifulSoup(resp.raw_response.content, 'html.parser')

	# Iterate through each link found in the url
	for link in soup.find_all('a', href=True):
		# Grab link, join it and defrag, and then append to links if the url is valid
		href = link.get("href")

		abs_url = urljoin(url, href)

		abs_url, _ = urldefrag(abs_url)

		if is_valid(abs_url):
			links.append(abs_url)

	return links

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
	try:
		parsed = urlparse(url)
		
		if parsed.scheme not in set(["http", "https"]):
			return False
		
		# Return false if url not apart of specified domains
		if not(
			parsed.netloc.endswith("ics.uci.edu") or
			parsed.netloc.endswith("cs.uci.edu") or
			parsed.netloc.endswith("informatics.uci.edu") or
			parsed.netloc.endswith("stat.uci.edu")
		): 
			return False

		if "doku.php" in parsed.path.lower():
			return False

		if parsed.query and re.search(r"(page|sort|filter|sessions|do=|tab_|image=|ns=)", parsed.query.lower()):
			return False

		if parsed.path.count("/") > 10:
			return False

		return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

	except TypeError:
		print ("TypeError for ", parsed)
		raise
