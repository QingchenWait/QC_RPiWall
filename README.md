# QC_RPiWall
基于 PyQt 的树莓派小屏幕智能闹钟项目，具有万年历、所在城市天气查询、天气预报等功能。目前只是一个简单的 Demo ，有时间的话将在后期添加更多功能。

![image](https://github.com/QingchenWait/QC_RPiWall/blob/master/DemoImages/RPiWall_20B_1.png)
![image](https://github.com/QingchenWait/QC_RPiWall/blob/master/DemoImages/RPiWall_20B_2.png)

## 基本说明
本项目在树莓派 4 上，使用 eric 6 + PyQt 5 进行闹钟 GUI 界面的开发，在树莓派本机上测试通过。eric6 的工程项目（.e4p）文件，已经随源码上传到仓库，方便调试与二次开发。

本项目专为分辨率为 480x320 的树莓派专用 3.5 寸小屏幕设计，后期将通过添加 DPI 缩放功能，实现更多分辨率的屏幕支持。

## 部署方式 & 注意事项
1. 需要在树莓派上安装 PyQt5 环境。

2. 本项目的天气相关服务，调用了 `和风天气` 的付费天气查询接口。价格为 1 元 / 1000 次，而本版本程序每天只调用 8 次接口，所需成本极低。

     首先，在 [和风天气开发平台](https://dev.heweather.com/) 中，注册一个开发者账户，在控制台中，新建一个应用，并购买 `按量付费` 的天气预报服务。
     
     在控制台的 `应用管理` 页面，找到应用的 KEY。 在 `__init__.py` 的第 `44、53、75` 行，把末尾 `key=**********` 里面的 ********** ，替换成自己的 KEY 。
     
3. 如果在使用 PyQt 进行二次开发中，修改了图片的资源库，那么，则需要在终端中执行以下命令，将修改导入到资源库文件中：

     `pyrcc5 -o Pictures_rc.py Pictures.qrc`
