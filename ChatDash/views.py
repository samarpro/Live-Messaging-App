from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ChatAuth.models import CustomAbstractUser
from ChatsBackend.models import ChatsModel 
from django.db.models import Q
from ChatsBackend.consumers import ChatHandlerConsumer
from django.utils.timezone import now
# Create your views here.

@login_required(login_url='ChatAuth:Login') # if login is not done then redirects to login_url
def DashBoardHandler(req):
    curr_user = CustomAbstractUser.objects.get(username=req.user.username)
    curr_user.last_login = now()
    curr_user.save()
    #  Getting all the user in Database and excluding the loggged in one
    user_names = CustomAbstractUser.objects.all().exclude(username=req.user.username)
    # Dictionary -> sent to frontend
    ParseDict = {
        'usernames':user_names, 
    }
    return render(req,"ChatDash/DashBrd.html",ParseDict)


def ChatProvider(req,receiver_name,render_all):
    print(render_all)

    curr_user = CustomAbstractUser.objects.get(username=req.user.username)
    if receiver_name == None:
        receiver_user = curr_user
    else:
        receiver_user=CustomAbstractUser.objects.get(username =receiver_name)

    TempQuery = ChatsModel.objects.filter(Q(sender = curr_user) | Q(receiver =curr_user),Q(sender = receiver_user) | Q(receiver =receiver_user)).order_by('timeStamp')

    #  this code is mainly requireed at beginning to load all the message
    dict_sendable ={}
    if bool(render_all):
        for obj in TempQuery:
            dict_sendable[str(obj.timeStamp)]={
                'sender':str(obj.sender),
                'receiver':str(obj.receiver),
                'message':str(obj.message)
            }
    else:
        TempQuery_obj = TempQuery.last()
        dict_sendable[str(TempQuery_obj.timeStamp)]={
                'sender':str(TempQuery_obj.sender),
                'receiver':str(TempQuery_obj.receiver),
                'message':str(TempQuery_obj.message)
            }

    print(dict_sendable)

    # Return a JSON response
    return JsonResponse(dict_sendable)

def Demo(req):
    return render(req,"ChatDash/demo.html")