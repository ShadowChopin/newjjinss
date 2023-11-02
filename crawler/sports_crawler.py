import urllib.request
import numpy as np
import common_info as ci
import common_lib as cl

def collect_sports_news():
  print("{} started collecting articles in sports".format(ci.LOG_PREFIX))

  soup = cl.get_html(ci.SPORTS_URL)

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

  num_of_news = 0
  for class_ in ci.CLASS_SPORTS:
    news_each = soup.find('div', attrs = {'data-category':class_})
  #  print("{} collecting articles in {} area".format(ci.LOG_PREFIX, class_))

    li_list = news_each.find_all('li')

    idx = 0
    for li in li_list:
      a_tag = li.find('a')
      title = li.string
      link = a_tag['href']
      press = a_tag['data-tiara-provider']

      news_detail = cl.get_html(link) # 사진을 가져와서 썸네일로 만들기 위해서 기사 본문을 액세스
      p_tag = news_detail.find_all('p', attrs = {'class':'link_figure'})

      date = news_detail.find('span', attrs = {'class':'num_date'}).string # 기사 작성일 추출

      id = cl.generate_id(ci.NEWS_CLASS.SPORTS, date, str(num_of_news))


      p_tag = news_detail.find_all('p', attrs = {'class':'link_figure'})
      if p_tag: # meaning is 'if p_tag is not empty'
        img_tag = p_tag[0].img  # img_tag is string
        if img_tag is not None: # meaning is 'if img_tag is null'
          thumb_url = img_tag['src']
          # thumbnail extraction
          #urllib.request.urlretrieve(img_tag['src'], "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
          #urllib.request.urlretrieve(img_tag['src'], "crawler/img/thumb{}{}.jpg".format(class_, idx))
          urllib.request.urlretrieve(thumb_url, "C:/JavaDev/loginSys2/src/main/webapp/resources/thumbnails/thumb{}.jpg".format(id))
          np_thumbnail = np.append(np_thumbnail, "resources/thumbnails/thumb{}.jpg".format(id))
        else:
          #np_thumbnail = np.append(np_thumbnail, None)
          np_thumbnail = np.append(np_thumbnail, "image/noimg.png")
      else:
        #np_thumbnail = np.append(np_thumbnail, None)
        np_thumbnail = np.append(np_thumbnail, "image/noimg.png")


      # img_tag = p_tag[0].img
      # thumb_url = img_tag['src']
      # #urllib.request.urlretrieve(thumb_url, "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
      # #urllib.request.urlretrieve(thumb_url, "crawler/img/thumb{}{}.jpg".format(class_, idx))
      # urllib.request.urlretrieve(thumb_url, "C:/JavaDev/loginSys2/src/main/webapp/resources/thumbnails/thumb{}.jpg".format(id))

      new_html = cl.generate_html(news_detail)
      #with open("Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      #with open("crawler/html/{}.html".format(id), 'w', encoding = 'utf-8-sig') as f:
      with open("C:/JavaDev/loginSys2/src/main/webapp/resources/contents/{}.jsp".format(id), 'w', encoding = 'utf-8-sig') as f:
        f.write(new_html)

      np_id = np.append(np_id, id)
      np_title = np.append(np_title, title)
      np_date = np.append(np_date, date)
      #np_link = np.append(np_link, "Bigdata_analysis_textbook/portfolio/crawler/html/{}.html".format(id))
      #np_link = np.append(np_link, "crawler/html/{}.html".format(id))
      np_link = np.append(np_link, "resources/contents/{}.jsp".format(id))
      np_srclink = np.append(np_srclink, link)
      np_press = np.append(np_press, press)
      #np_thumbnail = np.append(np_thumbnail, "Bigdata_analysis_textbook/portfolio/crawler/img/thumb{}{}.jpg".format(class_, idx))
      #np_thumbnail = np.append(np_thumbnail, "crawler/img/thumb{}{}.jpg".format(class_, idx))
      #np_thumbnail = np.append(np_thumbnail, "resources/thumbnails/thumb{}.jpg".format(id))
      np_subject = np.append(np_subject, ci.NEWS_CLASS.SPORTS)
      np_subcategory = np.append(np_subcategory, class_)



      from bs4 import BeautifulSoup
      new_html = BeautifulSoup(new_html, 'html.parser')
      p_list = new_html.find_all('p', attrs = {'dmcf-ptype':'general'})
      summary_txt = ""
      for i in range(0, len(p_list)):
        summary_txt += p_list[i].get_text()
        summary_txt = summary_txt[0:1000]

      if(summary_txt == ""):
        if(len(p_list) > 0):
          new_html2 = BeautifulSoup(str(p_list[0]), 'html.parser')
          summary_txt += new_html2.get_text()[0:1000]

      if(summary_txt == ""):
        div_list = new_html.find_all('div', attrs = {'dmcf-ptype':'general'})
        if(len(div_list) >= 1):
          summary_txt += div_list[0].get_text()[0:1000]

      np_summary = np.append(np_summary, summary_txt)



      idx += 1
      num_of_news += 1
      print("[{}] {}".format(num_of_news, title))

  df_news_list = cl.make_df_news(np_id,  np_link, np_title, np_thumbnail, np_date, np_press, np_srclink, np_subject, np_summary, np_subcategory)

  print("{} completed colletion articles in sports".format(ci.LOG_PREFIX))

  conn, cursor = cl.set_db(ci.DB_SYS_INFO, ci.DB_USER_INFO)
  sql = "insert into Contents(cid, link, title, thumbnail, pub_date, press, source, subject, summary, subcategory) values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"

  cl.execute_query(conn, cursor, sql, df_news_list.values.tolist())

  cl.unset_db(conn, cursor)



