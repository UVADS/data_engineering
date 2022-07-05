#!/Users/efrainolivares/envnltk/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import re
import threading
import csv
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import *
from multiprocessing import Lock
import os
from HTMLParser import HTMLParser
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#######################################################################################################################
# Util functions
#######################################################################################################################
def debug(out_str):
    """ Toggle debug comments by setting an the URL_CHECKER_DEBUG environment variable.
        At the command line, execute `export URL_CHECKER_DEBUG=True`.
        Example: `def my_function(): return debug("Hello World")` returns the string "[my_function]Hello World"
    """
    try:
        printout = eval(os.environ["URL_CHECKER_DEBUG"])
    except Exception as e:
        printout = False

    if printout: print "[{}]: {}".format(sys._getframe(1).f_code.co_name, out_str)


def hit(hit_str):
    """ Returns function_called_from: hit_str.  For example `my_function: some valuable message` """
    return "{}: {}".format(sys._getframe(1).f_code.co_name, hit_str)


def save_content_to_file(content, url):
    """ Saves content html to test_suite/some_url_com.  Replaces . with _ for file name compatability """
    try:
        save_content = eval(os.environ["URL_SAVE_CONTENT"])
        save_dest    = os.environ["URL_SAVE_DEST"]
        debug("SAVING CONTENT TO DISK AT: {}".format(save_dest))
    except Exception as e:
        save_content = False

    if not save_content: return

    target_dir = save_dest 
    debug("saving content to {}/{}".format(target_dir, url))
    try:
        with open("{}/{}".format(target_dir, url), 'w') as url_content:
            url_content.write(content)
    except Exception as e:
        debug("Exception saving file to disk: {}".format(e.message))

def get_response_from_file(url):
    try:
        disk_content = eval(os.environ["URL_DISK_CONTENT"])
        save_dest    = os.environ["URL_SAVE_DEST"]
        debug("******** READING CONTENT FROM {}/{} ************".format(save_dest, url))
    except Exception as e:
        disk_content = False
        return None, None

    if not disk_content:
        return None, None

    try:
        with open("{}/{}".format(save_dest, url), 'r') as source:
            content = source.read()
    except:
        print "Exception trying to open file {}/{}".format(save_dest, url)
        raise

    class Response():
        def __init__(self, url, code):
            self.url = url 
            self.status_code = code
            self.headers = { "keys": []} 
        
    response = Response(url, 200)
    return response, content 
# END Util functions

#######################################################################################################################
# Url Filter Main Functions
#######################################################################################################################

def process_one_url(url, lock):
    """ * Wrap around validate_url and catch any unexpected exceptions
        * Use lock to keep output from crowding onto one line.
    """
    try:
        sys.stderr.write("{}\n".format(url))
        url, result_url, status_code, title, junk_flag, sale_flag, real_flag, notes, binary = validate_url(url)
        binary_num = 1 if binary == "true" else 0
        one_str =  "{}\t{}\t{}\t{}".format(url, result_url, binary_num, notes)
        if lock != None:
            with lock:
                print one_str.strip()
    except Exception as e:
        print "{}\t{}\t{}\t{}".format(url,url,"0", "Uncaught exception: {}".format(e.message))


def validate_url(url):
    """ * Get a response and content set
        * If that's good, pass on for processing, otherwise exit with No Response
    """
    response, content = get_response_from_file(url)

    if response == None and content == None:
        response, content = get_response_and_content(url)

    if response == None:
        return url, url, 0, "", "N", "N", "N", hit("No Response"), "false"
    else:
        return evaluate_content_for_200s(response, url, content)



