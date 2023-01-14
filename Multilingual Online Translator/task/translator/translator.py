import sys
import requests
from bs4 import BeautifulSoup


class MultilingualOnlineTranslator:
    """
    This class is used to translate words from one language to another.
    """
    def __init__(self):
        self.__languages = [
            'Arabic', 'German', 'English', 'Spanish',
            'French', 'Hebrew', 'Japanese', 'Dutch',
            'Polish', 'Portuguese', 'Romanian', 'Russian',
            'Turkish'
        ]
        self.translated_words = self.translated_examples = ""
        self.__headers = {'User-Agent': 'Mozilla/5.0'}
        self.__input_lang = sys.argv[1]
        self.__output_lang = sys.argv[2]
        self.__text_lang = sys.argv[3]

    def welcome_message(self):
        print('Hello, welcome to the translator. Translator supports:')
        for i, language in enumerate(self.__languages, start=1):
            print(f'{i}. {language}')

    # def get_input_language(self):
    #     print("Type the number of your language:")
    #     var = input()
    #     return self.get_input(var)
    #
    # def get_output_language(self):
    #     print("Type the number of a language you want to translate to or '0' to translate to all languages::")
    #     var = input()
    #     if int(var) == 0:
    #         self.translate_to_all()
    #         return
    #     return self.get_input(var)

    def translate_to_all(self):
        # self.__text_lang = input('Type the word you want to translate:\n')
        # print()
        for index in range(len(self.__languages)):
            self.__output_lang = self.__languages[index].lower()
            if self.__output_lang == self.__input_lang:
                continue
            soup = self.get_web_content()
            if soup:
                self.translated_words, self.translated_examples = self.get_translation(soup)
            else:
                print("Please try again!")
            print(f"{self.__output_lang} Translations:")
            print(self.translated_words[0])
            print()
            print(f"{self.__output_lang} Examples:")
            print(self.translated_examples[0], self.translated_examples[1], sep="\n")
            print()
            line_1 = [
                f"{self.__output_lang} Translations:",
                self.translated_words[0]
            ]
            line_2 = [
                f"{self.__output_lang} Examples:",
                self.translated_examples[0],
                self.translated_examples[1]
            ]
            with open(f"{self.__text_lang}.txt", 'a') as f:
                f.writelines(line + "\n" for line in line_1)
                f.write("\n")
                f.writelines(line + "\n" for line in line_2)
                f.write("\n")
        sys.exit()

    # def get_input(self, var):
    #     while True:
    #         try:
    #             ret_val = int(var)
    #         except ValueError:
    #             print(f"Invalid input, Input must be an integer value (0 - {len(self.__languages)})")
    #         else:
    #             if ret_val in range(len(self.__languages)):
    #                 return self.__languages[ret_val - 1].lower()
    #             else:
    #                 print(f"Incorrect input, number must be in range [0, {len(self.__languages)}]")
    #                 var = input()

    def get_web_content(self):
        url_core = "https://context.reverso.net/translation"
        lang = f"{self.__input_lang}-{self.__output_lang}"
        url = f"{url_core}/{lang}/{self.__text_lang}"
        page = requests.get(url, headers=self.__headers)

        if page.ok:
            return BeautifulSoup(page.text, 'html.parser')
        elif page.status_code == 404:
            print(f"Sorry, unable to find {self.__text_lang}")
            sys.exit()
        else:
            # print(page.status_code, page.reason)
            print("Something wrong with your internet connection")
            sys.exit()

    @staticmethod
    def get_translation(soup):
        trans_array = [element.text.strip() for element in
                       soup.find('div', id='translations-content').find_all('span', class_='display-term')]
        example_array = [element.text.strip() for element in
                         soup.find('section', id="examples-content").find_all('span', class_="text")]
        if len(trans_array):
            return trans_array, example_array
        else:
            print("No translations found!")

    def output_translation(self, translations, examples):
        print(f"{self.__output_lang} Translations:")
        with open(f"{self.__text_lang}.txt", 'w') as f:
            f.write(f"{self.__output_lang} Translations:" + '\n')
            for i in range(5):
                if translations[i]:
                    print(translations[i])
                    f.write(translations[i] + '\n')
            f.write("\n")

        print()
        print(f"{self.__output_lang} Examples:")
        with open(f"{self.__text_lang}.txt", 'a') as f:
            f.write(f"{self.__output_lang} Examples:" + '\n')
            for i in range(10):
                if examples[i]:
                    print(examples[i])
                    print() if i % 2 and i < 9 else ""
                    f.write(examples[i] + '\n')
                    f.write("\n" if i % 2 and i < 9 else "")

    def main(self):
        # self.welcome_message()
        # self.__input_lang = self.get_input_language()
        # self.__output_lang = self.get_output_language()
        # self.__text_lang = input('Type the word you want to translate:\n')
        # print()
        if self.__output_lang.capitalize() not in self.__languages and self.__output_lang != "all":
            print(f"Sorry, the program doesn't support {self.__output_lang}")
            sys.exit()
        if self.__input_lang.capitalize() not in self.__languages and self.__input_lang != "all":
            print(f"Sorry, the program doesn't support {self.__input_lang}")
            sys.exit()
        if self.__output_lang == 'all':
            self.translate_to_all()
        soup = self.get_web_content()
        if soup:
            self.translated_words, self.translated_examples = self.get_translation(soup)
        else:
            print("Please try again!")

        self.output_translation(self.translated_words, self.translated_examples)


if __name__ == '__main__':
    MultilingualOnlineTranslator().main()
