from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleAddSer
from rest_framework.renderers import TemplateHTMLRenderer
from .tasks import articles

class ArticleFlow(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main/article_flow.html'

    def get(self, request, format=None):
        #if we wanna show article flow
        queryset = Article.objects.all()
        # queryset = articles
        # articles = []
        # serializer = ArticleSer(articles, many=True) #будет отдавать много объектов в одном - list of OrderdDict
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
