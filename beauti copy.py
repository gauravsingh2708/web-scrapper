from bs4 import BeautifulSoup
from urllib.request import urlopen
my_url='https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy,4io&otracker=nmenu_sub_Electronics_0_Mi'

ureq=urlopen(my_url)
page_soup=BeautifulSoup(ureq.read(),'html.parser')

containers=page_soup.findAll('div',{'class':'_3wU53n'})
price=page_soup.findAll('div',{'class':'_1vC4OE _2rQ-NK'})
print(containers)
print('name of the mobile phone', '     price of the mobile phone')
for i in range(0,5):
	print(type(containers[i].text))
	break
