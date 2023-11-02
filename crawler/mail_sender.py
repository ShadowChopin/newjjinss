from email.mime.application import MIMEApplication
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime as dt
import common_info as ci
import common_lib as cl


def send_mail(in_subject, in_text, in_from, in_to):
    recipients = [in_to] # 문자열을 리스트로 변환
    message = MIMEMultipart("alternative")
    message["Subject"] = in_subject
    message["From"] = in_from
    message["To"] = in_to
    # write the HTML part
    html = """\
    <html>
    <body>
        <p><{text}</p>
    </body>
    </html>
    """.format(text=in_text)
    contents = MIMEText(html, "html")
    message.attach(contents)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('folioport19@gmail.com', 'utadxdhyfmvwfhrv')
        s.sendmail(in_from, recipients, message.as_string())
        s.quit()
        print("Successfully sent the mail.")
    except Exception as mail_sender_e:
        print("Failed to send the mail..", mail_sender_e)

def make_dic_factory(cursor):
    column_names = [d[0] for d in cursor.description]

    def create_row(*args):
        return dict(zip(column_names, args))

    return create_row

def get_news(conn, cursor, area, pub_date):
  sql = "select * from contents where subject = '{}' and pub_date like '{}'".format(area, pub_date)
  cursor.execute(sql)
  cursor.rowfactory = make_dic_factory(cursor)
  articles = cursor.fetchall()
  conn.commit()
  
  return articles

def get_news2(conn, cursor, area):
  sql = "select * from contents where subject = '{}'".format(area)
  cursor.execute(sql)
  
  return cursor

def get_member_data(conn, cursor, uid):
	if (uid is not None):
		sql = "select * from member where uid = '{}'".format(uid)
	else:
		sql = "select * from member"
	cursor.execute(sql)
	cursor.rowfactory = make_dic_factory(cursor)
	members = cursor.fetchall()
	conn.commit()
  
	return members


MAIL_HTML_P1 = '''
<!DOCTYPE html>
<html>
<head>
	<meta content="width=device-width" name="viewport">
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
	<title>뉴찐스</title>
</head>
<body style="-webkit-font-smoothing: antialiased;-webkit-text-size-adjust: none;height: 100%;background-color: #f0f5f7;width: 100%!important;">
	<!-- HEADER -->
	<table bgcolor="#FFFFFF" class="head-wrap" style="width: 100%;">
		<tr>
			<td></td>
			<td align="" class="header container" style="display: block!important;max-width: 600px!important;margin: 0 auto!important;clear: both!important;">
				<!-- /content -->
				<div class="content" style="padding: 15px;max-width: 600px;margin: 0 auto;display: block;">
					<table bgcolor="#FFFFFF" style="width: 100%;">
						<tr>
							<td>
								<a href="" style="color: #2BA6CB;text-decoration: none;"><img src="''' + '''http://placehold.it/200x50/'''
MAIL_HTML_P2 = '''" style="max-width: 100%;"></a>
							</td>
							<td align="right">
								<h4 style="font-family: 'Nanum Pen Script', cursive;font-weight: 500;font-size: 23px;">'''
MAIL_HTML_P3 = '''&nbsp;|&nbsp;<a class="sub" href="" style="color: #2BA6CB;text-decoration: none;font-family: 'Nanum Pen Script', cursive;">구독하기&nbsp;</a></h4>
							</td>
						</tr>
					</table>
				</div><!-- /content -->
			</td>
			<td></td>
		</tr>
	</table><!-- /HEADER -->
	<!-- BODY -->
	<table bgcolor="" class="body-wrap" style="width: 100%;">
		<tr>
			<td></td>
			<td align="" bgcolor="#FFFFFF" class="container" style="display: block!important;max-width: 600px!important;margin: 0 auto!important;clear: both!important;">
				<!-- content -->
				<div class="content" style="padding: 15px;max-width: 600px;margin: 0 auto;display: block;">
					<hr class="hr" style="width: 100%;background: linear-gradient(90deg, #75b9f5, #439bf3, #2473d4, #0e4bad, #0b3996, #032077, #020b46);border: none;height: 2px;">
					<br>
					<table style="width: 100%;">
						<tr>
							<td>
								<h1 style="font-family: 'Nanum Pen Script', cursive;font-weight: 200;font-size: 44px;">''' + '''오늘의 소식!'''
MAIL_HTML_P4 = '''</h1><br>
								<p class="lead" style="margin-bottom: 10px;font-weight: normal;font-size: 17px;line-height: 1.6;">''' + '''아침 저녁 날씨가 정말 쌀쌀해졌네요. 감기 조심하세요 여러분!!<br>
								오늘도 알찬 뉴찐스의 소식을 만나볼까요?!'''
MAIL_HTML_P5 = '''</p><!-- A Real Hero (and a real human being) -->
								<a class="press" href="" style="color: black;text-decoration: none;"></a>
								<p style="margin-bottom: 10px;font-weight: normal;font-size: 14px;line-height: 1.6;"><img src="''' + '''http://placehold.it/600x300'''
