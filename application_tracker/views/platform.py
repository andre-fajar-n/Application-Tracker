from application_tracker.models import Platform
from application_tracker.common.pagination import GetPaginationRequest
from application_tracker.forms import PlatformForm
from application_tracker.common.errors import getErrorMessageFromForm

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required(login_url='application_tracker:login')
def get_all(request):
    context = {}

    pagination_request = GetPaginationRequest()
    
    platform = Platform.objects.all().order_by("id")
    platform = platform.filter(user=request.user.id)

    paginator = Paginator(platform, pagination_request.get_per_page(request))
        
    data = paginator.get_page(pagination_request.get_page(request))

    context["pagination_data"] = data
    context["is_platform"] = "active"
    context["is_config"] = "active"

    return render(request, "config/platform/list.html", context)

@login_required(login_url='application_tracker:login')
def create(request):
    context = {}

    if request.method == "POST":
        form = PlatformForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user = request.user
            try:
                post.save()
            except DatabaseError as e:
                msg = ValidationError(e).messages[0]
                if "unique_platform" in msg:
                    msg = "This name already exist"
                messages.error(request, msg)
                return HttpResponseRedirect("/config/platform/new")

            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect("/config/platform/new")

            return HttpResponseRedirect("/config/platform")
        else:
            context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))
            return HttpResponseRedirect("/config/platform/new")

    return render(request, "config/platform/create.html", context)
