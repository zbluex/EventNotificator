# EventNotificator


`作者：Aiwizhu`

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
    usage: EventNotificator.py [-h] [-t TIME_INTERVAL] [-l LOGFILE]
    
    This tool is used to trigger events. When event triggered, it will send email
    to notice specified persons.
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TIME_INTERVAL, --time_interval TIME_INTERVAL
                            set to specified default time interval of Event
                            trigger, unit is second.
      -l LOGFILE, --logfile LOGFILE
                            specified log file path.
    
    Author: zbluex@gmail.com

## 三、Event事件配置说明
### 1、添加Event监听事件
如果要添加监听事件，需要在EventNotificator中的EventList列表中添加监听实例。

实例实例如下所示：

    from event import EventSSH
    
    EventList = [
            EventSSH.EventSSH('cat /etc/os-release |grep "^NAME="', 'NAME="SLES"',
                              "root", "password", "127.0.0.1",
                              time_interval=5,
                              extra_cmd=['data',],
                              user_to=['demo@gmail.com',],
                              user_cc=['demo@gmail.com',]),
    ]
以上初始化了一个EventSSH实例，该实例执行'cat /etc/os-release |grep "^NAME="'命令，并且期望获得'NAME="SLES"'的结果，如果期望发生，则利用邮件通知用户。后面跟的参数分别为ssh连接的用户名、密码、ip、端口等，更多的事件实例后续会进行介绍。

### 2、EventSSH
该实例是一个SSH监听实例，利用ssh协议连接到指定节点执行指定命令，获取结果与期望值进行匹配，如果匹配成功，则发送邮件进行通知。

实例初始化参数：

    class EventSSH(EventBase.EventBase):

    def __init__(self, cmd, expect, user, passwd, host, port=22, *args, **kwargs):
        .....
初始化实例参数从前往后的顺序为：

    cmd             #执行的shell命令
    expect          #命令期望值
    user            #ssh用户名
    password        #ssh密码
    host            #ssh连接ip
    port            #ssh连接端口
以及扩展参数：
    
    extra_cmd       #list()， 事件发生时额外执行的命令，将结果添加到附件
    user_to         #list()， 事件发生时需要额外主送的人员
    user_cc         #list()， 事件发生时需要额外抄送的人员
    re_trigger      #True or False，该事件是否为重复监听事件
    time_interval   #int， 设定监听事件间隔，单位为秒