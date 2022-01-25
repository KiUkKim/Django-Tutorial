from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorator import account_ownership_required
from accountapp.forms import AccountUpdateForm
from accountapp.models import HelloWorld

has_ownership = [account_ownership_required, login_required]


@login_required
def hello_world(request):
    #  로그인 인증이 되었을 경우, hello_world의 웹으로 요청
    if request.method == "POST":

        temp = request.POST.get('hello_world_input')

        new_hello_world = HelloWorld()
        new_hello_world.text = temp
        new_hello_world.save()

        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    else:
        hello_world_list = HelloWorld.objects.all()
        return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})


class AccountCreateView(CreateView):
    # User라는 장고에서 기본적으로 사용하는 model사용
    model = User
    # form 지정
    form_class = UserCreationForm
    # 연결 성공시 이동하는 페이지 지정
    # reverse는 그대로 class에서 사용할 수 없기때문에, class형 view에서는 reverse_lazy
    # reverse는 function형 view에서 사용
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    # User라는 장고에서 기본적으로 사용하는 model사용
    model = User
    # form 지정
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    # 연결 성공시 이동하는 페이지 지정
    # reverse는 그대로 class에서 사용할 수 없기때문에, class형 view에서는 reverse_lazy
    # reverse는 function형 view에서 사용
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'
