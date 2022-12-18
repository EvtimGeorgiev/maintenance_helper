# issues/urls.py

from django.urls import path, include

from maintenance_helper.issues.views import IssuesListView, issue_create, IssueDetailsView, IssueEditView

urlpatterns = (
    path('issues/', include([
        path('', IssuesListView.as_view(), name='issues'),
        path('create/', issue_create, name='issue create'),
        path('<int:pk>/details/', IssueDetailsView.as_view(), name='issue details'),
        path('<int:pk>/edit/', IssueEditView.as_view(), name='issue edit'),
        # path('/issues/edit-closed-issue-error.html/', )
    ])),
)
