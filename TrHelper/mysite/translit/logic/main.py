# from .translit import IntegralTerm, Translit



#
# def translit_loop(raw, user_dict):
#     '''
#         user_dict should be django model instanse
#         with three fields: kurd, ru, info
#     '''
#
#     res = Translit(raw)
#     res()


    # result = []
    # info_lst = []
    # rus_term = []
    # raw = raw.split(', ')
    # #in worth case raw is list of integral names
    # for name in raw:
    #     if is_integral(name):
    #         integral_term = IntegralTerm(name)
    #         prepared_lst = integral_term.save_format_and_prepare()
    #         for term in prepared_lst:
    #             res = translit(term, user_dict)
    #             rus, *info = res,
    #             info_lst.append(str(info))
    #             rus_term.append(rus)
    #
    #         rus_term = integral_term.reconstruct_format(rus_term)
    #
    #         result.append(''.join(rus_term))
    #
    #     else:
    #         res = translit(name, user_dict)
    #         rus, *info = res,
    #         if not info:
    #             i = None
    #         else:
    #             info_lst.append(str(info))
    #         result.append(rus)
    #     print(result, info_lst)
    #
    #     r = ', '.join(result)
    #
    #
    #
    # return r, i
