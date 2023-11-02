from bs4 import BeautifulSoup
import requests
import urllib.request
import numpy as np
import common_info as ci
import common_lib as cl

def collect_general_news():
  class_news = np.array([ci.NEWS_CLASS.SOCIETY, ci.NEWS_CLASS.POLITICS, ci.NEWS_CLASS.ECONOMIC, ci.NEWS_CLASS.INTERNATIONAL, ci.NEWS_CLASS.CULTURE, ci.NEWS_CLASS.SCIENCE])
  #title_news = np.array(['society', 'politics', 'economic', 'interational', 'culture', 'science'])

  print("{} started collecting news articles".format(ci.LOG_PREFIX))

  class_idx = 0
  np_id = ([])
  np_title = ([])
  np_date = ([])
  np_link = ([])
  np_press = ([])
  np_thumbnail = ([])
  np_srclink = ([])
  np_subject = ([])
  np_summary = ([])
  np_subcategory = ([])

  for class_ in class_news:
    soup = cl.get_html(ci.BASE_URL + class_)
    print(ci.BASE_URL + class_)

    # main news list crawling
    main_list = soup.find_all('div', attrs = {'class':'item_column'})
    idx = 0
    for li in main_list:
    #  img_tag = li.find('img')
      a_tag = li.find('a', attrs = {'class':'link_txt'})
      span_tag = li.find('span', attrs = {'class':'txt_info'})
      m_link = a_tag['href']
      m_title = a_tag.string
      m_press = span_tag.string


      soup_in = cl.get_html(m_link) # 기사 작성일을 가져오기 위해 기사 본문 액세스
      m_date = soup_in.find('span', attrs = {'class':'num_date'}).string
      id = cl.generate_id(class_, m_date, str(idx))
      img_tag = soup_in.find('img')


      p_tag = soup_in.find_all('p', attrs = {'class':'link_figure'})
      if p_tag: # meaning is 'if p_tag is not empty'
        img_tag = p_tag[0].img  # img_tag is string
        if img_tag is not None: # meaning is 'if img_tag is not null'
          thumb_url = img_tag['src']
          # thumbnail extraction
          #urllib.request.urlretrieve(img_tag['src'], "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
          #urllib.request.urlretrieve(img_tag['src'], "crawler/img/thumb{}{}.jpg".format(class_, idx))
          rt = urllib.request.urlretrieve(thumb_url, "C:/JavaDev/loginSys2/src/main/webapp/resources/thumbnails/thumb{}.jpg".format(id))
          print(thumb_url)
          # from PIL import Image
          # img = Image.open(rt[0])
          # print(img.size)
          # img = img.resize((450, 163))
          np_thumbnail = np.append(np_thumbnail, "resources/thumbnails/thumb{}.jpg".format(id))
        else:
          #np_thumbnail = np.append(np_thumbnail, None)
          np_thumbnail = np.append(np_thumbnail, "image/noimg.png")
      else:
        #np_thumbnail = np.append(np_thumbnail, None)
        np_thumbnail = np.append(np_thumbnail, "image/noimg.png")


      # if img_tag is not None: # meaning is 'if img_tag is null'
      #   # thumbnail extraction
      #   #urllib.request.urlretrieve(img_tag['src'], "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
      #   #urllib.request.urlretrieve(img_tag['src'], "crawler/img/thumb{}{}.jpg".format(class_, idx))
      #   urllib.request.urlretrieve(img_tag['src'], "C:/JavaDev/loginSys2/src/main/webapp/resources/thumbnails/thumb{}.jpg".format(id))

      
      new_html = cl.generate_html(soup_in)
      #with open("Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      #with open("crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      with open("C:/JavaDev/loginSys2/src/main/webapp/resources/contents/{}.jsp".format(id), 'w', encoding = 'utf-8-sig') as f:
        f.write(new_html)

      np_id = np.append(np_id, id)
      np_title = np.append(np_title, m_title)
      np_date = np.append(np_date, m_date)
      #np_link = np.append(np_link, "Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id))
      #np_link = np.append(np_link, "crawler/html/{}.html".format(id))
      np_link = np.append(np_link, "resources/contents/{}.jsp".format(id))
      np_srclink = np.append(np_srclink, m_link)
      np_press = np.append(np_press, m_press)
      #np_thumbnail = np.append(np_thumbnail, "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
      #np_thumbnail = np.append(np_thumbnail, "crawler/img/thumb{}{}.jpg".format(class_, idx))
      np_subject = np.append(np_subject, class_)
      np_subcategory = np.append(np_subcategory, "") 

      # from bs4 import BeautifulSoup
      # new_html = BeautifulSoup(new_html, 'html.parser')
      # p_list = new_html.find_all('p', attrs = {'dmcf-ptype':'general'})
      # summary_txt = p_list[0].string
      # np_summary = np.append(np_summary, summary_txt)


      from bs4 import BeautifulSoup
      new_html = BeautifulSoup(new_html, 'html.parser')
      p_list = new_html.find_all('p', attrs = {'dmcf-ptype':'general'})
      summary_txt = ""
      #for i in range(0, len(p_list)):
      if(len(p_list) >= 2):
        for i in range(0, 2):
          if p_list[i].string is not None:
            summary_txt += p_list[i].string

      np_summary = np.append(np_summary, summary_txt)

      idx = idx + 1
      print("[{}:{}] {}".format(class_idx, idx, m_title))

    # sub news list crawling
    sub_news= soup.find('ul', attrs = {'class':'list_newsmajor'})
    sub_news_list = sub_news.find_all('li')
    for li in sub_news_list:
      a_tag = li.find('a')
      span_tag = li.find('span')
      s_title = a_tag.string
      s_link = a_tag['href']
      s_press = span_tag.string
      # thumbnail extraction
  #    resp = requests.get(s_link)
  #    news_detail = BeautifulSoup(resp.text, 'html.parser')
      news_detail = cl.get_html(s_link)

      # 기사 작성일을 가져오기 위해 기사 본문 액세스
      s_date = news_detail.find('span', attrs = {'class':'num_date'}).string
      id = cl.generate_id(class_, s_date, str(idx))

      p_tag = news_detail.find_all('p', attrs = {'class':'link_figure'})
      if p_tag: # meaning is 'if p_tag is not empty'
        img_tag = p_tag[0].img  # img_tag is string
        if img_tag is not None: # meaning is 'if img_tag is null'
          thumb_url = img_tag['src']
          # thumbnail extraction
          #urllib.request.urlretrieve(img_tag['src'], "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
          #urllib.request.urlretrieve(img_tag['src'], "crawler/img/thumb{}{}.jpg".format(class_, idx))
          rt = urllib.request.urlretrieve(thumb_url, "C:/JavaDev/loginSys2/src/main/webapp/resources/thumbnails/thumb{}.jpg".format(id))
          print(thumb_url)
          # from PIL import Image
          # img = Image.open(rt[0])
          # print(img.size)
          # img = img.resize((450, 163))
          np_thumbnail = np.append(np_thumbnail, "resources/thumbnails/thumb{}.jpg".format(id))
        else:
          #np_thumbnail = np.append(np_thumbnail, None)
          np_thumbnail = np.append(np_thumbnail, "image/noimg.png")
      else:
        #np_thumbnail = np.append(np_thumbnail, None)
        np_thumbnail = np.append(np_thumbnail, "image/noimg.png")

      new_html = cl.generate_html(news_detail)
      #with open("Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      #with open("crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      with open("C:/JavaDev/loginSys2/src/main/webapp/resources/contents/{}.jsp".format(id), 'w', encoding = 'utf-8-sig') as f:
        f.write(new_html)

      np_id = np.append(np_id, id)
      np_title = np.append(np_title, s_title)
      np_date = np.append(np_date, s_date)
      #np_link = np.append(np_link, "Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id))
      #np_link = np.append(np_link, "crawler/html/{}.html".format(id))
      np_link = np.append(np_link, "resources/contents/{}.jsp".format(id))
      np_press = np.append(np_press, s_press)
      np_srclink = np.append(np_srclink, s_link)
      #np_thumbnail = np.append(np_thumbnail, "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
      #np_thumbnail = np.append(np_thumbnail, "crawler/img/thumb{}{}.jpg".format(class_, idx))
      np_subject = np.append(np_subject, class_)
      np_subcategory = np.append(np_subcategory, "") 



      from bs4 import BeautifulSoup
      new_html = BeautifulSoup(new_html, 'html.parser')
      p_list = new_html.find_all('p', attrs = {'dmcf-ptype':'general'})
      summary_txt = ""
      for i in range(0, len(p_list)):
        summary_txt += p_list[i].get_text()
        #summary_txt = summary_txt[0:1000]

      if(summary_txt == ""):
        for i in range(0, len(p_list)):
          new_html2 = BeautifulSoup(str(p_list[i]), 'html.parser')
          summary_txt += new_html2.get_text()
        #summary_txt = summary_txt[0:1000]

      if(summary_txt == ""):
        div_list = new_html.find_all('div', attrs = {'dmcf-ptype':'general'})
        #if(len(div_list) >= 1):
        for i in range(0, len(div_list)):
          summary_txt += div_list[i].get_text()
        #summary_txt = summary_txt[0:1000]

      np_summary = np.append(np_summary, summary_txt[0:1000])



      idx = idx + 1
      print("[{}:{}] {}".format(class_idx, idx, s_title))

    class_idx += 1

  df_news_list = cl.make_df_news(np_id,  np_link, np_title, np_thumbnail, np_date, np_press, np_srclink, np_subject, np_summary, np_subcategory)

  print("{} completed collecting articles in entertainment".format(ci.LOG_PREFIX))

  conn, cursor = cl.set_db(ci.DB_SYS_INFO, ci.DB_USER_INFO)
  sql = "insert into Contents(cid, link, title, thumbnail, pub_date, press, source, subject, summary, subcategory) values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"

  cl.execute_query(conn, cursor, sql, df_news_list.values.tolist())

  cl.unset_db(conn, cursor)
