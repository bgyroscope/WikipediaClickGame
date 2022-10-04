# 2022.09.26 
# use beautiful soup to try to find connections between different wikipedia pages
# goal to optimize connection from random page to Jesus using only abstract 

import requests
from bs4 import BeautifulSoup

### function to find links in the abstract 
def find_abstract_links( url, url_head= 'https://en.wikipedia.org', link_lim=50): 
    ''' output the wikipdia links in the abstract of a page '''  

    trial_article_links = [] 
    trial_article_links_names = [] 

    r = requests.get( url ) 
    soup = BeautifulSoup( r.content, 'html.parser' ) 
    bc = soup.find( id="bodyContent") 
    for tempdiv in bc.find_all( 'div' ): 
        if tempdiv.get('id') : 
            if tempdiv['id'] == 'mw-content-text': 
                pp = tempdiv.find_all('p') 
                for ptag in pp: 
                    links = ptag.find_all('a') 
                    for link in links: 
                        if link.get('href') and  link.get('href')[1:5]  == 'wiki' and not( 'Help' in link.get('href') ) and not('Wikipedia' in link.get('href') )  and not( 'Talk' in link.get('href') ) : 
                            trial_article_links.append( url_head+ link.get('href') )  
                            trial_article_links_names.append( link.string )  
  
                            # temporary to shorten seach 
                            if len(trial_article_links) > link_lim: 
                                return trial_article_links, trial_article_links_names

    return trial_article_links, trial_article_links_names




### initializing parameters 

depth_lim = 5       # how many pages in to search 
use_link_lim =  20  # how many links to grab from each page.  



# url_head = 'https://en.wikipedia.org'

random_url = 'https://en.wikipedia.org/wiki/Special:Random'

r = requests.get( random_url ) 
url = r.url

# other example urls
# url = 'https://en.wikipedia.org/wiki/Religion'
# url = 'https://en.wikipedia.org/wiki/Christianity'
# url = 'https://en.wikipedia.org/wiki/Talk:Morality'


destination_url = 'https://en.wikipedia.org/wiki/Jesus'

print( 'Starting URL: ' + url ) 

# perform the search ----------------------------- 
sol_dict = dict() 
visited = set([url] ) 
links, names = find_abstract_links( url, link_lim=use_link_lim )
queue = [ [ [name], 0, elm] for [name,elm] in zip( names,links)    ]   # path, depth, curr_url
for link in links: 
    visited.add(link) 

print( '\n\n\n Visited: \n ', visited ) 


while queue:
    path, depth, curr_url = queue.pop(0)


    print( path, depth, curr_url ) 

    if curr_url == destination_url: 
        # found jesus 
        print( '\n\n Found path: \n\n' , path + [curr_url]  ) 
        exit() 

    elif depth >= depth_lim: 
        continue 

    else:
        # search the links on this page 
        new_links, new_names  = find_abstract_links( curr_url, link_lim = use_link_lim  ) 
        for j, link in enumerate(new_links): 
            if not( link in visited ) :     
                queue.append( [ path+[new_names[j]] , depth + 1 , link ] ) 
                visited.add( link ) 



