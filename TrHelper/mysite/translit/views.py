from django.shortcuts import render
from .forms import InputForm, AddForm
from .models import UserDict
from django.http import HttpResponseRedirect
from .logic.tr_new import RawTranslit

def show_dict(request):
    if request.method == 'POST':
        context = {}
        data = UserDict.objects.all()
        context['data'] = data
        return render(request, 'show_dict.html', context=context )

        if 'back' in request.POST:
            return HttpResponseRedirect('/translit')
        if 'except' in request.POST:
            return HttpResponseRedirect('/add_term')


class TrView():
    def set_ru(request):
        print('I am in set_ru')
        if request.method == 'POST':
            if 'dict' in request.POST:
                return HttpResponseRedirect('/dict')
            if 'except' in request.POST:
                return HttpResponseRedirect('/add_term')


        if request.method == 'GET':
            form = InputForm(request.GET)

            if form.is_valid():
                print('form is valid!!!')

                kurd = form.cleaned_data['kurd_input']

                if 'improve' in request.GET:
                    print('I am in improve')
                    form = AddForm(initial = {'kurd' : kurd})

                    return render(
                        request,
                        'add_term.html',
                        {'message' : None, 'form': form}
                        )
                if 'translit' in request.GET:
                    ru, info = RawTranslit(str(kurd), user_dict=UserDict)()
                    o_form = InputForm(
                        initial={'kurd_input':kurd, 'ru_output':ru, 'info':info}
                        )
                    context = True
                    if not info:
                        return render(request, 'translit.html', {'context':context,'form': o_form})
                    return render(request, 'translit.html', {'context':context,'info':info, 'form': o_form})

        form = InputForm()
        return render(request, 'translit.html', {'form': form})


    # def redirect_to_add_term(request):
    #     print('I am in redirect')
    #     if request.method == 'POST':
    #         print('I am in post')
    #         print(request.POST)
    #         if 'back' in request.POST:
    #             print('I am in post and back')
    #             return HttpResponseRedirect('/translit')
    #         form = AddForm(request.POST)
    #         return render(
    #             request,
    #             'add_term.html',
    #             {'message' : None, 'form' : form}
    #             )


    def add_term(request):
        print('I am in add_term')
        if request.method == 'POST':
            if 'back' in request.POST:
                return HttpResponseRedirect('/translit')

            form = AddForm(request.POST)
            if form.is_valid():
                print('add, valid, form.data')
                kurd = form.cleaned_data['kurd']
                ru = form.cleaned_data['ru']
                info = form.cleaned_data['info']
                record = UserDict(
                    kurd = kurd,
                    ru = ru,
                    info = info
                )
                record.save()
                message = 'Added Sucсesfully! {}--{}'.format(kurd, ru)

            else:
                try:
                    kurd = request.POST['kurd']
                    ru = UserDict.objects.get(kurd=kurd)
                    message = 'Already in the dictionary: {} -- {}\n'.format(kurd, ru)
                    message += 'If you wanna change it - contact with admin'

                except Exception:
                    message = None

            clean_form = AddForm()
            return render(
                    request,
                    'add_term.html',
                    {'message' : message, 'form': clean_form})
