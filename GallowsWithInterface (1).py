import random
import re
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import messagebox 
#from tkinter import scrolledtext
from PIL import ImageTk, Image
import os
import sys



with open('Gallows.txt',"r") as file:
    words = file.read().split()
#encoding="utf-8-sig"
try:
    with open('Gallows_delete.txt',"r",encoding="utf-8-sig") as file:
        words_delete = file.read().split()  
except: words_delete = []
    
# image_win = plt.imread("image_win.jpg")    
# image_lose = plt.imread("image_lose.jpg")
    
class Gallows:
    def __init__(self,window,words):
        self.window = window
        self.words = words
        self.medium_range = [4,5]
        self.number_of_choice = 9
        self.range_row = 0
        self.range_row_letter = 0
        
        self.btn_reload = Button(self.window, text = 'Новая игра', command = self.reload_game)
        self.btn_reload.grid(column = 4, row = 0)
        
    def start(self):
        self.word = self.choice_word()
        self.word_guess = ['_' for i in self.word]  
        self.word_not_guess = []
        #print('Угадай!', '_ '*len(self.word))
        #print('Количество попыток: ',self.number_of_choice)
        self.lbl_flood1 = Label(self.window, text='Угадай! '+'_ '*len(self.word))  
        self.lbl_flood1.grid(column=0, row=self.range_row) 
        self.range_row += 1
        self.lbl_flood2 = Label(self.window, text='Количество попыток: '+str(self.number_of_choice))  
        self.lbl_flood2.grid(column=0, row=self.range_row) 
        self.range_row += 1
        self.lbl_flood3 = Label(self.window, text='Использованные буквы')  
        self.lbl_flood3.grid(column=2, row=self.range_row_letter) 
        self.range_row_letter += 1
        self.range_row_writing = self.range_row
        self.listbox=Listbox(self.window, bd=0,background="grey94", highlightthickness=0, height=15, width=30)
        self.listbox.grid(row=self.range_row_writing+1, column=0)
        self.listbox_letter=Listbox(self.window, bd=0,background="grey94", highlightthickness=0, height=15, width=10)
        self.listbox_letter.grid(row=self.range_row_writing+1, column=2)
        return self.guess_letters()

    def choice_word(self):
        return random.choice(self.words_topic)

    def guess_letters(self):
        self.txt_letter = Entry(window, width = 30)
        self.txt_letter.grid(column = 0, row = self.range_row_writing)
        self.txt_letter.focus()
        self.btn_letter = Button(self.window, text = 'Вводим букву', command = self.main_func)
        self.btn_letter.grid(column = 1, row = self.range_row_writing)
        self.window.bind('<Return>', lambda event=None: self.btn_letter.invoke()) 
        self.range_row += 1
#         self.a = input('Введите букву: ').lower()
#         return self.main_func()

    def main_func(self):
        self.a = self.txt_letter.get().lower()
        
#         if self.a=='q':
#             return 
        
        if self.a==self.word:
            self.draw_image(image_win)
            self.listbox.insert(END, 'Conglatulations!')
            self.listbox.see(END)
            self.btn_letter['state'] = 'disabled'
            self.txt_letter['state'] = 'disabled'
            return
            #return print('Conglatulations!')
        
        if self.check():
            
            # Вывод буквы
            self.listbox_letter.insert(END, self.a)
            self.listbox_letter.see(END)
            
            for i in range(len(self.word)):
                if self.a==self.word[i]:
                    self.word_guess[i] = self.a
            if self.a not in self.word: 
                self.number_of_choice-=1
                self.draw()
            #print('Количество попыток: ',self.number_of_choice)
            self.listbox.insert(END, 'Количество попыток: '+str(self.number_of_choice))
            self.listbox.see(END)
#             self.lbl_choice = Label(self.window, text='Количество попыток: '+str(self.number_of_choice))  
#             self.lbl_choice.grid(column=0, row=self.range_row) 
#             self.range_row += 1
            if self.number_of_choice==0:
                self.draw_image(image_lose)
                self.listbox.insert(END, 'Проиграл :c')
                self.listbox.see(END)
                self.listbox.insert(END, 'Слово было: '+self.word)
                self.listbox.see(END)
                self.btn_letter['state'] = 'disabled'
                self.txt_letter['state'] = 'disabled'
                return
#                 print('Проиграл :c')
#                 return print('Слово было: ',self.word)  
            self.listbox.insert(END, ' '.join(self.word_guess))
            self.listbox.see(END)
#             print(' '.join(self.word_guess))
            if '_' not in self.word_guess:
                self.draw_image(image_win)
                self.listbox.insert(END, 'Conglatulations!')
                self.listbox.see(END)
                self.btn_letter['state'] = 'disabled'
                self.txt_letter['state'] = 'disabled'
