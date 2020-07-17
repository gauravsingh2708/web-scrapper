from bs4 import BeautifulSoup
from urllib.request import urlopen
from tabulate import tabulate
my_url='https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy,4io&otracker=nmenu_sub_Electronics_0_Mi'

ureq=urlopen(my_url)
page_soup=BeautifulSoup(ureq.read(),'html.parser')

name=page_soup.findAll('div',{'class':'_3wU53n'})
price=page_soup.findAll('div',{'class':'_1vC4OE _2rQ-NK'})

phone=[['phone_name','phone_price']]
for i in range(0,len(name)):
	phone.append([name[i].text,price[i].text])

print(tabulate(phone,tablefmt='grid'))
	