#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date   : 2017/7/19
# @Author : trl
"""
txt
{
    "target_type" : "users", // users 给用户发消息。chatgroups: 给群发消息，chatrooms: 给聊天室发消息
    "target" : ["u1", "u2", "u3"], // 注意这里需要用数组，数组长度建议不大于20，即使只有一个用户，
                                   // 也要用数组 ['u1']，给用户发送时数组元素是用户名，给群组发送时  
                                   // 数组元素是groupid
    "msg" : {
        "type" : "txt",
        "msg" : "hello from rest" //消息内容，参考[[start:100serverintegration:30chatlog|聊天记录]]里的bodies内容
        },
    "from" : "jma2" //表示消息发送者。无此字段Server会默认设置为"from":"admin"，有from字段但值为空串("")时请求失败
}
img
{
    "target_type" : "users",   //users 给用户发消息。chatgroups: 给群发消息，chatrooms: 给聊天室发消息
    "target" : ["u1", "u2", "u3"],// 注意这里需要用数组，数组长度建议不大于20，即使只有一个用户，
                                  // 也要用数组 ['u1']，给用户发送时数组元素是用户名，给群组发送时  
                                  // 数组元素是groupid
    "msg" : {  //消息内容
        "type" : "img",   // 消息类型
        "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/55f12940-64af-11e4-8a5b-ff2336f03252",  //成功上传文件返回的UUID
        "filename": "24849.jpg", // 指定一个文件名
        "secret": "VfEpSmSvEeS7yU8dwa9rAQc-DIL2HhmpujTNfSTsrDt6eNb_", // 成功上传文件后返回的secret
        "size" : {
          "width" : 480,
          "height" : 720
      }
     },
    "from" : "jma2" //表示消息发送者，无此字段Server会默认设置为"from":"admin"，有from字段但值为空串("")时请求失败
}
audio
{
    "target_type" : "users",  //users 给用户发消息。chatgroups: 给群发消息，chatrooms: 给聊天室发消息
    "target" : ["testd", "testb", "testc"],// 注意这里需要用数组，数组长度建议不大于20，即使只有一个  
                                           // 用户或者群组，也要用数组形式 ['u1']，给用户发送  
                                           // 此数组元素是用户名，给群组发送时数组元素是groupid
    "msg" : {   //消息内容
        "type": "audio",  // 消息类型
        "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/1dfc7f50-55c6-11e4-8a07-7d75b8fb3d42",  //成功上传文件返回的UUID
        "filename": "messages.amr", // 指定一个文件名
        "length": 10,
        "secret": "Hfx_WlXGEeSdDW-SuX2EaZcXDC7ZEig3OgKZye9IzKOwoCjM" // 成功上传文件后返回的secret
    },
    "from" : "testa"   //表示消息发送者，无此字段Server会默认设置为"from":"admin"，有from字段但值为空串("")时请求失败
}
"""


class MessageBody(object):
    def __init__(self, target_type, target, msg, msg_from='admin'):
        self.target_type = target_type
        self.target = target
        self.msg = msg
        self.msg_from = msg_from

    def __call__(self, *args, **kwargs):
        body = {
            "target_type": self.target_type,
            "target": self.target,
            "msg": self.msg,
            "from": self.msg_from
        }
        return body
