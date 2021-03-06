from handler import LinkHandler, AnfLinkHandler
import argparse

LinkHandler.add_handler('anfenglish.com', AnfLinkHandler)

def loop(count=False):
    print('Welcome to web-page handler for translators. Lets start!')
    while 1:
        try:
            url = input('\nPaste the link:\t')
            i = url.strip('htps:/w.').split('/')[0]
            handler = LinkHandler.handlers_dict[i]
            article = handler(url)
            article.write_docx()
            if count:
                number = article.count_simbols()
                print('\n\tInfo:', number, 'symbols in article')
        except (KeyError, NameError):
                print(
                '''Sorry, we cant handle this link, try with other one.
                This parser works only with links from:'''
                )
                for key in sorted(LinkHandler.handlers_dict.keys()):
                    print('-- {}\n'.format(key))

        except KeyboardInterrupt:
            print('\nParser is closed.')
            break

def argparser():
    parser = argparse.ArgumentParser(
        description='''
        This is the handler to help translators
        to organize the work and form docx files from
        different news' web-pages'''
        )
    parser.add_argument(
        '-c', '--count',
        help='count amount of symbols with spases in the article',
        action='store_true'
        )
    args = parser.parse_args()
    return args.count

if __name__ == '__main__':
    loop(count=True) if argparser() else loop()
