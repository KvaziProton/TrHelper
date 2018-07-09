from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Article
# from .serializers import ArticleAddSer
from rest_framework.renderers import TemplateHTMLRenderer
from .tasks import articles_queue, check_if_new

class ArticleFlow(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/article_flow.html'

    def get(self, request, format=None):

        if 'ajax-ask' in request.data:
            json = {}
            #articles_queue is mutable object, so it should renew itself dinamicly
            for i in range(len(articles_queue)):
                data = articles_queue.pop
                json[i] = data.__dict__
            content = JSONRenderer().render(json)
            return Response(content)
        #if we wanna show article flow

#draft for handle buttom click
        if 'ajax-send' in request.data:
            translator = request.data['user_id']
            pk = request.data['article_id']
            a = Article.objects.get(pk=pk)
            a.translator = translator

            return Response(status=status.HTTP_201_CREATED)

#draft for main flow
        else:
            check_if_new()
            queryset = Article.objects.order_by('-published')[:20] #last 20! not all)
            return Response({'articles': queryset})

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
