from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError

from application_tracker.models import ApplicationHistory, Application, ApplicationStatus
from application_tracker.forms import CreateNewApplicationHistoryForm
from application_tracker.common.errors import getErrorMessageFromForm

canceled_redirect_url_key = "canceled_redirect_url"

base_template_path = "page/application_history/"
base_url = "/application"
url_list = base_url

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Delete(View):
    context = {}
    template = base_template_path + "detail.html"
    path = base_url

    def get(self, request, application_id, id):
        try:
            with transaction.atomic():
                ApplicationHistory.objects.filter(application_id=application_id, id=id).delete()

                # get last history
                history = ApplicationHistory.objects.filter(application_id=application_id).order_by("-update_status_at", "-created_at")[0]

                application = Application.objects.get(id=application_id)
                application.last_status = history.status
                application.last_updated = history.update_status_at
                application.save()
        except:
            messages.error(request, f"Failed to delete application with id {id}")
        return HttpResponseRedirect(self.path + f"/{application_id}")

@method_decorator(login_required(login_url='application_tracker:login'), name='get')
class Create(View):
    context = {
        canceled_redirect_url_key:url_list
    }
    template = base_template_path + "create.html"
    path = base_url

    def get(self, request, application_id):
        self.context[canceled_redirect_url_key] = url_list + f"/{application_id}"
        
        form = CreateNewApplicationHistoryForm(request.GET)
        self.context['form'] = form

        application = Application.objects.get(user=request.user, id=application_id)
        self.context['application'] = application

        application_status = ApplicationStatus.objects.filter(user=request.user).order_by("name")
        self.context['application_status'] = application_status
        return render(request, self.template, self.context)

    def post(self, request, application_id):
        history_path = self.path + f"/{application_id}/history"
        detail_path = self.path + f"/{application_id}"
        
        form = CreateNewApplicationHistoryForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            application = Application.objects.get(id=application_id)
            post.application = application
            try:
                with transaction.atomic():
                    post.save()

                    # get last history
                    history = ApplicationHistory.objects.filter(application_id=application_id).order_by("-update_status_at", "-created_at")[0]

                    application.last_status = history.status
                    application.last_updated = history.update_status_at
                    application.save()
            except DatabaseError as e:
                msg = ValidationError(e).messages[0]
                messages.error(request, msg)
                return HttpResponseRedirect(history_path)

            except:
                messages.error(request, "Error server")
                return HttpResponseRedirect(history_path)

            return HttpResponseRedirect(detail_path)
        else:
            self.context['form'] = form
            messages.error(request, getErrorMessageFromForm(form))
            return HttpResponseRedirect(history_path)
