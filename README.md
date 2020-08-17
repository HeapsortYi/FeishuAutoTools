# FeishuAutoTools
一款用于[飞书](https://www.feishu.cn/)的流程自动化工具😊

## Introduction
自己的业务主要是为了汇总共享文档里的日报，在此需求上实现了几个接口，如有需求者可以自取。

### project tree:
```
FeishuAutoTools
│  crontab.cfg    // crontab配置文件
│  script.sh      // 运行业务代码的脚本
├─biz                           // 自己的业务代码
│  │  conf.py
│  │  download_sheet_data.py    // 下载飞书云文档的sheet内容到本地
│  │  log_conf.py
│  │  refresh_token.py         // 刷新user_access_token和refresh_token
│  │  send_email.py            // 发送邮件的模块
│  │  work_summary.py          // 汇总日报
│  └─ __init__.py
├─daily_reports                // 保存日报的目录
├─feishu                       // 飞书相关接口
│  │  authen_api.py            // 身份验证相关接口
│  │  conf.py
│  │  http_utils.py            // https utils
│  │  sheets_api.py            // 操作sheet相关接口
│  │  token.txt                // 保存user_access_token和refresh_token
│  └─ __init__.py
├─log          // 日志目录
└─template     // 业务用到的.xlsx和.docx
```

## How to Use API
### 1. 创建应用和获得凭证
1. 创建企业自建应用: [参考文档](https://open.feishu.cn/document/uQjL04CN/ukzM04SOzQjL5MDN)
2. 获取授权凭证：[参考文档](https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM)

### 2. 进行身份验证
1. 身份验证开发指南：[参考文档](https://open.feishu.cn/document/ukTMukTMukTM/uETOwYjLxkDM24SM5AjN)
2. 第一次使用时，需要构造`https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri={REDIRECT_URI}&app_id={APPID}`格式的链接，在浏览器发送请求，然后完成扫码登录。登录成功后会生成登录预授权码 code，并作为参数重定向到重定向URL。
用返回的code修改`./feishu/authen_api.py`里**authen\_code\_**的值，然后运行`authen_api.py`，将返回结果中的**access_token**和**refresh_token**复制出来粘贴到`./feishu/token.txt`
3. 由于access_token不到两小时就会过期，可以配置一个定时任务保持刷新 --> 代码见`./biz/refresh_token.py`

### 3. 调用相关API
1. 调用`./feishu/authen_api.py`和`./feishu/sheets_api.py`中的接口即可。注意：调用需要access_token的API前，最好先刷新一下tokens避免过期
2. 可以参考官网文档实现更多API：
	+ [服务端API](https://open.feishu.cn/document/ukTMukTMukTM/uITNz4iM1MjLyUzM)
	+ [开放能力](https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uEDN04SM0QjLxQDN)

## Reference
- [飞书开放平台文档](https://open.feishu.cn/document/uQjL04CN/ucDOz4yN4MjL3gzM)
- [Python调用飞书API接口- 知乎](https://zhuanlan.zhihu.com/p/127962748)