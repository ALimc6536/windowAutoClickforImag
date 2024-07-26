# windowAutoClickforImag
自动点击一个窗口中的特定图像
使用一些简单的指示，自动寻找窗体中的匹配图像并自动化点击
也支持一些其他的点击行为

inf.json
winClass：窗体类名
winName：窗体标题
windowSize：窗体大小
steps：步骤
[步骤名字, 步骤类型, 步骤参数, 点击图像, 更多参数...]
步骤类型:
sleep等待/秒
number点击指定图像，参数为次数
waitFor持续点击指定图像，直到参数所填的图像出现

例子：
["暂停","sleep",1] 暂停1秒
["做饭","number",3,"a.jpg"] a.jpg图像3次
["铲饭","waitFor","b.jpg","c.jpg",0.5] 持续点击c,jpg图像，每次点击后暂停0.5秒的执行，当出现b.jpg图像时，停止点击c.jpg（可忽略0.5）
