# A Web Scraper that can scrap our desired stuffs from Webpages
# ---------------------------------------------------------------------
import os
import sys
import requests
from bs4 import BeautifulSoup

# Some Conditional Imports
is_github_url = True if sys.argv[1].find('github') != -1 else False
if is_github_url:
    import github

class Scraper:
    ''' Main Wrapper for the entire Scraper Stuff '''

    def __init__(self, url):# {{{
        self.url = url if url[-1] == '/' else url + '/'
        self.ft_type = self.set_file_type()
        self.kwlist = []
        self.keywords_handler()

        print('\t\t\t\t Connecting to the Internet')
        if is_github_url:
            self.github = github.Github(self.url, self.ft_type, self.kwlist)
            self.down_dict = self.github.retrieve_urls()
        else:
            self.down_dict = {}
            self.gathering_links()
        try:
            self.user_choice_menu()
        except KeyboardInterrupt:
            exit(1)# }}}

    def set_file_type(self):# {{{
        ''' Method determines which filetype user is looking for '''

        print('\t\tChoose from the following:')
        print('\t\t\t1. Video Files [mkv, mp4, webm]')
        print('\t\t\t2. Compressed Files [rar, zip]')
        print('\t\t\t3. Audio Files [flac, mp3, m4a]')
        print('\t\t\t4. Documents [ pdf, epub, chm]')
        print('\t\t\t5. Custom File Type ')

        ft_dict = {
                1: ('mkv', 'mp4', 'webm', 'mkv\n', 'mp4\n', 'webm\n'),
                2: ('rar', 'rar\n','zip', 'zip\n'),
                3: ('flac', 'mp3', 'm4a', 'flac\n', 'mp3\n', 'm4a\n'),
                4: ('pdf', 'pdf\n', 'epub', 'chm')
                }
        try:
            type_choice = int(input('\t\t\t\tEnter Your Choice: '))
        except ValueError:
            print('\t\tEnter a correct choice idiot')
            file_type_menu()

        try:
            return ft_dict[type_choice]
        except KeyError:
            if type_choice == 5:
                print('\n\t\tEnter Filetypes you want below [ e.g.: pdf, docx, mkv]: ')
                file_type = sys.stdin.readline()[:-1]
                file_type = file_type.split(',')
                temp_list = []
                for item in file_type:
                    if item[0] == ' ':
                        item = item[1:]
                    if item[-1] == ' ':
                        item = item[:-1]
                    temp_list.append(item)
                return tuple(temp_list)
            else:
                print('Enter a correct choice idiot')
                file_type_menu()# }}}

    def keywords_handler(self):# {{{
        ''' Manages keywords to narrow down the search results
            Creates a new attribute:
                kwlist : A list of all keywords
        '''
        check = input('Do You want to specify any external keywords (to narrow down search) ? (y/n) : ')
        if check == 'y' or check == 'Y':
            print('Enter keywords to look for : ')
            kwords = sys.stdin.readline()[:-1]
            kwords = kwords.split(',')
            for item in kwords:
                self.kwlist.append(item.replace(' ', ''))
        return# }}}

    def gathering_links(self):# {{{
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Taking out all the anchor tags
        # links = [ x.get('href') for x in soup.find_all('a') if x.get('href') is not None ]
        links = []
        for element in soup.find_all('a'):
            link = element.get('href')
            if link is not None:
                if link[-1] == '\n':
                    link = link[:-1]
                if link[0] == '/':
                    link = link[1:]
                links.append(link)

        count = 0
        for link in links:
            if link.endswith(self.ft_type):
                if len(self.kwlist) == 0:
                    if link not in self.down_dict.values():
                        self.down_dict[count] = link
                        count += 1
                else:
                    for item in self.kwlist:
                        if link.find(item) != -1:
                            self.down_dict[count] = link
                            count += 1
                            break# }}}

    def user_choice_menu(self):# {{{
        '''
        Presents the user with
            [choice_no]: [File_name to downlaod]
        '''
        for key in self.down_dict:
            print("\t\t[{0:>2}]: {1}".format(key, self.down_dict[key].rsplit('/', maxsplit=1)[-1] ))

        choice = int(input('Enter your choice [Bulk Download : -1]: '))
        if choice == -1:
            down_cri  = int(input('\t\t[Download_all: -1]'
                                + '\t[Selective Download: -2]'
                                + '\t[Selective Removal: -3]'
                                + '\n\t\tYour Choice: '))

            if down_cri == -1:
                choice_list = [ x for x in self.down_dict ]

            elif down_cri == -2:
                print('Enter your choices [ e.g. 1,2, 3, 4, 5, 6, 67, 7 ]: ')
                choices = sys.stdin.readline()[:-1]
                choices = choices.split(',')
                choice_list = [ int(x) for x in choices ]

            elif down_cri == -3:
                print("Enter your choice for Removal [e.g. 1, 2, 3 ]: ")
                removal_choices = sys.stdin.readline()[:-1]
                removal_choices = removal_choices.split(',')
                removal_choices = [ int(x) for x in removal_choices ]
                # Modifying the Choices List
                choice_list = [ x for x in self.down_dict if x not in removal_choices ]

            else:
                print('\n\tYou entered an invalid option, Please Try Again')
                self.user_choice_menu()

            for item in choice_list:
                self.downloader(item)
        else:
            self.downloader(choice)# }}}

    def downloader(self, user_choice):
        print('To Download: {0:>2} ==> "{1}"'.format(user_choice, self.down_dict[user_choice]))
       #file_name = input('Enter the FileName: ')
        file_name = self.down_dict[user_choice].split('/')[-1].split('?')[-1].split('=')[-1]
        print("FileName :- ", file_name)
        if self.down_dict[user_choice].startswith(('http', 'https')):
            os.system('axel -n 10 "{}" -o "{}"'.format(self.down_dict[user_choice], file_name))
        else:
            os.system('axel -n 10 "{}" -o "{}"'.format(self.url + self.down_dict[user_choice], file_name))
        # os.system('axel -n 10 "{}" -o {}'.format(self.url + self.down_dict[user_choice].rsplit('/', maxsplit=3)[-1], file_name))

if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        url = input('Enter the url to scrap: ')
    scraper = Scraper(url)
