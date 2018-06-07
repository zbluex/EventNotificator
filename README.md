# EventNotificator


`作者：zhuqi00347042`

#### 导语

> 该工程用于监听指定时间是否发生，如果发生则根据配置在config.cfg中的配置信息发送邮件通知

## 一、配置说明

**config.cfg**

*[profile]*

    smtp_server         #smtp服务器地址
    smtp_port           #smtp服务器端口
    smtp_user           #登录smtp的账户
    smtp_passwd         #登录密码
    smtp_email_address  #用于显示发件人
    smtp_ssl            #是否启用ssl, True of False
    
*[DEFAULT]*

    user_to             #邮件默认发送主送人员，人员之间用,或者;符号隔开
    user_cc             #邮件默认发送抄送人员，人员之间用,或者;符号隔开
    
## 二、使用说明
    python EventNotificator.py -h
    usage: EventNotificator.py [-h] [-t TIME_INTERVAL] [-d] [-l LOGFILE]

    This tool is used to trigger events. When event triggered, it will send email
    to notice specified persons.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TIME_INTERVAL, --time_interval TIME_INTERVAL
                            set to specified default time interval of Event
                            trigger, unit is second.
      -d, --daemon          set program run as a daemon. Only support linux.
      -l LOGFILE, --logfile LOGFILE
                            specified log file path.
    
    Author: zhuqi1@huwei.com


