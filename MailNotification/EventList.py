import event.EventSSH as ES

EventList = [
        ES.EventSSH("ps -ef |grep loop_test.sh|grep -v grep", "",
                    "root", "Huawei12#$", "192.168.140.218",
                    time_interval=5)
    ]