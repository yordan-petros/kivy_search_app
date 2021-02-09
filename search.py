import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Search(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        if os.path.isfile("previous_search.txt"):
            with open("previous_search.txt", 'r') as file:
                data = file.read().split(", ")
                prev_search = data[0]
                prev_extension = data[1]
                prev_path = data[2]
        else:
            prev_search = ''
            prev_extension = ''
            prev_path = ''

        self.add_widget(Label(text="Search for: "))
        self.search = TextInput(text=prev_search, multiline=True)
        self.add_widget(self.search)

        self.add_widget(Label(text="Extension of file: "))
        self.extension = TextInput(text=prev_extension, multiline=False)
        self.add_widget(self.extension)

        self.add_widget(Label(text="Search path: "))
        self.path = TextInput(text=f"{prev_path}", multiline=True)
        self.add_widget(self.path)

        self.add_widget(Label(text="Files found: "))
        self.files_found = TextInput(multiline=True)
        self.add_widget(self.files_found)

        self.btn1 = Button(text="Search")
        self.btn1.bind(on_press=self.search_func)
        self.add_widget(Label())
        self.add_widget(self.btn1)

    def search_func(self, word):
        word = self.search.text
        extension = self.extension.text
        path = self.path.text
        files_dir = [x for x in os.listdir(path) if x.endswith(extension)]

        with open("previous_search.txt", 'w') as file:
            file.write(f"{word}, {extension}, {path}")

        list_of_files = []
        files_string = ''

        for item in files_dir:
            with open(path + '/' + item, 'r') as file:
                for line in file:
                    if word in line and item not in list_of_files:
                        list_of_files.append(item)

        print(list_of_files)
        for i in list_of_files:
            files_string += i
            files_string += '\n'

        if len(list_of_files) > 0:
            self.files_found.text = files_string
        else:
            self.files_found.text = "Nothing found!"


class NewApp(App):
    def build(self):
        return Search()


if __name__ == '__main__':
    NewApp().run()



