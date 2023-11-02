import schedule
import time
import entertain_crawler as ec
import news_crawler as nc
import sports_crawler as sc
import mail_sender as ms

def do_crawling():
  nc.collect_general_news()
  sc.collect_sports_news()
  ec.collect_entertain_news()
  

def main():
  #schedule.every(20).minutes.do(do_crawling)

  '''
  schedule.every().day.at("09:40").do(do_crawling)
  schedule.every().day.at("10:35").do(ms.do_mailing)
  
  schedule.every().day.at("16:00").do(do_crawling)
  schedule.every().day.at("17:00").do(ms.do_mailing)
  '''
  
  #do_crawling()


  while True:
    schedule.run_pending()
    time.sleep(3)

if __name__ == "__main__":
  main()

  
  

