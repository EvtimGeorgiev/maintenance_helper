from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from maintenance_helper.core import mixins as cust_mixins
from maintenance_helper.machines.models import Machine

UserModel = get_user_model()


class MachinesListView(views.ListView):
    context_object_name = 'machines_list'
    model = Machine
    template_name = 'machines/machines_list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['user'] = UserModel
    #     print(context)
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.__get_pattern()
        if pattern:
            queryset = queryset.filter(name__icontains=pattern)
            self.extra_context = {'pattern': pattern}

        queryset = queryset.order_by('name')

        return queryset

    def __get_pattern(self):
        pattern = self.request.GET.get('pattern')
        return pattern if pattern else None


class MachineCreateView(LoginRequiredMixin, cust_mixins.MaintenanceOnlyAccessMixin, views.CreateView):
    template_name = 'machines/machine-create.html'
    model = Machine
    fields = '__all__'

    # success_url = reverse_lazy('index')  # static redirect url

    # dynamic redirection
    def get_success_url(self):
        return reverse('machine details', kwargs={
            'pk': self.object.pk,
        })


class MachineDetailsView(views.DetailView):
    model = Machine
    template_name = 'machines/machine-details.html'


# def machine_edit(request, pk):
#     machine = Machine.objects.filter(pk=pk).get()
#
#     if request.method == 'GET':
#         form = MachineEditForm(instance=machine)
#     else:
#         form = MachineEditForm(request.POST, instance=machine)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#     context = {
#         'form': form,
#         'machine': machine,
#     }
#
#     return render(request, 'machines/machine-edit.html', context)


class MachineEditView(LoginRequiredMixin, cust_mixins.MaintenanceOnlyAccessMixin, views.UpdateView):
    model = Machine
    # form_class = MachineEditForm
    template_name = 'machines/machine-edit.html'
    fields = ('name', 'type', 'image', 'detailed_info')

    def get_success_url(self):
        return reverse_lazy('machine details', kwargs={
            'pk': self.object.pk,
        })


class MachineDeleteView(LoginRequiredMixin, cust_mixins.ManagerOnlyAccessMixin, views.DeleteView):
    fields = '__all__'
    model = Machine
    template_name = 'machines/machine-delete.html'
    success_url = reverse_lazy('machines')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except models.RestrictedError:
            error_message = f'Cannot delete {self.object.name} because it has assigned issues'
            return HttpResponse(error_message)
    # render the template with your message in the context
    # or you can use the messages framework to send the message

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     try:
    #         self.object.delete()
    #         return HttpResponseRedirect(success_url)
    #     except models.RestrictedError:
    #         return HttpResponse('!!! Machine has assigned issues and cannot be deleted !!!')
