from django.urls import path, include

from maintenance_helper.machines.views import MachinesListView, MachineCreateView, MachineEditView, MachineDetailsView, \
    MachineDeleteView

urlpatterns = (
    path('', MachinesListView.as_view(), name='machines'),
    path('create/', MachineCreateView.as_view(), name='machine create'),
    path('<int:pk>/', include([
        path('edit/', MachineEditView.as_view(), name='machine edit'),
        path('details/', MachineDetailsView.as_view(), name='machine details'),
        path('delete/', MachineDeleteView.as_view(), name='machine delete'),
    ])),

)
