from django.contrib.auth.decorators import login_required, user_passes_test

def is_user(tipo_user, function=None):
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated and u.is_tipo(tipo_user), 
		login_url='/', 
		redirect_field_name=None
	)

	if function:
		return actual_decorator(function)
	return actual_decorator