from os import supports_bytes_environ
import bs4
import requests
import time
import csv


def scraping():
    url = "https://game8.jp/dq9/75149"
    response = requests.get(url=url)
    soup=bs4.BeautifulSoup(response.text,'html.parser')
    monster_dicts=get_links_array_from_soup(soup)
    monster_detail_dicts=[]
    # for monster_dict in monster_dicts:
        # monster_detail_dicts.append(get_monster_detail(monster_dict["link"],monster_dict["name"]))
    # for i in range(1,5):
    for i in range(1,len(monster_dicts)):
        monster_detail_dicts.append(get_monster_detail(monster_dicts[i]["link"],monster_dicts[i]["name"]))
        time.sleep(1)
    label = ["名前","頭文字","図鑑No","推奨レベル","HP","系統"]
    output_to_csv(monster_detail_dicts, "./monster_detail.csv", label)
        
def get_links_array_from_soup(soup):
    page_element=soup.find('div',class_="archive-style-wrapper")
    monster_tables=page_element.find_all('table',class_="a-table a-table a-table",recursive=False)
    link_array=[]
    for monster_table in monster_tables:
        tr_tags=monster_table.find_all('tr')
        for index,tr_tag in enumerate(tr_tags):
            tr_tag == tr_tags[index]
            td_tag=tr_tag.find('td')
            if td_tag is not None:
                a_tag=td_tag.find('a',class_="a-link")
                if a_tag is not None:
                    monster_info={}
                    link=a_tag.get('href')
                    monster_info["link"]=link
                    monster_name=a_tag.text
                    monster_info["name"]=monster_name
                    link_array.append(monster_info)
                    
    return link_array

def get_monster_detail(url:str,monster_name:str)->dict:
    print(url)
    return_dict = {"名前":monster_name}
    response = requests.get(url=url)
    soup=bs4.BeautifulSoup(response.text,'html.parser')
    if "ページは作成されていない場合があります" in soup.text:
        return
    if "前のボス" in soup.text:
        page_element=soup.find('div',class_="archive-style-wrapper")
        element_tables=page_element.find_all('table',class_="a-table a-table",recursive=False)[1]
        tr_tag=element_tables.find_all('tr')[1]
        info_tag=tr_tag.find_all('td',class_="center")
        needed_level = info_tag[0]
        return_dict["推奨レベル"] = needed_level.text
        hitpoints =info_tag[1]
        return_dict["HP"] = hitpoints.text
        monster_type=info_tag[2]
        return_dict["系統"] = monster_type.text.replace("\n","")
        
    else:
        page_element=soup.find('div',class_="archive-style-wrapper")
        info_tag_nomal=page_element.find('table',class_="a-table a-table a-table",recursive=False).find_all('tr')[1].find_all('td',class_="center")
        initial=info_tag_nomal[0]
        return_dict["頭文字"]=initial.text.replace("\n","").replace(" ","")
        nunber=info_tag_nomal[1]
        return_dict["図鑑No"]=nunber.text.replace("\n","").replace(" ","")
        monster_type=info_tag_nomal[2]
        return_dict["系統"]= monster_type.text.replace("\n","").replace(" ","")
    print(return_dict)
    return return_dict

def output_to_csv(monster_detail_dicts,file_path,label):
    with open(file_path, 'w',encoding='utf_8_sig') as f:
        writer= csv.DictWriter(f, label)
        writer.writeheader()
        for dict in monster_detail_dicts:
            if dict is not None:
                writer.writerow(dict)

if __name__ == '__main__':
    # get_monster_detail('https://game8.jp/dq9/88659',"test")
    scraping()