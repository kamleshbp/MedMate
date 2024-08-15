from rest_framework import serializers
from medapi.models import Client, Location,Account,OrderRequest,Robot

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['cName','hospital','gender','birthday','occupation','workLocation']
        read_only_fields = ['workLocation']



class AccountRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['contactNo','password']
        extra_kwargs = {
				'password': {'write_only': True},
		}

    def	save(self):
        account = Account(
        			contactNo=self.validated_data['contactNo']
        		)
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account

class ChangeClientLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['workLocation']

class OrderRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderRequest
		#fields = ['rGeneratorClient', 'slocation', 'rlocation', 'reqMsg']
		fields = '__all__'
		#fields = ['rGeneratorClient', 'slocation', 'rlocation', 'reqMsg']
		read_only_fields = ['requestId', 'senMsg','recMsg','ordReqStatus','operator','robot']

class RobotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Robot
		fields = '__all__'

class SetRobotStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Robot
        fields=['rStatus','location','direction']
