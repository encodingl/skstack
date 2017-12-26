from models import AlarmList


def initAlarmList(instance):
    user_objs = instance.user.all()
    if user_objs:
        for user in user_objs:
            AlarmList.objects.get_or_create(name=user, group=instance)
    alarmlists = AlarmList.objects.filter(group=instance)
    if alarmlists:
        for alarmlist in alarmlists:
            if alarmlist.name not in user_objs:
                alarmlist.delete()
