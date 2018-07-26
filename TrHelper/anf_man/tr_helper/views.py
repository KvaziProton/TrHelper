from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .models import Article, Translator
from rest_framework.renderers import TemplateHTMLRenderer
import datetime
from .tasks import check_user_add
from django.http import HttpResponse
from docx import Document
from io import BytesIO
from .toolbox import NewArticle
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.views.generic import CreateView

# from .forms import TranslatorSignUpForm, EditorSignUpForm

# from django.contrib.auth import authenticate, login

# def my_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('main/')
#
#     else:
#         pass
#
# class TranslatorAuthen(CreateView):
#     model = User
#     form_class = TranslatorSignUpForm
#     template_name = 'registration/login.html'
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('main/')
from django.contrib.auth import logout

class LogoutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/logout.html'

    def get(self, request, format=None):
        logout(request)
        return Response()



class ArticleFlow(LoginRequiredMixin, APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/article_flow.html'

    def get(self, request, format=None):
        print(request.data)
        print(self.request.user)
        if 'ajax-ask' in request.data:
            json = {}
            #articles_queue is mutable object, so it should renew itself dinamicly
            for i in range(len(articles_queue)):
                data = articles_queue.pop
                json[i] = data.__dict__
            content = JSONRenderer().render(json)
            return Response(content)

#draft for handle buttom click
        if 'take' in request.data:
            print('in take')
            translator = request.data['user_id']
            pk = request.data['article_id']
            a = Article.objects.get(pk=pk)
            a.translator = translator

            return Response(status=status.HTTP_201_CREATED)

#draft for main flow
        else:
            queryset = Article.objects.order_by('-published')[:20]
            return Response({
                'articles': queryset,
                'date_today': datetime.date.today()
                })

    def post(self, request, format=None):
        # serializer = ArticleAddSer(data=request.data)
        # if serializer.is_valid():
        print(request.data)
        print(self.request.user)
        if 'user-add' in request.data:
            print('I am in post')
            url = request.data['input-url'].strip()
            # try:
            #     #get from bd
            # except:

            similar_url = check_user_add.delay(url).get()
            if similar_url:
                query = Article.objects.get(url=similar_url)
                return Response({
                        'url' : url,
                        'similar' : query
                        })
            else:
                query = Article.objects.get(url=url)
                message = 'За последние 24 часа такой нет. Успешно добавлено!'
                return Response({
                        'message' : message,
                        'url' : query
                })

        if 'take' in request.data:
            article = Article.objects.get(pk=request.data['article-pk'])
            user = self.request.user
            print(user)
            article.translator = Translator.objects.get(user=user )
            article.save()
            queryset = Article.objects.order_by('-published')[:20]
            return Response({
                'articles': queryset,
                'date_today': datetime.date.today()
                })

        if 'parse' in request.data:
            print('parsed')
            article = Article.objects.get(pk=request.data['article-pk'])
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

            # queryset = Article.objects.order_by('-published')[:20]
            # return Response({
            #     'articles': queryset,
            #     'date_today': datetime.date.today()
            #     })

        if 'load' in request.data:
            article = Article.objects.get(pk=request.data['article-pk'])
            article.loaded = True
            article.save()
            # user = self.request.user
            # statistic = TranslationStatistic(
            #     translator=Translator.objects.get(user=user),
            #     article=article,
            #     symbols_ammount
            # )
            print('loaded')
            queryset = Article.objects.order_by('-published')[:20]
            return Response({
                'articles': queryset,
                'date_today': datetime.date.today()
                })








        if 'sure' in request.data:
            similar_url
            url
            #write_bd

              # -- добавить обработку для разных сценариев (нашел-не нашел похожие)
                     # -- использовать класс для автозаполнения в сериалайзере или без него?
        return Response(status=status.HTTP_201_CREATED)

    #     #if we wanna manually add article
    # def post(self, request, format=None):
    #     # data = JSONParser().parse(request) #parse json to python
    #     # data[title] = get_title_from_url #or get by js
    #     # data[symbols_ammount] = get_symbols
    #
    #     serializer = ArticleAddSer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
