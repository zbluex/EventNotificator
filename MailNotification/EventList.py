from event import EventSSH

EventList = [
        EventSSH.EventSSH('cat /etc/os-release |grep "^NAME="', 'NAME="SLES"',
                          "root", "password", "127.0.0.1",
                          time_interval=5,
                          extra_cmd=['data',],
                          user_to=['demo@gmail.com',],
                          user_cc=['demo@gmail.com',]),
    ]
