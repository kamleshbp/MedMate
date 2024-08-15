from django.db import transaction
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from PUBSUB.views import pubsub_view
from .backend import request_allocation
from medapi.models import Location, Client, Hospital, Operator, Robot, OrderRequest
from .serializers import AccountRegistrationSerializer, ClientSerializer, OrderRequestSerializer,ChangeClientLocationSerializer,RobotSerializer,SetRobotStatusSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def client_registration_view(request):
    if request.method == 'POST':
        logger.info("registration method invoked")
        data = {}
        data['contactNo'] = request.data.get('contactNo')
        data['password'] = request.data.get('password')
        accountSer = AccountRegistrationSerializer(data=data)
        data = {}
        data['cName'] = request.data.get('cName')
        data['hospital'] = request.data.get('hospital')
        data['gender'] = request.data.get('gender')
        data['birthday'] = request.data.get('birthday')
        data['occupation'] = request.data.get('occupation')
        #data['workLocation'] = request.data.get('workLocation')
        serializer = ClientSerializer(data=data)
        data = {}
        if accountSer.is_valid() and serializer.is_valid():
            account = accountSer.save()
            client = serializer.save(client=account)
            data['response'] = 'client successfully registered'
            data['cName'] = client.cName
            data['hospital'] = client.hospital.pk
            #data['workLocation'] = client.workLocation.pk
            token = Token.objects.get(user=client.client).key
            data['token'] = token
            logger.info("registration successful : " + token)
        elif not accountSer.is_valid():
            data['error'] = True
            data['errors'] = accountSer.errors
            logger.info("registration fail")
        else:
            data['error'] = True
            data['errors'] = serializer.errors
            logger.info("registration fail")
        return Response(data)


@transaction.atomic
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def client_login_view(request):
    if request.method == 'POST':
        logger.info("client_login_view method invoked")
        contactNo = request.data.get('contactNo')
        password = request.data.get('password')
        account = authenticate(contactNo=contactNo, password=password)
        data = {}
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            try:
                client = Client.objects.get(client=account.pk)
            except Client.DoesNotExist:
                data['error'] = True
                data['response'] = 'Error'
                data['error_message'] = 'Invalid credentials'
                return Response(data=data)

            data['cName'] = client.cName
            data['hospital'] = client.hospital.pk
            data['workLocation'] = client.workLocation.pk
            data['response'] = 'Successfully authenticated.'
            data['token'] = token.key
        else:
            data['error'] = True
            data['response'] = 'Error'
            data['error_message'] = 'Invalid credentials'

        return Response(data)


@transaction.atomic
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def fetch_all_valid_locations_view(request, hKey):
    if request.method == 'GET':
        logger.info("fetch_all_valid_location_view method invoked : "+str(request.user.contactNo))
        try:
            _ = Hospital.objects.get(hKey=hKey)
        except Hospital.DoesNotExist:
            data = {}
            data['response'] = 'Error'
            data['error_message'] = 'Hospital Key invalid'
            return Response(data)
        data = {}
        data['location'] = []
        location = Location.objects.filter(Q(hospital=int(hKey)) & ~Q(physicalName='Unknown'))
        for l in location:
            d = {}
            d['sensorId'] = l.sensorId
            d['physicalName'] = l.physicalName
            data['location'].append(d)
        return Response(data)

@transaction.atomic
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def fetch_all_locations_view(request, hKey,cachedTs):
    if request.method == 'GET':
        logger.info("fetch_all_location_view : "+str(request.user.contactNo))
        try:
            hospital = Hospital.objects.get(hKey=hKey)
        except Hospital.DoesNotExist:
            data = {}
            data['error'] = True
            data['response'] = 'Error'
            data['error_message'] = 'Hospital Key invalid'
            return Response(data)
        if cachedTs == str(hospital.update_ts)[:19]:
            return Response({'msg':'Use Cached data'})
        data = {}
        data['msg']='updated'
        data['cachedTs']=str(hospital.update_ts)[:19]
        data['location'] = []
        location = Location.objects.filter(hospital=int(hKey))
        for l in location:
            d = {}
            d['sensorId'] = l.sensorId
            d['xCor']=l.xCor
            d['yCor']=l.yCor
            d['floorNo']=l.floorNo
            d['physicalName'] = l.physicalName
            data['location'].append(d)
        return Response(data)

