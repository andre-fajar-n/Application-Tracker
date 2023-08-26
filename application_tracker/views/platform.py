from application_tracker.models import Platform
from application_tracker.common.pagination import GetPaginationRequest
from application_tracker.forms import PlatformForm
from application_tracker.common.errors import getErrorMessageFromForm

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator

canceled_redirect_url_key = "canceled_redirect_url"
create_url_key = "create_url"

url_list = "/config/platform"
create_url = "/config/platform/new"

@login_required(login_url='application_tracker:login')
def get_all(request):
    context = {
        create_url_key:create_url
    }

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
    context = {
        canceled_redirect_url_key:url_list
    }
    template = "config/platform/create.html"
    path = "/config/platform/new"

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
                return HttpResponseRedirect(path)

            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(path)

            return HttpResponseRedirect("/config/platform")
        else:
            context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))
            return HttpResponseRedirect(path)

    return render(request, template, context)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Edit(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = "config/platform/edit.html"
    
    def insert_id_to_path(self, id):
        return f"/config/platform/{id}/edit"
    
    def get_detail_data(self, id, user):
        return Platform.objects.get(id=id, user=user)

    def get(self, request, id):
        try:
            data = self.get_detail_data(id, request.user)
            self.context['data'] = data
        except:
            self.template = "data_not_found.html"
        return render(request, self.template, self.context)

    def post(self, request, id):
        current_data = self.get_detail_data(id, request.user)
        form = PlatformForm(request.POST, instance=current_data)
        if form.is_valid():
            try:
                form.save()
            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(self.insert_id_to_path(id))

            return HttpResponseRedirect("/config/platform")

        self.context['form'] = form
        messages.error(request, getErrorMessageFromForm(form))
        return HttpResponseRedirect(self.insert_id_to_path(id))

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Delete(View):
    context = {}
    template = "config/platform/list.html"
    platform = Platform

    def get(self, request, id):
        try:
            self.platform.objects.filter(id=id, user=request.user).delete()
        except:
            messages.add_message(request, 1, f"Failed to delete platform with id {id}")
        return redirect('application_tracker:list_platform')