def get_response_and_content(_url):
    """ Return response object and content.
        * All content retrievel should be done here, since we cutoff streaming content, and limit
            the text length it's best to just be done what that once.
        * All http requests, redirects, cookie content, retries etc should also be done.  By the time we exit this
            function everything else should just nothing left to do but text processing.
        * This function is essentialy a classic depth first tree search with the following characteristics
            - initial node is a url
            - successor nodes are found by redirects
            - visiting a node means attempting connection and retrieving content
            - GOAL node is found if 1. no successors, valid response, has content
    """
    debug("START {}".format(_url))
    urls_set = build_end_url_list(_url)
    deja_vu = []
    response = None
    content = None
    safety = 10 # some urls have infinite loop redirs, where urls are generated and put in a meta-equip tag.
    while (len(urls_set) > 0):
        debug(str(urls_set))
        # Get next url, and add it deja_vu list so we don't add it again
        url_iter = urls_set.pop(0)
        deja_vu.insert(0, url_iter)

        # Get response and content
        response, content = get_raw_response_content(url_iter)
        if response == None: continue

        # Check if it has redirects, and not in deja_vu, push it and take next one.
        debug("content_length: {}".format(str(len(content))))
        redir_url = contains_redirect(content, _url)
        if safety < 0:
            debug("loop safety triggered, too many redirects")
            break
        if redir_url:
            safety -= 1
            debug("redir_url: {}".format(redir_url))
            if redir_url not in deja_vu: urls_set.insert(0, redir_url)
            continue

        # If we get here we have no redirects, so if have a response, let's exit!
        if response != None:
            break
        # clear response for clean start on next loop, or to signal failure if this was the last one
        response = None

    # If we got no response at all, leave it be so next function can handle, otherwise check if we want to save content
    if response:
        debug("EXIT: code: {} url: {} content_length: {}".format(response.status_code, response.url, str(len(content))))
        save_content_to_file(content, _url)
    else:
        debug("EXIT: no response object")
    return response, content


def get_raw_response_content(url_iter):
    """ Get response and content, retry if we need a cookie to get to end content """
    response = attempt_connection(url_iter)
    if response == None:
        debug("returning with None")
        return None, None
    not_text = is_non_text_content(response)
    if not_text:
        return response, ""

    content = get_content(response, url_iter)

    cookie_str = contains_setCookie(content)
    if cookie_str != "":
        response = attempt_connection(url_iter, cookie_str)
        content = get_content(response, url_iter)

    return response, content

def contains_redirect(content, _url):
    """ Returns a fully formed url if it found in either of a meta tag, or a frame tag """
    frame_url = contains_frame_redirect(content) if (len(content) < 10000000) else False
    if frame_url:
        debug("frame_url: {}".format(frame_url))
        return frame_url

    meta_redir = contains_special_redirect(content, _url)
    if meta_redir:
        debug("metaredir: {}".format(meta_redir))
        return meta_redir

    return False


def build_end_url_list(url):
    """ Create all possible combinations of http/https and www/. to create first set of candidate urls to attempt """
    http_types = ["http://", "https://"]
    dub_types = ["www.", ""] # this order needs to preserved for testing at www.hgdatascience.com
    http_dub_urls = ["{}{}{}".format(h_type, dub_type, url) for dub_type in dub_types for h_type in http_types]
    return http_dub_urls


def attempt_connection(url, cookie=""):
    """ By default, we try using a User-Agent in the header and no cookie content.
        * Return only the response object, we don't try to get content yet.  The get request is set with the
            stream flag set to True so we can selectively get a known length of content later.
    """
    debug(url.strip())
    header_dict = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36"}
    if cookie != "": header_dict['Cookie'] = cookie
    try:
        response = requests.get(url.decode("utf-8", "replace"), timeout=15, allow_redirects=True, verify=False, headers=header_dict, stream=True)
        if (response == None): response = requests.get(url, timeout=15, allow_redirects=True, verify=False, stream=True)
        return response
    except (ConnectionError, ConnectTimeout, HTTPError, ReadTimeout, Timeout, TooManyRedirects,
            requests.packages.urllib3.exceptions.LocationValueError,
            requests.packages.urllib3.exceptions.LocationParseError, UnicodeDecodeError, ProxyError,
            SSLError, MissingSchema, InvalidSchema, InvalidURL, ChunkedEncodingError, ContentDecodingError,
            StreamConsumedError, RetryError) as e:
        debug(str(e.message))
        return None


def get_content(response, url, content_cutoff=1000000):
    """ Get up to 500000 characters by default.  Return content as a String """
    size = 0
    chunks = []
    for chunk in response.iter_content(chunk_size=1024):
        if size > content_cutoff: break
        chunks.append(chunk)
        size += len(chunk)
    return ''.join(chunks)


