#用户认证体系

##### 获取用户UUID（授权）
> POST  : http://.../uc/auth
> 
> DATA  : user=一卡通;password=统一身份认证密码;appid=应用唯一标识符;
> 
> RETURN: 用户唯一标识符（UUID）;参数错误:HTTP400;获取失败:HTTP401

##### 用户标识符合法性检查
> POST  : http://.../uc/check
> 
> DATA  : uuid=用户唯一标识符;appid=应用唯一标识符;
> 
> RETURN: 参数错误:HTTP400;uuid不合法:HTTP401;uuid合法:HTTP200 ‘OK’

##### 更新用户信息
> POST  : http://.../uc/update
> 
> DATA  : appid=应用唯一标识符;cardnum=一卡通;number=学号;password=统一身份认证密码;pe_password=体育系密码;lib_username=图书馆用户名;lib_password=图书馆密码;card_query_password=一卡通查询密码;
> 
> RETURN: 参数错误:HTTP400;uuid不合法:HTTP400;注销成功:HTTP200 ‘OK’

##### 注销用户UUID（解除授权）
> POST  : http://.../uc/deauth
> 
> DATA  : uuid=用户唯一标识符;appid=应用唯一标识符;
> 
> RETURN: 参数错误:HTTP400;uuid不合法:HTTP401;注销成功:HTTP200 ‘OK’

##### 调用API获取用户信息（使用API）
> POST  : http://.../uc/api/[API NAME]
> 
> DATA  : uuid=用户唯一标识符;appid=应用唯一标识符;
> 
> RETURN: 参数错误:HTTP400;成功:HTTP200 API返回内容

##### API NAME 信息
- srtp
- term
- sidebar
- curriculum
- gpa
- pe
- simsimi
- nic
- card
```
