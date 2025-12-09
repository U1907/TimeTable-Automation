import datetime
import subprocess
from page import generate_daily_html
from parser import CourseParser

CMD1=r'curl --cookie-jar - -s -o /dev/null -L "http://gstudent.gitam.edu/Login/?id=1KfzbrzcraVzS3aqK3oGsw=="'
CMD1_OUT=subprocess.check_output(CMD1, shell=True).decode()
ASPNET_ID=CMD1_OUT.strip().split()[-1]

CMD2=f'curl -s --cookie "ASP.NET_SessionId={ASPNET_ID}" https://gstudent.gitam.edu/Home/Gettimetable'
TT_PAGE=subprocess.check_output(CMD2, shell=True).decode()
    
today = datetime.datetime.now().strftime("%A")

parser = CourseParser()
parser.feed(TT_PAGE)

todays_courses = [c for c in parser.courses if c["day"] == today]

todays_timetable = generate_daily_html(today, todays_courses)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(todays_timetable)
