from models import AlarmList


def initAlarmList(instance):
    user_objs = instance.user.all()
    if user_objs:
        for user in user_objs:
            AlarmList.objects.get_or_create(name=user.name, group=instance.name,)
    alarmlists = AlarmList.objects.filter(group=instance.name)
    if alarmlists:
        users = [u[0] for u in user_objs.values_list('name')]
        for alarmlist in alarmlists:
            if alarmlist.name not in users:
                alarmlist.delete()
