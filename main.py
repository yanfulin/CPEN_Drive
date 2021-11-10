import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import time
from pathlib import Path

base_url = "https://cpentalk.com/drive/index.php"
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.133 Safari/537.39'
DYN_UA_FORMAT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.{:04d}.{:03d} Safari/537.39'


def random_ua(id):
    return DYN_UA_FORMAT.format(random.randrange(9999), id + 1)

class Book():
    def __init__(self):
        self.category=""
        self.bookname=""
        #self.title=""
        #self.publisher=''
        #self.publish_date=''
        #self.ISDN=0
        #self.ctfile_sn=""
        #self.ctfile_url=''
        self.download_url=''
        self.file_size = 0
    def get_category_url(self):
        category_list = []
        payload = {
            'origin': base_url,
            'referer': base_url,
            #'id': f'{self.id}.html'
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }
        #url=f"https://yabook.org/post/{self.id}.html"
        #https: // cpentalk.com / drive / index.php?p =
        #< a title = "Direct link" href = "?p=Artificial+Intelligence+Books" > < i class ="fa fa-link" aria-hidden="true" > < / i > < / a >
        resp = requests.post(base_url,data=payload, headers=headers)
        resp.encoding = resp.apparent_encoding
        resp.raise_for_status()
        #print(resp.text)
        soup = BeautifulSoup(resp.text, 'lxml')
        a_links = soup.find_all(title='Direct link')
        #print("href direct link is ", a_links)
        for item in a_links:

            category_list.append(base_url + item['href'] + "%2FBooks%28+CPENTalk.com+%29")
        return category_list


    def get_book_url(self, category_url):
        # <a title="Download" href="?p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&amp;view=+Artificial+Intelligence+and+Games+%28+CPENTalk.com+%29.pdf"><i class="fa fa-download"></i></a>
        # https://cpentalk.com/drive/index.php?p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&view=+Artificial+Intelligence+and+Games+%28+CPENTalk.com+%29.pdf
        #
        # https://cpentalk.com/drive/index.php?download=true&p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&dl=+Artificial+Intelligence+and+Games+%28+CPENTalk.com+%29.pdf
        #
        # <a title="Download" href="?p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&amp;view=+Artificial+Intelligence+and+Games+%28+CPENTalk.com+%29.pdf"><i class="fa fa-download"></i></a>
        #
        #https://cpentalk.com/drive/index.php?download=true&p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&dl=workshop+on+robotics+and+artificial+intelligence+%28+CPENTalk.com+%29.pdf
        #https://cpentalk.com/drive/index.php?p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&view=workshop+on+robotics+and+artificial+intelligence+%28+CPENTalk.com+%29.pdf
        #https://cpentalk.com/drive/index.php?download=true&p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&dl=workshop+on+robotics+and+artificial+intelligence+%28+CPENTalk.com+%29.pdf
        payload = {
            'origin': base_url,
            'referer': base_url,
            #'id': f'{self.id}.html'
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }

        resp = requests.post(category_url,data=payload, headers=headers)
        resp.encoding = resp.apparent_encoding
        resp.raise_for_status()
        #print(resp.text)
        soup = BeautifulSoup(resp.text, 'lxml')
        a_links = soup.find_all(title='Download')
        #print("href direct link is ", a_links)
        download_list=[]
        for item in a_links:
            #print(item['href'])
            item['href']=item['href'].replace("?p=","?download=true&p=").replace("&view=","&dl=")
            download_list.append(base_url + item['href'])
            #print(item['href'])
            #print(category_list)
        return download_list

        # def parse_params(file):
        #     """
        #     Get required params from webpage.
        #     """
        #     file_data = file
        #     filename = file_data['file_name']
        #     userid = file_data['userid']
        #     file_id = file_data['file_id']
        #     folder_id = file_data.get('file_dir')
        #     file_chk = file_data['file_chk']
        #     file_size = file_data['file_size']
        #     mb = 0  # not mobile
        #     app = 0
        #     code = 200
        #
        #     verifycode = ''
        #     rd = random.random()
        #
        #     return userid, filename, file_id, folder_id, file_chk, file_size, mb, app, verifycode, rd

        # userid, filename, file_id, folder_id, file_chk, file_size, mb, app, verifycode, rd = parse_params(file_link)
        # get_file_api = f"/get_file_url.php?uid={userid}&fid={file_id}&folder_id={folder_id}&file_chk={file_chk}&mb={mb}&app={app}&acheck=1&verifycode={verifycode}&rd={rd}"
        # baseurl = "https://webapi.ctfile.com" + get_file_api
        # print(baseurl)




# start = df["book_id"].max()
# fail_count=0
# print(start)
# for i in range(0, 200, 1):
#     for j in range(0, 5, 1):
#         k=i*5+j+1+start
#         if k in [46,59,64,120,2114,2121,2123,2352, 2363,2366,2365,2372, 2376,2379,2382,2454, 3007 ]: continue
#         book = Book(k)
#         print(book.id)

#         data = {"book_id":book.id,
#                 "bookname":book.bookname,
#                 "title":book.title,
#                 "publisher":book.publisher,
#                 "publish_date":book.publish_date,
#                 "ISDN":book.ISDN,
#                 "ctfile_sn":book.ctfile_sn,
#                 "ctfile_url":book.ctfile_url,
#                 "download_url":book.download_url,
#                 "file_size":book.file_size
#                 }
#
#         df.loc[len(df)]=data
#
#     if fail_count > 50:
#         #print("fail count more than 100. Stop the program")
#         break
#     print(df.tail())
#     df.to_csv("yabook.csv", index_label=False)
#     time.sleep(4)





def get_download_list(cateory):
    book.get_book_url(category)

def csv_db_update(dataframe, category, download_link):
    # df = pd.read_csv("\CPENTalk_Books\cpentalk.csv")
    # column = ["category","download_url", "file_size", "downloaded"]
    # df = pd.DataFrame(columns=column)
    df = dataframe
    if ((df['category'] == category) & (df['download_url'] == download_link)).any():
        pass
    else:
        df = pd.concat([pd.DataFrame([[category, download_link,0,0]], columns=df.columns), df], ignore_index=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    target_csv = Path("CPENTalk_Books/cpentalk.csv")
    columns = ["clean_cat", "category", "download_url", "file_name", "file_size", "downloaded"]
    df = pd.read_csv(target_csv, names=columns,header=0)

    #df = pd.DataFrame(columns=column)
    print(df.columns)
    print(df.head())

    book=Book()
    categories = book.get_category_url()
    for cat in categories:
        clean_cat = cat.split("=")[1].split("%2F")[0].replace("+", "_")
        urls = book.get_book_url(cat)
        for url in urls:
            if ((df['category'] == cat) & (df['download_url'] == url)).any():
                pass
            else:

                # https://cpentalk.com/drive/index.php?download=true&p=Artificial+Intelligence+Books%2FBooks%28+CPENTalk.com+%29&dl=workshop+on+robotics+and+artificial+intelligence+%28+CPENTalk.com+%29.pdf
                file_name=url.split("=")[-1].replace("+%28+CPENTalk.com+%29","").replace("+", "_")
                print(clean_cat)
                print(file_name)
                df = pd.concat([pd.DataFrame([[clean_cat, cat, url,file_name, 0, 0]], columns=df.columns), df],
                               ignore_index=True)
    df.to_csv(target_csv, index=False)
