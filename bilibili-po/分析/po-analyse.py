# -*- coding: utf-8 -*-
"""
Created on Thu May 29 21:29:38 2014

@author: Administrator
"""
import re

filename = 'bilibili-relation.txt';

def GetUpList():
    f = open(filename);
    uplist = [];
    for line in f:
        find = re.findall(r'^Up:.* (\d+)$',line)
        if find != []:
            uplist.append(int(find[0]));
    f.close();
    return uplist

def CreateDictBetweenUp(uplist):
    uplist = set(uplist);
    f = open(filename);
    updict = {};
    for line in f:
        find = re.findall(r'^Up:.* (\d+)$',line)
        if find != []:
            cur = int(find[0]);
            updict[cur] = {};
            updict[cur]['follow'] = set();
            find = re.findall(r'^Up:(.*) \d+$',line)
            if find != []:
                updict[cur]['name'] = find[0];
            else:
                print cur
            continue;
        find = re.findall(r'^fans:(\d+)$',line)
        if find != []:
            fans = int(find[0]);
            updict[cur]['fans'] = fans;
            continue;
        find = re.findall(r'^article:(\d+)$',line)
        if find != []:
            article = int(find[0]);
            updict[cur]['article'] = article;
            continue;
        find = re.findall(r'\t(\d+)$',line)
        if find != []:
            follow = int(find[0]);
            if follow in uplist:
                updict[cur]['follow'].add(follow);
    f.close();
    return updict

def GetNext(cor_fo,updict,ups):
    result = [];
    upNum = len(ups)
    for corfo in cor_fo:
        for i in xrange(upNum-1,-1,-1):
            if ups[i] <= corfo[-1]:
                break;
            flag = 1;
            for user in corfo:
                if ups[i] in updict[user]['follow'] and user in updict[ups[i]]['follow']:
                    continue
                else:
                    flag = 0;
                    break
            if flag:
                result.append(corfo+[ups[i]])
    return result

if __name__ == "__main__":
    uplist = GetUpList();
    updict = CreateDictBetweenUp(uplist);
    #保存每个Up的id，投稿数和粉丝数以便分析
    f = open('article-fans.txt','w');
    for up in updict:
        f.write("%d %d %d\n"%(up,updict[up]['article'],updict[up]['fans']))
    f.close();
    #查找最大关注圈
    ups = updict.keys();
    ups.sort();
    result = [[[i] for i in ups]];
    las = GetNext(result[-1],updict,ups);
    while las != []:
        result.append(las);
        las = GetNext(result[-1],updict,ups);
    #保存成文件
    for i in range(len(result)):
        f = open(str(i+1)+'.txt','w');
        for pair in result[i]:
            for po in pair:
                f.write(updict[po]['name']);
                f.write('\t');
            f.write('\n')
        f.close()
    print 'Finished'