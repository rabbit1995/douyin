from login import models

def check_user(request):
    if request.session.get('is_login', None):
        user_id = request.session.get('user_id', None)
        user = models.User.objects.get(id=user_id)
        # 判断用户是不是新登录的
        if request.session.get('new', None):
            # 更新sessionid记录的用户为最新用户登录
            user.sessionid = request.session.session_key
            user.save()
            # 把标志为设置为false
            request.session['new'] = False
            return True
        else:
            # 如果不是新登录的用户，判断当前用户的sessionid于数据的最新session是否相等
            if user.sessionid == request.session.session_key:
                return True
            else:
                # 不相等则把当前用户的session注销,返回false
                request.session.flush()
                return False
    return False