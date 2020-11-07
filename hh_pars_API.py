class Lab12():

    def __init__(self, text_zapros, list_of_skills):
        self.url_hh = 'https://api.hh.ru/vacancies'
        self.text_zapros = text_zapros
        self.cursi = Lab12.cursi_val()
        self.params = {'text': self.text_zapros}
        self.number_pages = Lab12.get_num_pages(self)
        self.salary = []
        self.list_of_skills = list_of_skills

    # иногда ЗП дают в валюте, что бы привести все к рублю, получаем курсы валют
    # и делаем перерасчет
    def cursi_val():
        import requests
        url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        response = requests.get(url)
        return response.json()['Valute']

    def get_num_pages(self):
        import requests
        return requests.get(self.url_hh, params=self.params).json()['pages']

    # Собирает требования и оплату в список
    def harvest_vac(self):
        import requests
        list_requirements = []
        salary = []
        for p in range(self.number_pages):
            self.params.update({'page': p})
            page = requests.get(self.url_hh, params=self.params).json()
            for i in range(len(page['items'])):
                list_requirements.append(page['items'][i]['snippet']['requirement'])
                if page['items'][i]['salary'] is not None:
                    salary.append(page['items'][i]['salary'])
        return {'list_requirements': list_requirements, 'salary': salary}

    def calculate_mid_salary_list(self):
        list_mid_sal = []
        salary_list = (Lab12.harvest_vac(self))['salary']
        for i in range(len(salary_list)):
            salary = Lab12.calculate_mid(self, salary_list[i])
            if salary < 500000 and salary > 60000:
                list_mid_sal.append(Lab12.calculate_mid(self, salary_list[i]))
        return list_mid_sal


    def calculate_mid(self, dict_r):
        if dict_r['currency'] != 'RUR':
            currency_r = dict_r['currency']
            if currency_r == 'BYR':
                currency_r = 'BYN'
            curs = self.cursi[currency_r]['Value']
            if curs != None:
                if dict_r['from'] is not None and dict_r['to'] is not None:
                    mid_s = int((int(dict_r['from']) * curs + int(dict_r['to']) * curs) / 2)
                else:
                    if dict_r['from'] == None:
                        mid_s = int(int(dict_r['to']) * curs)
                    elif dict_r['to'] == None:
                        mid_s = int(int(dict_r['from']) * curs)
            else:
                print(self.cursi[currency_r])
        else:
            if dict_r['from'] is not None and dict_r['to'] is not None:
                mid_s = (int(dict_r['from']) + int(dict_r['to'])) / 2
            else:
                if dict_r['from'] is None:
                    mid_s = int(dict_r['to'])
                elif dict_r['to'] is None:
                    mid_s = int(dict_r['from'])
        return mid_s

    def collect_all_requirements_to_text(self):
        text = ''
        list_requirements = (Lab12.harvest_vac(self))['list_requirements']
        for i in range(len(list_requirements)):
            if list_requirements[i] is not None:
                text = text + " " + list_requirements[i]
        return text

    def top_skills(self):
        import pymorphy2
        import operator
        import string

        punctuation = string.punctuation
        text = Lab12.collect_all_requirements_to_text(self)
        list_punk = list(punctuation)
        list_punk.append('»')
        list_punk.append('«')
        list_punk.append('—')
        for i in list_punk:
            text = text.replace(i, '')
        #сформировать list со словами (split);
        list_words = text.split()
        morph = pymorphy2.MorphAnalyzer()
        norm_list_word2 = [morph.parse(i)[0].normal_form for i in list_words]
        words = set(norm_list_word2)
        words_dic2 = {}
        for i in self.list_of_skills:
            words_dic2.update({i: norm_list_word2.count(i)})
        small_sort2 = sorted(words_dic2.items(), key=operator.itemgetter(1), reverse=True)
        return small_sort2[:10]




# list_of_skills = ['python', 'sql', 'git', 'linux', 'javascript', 'django', 'hive', 'sas', 'scrum',
#                 'aosp', 'unix', 'ruby', 'php', 'nodejs', 'matlab', 'frontend', 'backend', 'web',
#                 'office', 'qt', 'pyqt', 'java', 'c+', 'c#', 'experience', 'r', 'pandas', 'numpy']
