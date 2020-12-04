from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import json
import secrets 

CACHE_FILENAME="final.json"
cache_dict={}

def save_cache(cache_dict):
 
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def open_cache():

    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


class College:


    def __init__(self, rank='', name='', address='', zipcode='', phone='', url='', state=''):
        self.rank=rank
        self.name=name
        self.address=address
        self.zipcode=zipcode
        self.phone=phone
        self.url=url
        self.state=state

    def info(self):
        return f"#{self.rank} {self.name} : {self.address} {self.zipcode}"
   


def build_state_url_dict():
    

    cache_dict = open_cache()
    if 'state_url_dict' not in cache_dict.keys():
        html=requests.get('https://www.nps.gov/index.htm')
        soup=BeautifulSoup(html.text,'html.parser')
        a= soup.find('ul', class_="dropdown-menu SearchBar-keywordSearch")
        list_1 = a.find_all('a')
        dict_1={}
        for state in list_1:
            dict_1[state.text.lower()] = 'https://www.nps.gov' + state.attrs['href']
        
        cache_dict['state_url_dict']=dict_1
        save_cache(cache_dict)
        return dict_1

    else:
        return cache_dict['state_url_dict']
    

     

def get_site_instance(site_url):

    cache_dict = open_cache()
    
    if site_url in cache_dict.keys():
        print('using chache')
        name=cache_dict[site_url]['name']
        rank=cache_dict[site_url]['rank']
        address=cache_dict[site_url]['address']
        zipcode=cache_dict[site_url]['zipcode']
        phone=cache_dict[site_url]['phone']
        
        return College(rank,name,address,zipcode,phone)

    else:
        print('fetching')
        session = HTMLSession()
        html=session.get(site_url)
        soup=BeautifulSoup(html.text,'html.parser')

        name = soup.find('div', class_="Villain__TitleContainer-sc-1y12ps5-6 IeWTZ").find('h1').text
        rank = soup.findsoup.find('span', class_="ProfileHeading__RankingSpan-esdqt6-3 kzzvUV").text
        
        try:
            address=soup.find('p', class_="Paragraph-sc-1iyax29-0 fOjiwz Hide-kg09cx-0 eEcEPJ").text

        except:
            address=''

        try:
            fzipcode = soup.find('p', class_="adr").find_all('span')[1].find_all('span')[2].text
            zipcode = fzipcode.replace(' ','')
        except:
            zipcode=''
        
        try:
            fphone = soup.find('div', class_="vcard").find_all('p')[1].find('span').text
            phone = fphone.replace('\n','')
        except:
            phone=''

        cache_dict[site_url]={'name':name,'category':category,'address':address,'zipcode':zipcode,'phone':phone}
        save_cache(cache_dict)
        
        
        return College(rank,name,address,zipcode,phone)


def get_sites_for_state(state_url):
  
    html = requests.get(state_url)
    soup_2=BeautifulSoup(html.text,'html.parser')
    
    a1 = soup_2.find_all('li', class_="clearfix")

    url_list=[]

    for parks in a1:
        cols=parks.find_all('h3')
        if cols==[]: 
            continue
        for i in cols:
            url_list.append()
    
    instance_list=[]
    for urls in url_list:
        instance_list.append(get_site_instance(urls))
    
    return instance_list


    session = HTMLSession()
    html=session.get('https://www.usnews.com/best-colleges/az')
    soup=BeautifulSoup(html.text,'html.parser')
    a = soup.find_all('a', class_="Anchor-byh49a-0 DetailCardColleges__StyledAnchor-cecerc-7 cmivCu card-name")
    b={}
    for items in a:
        b[items.text]=f'https://www.usnews.com{items.attrs["href"]}'
    
    print(b)

    c=list(b.items())

    def insert_2(item):
        connection = sqlite3.connect("finaldatabase.sqlite")
        cursor = connection.cursor()
        cursor.execute(f"insert into college(name,url,state) values('{item[0]}','{item[1]}','az')")
        connection.commit()
        connection.close()

    for items in c:
        insert_2(items)

        


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    cache_dict = open_cache()
    if site_object.name in cache_dict.keys():
        print('using cache')
        return cache_dict[site_object.name]
    else:
        print('fetching')
        key = secrets.API_KEY
        origin = site_object.zipcode
        
        response = requests.get(f'https://www.mapquestapi.com/search/v2/radius?origin={origin}&radius=10&maxMatches=10&ambiguities=ignore&outFormat=json&key={key}')
        f=json.loads(response.text)
        cache_dict[site_object.name]=f
        save_cache(cache_dict)
        return f
    

