from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer


# Create your models here.


class User(AbstractUser):
	"""用户模型"""
	mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

	class Meta:
		db_table = 'tb_users'
		verbose_name = '用户'
		verbose_name_plural = verbose_name

	def generate_mobile_token(self):
		"""
		使用手机号生成token
		TimedJSONWebSignatureSerializer()可以生成对象
		该对象可以使用.dump()生成带有时效的token,bytes类型
		"""
		serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 300)
		# data = token中的载荷
		data = {'mobile': self.mobile}
		token = serializer.dumps(data).decode()
		return token