@transaction.atomic
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def change_client_location_view(request):
    if request.method == 'PUT':
        logger.info("change_client_location_view method invoked : "+str(request.user.contactNo))
        try:
            client=Client.objects.get(client=request.user)
        except Client.DoesNotExist:
            data = {}
            data['error'] = True
            data['response'] = 'Error'
            data['error_message'] = 'Invalid user'
            return Response(data)
        data = {}
        data['workLocation'] = request.data.get('workLocation')
        serializer=ChangeClientLocationSerializer(client,data=data,partial=True)
        if serializer.is_valid():
            data={}
            serializer.save()
            data['response'] = 'Success'
            return Response(data=data)
        data['error'] = True
        data['errors'] = serializer.errors
        return Response(data)


@transaction.atomic
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def order_request_view(request):
    if request.method == 'POST':
        logger.info("order_request_view method invoked : "+str(request.user.contactNo))
        data={}
        data['rGeneratorClient']=str(request.user.contactNo)
        data['slocation']=request.data.get('slocation')
        data['rlocation']=request.data.get('rlocation')
        data['reqMsg']=request.data.get('reqMsg')
        serializer = OrderRequestSerializer(data=data)
        if serializer.is_valid():
            # call request allocation method and get macId of robot
            macId = request_allocation()
            if macId is None:
                data = {}
                data['error'] = True
                data['errors'] = 'No Robots available. Please Try after some Time'
                return Response(data)
                #return Response({'Response':'No Robots available. Please Try after some Time'})
            order = serializer.save()


            requestId = OrderRequest.objects.get(requestId=order.pk)
            requestId.robot = Robot.objects.get(macId=macId)
            requestId.ordReqStatus = 'P'  # modified
            requestId.save()
            pubsub_data={}
            pubsub_data['request_id'] = str(requestId.pk);
            #channel name as a hospitalkey of that client should be passed to send the notifications
            #only to that hospital's operators
            pubsub_view(pubsub_data)
            data = {}
            data['response'] = 'Your request is received and is pending.'
            return Response(data)
        data={}
        data['error'] = True
        data['errors'] = serializer.errors
        return Response(data)

@transaction.atomic
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_all_requests_view(request):
    #To get all the requests attached with one client
    if request.method == 'GET':
        logger.info("get_all_requests_view method invoked : "+str(request.user.contactNo))
        try:
            client = Client.objects.get(client=request.user)
        except Client.DoesNotExist:
            data = {}
            data['error'] = True
            data['response'] = 'Error'
            data['error_message'] = 'Invalid user'
            return Response(data)

        data = {}
        orders = OrderRequest.objects.filter(Q(rGeneratorClient=client) & ~Q(ordReqStatus='D'))
        if not orders:
            data['noorder'] = True
            data['response'] = 'No orders'
            return Response(data)
        data['orders'] = []
        for o in orders:
            d = {}
            d['requestId'] = o.requestId
            d['sloaction'] = o.slocation.pk
            d['rlocation'] = o.rlocation.pk
            d['reqMsg'] = o.reqMsg
            d['ordReqStatus'] = o.ordReqStatus
            d['robotLocation']=o.robot.location.pk
            d['robotDirection']=o.robot.direction
            data['orders'].append(d)
        return Response(data)