#                 print('Conglatulations!')
                return 
            else: self.guess_letters()
            
    def check(self):
        if self.a in self.word_not_guess:
            # print("Не повторяйся!")
            messagebox.showinfo('Ошибка', 'Не повторяйся!')
            return self.guess_letters()
        elif re.findall('[а-яА-ЯёЁ]',self.a)==[]:
            # print("Некорректный символ, нужна кириллица")
            messagebox.showinfo('Ошибка', 'Некорректный символ, нужна кириллица')
            return self.guess_letters()
        else: 
            self.word_not_guess.append(self.a)
            return True
    
    def draw(self):
        width_canvas = 200
        height_canvas = 200
        self.c = Canvas(self.window, width=width_canvas, height=height_canvas)
        self.c.grid(column=3, row=0)

        X = [[0,0],[0,5],[5,5],[0.5],[5,5],[5,4],[5,6],[5,4],[5,6]]
        Y = [[0,10],[10,10],[10,8],[0.5],[7,5],[6.5,8],[6.5,8],[5,3],[5,3]]
        
        # Перевод в координаты canvas (из xlim и ylim, а также сдвигаем начало координат по y вверх)
        X_canvas = []
        for x in X:
            lst = []
            for x_o in x:
                lst.append(200*(x_o+2)/12)
            X_canvas.append(lst)
        
        Y_canvas = []
        for y in Y:
            lst = []
            for y_o in y:
                lst.append(-(200*(y_o+1)/12)+200)
            Y_canvas.append(lst)
        
        def create_circle(x, y, r, canvasName): #center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1)

        
        for i in range(9-self.number_of_choice):
            if i==3: 
                create_circle(X_canvas[i-1][1], Y_canvas[i-1][1]-(Y_canvas[i-1][1]-Y_canvas[i+1][0])/2, (Y_canvas[i-1][1]-Y_canvas[i+1][0])/2, self.c)
            else:
                self.c.create_line(X_canvas[i][0], Y_canvas[i][0], X_canvas[i][1], Y_canvas[i][1])
#         for i in range(9-self.number_of_choice):
#             if i==3:
#                 theta = np.linspace(0,2*np.pi,100)
#                 circle_x = 5+X[i]*np.cos(theta)
#                 circle_y = 7.5+Y[i]*np.sin(theta)
#                 plt.plot(circle_x,circle_y,color='black')
#             else: plt.plot(X[i],Y[i],color='black')
#         plt.xticks([])
#         plt.yticks([])
#         plt.xlim(-2, 10)
#         plt.ylim(-1, 11)
#         plt.show()
        
    def draw_image(self,image):
        panel = Label(self.window, image = image)
        panel.grid(column=3, row=self.range_row_writing + 1)
