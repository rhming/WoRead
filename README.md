# WoRead
沃阅读日常活动 使用腾讯云函数定时执行任务

+ 将src文件夹下的文件打包成zip上传到腾讯云函数 src文件夹下index.py函数主入口 需配置联通手机号(支持多账号)

+ 云函数环境配置 执行时间需大于10分钟(600秒)
> ![image](https://user-images.githubusercontent.com/49028484/127760009-ea0a3a13-cda9-4f0a-a726-db21226417d9.png)

+ 云函数触发配置 至少间隔10分钟执行一次 总共需执行10次(图片中是每半小时执行一次)
> ![image](https://user-images.githubusercontent.com/49028484/127760022-ca02d98d-456f-4a63-ba7a-572dfe3bbc38.png)


