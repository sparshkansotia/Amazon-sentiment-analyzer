#import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from textblob import TextBlob
driver=webdriver.Chrome(executable_path=r'C:\Users\SPARSH\Downloads\phantomjs-2.1.1-windows\chromedriver.exe')

final=[]
positive=0
negative=0
neutral=0
total_rating=0
url="https://www.amazon.in/Oppo-Black-Screen-Display-Offers/product-reviews/B0776VS18L/ref=cm_cr_othr_d_paging_btm_4?ie=UTF8&reviewerType=all_reviews&pageNumber="
#url="https://www.amazon.in/Logitech-F310-Gamepad-Cable-Connection/product-reviews/B003VAHYQY/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
for i in range(1,19):
	#r=requests.get(url+str(i))
	'''r = ''
	while r == '':
	    	try:
			    r = requests.get(url+str(i))
			    break
	    	except:
		        time.sleep(2)
		        continue
	c=r.content'''
	driver.get(url+str(i))
	soup=BeautifulSoup(driver.page_source,"html.parser")
	#soup=BeautifulSoup(c,"html.parser")
	#print (soup.prettify())
	try:
		fm=soup.find_all("div",{"class":"a-section review"})
	except:
		fm=[]
		
	#print (fm)
	#body=soup.find("body",{"class":"custom color-red-flare pattern-noise"})
	#print(body)
	#final=fm[0].find_all("span")
	for listitem in fm:
		d={}
		d["User Rating"]=listitem.find("a",{"class":"a-link-normal"}).text.replace(" out of 5 stars","")
		d["Username"]=listitem.find("a",{"class":"a-size-base a-link-normal author"}).text
		d["Date"]=listitem.find("span",{"class":"a-size-base a-color-secondary review-date"}).text.replace("on ","")
		d["Comment"]=listitem.find("span",{"class":"a-size-base review-text"}).text
		analysis=TextBlob(d["Comment"])
		d["polarity"]=analysis.sentiment.polarity
		d["subjectivity"]=analysis.sentiment.subjectivity
		total_rating+=float(d["User Rating"])
		if d["polarity"]>0.0001:
			positive+=1
		elif d["polarity"]<-0.0001:
			negative+=1
		else:
			neutral+=1		
		final.append(d)

#print(listitem.find("a",{"class":"a-size-base a-link-normal author"}).text)
#print (len(final))
#for item in final:
#	print(item)
print("The effective customer rating of the product is "+str(total_rating/len(final))+" out of 5")
print("There are "+str(positive)+" positive comments that constitute "+str(positive/len(final)*100)+" %  of the total "+str(len(final))+" comments")
print("There are "+str(negative)+" negative comments that constitute "+str(negative/len(final)*100)+" %  of the total "+str(len(final))+" comments")
print("There are "+str(neutral)+" neutral comments that constitute "+str(neutral/len(final)*100)+" %  of the total "+str(len(final))+" comments")
#df=pandas.DataFrame(final)
#df.to_csv("Output.csv")
driver.quit()