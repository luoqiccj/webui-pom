#运行测试用例执行命令
参数1：浏览器类型，支持ie、chrome、firefox
参数2：用例执行范围 1表示执行所有测试用例、2表示读取case_list指定的用例，默认1
1、进入RunAllCase目录
2、执行python run_all_case.py ie 2

用例执行完成后，发送用例执行结果邮件
1、进入utils目录
2、执行python send_email.py