@transaction.atomic
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def operator_login_view(request):
    if request.method == 'POST':
        logger.info("operator_login_view method invoked")
        contactNo = request.data.get('contactNo')
        password = request.data.get('password')
        account = authenticate(contactNo=contactNo, password=password)
        data = {}
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            try:
                operator = Operator.objects.get(operator=account)
            except Operator.DoesNotExist:
                data['response'] = 'Error'
                data['error_message'] = 'Invalid credentials'
                return Response(data=data)

            data['oName'] = operator.oName
            data['hospital'] = operator.hospital.pk
            data['response'] = 'Successfully authenticated.'
            data['token'] = token.key
        else:
            data['response'] = 'Error'
            data['error_message'] = 'Invalid credentials'

        return Response(data)


@transaction.atomic
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def operator_ack_view(request, requestId):
    if request.method == 'GET':
        logger.info("operator_ack_view method invoked : "+str(request.user.contactNo))
        try:
            order = OrderRequest.objects.get(requestId=requestId)
        except OrderRequest.DoesNotExist:
            return Response({'status': 'No such request exist'})
        if (order.operator is None):
            try:
                operator = Operator.objects.get(operator=request.user)
            except Operator.DoesNotExist:
                return Response({'status': 'No such operator exist'})
            operator.opStatus = 1  # 1 for occupied
            operator.save()
            order.ordReqStatus = 'A'  # P for pending A for assigned D for done
            order.operator = operator
            order.activated_ts=datetime.now()
            order.save()
            orderRequestSerializer = OrderRequestSerializer(instance=order)
            robotSerializer = RobotSerializer(instance=order.robot)
            clientSerializer = ClientSerializer(instance=order.rGeneratorClient)
            data={}
            data['orderRequest']=orderRequestSerializer.data
            data['robot']=robotSerializer.data
            data['client']=clientSerializer.data
            data['completed']=False
            return Response(data=data)

        else:
            return Response({'completed':True,'status': 'request is already assigned!'})


@transaction.atomic
@api_view(['PUT'])
@permission_classes([])
@authentication_classes([])
def set_robot_status_view(request):
    if request.method == 'PUT':
        macId=request.data.get('macId')
        logger.info("set_robot_status_view method invoked : "+macId)
        try:
            robot = Robot.objects.get(macId=macId)
        except Robot.DoesNotExist:
            return Response({'status': 'No such Robot exist'})
        data={}
        status=request.data.get('status')
        data['direction']=request.data.get('direction')
        data['location']=request.data.get('location')
        if  status== 'Decrement':
            if int(robot.rStatus)>0:
                data['rStatus']=int(robot.rStatus)-1
            else:
                data['rStatus']=robot.rStatus
        elif  status== 'Increment':
            if int(robot.rStatus)<10:
                data['rStatus']=int(robot.rStatus)+1
            else:
                data['rStatus']=robot.rStatus
        else:
            data['rStatus']=robot.rStatus

        setRobotStatusSerializer=SetRobotStatusSerializer(robot,data=data,partial=True)
        if setRobotStatusSerializer.is_valid():
            setRobotStatusSerializer.save()
            data={}
            data['Response']='Success'
            return Response(data=data)
        return Response(setRobotStatusSerializer.errors)


@transaction.atomic
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def request_status_view(request, requestId, status):

    if request.method == 'GET':
        logger.info("request_status_view method invoked : "+str(request.user.contactNo))
        try:
            order = OrderRequest.objects.get(requestId=requestId)
        except OrderRequest.DoesNotExist:
            return Response({'status': 'No such request exist'})
        operator1=order.operator

        if(operator1.operator != request.user):
            return Response({'status':'you are not authorized!'})
        if status == 'success':
            order.ordReqStatus = 'D'
            msg = "Positive feedback"
        else:
            order.ordReqStatus = 'F'
            msg = "Negative feedback"
        #robot = Robot.objects.get(macId=order.robot.macId)
        operator = order.operator
        operator.opStatus = 0  # 0 for free
        operator.save()
        order.save()

        # send msg to client

        return Response({'status': 'your feedback submited successfully'})