def contains_special_redirect(content, response_url):
    """ This regex should catch if there is a `meta http-equiv' redirect in content, and return the url pointed by it """
    regs = [
            "<meta\s+http-equiv\s?=\s?[\'\"]?refresh[\'\"]?[\s\n]*content\s?=\s?[\'\"]?[\d];\s?url\s?=\s?(.*?)\"?\s?\/??>",
            "This Cargo website is currently available here:\s?<a href=[\"\'](.*?)[\"\']"
            ]
    for reg in regs:
        p = re.compile(reg, re.IGNORECASE)
        match = re.search(p, content)
        if match != None:
            if len(match.group(1)) > 0:
                append_string = match.group(1).replace('"', '').replace("'", '')
                debug(append_string)
                if append_string.startswith("http"):
                    return append_string
                else:
                    if not append_string.startswith("/") and not response_url.endswith("/"):
                        append_string = "/" + append_string
                    if append_string.startswith("/") and response_url.endswith("/"):
                        append_string = append_string[1:]
                    special_redirect = "http://" + response_url + append_string
                    return special_redirect.strip()
            else:
                return False
    return False


def contains_frame_redirect(content):
    """ Catch a secondary form of 'redirect', when content is included in a frame.  Return the link to the url in the frame """
    regs = [
        "<frame\s+src=\s?[\'\"](.*?)[\'\"]"
       ]
    for reg in regs:
        p = re.compile(reg, re.IGNORECASE)
        match = re.search(p, content)
        if match != None and match.group(1).startswith("http"):
            return match.group(1)
    return False


def contains_setCookie(content):
    """ This regex catches if there is a setCookie function in the javascript content and returns the cookie material
        so we can retry the http call with the cookie content in the header.
    """
    pa = re.compile("setCookie\(\'(.*?)\',[\s\r\n]?\'(.*?)\'", re.IGNORECASE)
    match = re.search(pa, content)
    if match != None:
        cookie_text = match.group(1) + '=' + match.group(2)
        debug(cookie_text)
        return cookie_text
    return ""

