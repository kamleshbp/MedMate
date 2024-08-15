from django.db import transaction
from medapi.models import Robot

@transaction.atomic
def request_allocation():
    #For Now with Only one robot available no extra logic but to test for the max request a robot can take
    robot=Robot.objects.get(macId='b827eb22ee0f')
    if int(robot.rStatus)>8:
        return None
    robot.rStatus=int(robot.rStatus)+1
    robot.save()
    return 'b827eb22ee0f'
