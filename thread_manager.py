# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     startThread
   Description :
   Author :       HSH
   date：          2017/11/13
-------------------------------------------------
   Change Activity:
                   2017/11/14:
-------------------------------------------------
"""
__author__ = 'HSH'
# 读取配置文件
import configparser
import requests

cf = configparser.ConfigParser()
cf.read('startThread.conf', encoding='UTF-8')
thread_list = cf['thread_list']


def start_threads():
    for key in thread_list.keys():
        start_thread(key)


def query_state():
    open_thread = []
    close_thread = []
    for key in thread_list.keys():
        try:
            data = {'className': cf[key]['classname']}
            url = 'http://localhost:' + cf[key]['port'] + '/enavpre/service/v1/ThreadManager/queryState'
            print(url)
            r = requests.get(url, data)
            if r.status_code == 303:
                open_thread.append( key)
            elif r.status_code == 304:
                close_thread.append(key)
        except Exception:
            print("连接tomcat" + cf[key]['port'] + "异常")
    print("开启中线程为：\n")
    num = 0
    for k in open_thread:
        print(str(num) + "." + thread_list[k] + "\n")
        num = num + 1
    print("关闭的线程为：\n")
    num = 0
    for k in close_thread:
        print(str(num) + "." + thread_list[k] + "\n")
        num = num + 1
    if input("是否需要改变状态？(y/n)") == 'y':
        arg_q = True
        while arg_q:
            arg_q = input("请输入指令")
            if arg_q == "exit":
                break
            arg_q = arg_q.split(",")
            if len(arg_q) != 2:
                print("参数有误请重新输入！")
                arg_q = True
            else:
                if arg_q[0] == "close":
                    shut_thread(open_thread[int(arg_q[1])])
                elif arg_q[0] == "start":
                    start_thread(close_thread[int(arg_q[1])])


def shut_thread(class_simnple_name):
    data = {'className': cf[class_simnple_name]['classname']}
    url = 'http://localhost:' + cf[class_simnple_name]['port'] + '/enavpre/service/v1/ThreadManager/shutDown'
    r = requests.get(url, data)
    if r.status_code == 304:
        print(cf['thread_list'][class_simnple_name] + "关闭成功,并且端口号为" + cf[class_simnple_name][
            'port'] + "的tomcat说" + r.text)
    else:
        print(cf['thread_list'][class_simnple_name] + "关闭失败,未知错误")


def start_thread(class_simnple_name):
    data = {'className': cf[class_simnple_name]['classname'], 'sleepTime': cf[class_simnple_name]['sleepTime']}
    url = 'http://localhost:' + cf[class_simnple_name]['port'] + '/enavpre/service/v1/ThreadManager/startRun'
    r = requests.get(url, data)
    if r.status_code == 200:
        print(cf['thread_list'][class_simnple_name] + "启动成功,并且端口号为" + cf[class_simnple_name][
            'port'] + "的tomcat说" + r.text)
    elif r.status_code == 400:
        print(cf['thread_list'][class_simnple_name] + "启动失败,并且端口号为" + cf[class_simnple_name][
            'port'] + "的tomcat说" + r.text + ",详情请查看tomcat日志")
    elif r.status_code == 201:
        print(cf['thread_list'][class_simnple_name] + "重启成功,并且端口号为" + cf[class_simnple_name][
            'port'] + "的tomcat说" + r.text)


def main():
    arg = True
    while arg:
        arg = input("请输入指令")
        if arg == "exit":
            exit()
        elif arg == "startall":
            start_threads()
        elif arg == "query":
            query_state()


if __name__ == '__main__':
    main()
