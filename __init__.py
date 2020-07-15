import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_MainWindow import Ui_Dialog
import requests
import json
import datetime #系统时间
import threading
import time #引入定时器
from PyQt5.QtCore import QTimer #引入定时器
 
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.Clock_timer()  #初始化闹钟定时器
        self.QueryWeather() #请求一次天气信息
        self.Weather_timer() #初始化天气查询定时器
    
#触发时间与天气信息更新的两个定时器
    def Clock_timer(self):
        self.timer1=QTimer()
        self.timer1.setInterval(1000) #设置定时器 1S触发一次
        self.timer1.start() #启动定时器
        self.timer1.timeout.connect(self.RefreshTimeLabels) #当定时器走完一个周期，执行一次RefreshTimeLabels

    def Weather_timer(self):
        self.timer2=QTimer()
        self.timer2.setInterval(10800000) #设置定时器 3 小时触发一次
        self.timer2.start() #启动定时器
        self.timer2.timeout.connect(self.QueryWeather) #当定时器走完一个周期，执行一次天气查询
  
#请求时间信息  
    def RefreshTimeLabels(self):
        now = datetime.datetime.now() #获取系统时间
        self.ui.TimeLabel.setText("<font color=%s>%s</font>" %('#ffffff', now.strftime("%H:%M")))#TimeLabel用于放置时间
        self.ui.DateLabel.setText("<font color=%s>%s</font>" %('#ffffff', now.strftime("%Y-%m-%d %A")))#TimeLabel用于放置时间
        self.ui.SecondLabel.setText("<font color=%s>%s</font>" %('#ffffff', now.strftime("%S")))#TimeLabel用于放置秒
  
  #请求天气信息
    def QueryWeather(self):
        print('* queryWeather  ')
        #通过 API 请求城市天气信息
        rep = requests.get('https://api.heweather.net/s6/weather/now?location=auto_ip&lang=zh&key=××××××××××××××××××××××××××××××××××××××××')
        # 注意：这里使用了“和风天气”的付费API接口，用于获取全球范围的所在地天气详情信息。
        #可以在和风天气开发者中心里新建key，然后把key的值填入到上面一行代码的“&key=”的后面。
        # 调用基本天气接口：1元/1000次；调用天气预报接口：1元/1000次。
        # 本版本每天只调用8次接口，几块钱就能够满足一年的需求。
        statuscode = rep.status_code
        if statuscode==500:
            self.ui.WN_Temp.setText("<font color=%s>%s</font>" %('#ffffff', 'ERR')) 
            time.sleep(10)
            rep = requests.get('https://api.heweather.net/s6/weather/now?location=auto_ip&lang=zh&key=××××××××××××××××××××××××××××××××××××××××')
            statuscode2 = rep.status_code
            if  statuscode2==500:
                self.ui.WN_Temp.setText("<font color=%s>%s</font>" %('#ffffff', 'X')) 
        
        rep.encoding = 'utf-8'   #网页编码信息
        WeatherData1 = json.dumps(rep.json()) #打印json网页信息
        PyData = json.loads(WeatherData1)
        
        # 读取实时天气的JSON文本
        Now_Location = '%s' % PyData['HeWeather6'][0]['basic']['location']  #location
        Now_Status = '%s' % PyData['HeWeather6'][0]['now']['cond_txt'] + '\n' 
        Now_Wind = '%s' % PyData['HeWeather6'][0]['now']['wind_dir'] + ' %s 级' % PyData['HeWeather6'][0]['now']['wind_sc']#weather
        Now_Temp = '%s' % PyData['HeWeather6'][0]['now']['tmp'] + ''   #temp
        #写入Home页面中
        self.ui.WN_Location.setText("<font color=%s>%s</font>" %('#ffffff', Now_Location))#将请求的位置信息放入Now_Location文本框
        self.ui.WN_Status.setText("<font color=%s>%s<br>%s</br></font>" %('#ffffff', Now_Status, Now_Wind))
        self.ui.WN_Temp.setText("<font color=%s>%s</font><font color=#ffffff><font size=2px>℃</font></font>" %('#ffffff', Now_Temp))
        
        
        print('* ForecastWeather  ')
        #通过 API 请求城市天气信息
        rep2 = requests.get('https://api.heweather.net/s6/weather/forecast?location=auto_ip&lang=zh&key=××××××××××××××××××××××××××××××××××××××××')
        # 注意：这里使用了“和风天气”的付费API接口，用于获取全球范围的所在地天气详情信息。
        #可以在和风天气开发者中心里新建key，然后把key的值填入到上面一行代码的“&key=”的后面。
        # 调用基本天气接口：1元/1000次；调用天气预报接口：1元/1000次。
        # 本版本每天只调用8次接口，几块钱就能够满足一年的需求。
        rep.encoding = 'utf-8'   #网页编码信息
        WeatherData2 = json.dumps(rep2.json()) #打印json网页信息
        PyData2 = json.loads(WeatherData2)
        
        # 如果白天和夜间天气情况不同，则显示“X 转Y”，否则只显示白天天气
        for day in range (0, 3):
            if PyData2['HeWeather6'][0]['daily_forecast'][day]['cond_txt_d'] == PyData2['HeWeather6'][0]['daily_forecast'][day]['cond_txt_n']:
                castNight = ''
            else:
                castNight= '转'+ PyData2['HeWeather6'][0]['daily_forecast'][day]['cond_txt_n']
        
        # 读取天气预报的JSON文本
        Update_Date = '%s' % PyData['HeWeather6'][0]['update']['loc']  #天气信息更新时间
        Today_Status = '%s' % PyData2['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d'] + castNight #今天整天的天气情况
        Today_Temp = '%s' % PyData2['HeWeather6'][0]['daily_forecast'][0]['tmp_min'] + ' ~ %s℃' % PyData2['HeWeather6'][0]['daily_forecast'][0]['tmp_max']  #今天的温度范围
        Today_Hum = '%s%%' % PyData2['HeWeather6'][0]['daily_forecast'][0]['hum']  #今天空气湿度
        Today_RainProb ='%s%%' % PyData2['HeWeather6'][0]['daily_forecast'][0]['pop']  #今天降水概率
        Today_SunsetTime ='%s' % PyData2['HeWeather6'][0]['daily_forecast'][0]['ss']  #今天日落时间
        Tomorrow_Date = '%s' % PyData2['HeWeather6'][0]['daily_forecast'][1]['date'] #明天的天气预报日期
        Tomorrow_Temp = '%s' % PyData2['HeWeather6'][0]['daily_forecast'][1]['tmp_min'] + ' ~ %s℃' % PyData2['HeWeather6'][0]['daily_forecast'][1]['tmp_max']  #明天的温度范围
        Tomorrow_Status = '%s' % PyData2['HeWeather6'][0]['daily_forecast'][1]['cond_txt_d'] + castNight #明天整天的天气情况
        
       #写入今日天气信息到Weather页面中
        self.ui.WF_Location.setText("<font color=%s>%s</font><br>" %('#ffffff', Now_Location))
        self.ui.WF_Date.setText("<font color=%s>%s</font><br>" %('#ffffff', Update_Date))
        self.ui.WF_Status.setText("<font color=%s>%s</font><br>" %('#ffffff', Today_Status))
        self.ui.WF_Temp.setText("<font color=%s>%s</font><font color=#ffffff><font size=5px>℃</font></font>" %('#ffffff', Now_Temp))
        
        self.ui.WF_Title.setText("<font color=#ffffff>温度</font>")
        self.ui.WF_Title_2.setText("<font color=#ffffff>湿度</font>")
        self.ui.WF_Title_3.setText("<font color=#ffffff>降雨概率</font>")
        self.ui.WF_Title_4.setText("<font color=#ffffff>日落时间</font>")
        self.ui.ForecastToday.setText("<font color=%s>%s<br>%s</br><br>%s</br><br>%s</br></font>" %('#ffffff', Today_Temp, Today_Hum, Today_RainProb, Today_SunsetTime))#将请求的信息放入ForecastToday中，设置字体为 [白色]
    
        #写入明日天气信息到Weather页面中
        self.ui.WF_Nx_Title.setText("<font color=#ffffff>明天</font>")
        self.ui.WF_Nx_Time.setText("<font color=%s>%s</font>" %('#ffffff', Tomorrow_Date[5:])) #去除年份，只显示日期
        self.ui.ForecastNx_Status.setText("<font color=%s>%s</font>" %('#ffffff', Tomorrow_Status))
        self.ui.ForecastNx_Temp.setText("<font color=%s>%s</font>" %('#ffffff', Tomorrow_Temp))
 
    def TabToHome(self):
        self.ui.MainTab.setCurrentIndex(0)

    def TabToWeather(self):
        self.ui.MainTab.setCurrentIndex(1)

    def TabToAbout(self):
        self.ui.MainTab.setCurrentIndex(2)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    #win.showFullScreen()
    sys.exit(app.exec_())
