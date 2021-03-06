import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from goods.models import SKU
from user.models import User, Address
from celery_tasks.send_email.tasks import send_to_email


class RegisterSerializer(serializers.ModelSerializer):
	"""注册反序列化"""

	password2 = serializers.CharField(label='确认密码', write_only=True)
	sms_code = serializers.CharField(label='短信验证码', write_only=True)
	allow = serializers.CharField(label='同意协议', write_only=True)
	# 新增需要的token
	token = serializers.CharField(label='登录状态token', read_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token')
		extra_kwargs = {
			'username': {
				'min_length': 5,
				'max_length': 20,
				'error_messages': {
					'min_length': '仅允许5-20个字符的用户名',
					'max_length': '仅允许5-20个字符的用户名',
				}
			},
			'password': {
				'write_only': True,
				'min_length': 8,
				'max_length': 20,
				'error_messages': {
					'min_length': '仅允许8-20个字符的密码',
					'max_length': '仅允许8-20个字符的密码',
				}
			}
		}

	def validate_mobile(self, value):
		"""验证手机号"""
		if not re.match(r'^1[3-9]\d{9}$', value):
			raise serializers.ValidationError('手机号格式错误')
		return value

	def validate_allow(self, value):
		"""检验用户是否同意协议"""
		if value != 'true':
			raise serializers.ValidationError('请同意用户协议')
		return value

	def validate(self, data):
		# 判断两次密码
		if data['password'] != data['password2']:
			raise serializers.ValidationError('两次密码不一致')

		# 判断短信验证码
		redis_conn = get_redis_connection('verify_codes')
		mobile = data['mobile']
		real_sms_code = redis_conn.get('sms_%s' % mobile)
		if real_sms_code is None:
			raise serializers.ValidationError('无效的短信验证码')
		if data['sms_code'] != real_sms_code.decode():
			raise serializers.ValidationError('短信验证码错误')

		return data

	def create(self, validated_data):
		"""
		创建用户
		"""
		# 移除数据库模型类中不存在的属性
		del validated_data['password2']
		del validated_data['sms_code']
		del validated_data['allow']
		user = super().create(validated_data)

		# 调用django的认证系统加密密码
		user.set_password(validated_data['password'])
		user.save()

		# 补充生成记录登录状态的
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)
		user.token = token
		return user


class CheckSmsCodeSerializer(serializers.Serializer):
	"""校验短信验证码"""
	sms_code = serializers.CharField(min_length=6, max_length=6)

	def validate(self, attrs):
		account = self.context['view'].kwargs['account']
		user = User.objects.get(username=account)
		if not user:
			raise serializers.ValidationError('用户不存在')
		self.user = user
		sms_code = attrs.get('sms_code')

		redis_conn = get_redis_connection('verify_codes')
		mobile = user.mobile
		real_sms_code = redis_conn.get('sms_%s' % mobile).decode()
		if not real_sms_code:
			raise serializers.ValidationError('短信验证码过期或失效')
		if sms_code != real_sms_code:
			raise serializers.ValidationError('短信验证码输入错误')
		return attrs


class CheckUserIdSerializer(serializers.ModelSerializer):
	"""校验use_id和重置密码"""
	password2 = serializers.CharField(label='密码', write_only=True)
	access_token = serializers.CharField(label='token', write_only=True)

	class Meta:
		model = User
		fields = ['id', 'password', 'password2', 'access_token', ]
		extra_kwargs = {
			'password': {
				'write_only': True,
				'min_length': 8,
				'max_length': 20,
				'error_messages': {
					'min_length': '仅允许8-20个字符的密码',
					'max_length': '仅允许8-20个字符的密码',
				}
			}
		}

	def validate(self, attrs):
		"""验证用户信息"""
		# 调用模型中的方法,校验身份
		user_id_by_url = self.context['view'].kwargs['pk']
		access_token = attrs['access_token']
		allow = User.check_access_token_reset_password(user_id_by_url, access_token)
		if not allow:
			raise serializers.ValidationError('token失效或过期')

		password = attrs['password']
		password2 = attrs['password2']
		if password2 != password:
			raise serializers.ValidationError('两次密码不一致')
		return attrs

	# 更新数据中的密码
	def update(self, instance, validated_data):
		password = validated_data['password']
		pk = self.context['view'].kwargs['pk']
		user = User.objects.get(pk=pk)
		user.set_password(password)
		user.save()
		return user


class UserInfoSerializer(serializers.ModelSerializer):
	"""用户信息序列化器 """

	class Meta:
		model = User
		fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
	"""邮箱序列化"""

	class Meta:
		model = User
		fields = ['id', 'email']
		extra_kwargs = {
			'email': {
				'required': True
			}
		}

	def update(self, instance, validated_data):
		instance.email = validated_data['email']
		instance.save()
		# 生成url
		url = instance.generate_email_url()
		# 异步发送email
		send_to_email.delay(instance.email, url)

		return instance


class AddressSerializer(serializers.ModelSerializer):
	"""地址管理反序列化器"""
	province = serializers.StringRelatedField(read_only=True)
	city = serializers.StringRelatedField(read_only=True)
	district = serializers.StringRelatedField(read_only=True)
	province_id = serializers.IntegerField(label='省ID', required=True)
	city_id = serializers.IntegerField(label='市ID', required=True)
	district_id = serializers.IntegerField(label='区ID', required=True)

	class Meta:
		model = Address
		exclude = ('user', 'is_deleted', 'create_time', 'update_time')

	def validate_mobile(self, value):
		"""
		验证手机号
		"""
		if not re.match(r'^1[3-9]\d{9}$', value):
			raise serializers.ValidationError('手机号格式错误')
		return value

	def create(self, validated_data):
		"""
		保存
		"""
		validated_data['user'] = self.context['request'].user
		return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
	"""
	地址标题
	"""

	class Meta:
		model = Address
		fields = ('title',)


class UserBrowseSerializer(serializers.Serializer):
	"""校验sku_id,记录浏览记录"""

	sku_id = serializers.IntegerField(min_value=1)

	def validated_sku_id(self, value):
		try:
			SKU.objects.get(id=value)
		except Exception as e:
			raise serializers.ValidationError('sku_id不存在')
		return value

	def create(self, validated_data):
		"""教研成功后吧浏览记录保存到redis"""
		# redis 中保存的 形式:
		# user_id:['sku_id1','sku_id2','sku_id3',]

		user_id = self.context['request'].user.id
		sku_id = validated_data['sku_id']
		redis_conn = get_redis_connection('history')
		pl = redis_conn.pipeline()
		# 删除全部的相同的数据
		pl.lrem("history_%s" % user_id, 0, sku_id)
		pl.lpush("history_%s" % user_id, sku_id)
		pl.ltrim("history_%s" % user_id, 0, 5)

		pl.execute()

		return validated_data
