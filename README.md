##status:  
0： 成功   
1：失败  
##code：
1 ：以到达最后一页  
2：成功且不是最后一页  
0：没有内容
## /api/token
#### method: POST
#### headers 
```json
{
  "Content-Type": "application/json"
}
```
请求
```json
{
  "username": "aaa",
  "password": "123456"
}
```
响应
```json
{
  "message": "",
  "status": 0
}
```
```json
{
  "message": "",
  "status": 1,
  "token": ""
}
```
## /api/register
#### method: POST
```json
{
  "Content-Type": "application/json"
}
```
请求
```json
{
  "username": "aaa",
  "password": "123456"
}
```
响应
```json
{
  "message": "",
  "status": 0
}
```
```json
{
  "message": "",
  "status": 1
}
```
## /api/event 
#### method POST
headers
```json
{
  "Authorization": "passport token"
}
```
示例
```json
{
  "isPrivate": true,
  "isStory": true,
  "eventDate": "2019/11/22 11:00",
  "content": "ccc",
  "title": "ttt",
  "placeNumber": 1
}
```
响应
```json
{
  "message": "",
  "status": 1    
}
```
## /api/ground/events
#### method: GET
示例 /api/ground/events?pageNumber=1
响应:
```json
{
  "message": "",
  "code": 0
}
```
```json
{
    "code": 1,
    "events": [
        {
            "author": "aaa",
            "content": "ccc",
            "event_date": "Fri, 22 Nov 2019 11:00:00 GMT",
            "is_private": false,
            "is_story": 1,
            "place_number": 1,
            "post_date": "Fri, 22 Nov 2019 10:40:15 GMT",
            "title": "tttt",
            "event_id": 2
        },
        {
            "author": "aaa",
            "content": "ccc",
            "event_date": "Fri, 22 Nov 2019 11:00:00 GMT",
            "is_private": false,
            "is_story": 1,
            "place_number": 1,
            "post_date": "Fri, 22 Nov 2019 10:40:14 GMT",
            "title": "tttt",
            "event_id": 1
        }
    ],
    "message": "已经是最后一页"
}
```
## /api/user/history 
#### method: GET
示例 /api/user/history?username=aaa&pageNumber=1
headers
```json
{
  "Authorization": "passport token"
}
```
响应
```json
{
    "code": 1,
    "events": [
        {
            "author": "aaa",
            "content": "ccc",
            "event_date": "Fri, 22 Nov 2019 11:00:00 GMT",
            "is_private": false,
            "is_story": 1,
            "place_number": 1,
            "post_date": "Fri, 22 Nov 2019 10:40:15 GMT",
            "title": "tttt",
            "event_id": 3
        },
        {
            "author": "aaa",
            "content": "ccc",
            "event_date": "Fri, 22 Nov 2019 11:00:00 GMT",
            "is_private": false,
            "is_story": 1,
            "place_number": 1,
            "post_date": "Fri, 22 Nov 2019 10:40:14 GMT",
            "title": "tttt",
            "event_id": 2
        },
        {
            "author": "aaa",
            "content": "ccc",
            "event_date": "Fri, 22 Nov 2019 11:00:00 GMT",
            "is_private": true,
            "is_story": 1,
            "place_number": 1,
            "post_date": "Fri, 22 Nov 2019 10:38:09 GMT",
            "title": "tttt",
            "event_id": 1
        }
    ],
    "message": "已经是最后一页"
}
```
```json
{
  "message": "",
  "code": 0
}
```
## /api/event/comment 
#### method:POST
headers
```json
{
  "Authorization": "passport token"
}
```
```json
{
    "eid":1,
    "commentContent":"afwawfawfawf"
}
```
```json
{
    "message": "发送成功",
    "status": 1
}
```
## /api/event/comments
#### method:GET
示例 /api/event/comments?eid=1  
响应
```json
{
    "comments": [
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfawf",
            "title_of_event": "tttt"
        },
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfaaeaefaefwf",
            "title_of_event": "tttt"
        },
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfaaeafawawfaefaefwf",
            "title_of_event": "tttt"
        }
    ],
    "message": "获取成功",
    "status": 1
}
```
```json
{
  "message": "",
  "status": 0
}
```
## /api/user/comments
#### method:GET
示例 /api/user/comments?username=aaa  
响应  
```json
{
    "comments": [
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfawf",
            "title_of_event": "tttt"
        },
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfaaeaefaefwf",
            "title_of_event": "tttt"
        },
        {
            "comment_author": "aaa",
            "comment_content": "afwawfawfaaeafawawfaefaefwf",
            "title_of_event": "tttt"
        }
    ],
    "message": "获取成功",
    "status": 1
}
```
```json
{
  "message": "",
  "status": 0
}
```
## /api/password 
#### method : POST
```json
{
  "username": "aaa",
  "password": "123456",
  "newPassword": "12345"
}
```
响应  
```json
{
  "message": "修改成功",
  "status": 1
}
```
```json
{
  "message": "修改失败",
  "status": 0
}
```

## /api/username 
#### method: GET
示例 : /api/username?username=aaa"
响应
```json
{
  "message": "用户名已存在",
  "status": 0
}
```
```json
{
  "message": "用户名不能为空",
  "status": 0
}
```
```json
{
  "message": "用户名可用",
  "status": 1
}
```