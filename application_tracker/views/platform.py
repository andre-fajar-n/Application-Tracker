from application_tracker.models import Platform
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from application_tracker.common.pagination import GetPaginationRequest

@login_required(login_url='application_tracker:login')
def GetAll(request):
    context = {}

    pagination_request = GetPaginationRequest()
    
    platform = Platform.objects.all().order_by("id")
    platform = platform.filter(user=request.user.id)

    paginator = Paginator(platform, pagination_request.get_per_page(request))
        
    data = paginator.get_page(pagination_request.get_page(request))

    context["pagination_data"] = data
    context["is_platform"] = "active"
    context["is_config"] = "active"

    return render(request, "config/platform/platform.html", context)