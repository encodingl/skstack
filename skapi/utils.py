from models import AlarmList


def initAlarmList(instance):
    user_objs = instance.user.all()
    for user in user_objs:
        AlarmList.objects.get_or_create(user=user, group=instance)
    alarmlists = AlarmList.objects.filter(group=instance)
    for alarmlist in alarmlists:
        if alarmlist.user not in user_objs:
            alarmlist.delete()
