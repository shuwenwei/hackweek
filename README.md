##status:  
0： 成功   
1：失败  
##code：
1 ：以到达最后一页  
2：成功且不是最后一页  
0：没有内容
## /api/token
#### method: POST
登录json示例  
{  
    "username":"aaa",  
    "password":"123456"  
}  
返回  
{"token":token,  
"message":"",  
"status":(0,1)}
## /api/register
#### method:POST
注册
{  
    "username":"aaa",  
    "password":"123456"  
} 
返回
{  
"message":"",  
"status":(0,1)    
}
## /api/postEvent
#### method:POST
发送  
####headers: Authorization:passport 返回的token
eventDate为字符串格式为 %Y/%m/%d %H:%M    
{
"eventDate":"2019/11/20 20:00",  
"content":"",  
"title":"",
placeNumber:(int),  
"isPrivate":(true,false) ,
"isStory":(true,false) 
}  
返回  
{
"message":"",  
"status":(0,1)
}
## api/getGroundEvents
#### method:GET