def contains_staff_keyword(content, url, title):
    regexs = [
        "executive",
        "(\w job|job \w)",
        "(\w human|human \w)",
        "agency",
        "employment",
        "(\w resume|resume \w)",
        "posting",
        "job search",
        "(\w talent|talent \w)",
        "(\w consutling|consulting \w)",
        "(\w staffing|staffing \w)",
        "recruit",
        "(\w careers|careers \w)",
        "(\w employment|employment \w)",
        "(\w headhunter|headhunter \w)",
        "(\w hr|hr \w)",
        "(\w resume|resume \w)",
        "head hunter",
        "(\w agency|agency \w)",
        "post",
        "(\w locum|locum \w)",
        "(\w temp|temp \w)",
        "recursos humanos",
        "ricerca(\s|\w)*personale",
        "startups",
    ]
    class MyKeywords(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.keywords = ""

        def handle_startendtag(self, tag, attrs):
            debug("HERE2")
            print tag
            if tag == 'meta':
                for k, v in attrs:
                    if  k == 'name' and v == 'keywords':
                        for k2, v2 in attrs:
                            if k2 == 'content':
                                self.keywords = v2
            debug("OUT")

    parser = MyKeywords()
    content = content.encode('ascii', 'ignore').decode('ascii')
    debug(len(content))
    parser.feed(content)
    keywords = parser.keywords
    debug("KEYWORDS: {}".format(keywords)) 
    hit_words = [] 
    try:
        ls_keywords = keywords.encode('ascii', 'ignore').decode('ascii').lower().split(',')
        for keyword in ls_keywords:
            for regex in regexs:
                m = re.match(regex.strip(), keyword.strip())
                if m != None:
                    if regex not in hit_words:
                         hit_words.append(regex)
        if len(hit_words) == 0:
            return False 
        else:
            return hit(",".join(hit_words))
    except:
        debug("GOT THIS {}".format(str(hit_words)))
        return "STAFFING: Error retrieving keywords for {}".format(url)


def evaluate_content_for_200s(response, url, content):
    """ Input should be valid response object and content in string format.
        * Check header in case it is not text content
        * Check for sale paterns
        * Check for junk patterns
        * If it gets through those 3 main catches, then we call it GOOD.
    """
    content_hit = is_non_text_content(response)
    if content_hit:
        return url, response.url, response.status_code, "", "N", "N", "N", content_hit, "false"
    result_url = response.url

    title = get_title(content)
    # sale ones
    sale_hit = contains_sale_pattern(content)
    if sale_hit:
        debug("Sale pattern: {}".format(sale_hit))
        return url, response.url, response.status_code, title, "N", "Y", "N", sale_hit, "false"


    junk_pattern = contains_junk_pattern(content, url, title)
    if junk_pattern:
        debug("Junk pattern found: {}".format(junk_pattern))
        return url, response.url, response.status_code, title, "Y", "N", "N", junk_pattern, "false"

    
    
    try:
        # to set the env flag on hadoop add '-cmdenv URL_FULL_CONTENT=True'
        full_response = eval(os.environ["URL_FULL_CONTENT"])
    except Exception as e:
        full_response = False
    
    if full_response:
        debug("RETURN FULL CONTENT TO DISK FOR EVAL 200s")
        clean_content = re.compile(r'[\n\r\t\s]+').sub(' ', content.lower())
        return url, response.url, response.status_code, "", "N", "N", "N", hit(clean_content), "true"
    else:
        return url, response.url, response.status_code, "", "N", "N", "N", hit("No sale/junk patterns, nor bad title found"), "true"




def contains_sale_pattern(content):
    """ Run a list or regex on the content, if we have a match, return the matching regex string """
    regs = ['domain.*?\\.com for sale', '\\.com is for sale', 'buy\s.*?this domain' 'domain name.*?for sale', 'domain sale',
            "Below are sponsored listings for goods and services related to: <span class=\"htext\">\S*</span>",
            "HugeDomains.com(.*?)is for sale", "domain is for sale", "the domain \S+ is for sale. To purchase, call Afternic.com",
            "<a\s?rel=\"nofollow\"\s?href=\"https:\/\/www\.hover\.com\/\?source=parked\">",
            "<meta name=\"description\" content=\"Domain registriert bei united-domains\.de\">",
            "<meta name=\"description\" content=\"\S+ is a brandable business domain name for sale!\">",
            "<h2 class=\"txt-no-case\"><span id=\"txt-main-domain-name\" style=\"\">\S+<\/span><strong class=\"text-for-sale\">is for sale!<\/strong><\/h2>"]
    for reg in regs:
        p = re.compile(reg, re.IGNORECASE | re.DOTALL)
        if p.search(content):
            debug(reg)
            return hit(reg)

    texts = ["domain has recently been listed in the marketplace", "domain may be for sale", "Domain Brokerage providing Global Naming Assets Solutions"]
    for text in texts:
        if text in content:
            debug(text)
            return hit(text)

    return False


def contains_junk_pattern(content, url, title):
    """ Run a list or regex on the content, if we have a match, return the matching regex string
        * Last ditch effort, if we can't match a regex, check if title is a known bad indicator.
    """
    # hack: some freaky urls have ( or ) in the name and that breaks things
    url = url.replace("(", "\(").replace(")", "\)")

    if len(content) < 200:
        debug("Low content length {}, checking for junk patterns".format(str(len(content))))
        content = re.sub('\s+', ' ', content)
        if "<" not in content:
            return hit("No html tags in content: {}".format(content))
        else:
            return hit("low content length {} in #{}#".format(str(len(content)), content))

    debug("We have content, try matching patterns")
    patterns = [
                "<h5 class=\"text-center\">Dit domein is geregistreerd door een klant van<\/h5>",
                "Websites are FREE at\s+<a href=\"http:\/\/www.vistaprint.com\/websites.aspx\"\s+rel=\"nofollow\">\s+vistaprint.com\/websites\s+<\/a>",
                "<html><body><h1>It works!<\/h1>\s+<p>This is the default web page for this server.<\/p>",
                "this site is under construction", "this site is currently under construction", "{} is under construction".format(url),
                "This Page Is Under Construction", "403\s?error", "error\s?403", "404.*?page not found", "page not found.*?404",
                "Page Not Found", "This domain is registered at", "This site does not exist", "This page does not exist",
                "domain.*?expired", 'Domain.*?Suspended', "back shortly with a new website",
                "There has been a server misconfiguration", "site.*?not configured",
                "this temporary landing page will be replaced when you publish your site",
                "<html>\s*This website is temporarily unavailable, please try again later",
                "Web Hosting - courtesy of www.bluehost.com", "inquire about this domain",
                "This webpage was generated by the domain owner using sedo",
                "be back soon",
                "<span class=\"parkedtext\">This domain is parked free, courtesy of<\/span>",
                "jQuery.ajax\({ url: 'http:\/\/mcc\.securepaynet\.net\/parked\/park\.aspx\/\?q=",
                "Error\. Page cannot be displayed\. Please contact your service provider for more details",
                "<div id=\"sale_banner_gray\">\s*<a class=\"firstlink\" href=\"https:\/\/latonas\.com\/domains\/marketplace\/\?domain=",
                "<html ng-app\s?=\s?\"wixErrorPagesApp\">",
                "<title>InMotion Hosting<\/title>[\s\S]*Default Server Page<\/h2>",
                "<div id=\"courtesy\">This Web page parked FREE courtesy of <a",
                "iframe src\s?=\s?\"http:\/\/mcc.godaddy.com\/park\/".format(url),
                "https:\/\/www.name.com\/domain\/renew\/{}?.*?renew now<\/a>".format(url),
                "<link rel\s?=\s?[\'\"]shortlink[\'\"] href\s?=\s?[\'\"]https:\/\/enaming\.com\/\?p=",
                "You can access the page without frames with <a href\s?=\s?[\'\"]http:\/\/domainshop.com[\'\"]>",
                "content\s?=\s?\"http:\/\/www\.wix\.com\/lphtml\/parking\"",
                "src\s?=\s?\"http:\/\/parking.parklogic.com\/page\/enhance\.js",
                "src\s?=\s?\"http:\/\/dp.g.doubleclick.net\/apps/domainpark/domainpark\.cgi",
                "src\s?=\s?\"\/\/sedoparking\.com\/frmpark\/",
                "frame src=\"https:\/\/www\.yourhosting\.nl\/parkeerpagina\.html\"",
                "src\s?=\s?\"http:\/\/parkingcrew.net\/jsparkcaf\.php\?regcn",
                "src\s?=\s?\"http:\/\/return\.uk\.uniregistry\.com\/return_js\.php\?d=",
                "src\s?=\s?\"http:\/\/parking\.reg\.ru\/script\/get_domain_data\?domain_name=td-cv\.ru&amp;callback=callback\"",
                "src\s?=\s?\"//i\.cdnpark\.com\/themes\/registrar",
                "src\s?=\s?\"http:\/\/www\.google\.com\/adsense\/domains\/caf\.js\"",
                "\\.com[\s\n\r]*doesn&#8217;t&nbsp;exist",
                "<script type=\"text\/javascript\" src=\"\/\/i\.cdnpark.com\/registrar\/v3\/loader.js\"><\/script><\/body><\/html>",
                "<html><body><b>Http\/1\.1 Service Unavailable<\/b><\/body> </html>",
                "<p>Free One Page Hosting provided by <a href=\"http:\/\/www\.dynadot\.com\/\?drefid=\d+\">Dynadot<\/a>",
                "HTTP\/1\.1 200 OK\nServer: Microsoft-IIS\/8.5",
                "<frame name=\"topFrame\" src=\"http:\/\/www\.discountdomains\.co\.nz\/parked\" scrolling=\"auto\" frameborder=\"0\" marginwidth=\"0\" marginheight=\"0\" noresize> ",
                "window\.top\.location = \"http:\/\/www\.iyfrr\.com\/\?", "<script type=\"text\/javascript\" src=\"http:\/\/iyfrr\.com\/px\.js\?ch=\d\">"
                ]

    for pattern in patterns:
        p = re.compile(pattern, re.IGNORECASE)
        match = re.search(p, content)
        if match != None:
            str_match = re.sub(r'\s+', ' ', match.group())
            debug("Matched pattern: {}".format(str_match))
            return hit(str_match)

    debug("No patterns matched, trying secondary content matches")
    pattern1 = re.compile("page under construction", re.IGNORECASE)
    pattern2 = re.compile("page is hosted by.*?ibacom", re.IGNORECASE)
    match1 = pattern1.search(content)
    match2 = pattern2.search(content)
    pattern3 = re.compile("domain is.*?parked", re.IGNORECASE)
    match3 = pattern3.search(content)
    if (match1 and match2) or match3:
        debug("second try:")
        if (match1 and match2):
            debug("{} : {}".format(match1.group(), match2.group()))
            return hit("{} : {}".format(match1.group(), match2.group()))
        if (match3):
            debug(match3.group())
            return hit(match3.group())

    compact_content = content.replace(" ", "")
    debug("No matches, check {} against bad titles".format(title))
    if is_bad_title(title):
        return hit("bad title: {}".format(title))

    debug("EXIT with title: {}".format(title))
    return False


def get_title(content):
    """ Look for text between the <title> tags, and return it if found """
    content = content[:100000]
    pa = re.compile("<title.*?>(.*?)<\/title>", re.DOTALL | re.IGNORECASE)
    match = re.search(pa, content)
    title = ""
    if match != None:
        title_found = match.group(1)
        title = title_found.replace("\r", "").replace("\n", "").replace("\t", " ")
    return title


def is_bad_title(title):
    """ Match the given text against a list of known bat title indicators.  If match, return matching string """
    bad_examples = ["under construction", "test page", "redirect", "index of", "none ", "expired", "coming soon",
                    "error ", "domain pending", "at directnic", "pending validation", "website disabled",
                    "US Zip Code Information", # verified we need this, urls like 00000.us, 00001.us end up at zipcode.com
                    "domain default page", "non-existent domain", "v-webs hosting services",
                    "be back soon", "something went wrong", "Lunarpages Web Hosting Placeholder Page",
                    "Félicitations ! Votre domaine a bien été créé chez OVH !", "Domaine r&eacute;serv&eacute;",
                    " - For Sale | Undeveloped", "Yahoo&#39;s Aabaco Small Business: Websites, Ecommerce, Email &amp; Local Listings",
                    "service unavailable", "website disabled", "404 Not Found", "Not Found", "Page cannot be found"
                    ]
    for bad_title in bad_examples:
        if bad_title.lower() in title.lower():
            debug(bad_title)
            return hit(bad_title)

    exact_matches = ["web hosting", "webhosting"]
    for ma in exact_matches:
        if title.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "").lower() == ma:
            debug(ma)
            return hit(ma)
    return False


