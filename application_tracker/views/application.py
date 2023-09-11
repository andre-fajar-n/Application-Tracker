from application_tracker.models import Application, Platform, ApplicationStatus, ApplicationHistory
from application_tracker.common.pagination import GetPaginationRequest
from application_tracker.forms import CreateApplicationForm, UpdateApplicationForm
from application_tracker.common.errors import getErrorMessageFromForm

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import DatabaseError, transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
import datetime

canceled_redirect_url_key = "canceled_redirect_url"
create_url_key = "create_url"

base_url = "/application"
url_list = base_url
create_url = f"{base_url}/new"

base_template_path = "page/application/"

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class GetAll(View):
    context = {
        create_url_key:create_url
    }
    template = base_template_path + "list.html"

    def get(self, request):
        pagination_request = GetPaginationRequest()
        
        application_status = Application.objects.all().order_by("id")
        application_status = application_status.filter(user=request.user.id)

        paginator = Paginator(application_status, pagination_request.get_per_page(request))
            
        data = paginator.get_page(pagination_request.get_page(request))

        self.context["pagination_data"] = data
        self.context["is_application"] = "active"

        return render(request, self.template, self.context)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Create(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = base_template_path + "create.html"
    path = create_url

    def get(self, request):
        platform = Platform.objects.filter(user=request.user).order_by("name")
        self.context['platform'] = platform

        form = CreateApplicationForm(request.GET)
        self.context['form'] = form

        application_status = ApplicationStatus.objects.filter(user=request.user).order_by("name")
        self.context['application_status'] = application_status
        return render(request, self.template, self.context)

    def post(self, request):
        form = CreateApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            try:
                with transaction.atomic():
                    application.save()

                    application_history = ApplicationHistory()
                    application_history.status = application.last_status
                    application_history.application = application
                    application_history.note = request.POST.get("note")
                    application_history.save()
            except DatabaseError as e:
                msg = ValidationError(e).messages[0]
                messages.error(request, msg)
                return HttpResponseRedirect(self.path)

            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(self.path)

            return HttpResponseRedirect(url_list)
        else:
            self.context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))
            return HttpResponseRedirect(self.path)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Delete(View):
    context = {}
    template = base_template_path + "list.html"
    path = base_url

    def get(self, request, id):
        try:
            with transaction.atomic():
                ApplicationHistory.objects.filter(application_id=id).delete()
                Application.objects.filter(id=id, user=request.user).delete()
        except:
            messages.error(request, f"Failed to delete application with id {id}")
        return HttpResponseRedirect(self.path)

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Edit(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = base_template_path + "edit.html"
    
    def insert_id_to_path(self, id):
        return f"{base_url}/{id}/edit"
    
    def get_detail_data(self, id, user):
        return Application.objects.get(id=id, user=user)

    def get(self, request, id):
        try:
            data = self.get_detail_data(id, request.user)
            self.context['data'] = data

            platform = Platform.objects.filter(user=request.user).order_by("name")
            self.context['platform'] = platform
        except:
            self.template = "page/data_not_found.html"
        return render(request, self.template, self.context)

    def post(self, request, id):
        current_data = self.get_detail_data(id, request.user)
        form = UpdateApplicationForm(request.POST, instance=current_data)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.updated_at = datetime.datetime.now()
                post.save()
            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(self.insert_id_to_path(id))

            return HttpResponseRedirect(base_url)

        self.context['form'] = form
        messages.error(request, getErrorMessageFromForm(form))
        return HttpResponseRedirect(self.insert_id_to_path(id))

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Detail(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = base_template_path + "detail.html"

    def get_detail_data(self, id, user):
        return Application.objects.get(id=id, user=user)

    def get(self, request, id):
        try:
            data = self.get_detail_data(id, request.user)
            self.context['data'] = data

            histories = ApplicationHistory.objects.filter(application_id=data.id).order_by("-update_status_at", "-created_at")
            self.context['histories'] = histories
        except:
            self.template = "page/data_not_found.html"
        return render(request, self.template, self.context)