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

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class GetAll(View):
    context = {
        create_url_key:create_url
    }
    template = "page/config/platform/list.html"

    def get(self, request):
        pagination_request = GetPaginationRequest()
        
        platform = Platform.objects.all().order_by("id")
        platform = platform.filter(user=request.user.id)

        paginator = Paginator(platform, pagination_request.get_per_page(request))
            
        data = paginator.get_page(pagination_request.get_page(request))

        self.context["pagination_data"] = data
        self.context["is_platform"] = "active"
        self.context["is_config"] = "active"

        return render(request, self.template, self.context)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Create(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = "page/config/platform/create.html"
    path = "/config/platform/new"
    
    def get(self, request):
        return render(request, self.template, self.context)
    
    def post(self, request):
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
                return HttpResponseRedirect(self.path)

            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(self.path)

            return HttpResponseRedirect("/config/platform")
        else:
            self.context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))
            return HttpResponseRedirect(self.path)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Edit(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = "page/config/platform/edit.html"
    
    def insert_id_to_path(self, id):
        return f"/config/platform/{id}/edit"
    
    def get_detail_data(self, id, user):
        return Platform.objects.get(id=id, user=user)

    def get(self, request, id):
        try:
            data = self.get_detail_data(id, request.user)
            self.context['data'] = data
        except:
            self.template = "page/data_not_found.html"
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
    template = "page/config/platform/list.html"
    platform = Platform

    def get(self, request, id):
        try:
            self.platform.objects.filter(id=id, user=request.user).delete()
        except:
            messages.add_message(request, 1, f"Failed to delete platform with id {id}")
        return redirect('application_tracker:list_platform')