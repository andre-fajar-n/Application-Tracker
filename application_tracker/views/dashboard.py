from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Home(View):
    context = {
        "is_dashboard":"active",
    }
    def get(self, request):
        return render(request, 'page/home.html', self.context)
