from django.conf.urls import url

from user.views import UsernameView, MobileView, RegisterView

urlpatterns = [
	url(r'register/', RegisterView.as_view()),
	url(r'usernames/(?P<username>\w{5,20})/count/', UsernameView.as_view()),
	url(r'mobiles/(?P<mobile>(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8})/count/',
		MobileView.as_view()),
]
