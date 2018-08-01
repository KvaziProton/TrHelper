import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Article, User, CloudAccount
from .tasks import check_user_add
from .toolbox import NewArticle
from .forms import UserAddForm, CloudAccountAddForm

from docx import Document
from io import BytesIO



class LogoutView(View):
    template_name = 'account/logout.html'

    def get(self, request, format=None):
        logout(request)
        return render(request, self.template_name)


class CreateUser(LoginRequiredMixin, CreateView):
    template_name = 'account/add_user.html'
    model = User
    form_class = UserAddForm
    success_url = 'main/user_list'

    def form_valid(self, form):
        form.save()


class UserList(ListView):
    model = User
    template_name = 'account/user_list.html'


class ArticleFlow(LoginRequiredMixin, View):
    template_name = 'main/article_flow.html'

    def get(self, request):
        queryset = Article.objects.order_by('-published')[:20]
        return render(request, self.template_name,
            {'articles': queryset,
            'date_today': datetime.date.today()
            })

    def post(self, request):
        querydict = self.request.POST
        user = self.request.user

        if 'user-add' in querydict:
            url = querydict['input-url'].strip()
            if 'anf' in url:
            # try:
            #     #get from bd
            # except:

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

        if 'take' in querydict:
            article = Article.objects.get(pk=querydict['article-pk'])

            article.translator = User.objects.get(username=user)
            article.save()
            queryset = Article.objects.order_by('-published')[:20]
            return render(request, self.template_name,
                {
                'articles': queryset,
                'date_today': datetime.date.today()
                })

        if 'parse' in querydict:
            article = Article.objects.get(pk=querydict['article-pk'])
            parsed = NewArticle(url=article.url)
            lines = (parsed.title, parsed.lead, '', parsed.text, '', parsed.url)
            filename = parsed.url.split('/')[-1]
            document = Document()
            for line in lines:
                document.add_paragraph(line)

            file = BytesIO()
            document.save(file)
            length = file.tell()
            file.seek(0)
            response = HttpResponse(
                file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
            response['Content-Disposition'] = 'attachment; filename={}.docx'.format(filename)
            response['Content-Length'] = length
            return response

        if 'load' in querydict:
            article = Article.objects.get(pk=querydict['article-pk'])
            article.loaded = True
            article.save()
            # statistic = TranslationStatistic(
            #     user=User.objects.get(user=user),
            #     article=article,
            #     symbols_ammount
            # )
            print('loaded')
            queryset = Article.objects.order_by('-published')[:20]
            return render(request, self.template_name,
                {
                'articles': queryset,
                'date_today': datetime.date.today()
                })

        if 'sure' in querydict:
            similar_url
            url
            #write_bd