def is_non_text_content(response):
    """ TODO: This is misnamed, it should either be changed to check for html/text only, or be renamed """
    content_type = response.headers["Content-Type"].lower() if 'Content-Type' in response.headers.keys() else False
    content_types = ['audio/mpeg', 'application/octet-stream', 'application/zip', 'video/mp4']
    if content_type and content_type in content_types:
        debug("Content-Type: {}".format(content_type))
        return hit(content_type)
    else:
        return False


def is_header_content(response, key, value):
    """ is the value of this key in the header as expected?
        return True if key value matches, False if key not found or value does not match
    """
    try:
        if response.headers[key].lower() == value:
            return True
        else:
            return False
    except:
        return False


def process_textfile(inf):
    """ This really process stdin as this is the way the script is setup to take input """
    list_of_urls_to_check = [line.rstrip() for line in inf.readlines()]
    return list_of_urls_to_check


if __name__ == "__main__":
    """
        * Take in stdin and push list of urls into a list
        * Take 200 at a time from the list
            - pass each url to process_one_url, with a lock and set off each per thread
        * Each thread call will eventually output it's result to stdout
        * repeat
    """
    list_of_urls_to_check = process_textfile(sys.stdin)
    while len(list_of_urls_to_check) > 0:
        sys.stderr.write("----------\n")
        current = list_of_urls_to_check[-200:]
        del list_of_urls_to_check[-200:]
        lock = Lock()
        threads = [threading.Thread(target=process_one_url, args=(url,lock)) for url in current]
        for thread in threads:
            thread.setDaemon(True)
            thread.start()

        for thread in threads:
            thread.join(timeout=180)
