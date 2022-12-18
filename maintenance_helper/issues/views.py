import datetime

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from maintenance_helper.issues.forms import IssueCreateForm, IssueEditForm
from maintenance_helper.issues.models import Issue


class IssuesListView(views.ListView):
    context_object_name = 'issues_list'
    model = Issue
    template_name = 'issues/issues-list.html'

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
            return redirect('index')

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
            post['closed_on'] = datetime.datetime.today()
            request.POST = post
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('issue details', kwargs={
            'pk': self.object.pk,
        })

    @staticmethod
    def edit_closed_issue_error(request, issue):
        context = {
            'issue': issue,
        }
        return render(request, 'issues/edit-closed-issue-error.html', context)
