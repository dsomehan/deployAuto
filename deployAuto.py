# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     deployAuto.py
   Description : 自动部署tomcat
   Author :       HSH
   date：          2017/11/1
-------------------------------------------------
   Change Activity:
                   2017/11/1:
-------------------------------------------------
"""
__author__ = 'HSH'
import os
import configparser
import zipfile
import datetime
from functools import reduce
import thread_manager


# 解压
def unzip(src, dist):
    print('正在解压缩' + src + "到" + dist + '......')
    f = zipfile.ZipFile(src, 'r')
    for file in f.namelist():
        f.extract(file, dist)
    print('解压缩' + src + "到" + dist + '完成！')


# 压缩
def zip_dfile(src, dist_zipfile):
    if os.path.exists(src):
        if os.path.isfile(src) or (os.path.isdir(src) and len(os.listdir(src)) == 0):
            dist_zipfile.write(src, reduce(lambda x, y: x + os.sep + y, src.split(os.sep)[4:]))
        else:
            for d in os.listdir(src):
                d = src + os.sep + d
                zip_dfile(d, dist_zipfile)


def compressed(src, dist):
    print("正在压缩" + src + "到" + dist + '......')
    f = zipfile.ZipFile(dist, 'w')
    zip_dfile(src, f)
    f.close()
    print("正在压缩" + src + "到" + dist + "完成！")


def clear_cache(src):
    if os.path.isfile(src):
        os.remove(src)
    elif os.path.isdir(src) and len(os.listdir(src)) == 0:
        os.rmdir(src)
    else:
        while os.path.isdir(src) and len(os.listdir(src)) > 0:
            for d in os.listdir(src):
                d = src + os.sep + d
                clear_cache(d)


def clear_tomcat(tomcat_path):
    print('清理' + tomcat_path + '路径下的tomcat日志')
    path = tomcat_path + os.sep + 'bin'
    for file in os.listdir(path):
        if '.log' in file:
            file = path + os.sep + file
            clear_cache(file)
    path = tomcat_path + os.sep + 'logs'
    for file in os.listdir(path):
        file = path + os.sep + file
        clear_cache(file)
    print('清理' + tomcat_path + '路径下的tomcat缓存')
    path = tomcat_path + os.sep + 'work'
    for file in os.listdir(path):
        file = path + os.sep + file
        clear_cache(file)
    print('清理' + tomcat_path + '路径下的tomcat部署文件')
    path = tomcat_path + os.sep + 'webapps'
    for file in os.listdir(path):
        file = path + os.sep + file
        clear_cache(file)


def deploy_tomcat(zip_path, tomcat_path):
    print('开始部署' + tomcat_path + '路径下的tomcat部署文件......')
    src = zip_path + os.sep + os.listdir(zip_path)[0]
    dist = tomcat_path + os.sep + 'webapps'
    unzip(src, dist)
    print('部署' + tomcat_path + '路径下的tomcat部署文件完成！')


def shut_down_tomcat(tomcat_path):
    print('停止' + tomcat_path + '路径下的tomcat')
    if os.path.exists(tomcat_path):
        os.chdir(tomcat_path + os.sep + 'bin')
        os.system('shutdown.bat')
    else:
        print("错误！" + tomcat_path + "不存在，请检查配置文件！")


def start_up_tomcat(tomcat_path):
    if os.path.exists(tomcat_path):
        os.chdir(tomcat_path + os.sep + 'bin')
        os.system('startup.bat')
    else:
        print("错误！" + tomcat_path + "不存在，请检查配置文件！")


def backup_deploy_file(tomcat_path, back_path):
    print("备份部署文件")
    if not os.path.exists(back_path):
        os.makedirs(back_path)
    # for file in os.listdir(back_path):
    #     clear_cache(back_path + os.sep + file)
    path = tomcat_path + os.sep + 'webapps'
    for file in os.listdir(path):
        dest = path + os.sep + file
        compressed(dest, back_path + os.sep + file + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '备份.zip')


def check_conf(tomcat_path_dic, zip_path_dic, backup_path_dic):
    for k in tomcat_path_dic.keys():
        tomcat_path = tomcat_path_dic[k]
        if k not in zip_path_dic.keys():
            exit('请检查配置文件：未配置' + k + '部署文件路径')
        else:
            if not os.path.exists(zip_path_dic[k]):
                exit('请检查配置文件：' + k + '部署文件路径不存在')
        bin_path = tomcat_path + os.sep + 'bin'
        if not os.path.exists(bin_path):
            exit(k + '下文件缺失bin')
        if 'startup.bat' not in os.listdir(bin_path):
            exit(k + '下缺少启动脚本')
        if 'shutdown.bat' not in os.listdir(bin_path):
            exit(k + '下缺少关闭脚本')


def main():
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read('deploy.conf')
    tomcat_path_dic, zip_path_dic, backup_path_dic = cf['tomcat_path'], cf['zip_path'], cf['backup']
    # 检测配置文件有效性
    check_conf(tomcat_path_dic, zip_path_dic, backup_path_dic)
    # 关闭tomcat
    for k in tomcat_path_dic.keys():
        shut_down_tomcat(tomcat_path_dic[k])
    # 备份tomcat
    backup_deploy_file(tomcat_path_dic[backup_path_dic['backup_server']], backup_path_dic['path'])
    # 部署并启动tomcat
    for k in tomcat_path_dic.keys():
        tomcat_path = tomcat_path_dic[k]
        clear_tomcat(tomcat_path)
    if input("是否开始部署？（y/n）") == 'y':
        for k in tomcat_path_dic.keys():
            tomcat_path = tomcat_path_dic[k]
            deploy_tomcat(zip_path_dic[k], tomcat_path)
            start_up_tomcat(tomcat_path)
    is_start_thread = input("是否启动配置startThread中的线程？（y/n）")
    if is_start_thread == 'y':
        thread_manager.start_thread()


if __name__ == '__main__':
    main()