MAIL_HTML_P6 = '''" style="max-width: 100%;"></p><!-- /hero -->
								<p style="margin-bottom: 10px;font-weight: normal;font-size: 14px;line-height: 1.6;">''' + '''강서구청장 보궐선거에서 참패한 국민의힘, 수습책 마련에 고심이 깊어 보이는데요. 국민의힘이 수습책의 일환으로 선거관리위원회 해킹 관련 대응 TF를 구성한 것을 두고 우리의 김작자(김성회 정치연구소 와이 소장)는 “심각한 문제”라며 운을 떼고는 윤석열 대통령과 이준석 전 국민의힘 대표 사이에 있었던 일화를 소개했습니다. 또 우리의 장깨비(장성철 공론센터 소장)는 국민의힘의 후속 조치에 “아프면 치료를 해야 하는데 치료제가 아닌 진통제를 먹고 있다”라고 비판했는데요. 〈공덕포차〉에서 이야기해봅니다.'''
MAIL_HTML_P7 = '''</p>
							</td>
						</tr>
					</table>
				</div><!-- /content -->'''

MAIL_HTML_P8 = '''
			<!-- content -->
				<div class="content" style="padding: 15px; max-width: 600px; margin: 0 auto; display: block;">
					<table bgcolor="" style="width: 100%;">
							<tr>
									<td class="small" style="vertical-align: middle; padding-right: 10px;" width="20%">
											<img src="'''  # + 썸네일
MAIL_HTML_P9 = '''" style="max-width: 100%; height: 75px;">
									</td>
									<td>
											<h4 style="font-family: 'Nanum Pen Script', cursive; font-weight: 500; font-size: 18px; line-height: 0.5;">''' # + 언론사
MAIL_HTML_P10 = '''</h4>
											<a href = "''' # + 기사 링크
MAIL_HTML_P11 = '''"><p class="" style="margin-bottom: 10px; font-weight: normal; font-size: 14px; line-height: 1.6;">"''' # + 제목
MAIL_HTML_P12 = '''"</p></a>
									</td>
							</tr>
					</table>
				</div><!-- /content -->'''
MAIL_HTML_P13 = '''				
				<!-- content -->
				<div class="content" style="padding: 15px;max-width: 600px;margin: 0 auto;display: block;">
					<table bgcolor="" style="width: 100%;">
						<tr>
							<td>
								<p class="callout" style="margin-bottom: 15px;font-weight: normal;font-size: 14px;line-height: 1.6;padding: 15px;background-color: #ECF8FF;">''' # + 섹션이름
MAIL_HTML_P14 = ''' 
            &nbsp;&nbsp; <a href="#" style="color: #2BA6CB;text-decoration: none;font-weight: bold;">Subcribe! &raquo;</a></p>
							</td>
						</tr>
					</table>
				</div><!-- /content --> 
''' # MAIL_HTML_P13과 pair
MAIL_HTML_P15 = '''
				<!-- content -->
				<div class="content" style="padding: 15px;max-width: 600px;margin: 0 auto;display: block;">
					<hr class="hr" style="width: 100%;background: linear-gradient(90deg, #75b9f5, #439bf3, #2473d4, #0e4bad, #0b3996, #032077, #020b46);border: none;height: 2px;">
					<br>
					<br>
					<table bgcolor="" style="width: 100%;">
						<tr>
							<td>
								<!-- opinion & contact -->
								<table bgcolor="" class="social" style="background-color: #d7ecf3;width: 100%;" width="100%">
									<tr>
										<td style="display: flex;">
                      <!--- column 1 -->
                      <div class="column" style="width: 280px; min-width: 279px;">
                          <table align="left" bgcolor="" cellpadding="" style="width: 100%;">
                              <tr>
                                  <td style="padding: 15px;">
                                      <h5 class="" style="font-family: 'Nanum Pen Script', cursive; font-weight: 900; font-size: 17px;">오늘의 뉴찐스는 어땠나요?</h5><br>
                                      <p class="" style="margin-bottom: 10px; font-weight: normal; font-size: 14px; line-height: 1.6;">
                                          <a class="soc-btn good" href="#" style="color: #FFF; text-decoration: none; padding: 3px 7px; font-size: 12px; margin-bottom: 10px; font-weight: bold; display: block; text-align: center; background-color: #6a90e2!important;">좋다</a>
                                          <a class="soc-btn bad" href="#" style="color: #FFF; text-decoration: none; padding: 3px 7px; font-size: 12px; margin-bottom: 10px; font-weight: bold; display: block; text-align: center; background-color: #88c1db!important;">별로다</a>
                                      </p>
                                  </td>
                              </tr>
                          </table><!-- /column 1 -->
                      </div><!--- column 2 -->
                      <div class="column" style="width: 280px; min-width: 279px;">
                          <table align="left" bgcolor="" cellpadding="" style="width: 100%;">
                              <tr>
                                  <td style="padding: 15px;">
                                      <h5 class="" style="font-family: 'Nanum Pen Script', cursive; font-weight: 900; font-size: 17px;">Contact Info</h5><br>
                                      <p style="margin-bottom: 10px; font-weight: normal; font-size: 14px; line-height: 1.6;">Phone: <strong>010-1234-5678</strong><br>
                                      Email: <strong><a href="" style="color: #2BA6CB; text-decoration: none;">new@zzins.com</a></strong></p>
                                  </td>
                              </tr>
                          </table><!-- /column 2 -->
                      </div>
                  </td>
                  
									</tr>
								</table><!-- /opinion & contact -->
							</td>
						</tr>
					</table>
				</div><!-- /content -->
			</td>
			<td></td>
		</tr>
	</table><!-- /BODY -->
	<!-- FOOTER -->
	<table class="footer-wrap" style="width: 100%;clear: both!important;">
		<tr>
			<td></td>
			<td class="container" style="display: block!important;max-width: 600px!important;margin: 0 auto!important;clear: both!important;">
				<!-- content -->
				<div class="content" style="padding: 15px;max-width: 600px;margin: 0 auto;display: block;">
					<table style="width: 100%;">
						<tr>
							<td align="center">
								<p style="margin-bottom: 10px;font-weight: normal;font-size: 14px;line-height: 1.6;"><a href="#" style="color: #2BA6CB;text-decoration: none;">정책</a> | <a href="#" style="color: #2BA6CB;text-decoration: none;">이메일 주소 바꾸기</a> | <a href="#" style="color: #2BA6CB;text-decoration: none;">구독 해제</a></p>
							</td>
						</tr>
					</table>
				</div><!-- /content -->
			</td>
			<td></td>
		</tr>
	</table><!-- /FOOTER -->
</body>
</html>
'''

