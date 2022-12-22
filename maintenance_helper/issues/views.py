import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from maintenance_helper.issues.forms import IssueCreateForm, IssueEditForm
from maintenance_helper.issues.models import Issue
from maintenance_helper.spares.models import SparePart

UserModel = get_user_model()


class IssuesListView(views.ListView):
    context_object_name = 'issues_list'
    model = Issue
    template_name = 'issues/issues_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('pk')


def issue_create(request):
    if request.method == 'GET':
        form = IssueCreateForm()
    else:
        form = IssueCreateForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user.username
            issue.save()
            return redirect('issues')

    context = {
        'form': form,
    }

    return render(request, 'issues/issue-create.html', context)


class IssueDetailsView(views.DetailView):
    model = Issue
    fields = '__all__'
    template_name = 'issues/issue-details.html'


class IssueEditView(views.UpdateView):
    model = Issue
    form_class = IssueEditForm
    template_name = 'issues/issue-edit.html'

    def get(self, request, *args, **kwargs):
        issue = self.get_object()

        if issue.closed_on:
            return self.edit_closed_issue_error(request, issue)
        return super().get(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        if 'close issue' in request.POST:
            post = request.POST.copy()
            issue = self.get_object()
            post['closed_on'] = datetime.datetime.today()
            post['closed_by'] = request.user.username
            request.POST = post
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('issue details', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        issue = self.get_object()
        context = super().get_context_data(**kwargs)
        context['spare_parts'] = SparePart.objects.all()
        context['used_parts'] = SparePart.objects.filter(usedsparepart__issue=issue.pk)
        return context

    @staticmethod
    def edit_closed_issue_error(request, issue):
        context = {
            'issue': issue,
        }
        return render(request, 'issues/edit-closed-issue-error.html', context)