#         plt.imshow(image)
#         plt.xticks([])
#         plt.yticks([])
#         plt.show()
        with open('Gallows_delete.txt',"a", encoding="utf-8-sig") as file:
            file.write(f"{self.word}\n")
        
    def choice_topic(self):
        self.all_topics = re.findall(r'"(\w+)"',' '.join(self.words))
        if self.delete_guess_and_empty_topics():
            if self.all_topics == []:
                self.words_topic = self.words
                self.lbl_topic = Label(self.window, text="Сейчас тем нет. Выбраны все доступные слова")  
                self.lbl_topic.grid(column=0, row=self.range_row) 
                self.range_row += 1
                self.choice_level()
            elif len(self.all_topics) == 1:
                #print(f"Выбрана единственная тема {self.all_topics[0]}")
                self.lbl_topic = Label(self.window, text=f"Выбрана единственная тема: {self.all_topics[0]}")  
                self.lbl_topic.grid(column=0, row=self.range_row)
                self.range_row += 1
                self.words_topic = re.findall(f'"{self.all_topics[0]}"([\w\s]+)',' '.join(self.words))[0].split()
                self.choice_level()
            else:
                topics_str = ', '.join(self.all_topics)
                #print(f'Выберите тему из доступных: {topics_str}, все')
                self.lbl_topic = Label(window, text=f'Выберите тему из доступных: {topics_str}, все')  
                self.lbl_topic.grid(column=0, row=self.range_row)
                self.range_row += 1
                self.txt_topic = Entry(window, width = 30)
                self.txt_topic.grid(column = 0, row = self.range_row)
                self.txt_topic.focus()
                self.btn_topic = Button(self.window, text = 'Выбрать тему!', command = self.check_choice_topic)
                self.btn_topic.grid(column = 1, row = self.range_row)
                # Tkinter Button имеет метод invoke() , который вызывает команду button
                self.window.bind('<Return>', lambda event=None: self.btn_topic.invoke()) 
                self.range_row += 1
                self.all_topics.append('все')
                #self.check_choice_topic()
              
    def check_choice_topic(self):
        #self.topic = input().lower()
        self.topic = self.txt_topic.get()
        if self.topic not in self.all_topics:
            #print("Введите корректную тему!")
            messagebox.showinfo('Ошибка', 'Введите корректную тему!')
            self.range_row -= 2
            self.choice_topic()
        elif self.topic == 'все':
            self.words_topic = list(set(self.words)-set(re.findall(r'("\w+")',' '.join(self.words))))
            self.btn_topic['state'] = 'disabled'
            self.txt_topic['state'] = 'disabled'
            self.choice_level()
        else:
            self.words_topic = re.findall(f'"{self.topic}"([\w\s]+)',' '.join(self.words))[0].split()
            self.btn_topic['state'] = 'disabled'
            self.txt_topic['state'] = 'disabled'
            self.choice_level()
            
    def choice_level(self):
        self.low_word = [wrd for wrd in self.words_topic if len(set(list(wrd)))>self.medium_range[1]]
        self.medium_word = [wrd for wrd in self.words_topic if len(set(list(wrd))) in self.medium_range]
        self.hard_word = [wrd for wrd in self.words_topic if len(set(list(wrd)))<self.medium_range[0]]
        self.levels = [level_names for lst,level_names in zip([self.low_word,self.medium_word,self.hard_word],['легкий','средний','тяжелый']) if lst!=[]]
        if len(self.levels) == 1:
            #print(f"Вы играете на уровне сложности {self.levels[0]}")
            self.lbl_level = Label(self.window, text=f"Вы играете на уровне сложности: {self.levels[0]}")  
            self.lbl_level.grid(column=0, row=self.range_row)
            self.range_row += 1
            self.start()
        else:
            #print(f"Выберите подходящий уровень: {', '.join(self.levels)}, все")
            self.lbl_level = Label(self.window, text=f"Выберите подходящий уровень: {', '.join(self.levels)}, все")  
            self.lbl_level.grid(column=0, row=self.range_row)
            self.range_row += 1
            self.txt_level = Entry(window, width = 30)
            self.txt_level.grid(column = 0, row = self.range_row)
            self.txt_level.focus()
            self.btn_level = Button(self.window, text = 'Выбрать уровень!', command = self.check_choice_level)
            self.btn_level.grid(column = 1, row = self.range_row)
            self.window.bind('<Return>', lambda event=None: self.btn_level.invoke()) 
            self.range_row += 1
            #self.check_choice_level()
            
    def check_choice_level(self):
        level = self.txt_level.get()
        if level == 'легкий' and 'легкий' in self.levels: 
            self.words_topic = self.low_word
            self.btn_level['state'] = 'disabled'
            self.txt_level['state'] = 'disabled'
            self.start()
        elif level == 'средний' and 'средний' in self.levels: 
            self.words_topic = self.medium_word
            self.btn_level['state'] = 'disabled'
            self.txt_level['state'] = 'disabled'
            self.start()
        elif level == 'тяжелый' and 'тяжелый' in self.levels: 
            self.words_topic = self.hard_word
            self.btn_level['state'] = 'disabled'
            self.txt_level['state'] = 'disabled'
            self.start()
        elif level == 'все': 
            self.btn_level['state'] = 'disabled'
            self.txt_level['state'] = 'disabled'
            self.start()
        else:
            #print("Введите корректный уровень!")
            messagebox.showinfo('Ошибка', 'Введите корректный уровень!')
            self.range_row -= 2
            self.choice_level()
            
    def delete_guess_and_empty_topics(self):
        words_not_guess = list(set(self.words)-set(words_delete))
        self.words = [wrd for wrd in self.words if wrd in words_not_guess]
        if self.words == []:
            #print("К сожалению, слов не осталось :c")
            self.no_word = Label(self.window, text='К сожалению, слов не осталось :c')  
            self.no_word.grid(column=0, row=0)
            self.btn_reload['state'] = 'disabled'
            return False
        elif self.all_topics:
            tops_delete = []
            for top in self.all_topics:
                try:
                    word_topic = re.findall(f'"{top}"([\w\s]+)',' '.join(self.words))[0].split()
                    if word_topic == []: tops_delete.append(top)
                except:
                    tops_delete.append(top)
            self.all_topics = list(set(self.all_topics)-set(tops_delete))
            if self.all_topics == []:
                #print("К сожалению, слов не осталось :c")
                self.no_word = Label(self.window, text='К сожалению, слов не осталось :c')  
                self.no_word.grid(column=0, row=0)
                self.btn_reload['state'] = 'disabled'
                return False
            else: return True
        else: return True
        
    def reload_game(self):
        self.window.destroy()
        os.startfile(sys.argv[0])
        
        
window = Tk()
image_win = Image.open('image_win.jpg')
image_win = image_win.resize((200, 200), Image.ANTIALIAS)
image_win = ImageTk.PhotoImage(image_win)
image_lose = Image.open('image_lose.jpg')
image_lose = image_lose.resize((200, 200), Image.ANTIALIAS)
image_lose = ImageTk.PhotoImage(image_lose)
window.title("Висилица!")
window.geometry('1000x600')
# window = Frame(root)
# window.pack(fill="both", expand=True)
# scrolledtext.ScrolledText(window)
gallow = Gallows(window,words)
gallow.choice_topic()
window.mainloop()