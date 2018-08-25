import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, HttpResponseNotModified
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.decorators.http import condition

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, User, CloudAccount, TranslationStatistic, ArticleCase
from .tasks import check_user_add
from .toolbox import NewArticle, PyMailCloud, count_ammount_in_loaded, parse
from .forms import UserAddForm, CloudAccountAddForm, EmbedArticleForm
from .serializers import ArticleSerializer


class ButtonActions(LoginRequiredMixin, APIView):
    '''Test view to try handle buttons clicks with ajax '''

    template_name = 'main/ajax_article_button.html'

    def get(self, request):
        querydict = self.request.GET
        user = self.request.user
        pk = querydict.get('article_pk', None)

        if 'take' in querydict:
            print('in take!!')
            article = Article.objects.get(pk=pk)
            article.translator = User.objects.get(username=user)
            article.save()
            data =  {
                'article': article,
                }
            content = render(request, self.template_name, data).content
            response = Response({'content': content})
            return response


# def latest_changed(request):
#     return Article.objects.latest('published').last_change
#
# @condition(last_modified_func=latest_changed)
@api_view(['GET',])
def flow_refresh(request):
    '''Handle refreshing the main page if model Article was changed (or return
     HttpResponseNotModified) and generate data for notification in case of
     new article appearence'''

    last_change = str(Article.objects.latest('last_change').last_change)
    request_cookie = request.COOKIES.get('last_change')

    if request_cookie != last_change:
        queryset = ArticleCase.objects.order_by('-published')[:20]
        cases = [Article.objects.filter(case=case) for case in queryset]
        data = {'cases': cases}
        content = render(request, 'main/ajax_refresh_flow.html', data).content
        response = Response({'content': content})

        response.set_cookie('last_change', last_change)

        user_last_pk = request.COOKIES.get('last_pk')
        last = Article.objects.latest('pk')
        last_pk = str(last.pk)

        if user_last_pk != last_pk:
            response.delete_cookie('last_pk')
            response.set_cookie('last_pk', last_pk)
            response.data['new'] = ArticleSerializer(last).data

        return response

    response = Response(status=status.HTTP_304_NOT_MODIFIED)
    response.set_cookie('last_change', last_change)
    return response


class ArticleFlow(LoginRequiredMixin, View):
    '''Retrive articles from bd and handle buttoms clicks'''

    template_name = 'main/article_flow.html'
    form_class = EmbedArticleForm

    def get(self, request):
        '''Create article flow data for first user request for main paige'''

        print('in main flow')
        queryset = ArticleCase.objects.order_by('-published')[:20]
        cases = [Article.objects.filter(case=case) for case in queryset]
        last_pk = Article.objects.latest('pk').pk
        data = {
            'cases': cases,
            'date_today': datetime.date.today()
            }

        response = render(request, self.template_name, data)
        print(last_pk)
        response.set_cookie('last_pk', last_pk)
        last_change = Article.objects.latest('last_change').last_change
        response.set_cookie('last_change', last_change)
        return response

    def post(self, request):
        print('in post')
        querydict = self.request.POST
        print(querydict)
        user = self.request.user

        if 'user-add' in querydict:
            '''Handle attempts to add article from user'''

            if form.is_valid(self, form):
                url = form.cleaned_data(['url'])

                similar_url = check_user_add.delay(url).get()
                if similar_url:
                    query = Article.objects.get(url=similar_url)
                    return render(request, self.template_name,
                        {'url' : url,
                        'similar' : query
                        })

                else:
                    query = Article.objects.get(url=url)
                    message = 'За последние 24 часа такой нет. Успешно добавлено!'
                    return render(request, self.template_name,
                        {
                            'message' : message,
                            'url' : query
                    })
            message = 'unvalid url'
            return render(request, self.template_name,
                {'message' : message})


cloud_auth_dict ={}

class HandleFiles(LoginRequiredMixin, View):
    template_name = 'main/article_flow.html'

    def post(self, request):
        querydict = self.request.POST
        user = self.request.user

        if 'download' in querydict:
            '''Retrive text from article html and load it to user's computer'''

            print('in usuall parse')
            pk=querydict.get('download')
            article = Article.objects.get(pk=pk)
            response = parse(url=article.url)

            return response

        if 'load' in querydict:
            '''Load translation in .docx format to user's cloud account,
            write statistic (symbols' amount), mark article as loaded'''


            pk = querydict.get('article_pk', None)
            user = User.objects.get(username=user)

            if user.username in cloud_auth_dict:
                cloud_user, folder_name = cloud_auth_dict[user.username]
            else:
                cloud_account = CloudAccount.objects.get(user=user)
                folder_name = cloud_account.folder_name
                cloud_user = PyMailCloud(
                                        cloud_account.email,
                                        cloud_account.password
                                        )
                cloud_auth_dict[user.username] = cloud_user, folder_name


            f = self.request.FILES['file']
            file_name = f.name
            file = f.file

            res = cloud_user.upload_files(file, file_name, folder_name)

            if '200' in res:
                article = Article.objects.get(pk=querydict.get('load'))
                article.loaded = True
                article.save()

                symbols_ammount = count_ammount_in_loaded(loaded_file=f)

                statistic = TranslationStatistic(
                    translator=user,
                    article=article,
                    symbols_ammount = symbols_ammount,
                )
            queryset = Article.objects.order_by('-published')[:20]
            data = {
                'articles': queryset,
                'date_today': datetime.date.today()
                }
            return render(request, self.template_name, data)
            # data = {
            #     'file_name': 'expample.txt',
            #     'symbols_amount': 563
            # }
            #
            # return JsonResponse(data)

class LogoutView(View):
    '''Simple view to log out users'''
    template_name = 'account/logout.html'

    def get(self, request, format=None):
        logout(request)
        return render(request, self.template_name)


class CreateUser(LoginRequiredMixin, CreateView):
    '''View to create account for new translator'''

    template_name = 'account/add_user.html'
    model = User
    form_class = UserAddForm
    success_url = 'main/user_list'

    def form_valid(self, form):
        form.save()


class UserList(ListView):
    model = User
    template_name = 'account/user_list.html'
