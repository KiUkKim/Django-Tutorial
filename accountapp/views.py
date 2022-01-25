from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render


# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.forms import AccountUpdateForm
from accountapp.models import HelloWorld


def hello_world(request):
    #  로그인 인증이 되었을 경우, hello_world의 웹으로 요청
    if request.user.is_authenticated:
        if request.method == "POST":

            temp = request.POST.get('hello_world_input')

            new_hello_world = HelloWorld()
            new_hello_world.text = temp
            new_hello_world.save()

            return HttpResponseRedirect(reverse('accountapp:hello_world'))

        else:
            hello_world_list = HelloWorld.objects.all()
            return render(request, 'accountapp/hello_world.html', context={'hello_world_list': hello_world_list})

    #  로그인 인증이 되지 않았을 경우, login 웹으로 이동
    else:
        return HttpResponseRedirect(reverse('accountapp:login'))

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

    def get(self, *args, **kwargs): # 이 함수를 통해서 get내부의 행동을 지정해줄 수 있다.
        # 객체의 번호를 알면 누구나 수정이 가능하기 때문에, 이를 방지하기 위해서 현재 객체와 요청된 user가 같은지 확인해주어한다.
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, *args, **kwargs): # 이 함수를 통해서 post내부의 행동을 지정해줄 수 있다.
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()



class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'

    def get(self, *args, **kwargs): # 이 함수를 통해서 get내부의 행동을 지정해줄 수 있다.
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()

    def post(self, *args, **kwargs): # 이 함수를 통해서 post내부의 행동을 지정해줄 수 있다.
        if self.request.user.is_authenticated and self.get_object() == self.request.user:
            return super().get(*args, **kwargs)
        else:
            return HttpResponseForbidden()