def do_mailing():
	conn, cursor = cl.set_db(ci.DB_SYS_INFO, ci.DB_USER_INFO)
	
	members = get_member_data(conn, cursor, None)
	#print(members)
	#print(members[0]['PREF_SUBJ'])
	#print(len(members))
	#for m in members:
	#  print(m)
	
	##print(articles)
	#print(articles[0]['CID'])
			
	date = dt.datetime.now().date().strftime('%Y. %m. %d.')
	date_str = str(date) + "%"
	#print(date_str)
	
	sports_articles = get_news(conn, cursor, 'sports', date_str)
	politics_articles = get_news(conn, cursor, 'politics', date_str)
	economic_articles = get_news(conn, cursor, 'economic', date_str)
	entertainment_articles = get_news(conn, cursor, 'entertainment', date_str)
	society_articles = get_news(conn, cursor, 'society', date_str)
	culture_articles = get_news(conn, cursor, 'culture', date_str)
	digital_articles = get_news(conn, cursor, 'digital', date_str)
	foreign_articles = get_news(conn, cursor, 'foreign', date_str)
	
	articles = [sports_articles, politics_articles, economic_articles, society_articles, culture_articles, entertainment_articles, \
	            digital_articles, foreign_articles]
	#print(articles)
	#print(articles[0][0]['TITLE'])
	
	for i in range(0, len(members)):
		if(members[i]['SUBSCRIPTION'] == 0):
			continue
		
		text = MAIL_HTML_P1 + MAIL_HTML_P2 + dt.datetime.now().date().strftime('%Y.%m.%d %a') + MAIL_HTML_P3 + MAIL_HTML_P4 + MAIL_HTML_P5 + MAIL_HTML_P6 + MAIL_HTML_P7
		p_subj = members[i]['PREF_SUBJ']
		if(p_subj & 128): # sports
			text += MAIL_HTML_P13
			text += '스포츠'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 스포츠 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[0][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[0][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[0][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[0][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 64): # politics
			text += MAIL_HTML_P13
			text += '정치'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 정치 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[1][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[1][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[1][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[1][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 32): # economic
			text += MAIL_HTML_P13
			text += '경제'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 경제 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[2][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[2][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[2][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[2][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 16): # society
			text += MAIL_HTML_P13
			text += '사회'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 사회 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[3][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[3][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[3][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[3][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 8): # culture
			text += MAIL_HTML_P13
			text += '문화'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 문화 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[4][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[4][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[4][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[4][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 4): # entertainment
			text += MAIL_HTML_P13
			text += '연예'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 연예 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[5][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[5][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[5][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[5][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 2): # digital
			text += MAIL_HTML_P13
			text += '과학/IT'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 과학/IT 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[6][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[6][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[6][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[6][j]['TITLE']
				text += MAIL_HTML_P12
		if(p_subj & 1):	# international
			text += MAIL_HTML_P13
			text += '국제'
			text += MAIL_HTML_P14
			for j in range(0, 3): # 국제 섹션 3개의 뉴스
				text += MAIL_HTML_P8
				text += articles[7][j]['THUMBNAIL']
				text += MAIL_HTML_P9
				text += articles[7][j]['PRESS']
				text += MAIL_HTML_P10
				text += articles[7][j]['LINK']
				text += MAIL_HTML_P11
				text += articles[7][j]['TITLE']
				text += MAIL_HTML_P12
	
		text += MAIL_HTML_P15
		print(text)
		send_mail('test email 입니다.', text, 'folioport19@gmail.com', members[i]['EMAIL'])
		#send_mail('test email 입니다.', text, 'folioport19@gmail.com', 'any1me@naver.com')
	
	cl.unset_db(conn, cursor)
