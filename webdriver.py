from __future__ import print_function, unicode_literals
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.keys import Keys
from twitter_autom import face_comparing
from facepplib import FacePP, exceptions
import sys

face_detection = ""
faceset_initialize = ""
face_search = ""
face_landmarks = ""
dense_facial_landmarks = ""
face_attributes = ""
beauty_score_and_emotion_recognition = ""

# for i
# df = pd.read_csv('/home/webtunix/Documents/ss/pythonSelenium/new_coyotes_handles.csv', header=0,encoding='ISO-8859–1')        # for username in df['handle']:
# x = df.iloc[309:315,3]
# print(df.index(i))
# exit()

class LoginTest():
    def __init__(self):
        #linkedin login
        self.driver = webdriver.Firefox(executable_path="/home/webtunix/Documents/ss/pythonSelenium/geckodriver")
        self.driver.get("https://www.linkedin.com/")
        sleep(1)
        user = self.driver.find_element_by_xpath('//*[@id="session_key"]')
        sleep(1)
        user.send_keys('8968397005')
        sleep(1)

        pasd = self.driver.find_element_by_xpath('//*[@id="session_password"]')
        sleep(1)
        pasd.send_keys('Webtunix@123')
        sleep(1)
        self.driver.find_element_by_xpath('//*[@type="submit"]').click()
        sleep(1.30)
        exit()

        #finding csv user for twitter image
        df = pd.read_csv('/home/webtunix/Documents/ss/pythonSelenium/coyotes_handles.csv', header=0,encoding='ISO-8859–1')        # for username in df['handle']:
        # x = df.iloc[309:400,3]
        x = df.iloc[2861:2900, 2]
        count=0
        for username in x:
            try:
                pro_url = "https://twitter.com/" + username+'/photo'
                self.driver.get(pro_url)
                sleep(1.05)
                pic_link = self.driver.find_element_by_xpath("//img[@class='css-9pa8cd']")
                pic = pic_link.get_attribute('src')
                print(pic)
                count+=1
                print(count)
                sleep(2)

                #reading csv for name and location corresponding to username
                df = pd.read_csv(r'/home/webtunix/Documents/ss/pythonSelenium/coyotes_handles.csv',header= 0,encoding='ISO-8859–1')
                dset = df.loc[df['handle'] == username, 'name'].iloc[0]
                dset_loc = df.loc[df['handle'] == username, 'location'].iloc[0]
                loc = dset_loc.split(", ")
                location = loc[0]

                #entering name and location in search icon of linkdin

                self.driver.get('https://www.linkedin.com/feed/')
                sleep(1)
                self.driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(dset, ' ', location)
                sleep(1)
                self.driver.find_element_by_css_selector('.search-global-typeahead__input').send_keys(Keys.ENTER)
                sleep(1)

                #append multiple user with same name in a list for face matching
                try:
                    searcha=self.driver.find_elements_by_xpath('//div[@class="search-result__info pt3 pb4 ph0"]//a')
                    search=[]

                    for i in searcha:
                        linkdin_link = i.get_attribute('href')
                        search.append(linkdin_link)
                        sleep(1)
                    for i in search:
                        try:
                            link = str(i)
                            self.driver.get(link)
                            sleep(1)

                            self.driver.get(link +'photo')
                            img=self.driver.find_element_by_xpath('//div[@class="presence-entity pv-top-card__image presence-entity--size-9 ember-view"]//img')
                            sleep(2)
                            img_link = img.get_attribute('src')
                            print(img_link)

                            #compare each image url of linkdin with image url of twitter
                            api_key = 'xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
                            api_secret = 'TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'

                            try:
                                app= FacePP(api_key=api_key, api_secret=api_secret)
                                funcs= [
                                    face_detection,
                                    face_comparing,
                                    faceset_initialize,
                                    face_search,
                                    face_landmarks,
                                    dense_facial_landmarks,
                                    face_attributes,
                                    beauty_score_and_emotion_recognition
                                ]
                            except exceptions.BaseFacePPError as e:
                                print('Error:', e)

                            cmp_ = app.compare.get(image_url1=pic,image_url2=img_link)

                        # Comparing Photos
                           # df.to_csv(r'/home/webtunix/Documents/ss/pythonSelenium/coyotes_handles.csv',index=False)
                            if cmp_.confidence > 70:
                                print('Both photographs are of same person......')
                                df.loc[df.name==dset,['new_column']]=linkdin_link

                            else:
                                print('Both photographs are of two different persons......')
                                df.loc[df.name == dset, ['new_column']] ="no match"

                            df.to_csv(r"/home/webtunix/Documents/ss/pythonSelenium/coyotes_handles_2820_2900.csv", index=False,mode='a')
                        except:
                            pass

                except:
                    print("linkdin account doesn't exist")
                    pass

            except:
                print("twitter account doesn't exist")
                pass



def main():
    LoginTest()


if __name__ == "__main__":
    main()


