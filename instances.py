from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import json
import secrets




CACHE_FILENAME="final_cache.json"
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


    def __init__(self, rank='', name='', city='', zipcode='', phone='',tuition_in='',tuition_out='',url='',enrollment=''):
        self.rank=rank
        self.name=name
        self.city=city
        self.zipcode=zipcode
        self.phone=phone
        self.tuition_in=tuition_in
        self.tuition_out=tuition_out
        self.url=url
        self.enrollment=enrollment
        

    def info(self):
        return f"[{self.rank}] {self.name}"
   

def build_state_url_dict():
    cache_dict = open_cache()
    if 'state_url_dict' not in cache_dict.keys():
        
        session = HTMLSession()
        html=session.get('https://www.usnews.com/best-colleges')
        soup=BeautifulSoup(html.text,'html.parser')
        a= soup.find('ul', class_="List__ListWrap-rhf5no-0 bXMuQa")
        list_1 = a.find_all('a')
        dict_1={}
        for state in list_1:
            dict_1[state.text.lower()] = 'https://www.usnews.com' + state.attrs['href']
        
        cache_dict['state_url_dict']=dict_1
        save_cache(cache_dict)
        return dict_1

    else:
        return cache_dict['state_url_dict']



def get_college_instance(site_url):


    cache_dict = open_cache()
    
    if site_url in cache_dict.keys():
        print('using cache')
        name=cache_dict[site_url]['name']
        rank=cache_dict[site_url]['rank']
        city=cache_dict[site_url]['city']
        zipcode=cache_dict[site_url]['zipcode']
        phone=cache_dict[site_url]['phone']
        tuition_in=cache_dict[site_url]['tuition_in']
        tuition_out=cache_dict[site_url]['tuition_out']
        url=cache_dict[site_url]['url']
        enrollment=cache_dict[site_url]['enrollment']
        
        
        return College(rank,name,city,zipcode,phone,tuition_in,tuition_out,url,enrollment)

    else:
        print('fetching')
        session = HTMLSession()
        html=session.get(site_url)
        soup=BeautifulSoup(html.text,'html.parser')

        
        try:
            a = soup.find('p', class_="Paragraph-sc-1iyax29-0 fOjiwz Hide-kg09cx-0 eEcEPJ").text
        except:
            try:
                a= soup.find('span', class_="Span-sc-19wk4id-0 Wakanda__Subheading-rzha8s-5 Heading__DynamicSubheading-sc-6a32fq-4 itUSTS").text
            except:
                a=''
        

        try:
            tuitionx = soup.find('a', attrs={"class" :"Anchor-byh49a-0 gbsGda","data-tracking-placement":"Tuition and Fees"}).next_element
            tuition_in = int(tuitionx.replace('$','').replace(',',''))
            tuition_out = tuition_in
        except:
            try:
                tuitionx = soup.find('a', attrs={"class" :"Anchor-byh49a-0 gbsGda","data-tracking-placement":"Tuition and Fees (in-state)"}).next_element
                tuition_in = int(tuitionx.replace('$','').replace(',',''))
                tuitiony = soup.find('a', attrs={"class" :"Anchor-byh49a-0 gbsGda","data-tracking-placement":"Tuition and Fees (out-of-state)"}).next_element
                tuition_out = int(tuitiony.replace('$','').replace(',',''))
            except:
                tuition_in=0
                tuition_out=0




        try:
            name = soup.find('div', class_="Villain__TitleContainer-sc-1y12ps5-6 IeWTZ").find('h1').text
            
        except:
            try:
                name = soup.find('h1', class_="Heading__HeadingStyled-sc-1w5xk2o-0 bSrbmR Heading-sc-1w5xk2o-1 Wakanda__Title-rzha8s-10 kiCVGj").next_element + soup.find('span', class_="HeadingWithIcon__NoWrap-sc-1kfmde2-1 fvOhNd").next_element
                
            except:
                name=''
                

        try :
            rank = soup.find('span', class_="ProfileHeading__RankingSpan-esdqt6-3 kzzvUV").text
        except:
            try:
                rank = soup.find('span', class_="Span-sc-19wk4id-0 Wakanda__TopRanking-rzha8s-6 Heading__RankBlurb-sc-6a32fq-3 jlWEvL").next_element + ' in National Universities'
            except:
                rank=''

        
        try:
            city=a.split('|')[0].replace(name.split('|')[0].split(' ')[-2].replace(' ',''),'')

        except:
            city=''

        try:
            zipcode = a.split('|')[0].split(' ')[-2].replace(' ','')
        except:
            zipcode=''
        
        try:
            phone = a.split('|')[-1].replace(' ','')
           
        except:
            phone=''
        
        try:
            enrollmentx = soup.find('a', attrs={"class" :"Anchor-byh49a-0 gbsGda","data-tracking-placement":"Total Enrollment"}).text
            enrollment=int(enrollmentx.replace(',',''))
        except:
            enrollment=''


        
        cache_dict[site_url]={'rank':rank,'name':name,'city':city,'zipcode':zipcode,'phone':phone,'tuition_in':tuition_in,'tuition_out':tuition_out,'url':site_url,'enrollment':enrollment}
        save_cache(cache_dict)
        
        
        return College(rank,name,city,zipcode,phone,tuition_in,tuition_out,site_url,enrollment)


