import requests, webbrowser,shelve
from bs4 import BeautifulSoup
import pyperclip as py

error_shelf = shelve.open('errorDict')
serch_texts = py.paste()

# 指定文字列意外入力された時の表示関数
def y_or_n():
    return print("please input [y or n]")

# エラー内容作成関数
def makeErrorContents():
    contents = input("Error description input\n")
    return contents

# エラー解決方法作成関数
def makeErrorSolution():
    solution = []
    while True:
        sol = input("Add a solution(End with enter without input)\n")
        solution.append(sol)
        if sol == '':
            del solution[-1]
            break
    return solution

# エラー内容、解決方法表示関数
def display(cont, sol):
    print("Error :" + serch_texts + "\n")
    print("Error Contents :" + cont)

    for i in sol:
        print("・" + i)

# 辞書登録関数
def enterError(contents, solList):
    enter_error_dict = {}
    enter_error_dict['contents'] = contents
    enter_error_dict['solutions'] = solList
    return enter_error_dict

# 登録されているエラー検索関数
def dictSerch():
    flag = 0
    if serch_texts in error_shelf:
        print(serch_texts + " confirmed")
        contents = error_shelf[serch_texts]['contents']
        solList = error_shelf[serch_texts]['solutions']
        
        if contents == '':
            flag = 1
            while True:
                print("not registration problem. serch google?")
                answer = input("y/n:")
                if "y" == answer:
                    num = input("serch count(1~5) or End with enter without input:")
                    if num == '':
                        flag = 0
                        break
                    googleSerch(num)
                    break
                elif "n" == answer:
                    break
                else:
                    y_or_n()
            contents = makeErrorContents()

        if solList == '':
            flag = 1
            while True:
                print("not registration solution. serch google?")
                answer = input("y/n:")
                if "y" == answer:
                    num = input(
                        "serch count(1~5) or End with enter without input:")
                    if num == '':
                        flag = 0
                        break
                    googleSerch(num)
                    break
                elif "n" == answer:
                    break
                else:
                    y_or_n()
            solList = makeErrorSolution()

        # エラー登録内容表示
        display(contents,solList)
        if flag == 1:
            while True:
                user_input = input("Would you like to register?(y/n)->")
                if "y" == user_input:
                    error_shelf[serch_texts] = enterError(contents, solList)
                    break
                elif "n" == user_input:
                    break
                else:
                    y_or_n()

    else:
        while True:
            print("Unregistration error. serch google?")
            answer = input("y/n:")
            if "y" == answer:
                num = input(
                    "serch count(1~5) or End with enter without input:")
                if num == '':
                    flag = 0
                    break
                googleSerch(num)
                break
            elif "n" == answer:
                break
            else:
                y_or_n()
            
        contents = makeErrorContents()
        solution = makeErrorSolution()
        # エラー登録内容表示
        display(contents, solution)
        while True:
            user_input = input("Would you like to register?(y/n)->")
            if "y" == user_input:
                error_shelf[serch_texts] = enterError(contents, solution)
                break
            elif "n" == user_input:
                break
            else:
                y_or_n()
    print("#" * 50)

# グーグル検索関数
def googleSerch(num):
    url = 'https://www.google.com/search?q=' + serch_texts
    result = requests.get(url).text
    soup = BeautifulSoup(result, 'html.parser')
    tags = soup.select('.kCrYT a')

    for i in range(0,int(num)):
        url = tags[i].get('href').replace('/url?q=', '')
        after_url = url[:url.find('&')]
        webbrowser.open(after_url)

if __name__ == "__main__":
    while True:
        menu = input("【select Menu】 -> 1: serch error 2:end \n input key:")
        if "1" == menu:
            dictSerch()
        elif "2" == menu:
            exit()
        else:
            print("please [1] or [2]")

    error_shelf.close()
            