def get_sites_for_state(state_url):


    session = HTMLSession()
    html=session.get(state_url)
    soup_2=BeautifulSoup(html.text,'html.parser')


    a1 = soup_2.find_all('a',class_="Anchor-byh49a-0 DetailCardColleges__StyledAnchor-cecerc-7 cmivCu card-name")
    url_list=[]
    for b in a1:
        url_list.append('https://www.usnews.com' +b.attrs['href'])
    
    instance_list=[]
    for urls in url_list:
        instance_list.append(get_college_instance(urls))
    
    return instance_list



def get_nearby_places(college_object):

    cache_dict = open_cache()
    if college_object.name in cache_dict.keys():
        print('using cache')
        return cache_dict[college_object.name]
    else:
        print('fetching')
        key = secrets.API_KEY
        origin = college_object.zipcode
        
        response = requests.get(f'https://www.mapquestapi.com/search/v2/radius?origin={origin}&radius=10&maxMatches=10&ambiguities=ignore&outFormat=json&key={key}')
        f=json.loads(response.text)
        cache_dict[college_object.name]=f
        save_cache(cache_dict)
        
        return f


# # session = HTMLSession()
# # html=session.get('https://www.usnews.com/best-colleges/az')
# # soup=BeautifulSoup(html.text,'html.parser')
# # a = soup.find_all('a', class_="Anchor-byh49a-0 DetailCardColleges__StyledAnchor-cecerc-7 cmivCu card-name")
# # b={}
# # for items in a:
 
# #     b[items.text]=f'https://www.usnews.com{items.attrs["href"]}'
# # print(b)

# # c=list(b.items())

# # def insert_2(item):
# #     connection = sqlite3.connect("finaldatabase.sqlite")
# #     cursor = connection.cursor()
# #     cursor.execute(f"insert into college(name,url,state) values('{item[0]}','{item[1]}','az')")
# #     connection.commit()
# #     connection.close()

# # for items in c:
# #     insert_2(items)




# print(build_state_url_dict())

# session = HTMLSession()
# html=session.get('https://www.usnews.com/best-colleges/princeton-university-2627')
# soup=BeautifulSoup(html.text,'html.parser')
# a= soup.find('p', class_="Paragraph-sc-1iyax29-0 fOjiwz Hide-kg09cx-0 eEcEPJ").text

# print(a)


# # def insert_1(item):
# #     connection = sqlite3.connect("finaldatabase.sqlite")
# #     cursor = connection.cursor()
# #     cursor.execute(f"insert into state(statename,url) values('{item[0]}','{item[1]}')")
# #     connection.commit()
# #     connection.close()

# # def statedatabase():
# #     statedict=build_state_url_dict()
# #     statekey=list(statedict.items())

# #     connection = sqlite3.connect("finaldatabase.sqlite")
# #     cursor = connection.cursor()
# #     cursor.execute(f"delete from state")
# #     connection.commit()
# #     connection.close()

# #     for items in statekey:
# #         insert_1(items)

# # statedatabase()
