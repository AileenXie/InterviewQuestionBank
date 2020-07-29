# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import xlrd
import random
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from mdx_math import MathExtension
from question import Ui_Dialog
from PyQt5.QtWidgets import *


class UiMainWindow(QWidget, Ui_Dialog):
    def __init__(self, parent=None):
        super(UiMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_random_question)  # random
        self.pushButton_2.clicked.connect(self.get_prev_question)  # previous
        self.pushButton_3.clicked.connect(self.get_next_question)  # next
        self.pushButton_4.clicked.connect(self.show_answer)  # comment
        self.confirmBt.clicked.connect(self.open_sheet_and_question)
        self.jumpBt.clicked.connect(self.get_target_question)
        self.KeySearchBt.clicked.connect(self.key_search)
        self.SearchBt.clicked.connect(self.search_by_key)
        self.SearchPrev.clicked.connect(self.key_prev)
        self.SearchNext.clicked.connect(self.key_next)

        # initial
        self.wb, self.sheet_list = self.open_question_file("questions.xlsx")
        self.ques_index = 1  # 第一题
        self.rows = None  # 题目内容
        self.sheet = None
        self.num = 0
        self.key_index_list = []  # 关键字所在行索引
        self.show_key_search = False
        self.set_key_search_visible(self.show_key_search)
        self.cur_key_index = 0  # 关键字self.key_index_list中的索引
        self.comboBox.addItems(self.sheet_list)  # 下拉栏
        self.open_sheet_and_question()  # 显示当前问题（根据self.sheet, self.ques_index）

    def open_sheet_and_question(self):
        """
        【切换sheet】并显示首题
        """
        name = self.comboBox.currentText()
        self.sheet, self.num = self.open_sheet(name)
        total = self.num-1 if self.num else 0
        self.set_text(self.sumLabel, "【" + name + "】总题数：" + str(total))
        self.ques_index = 1
        if self.num < 2:  # 没题
            self.set_text(self.label, "该分类暂无题目！")
            self.update_button()
            self.spinBox.setRange(0, 0)
        else:
            self.spinBox.setRange(1, self.num - 1)
            self.update_question()  # 显示当前问题（根据self.sheet, self.ques_index）
        # 控件状态初始化
        self.browser.setVisible(True)
        self.browser.setHtml("")
        self.set_key_search_visible(False)

    def key_search(self):
        """
        设置关键字搜索区域可见性
        """
        self.show_key_search ^= 1  # 更新状态
        self.set_key_search_visible(self.show_key_search)
        # if self.show_key_search: print("关键字查找：展开")
        # else: print("关键字查找：隐藏")

    def search_by_key(self):
        """
        关键字【搜索】
        """
        key = self.lineEdit.text()
        if not key:  # 无内容
            return
        # print("查找关键字——"+key)
        # 查找关键字
        self.key_index_list = set()
        for i in range(1, self.num):
            row = self.sheet.row_values(i)
            for j in range(2):
                if key.lower() in row[j].lower():
                    self.key_index_list.add(i)
        self.key_index_list = list(self.key_index_list)
        self.key_index_list.sort()
        # print(self.key_index_list)
        self.cur_key_index = 0
        if self.key_index_list:
            self.ques_index = self.key_index_list[self.cur_key_index]
            self.update_question()
        self.update_key_button()

    def key_next(self):
        """
        关键字搜索结果【下一个】
        """
        self.cur_key_index += 1
        self.ques_index = self.key_index_list[self.cur_key_index]
        self.update_key_button()
        self.update_question()

    def key_prev(self):
        """
        关键字搜索结果【上一个】
        """
        self.cur_key_index -= 1
        self.ques_index = self.key_index_list[self.cur_key_index]
        self.update_key_button()
        self.update_question()

    def get_target_question(self):
        """
        【跳转】到指定题目
        """
        self.ques_index = self.spinBox.value()
        self.update_question()

    def get_random_question(self):
        """
        【随机】更新问题
        """
        index = random.randint(1, self.num-1)
        while index == self.ques_index:  # 避免重复
            index = random.randint(1, self.num - 1)
        self.ques_index = index
        self.update_question()

    def get_next_question(self):
        """
        【下一题】
        """
        self.ques_index +=1
        self.update_question()

    def get_prev_question(self):
        """
        【上一题】
        """
        self.ques_index -=1
        self.update_question()

    def set_key_search_visible(self, flag=False):
        """
        设置【关键字查找】模块的可见性
        """
        self.lineEdit.setVisible(flag)  # ##
        self.SearchBt.setVisible(flag)
        if not flag:
            self.SearchPrev.setVisible(False)
            self.SearchNext.setVisible(False)
            self.numberLabel.setVisible(False)
        else:
            self.SearchPrev.setVisible(True)
            self.SearchNext.setVisible(True)
            self.numberLabel.setVisible(True)
            self.set_button_enabled(self.SearchNext, False)
            self.set_button_enabled(self.SearchPrev, False)
            self.set_text(self.numberLabel, "0/0")

    def open_question_file(self, filename):
        """
        Open excel file
        :param filename: file path
        :return: xlrd object, sheet list
        """
        wb = xlrd.open_workbook(filename=filename)  # 打开文件
        sheet_list = wb.sheet_names()
        print(sheet_list)  # 获取所有表格sheet名字
        return wb, sheet_list

    def open_sheet(self, sheet_name):
        """
        Open sheet by name
        :param sheet_name: target sheet name
        :return: target sheet object, total number of rows
        """
        sheet = self.wb.sheet_by_name(sheet_name)  # 通过名字获取表格
        num = sheet.nrows
        print("问题类型:{}，题目数:{}".format(sheet.name, num-1))
        return sheet,num

    def update_button(self):
        if self.ques_index >= self.num - 1:  # 最后一题
            print("————————已是最后一题——————————")
            self.set_button_enabled(self.pushButton_3, False)  # 【下一题】不可点击
        else:
            self.set_button_enabled(self.pushButton_3, True)
        if self.ques_index == 1:  # 第一题
            print("————————已是第一题——————————")
            self.set_button_enabled(self.pushButton_2, False)  # 【上一题】不可点击
        else:
            self.set_button_enabled(self.pushButton_2, True)
        if self.num <= 1:  # 没题
            print("————————该分类没有题目——————————")
            self.set_button_enabled(self.pushButton_4, False)  # 【题解】不可点击
            self.set_button_enabled(self.jumpBt, False)  # 【题号跳转】不可点击
        else:
            self.set_button_enabled(self.pushButton_4, True)
            self.set_button_enabled(self.jumpBt, True)
        if self.num <= 2:  # 小于一题
            print("————————该分类只有一题——————————")
            self.set_button_enabled(self.pushButton, False)  # 【随机】不可点击
        else:
            self.set_button_enabled(self.pushButton, True)  # 【随机】

    def update_key_button(self):
        total = len(self.key_index_list)
        if not self.key_index_list:
            self.set_button_enabled(self.SearchNext, False)
            self.set_button_enabled(self.SearchPrev, False)
            self.set_text(self.numberLabel, "无结果")
        else:
            if self.cur_key_index == total-1:  # 到底了
                self.set_button_enabled(self.SearchNext, False)
            else:
                self.set_button_enabled(self.SearchNext, True)
            if self.cur_key_index == 0:  # 到头了
                self.set_button_enabled(self.SearchPrev, False)
            else:
                self.set_button_enabled(self.SearchPrev, True)
            self.set_text(self.numberLabel, str(self.cur_key_index+1)+"/"+str(total))

    def update_question(self):
        """
        显示题目，更新按键
        """
        rows = self.sheet.row_values(self.ques_index)  # 获取行内容
        self.rows = rows
        self.browser.setHtml("")  # 清空解析
        self.set_text(self.label, str(self.ques_index) + ". " + rows[0])  # 更新题目
        self.update_button()

    def show_answer(self):
        """
        显示题解
        """
        if self.rows[2] == 1:
            # print("[Plaintext]")
            self.browser.setHtml(self.rows[1])
        else:
            # print("[Markdown]")
            self.browser.setHtml(self.markdown_to_html(self.rows[1]))
        self.set_button_enabled(self.pushButton_4, False)

    def set_button_enabled(self, button, flag):
        button.setEnabled(flag)
        button.repaint()  # mac上的bug

    def set_text(self, box, text):
        box.setText(text)
        box.repaint()

    def markdown_to_html(self,text):
        # 扩展用法
        key = ["+", ">"]  # 添加换行
        for k in key:
            text = text.replace("\n" + k, "\n\n" + k)

        html = markdown.markdown(text, output_format='html5',
                                 extensions=[MathExtension(enable_dollar_delimiter=True),
                                             'markdown.extensions.toc',
                                             WikiLinkExtension(base_url='https://en.wikipedia.org/wiki/',
                                                               end_url='#Hyperlinks_in_wikis'),
                                             'markdown.extensions.sane_lists',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.abbr',
                                             'markdown.extensions.attr_list',
                                             'markdown.extensions.def_list',
                                             'markdown.extensions.fenced_code',
                                             'markdown.extensions.footnotes',
                                             'markdown.extensions.meta',
                                             'markdown.extensions.nl2br',
                                             'markdown.extensions.tables'])
        html = html.replace("<table>", "<table border='1' cellpadding='2' cellspacing='0'>")
        html_head_file = open("html_head.txt", "r", encoding='utf-8')
        html_head = html_head_file.read()
        html_head_file.close()
        html_tail = "\n</body>\n</html>"
        html = html_head+html+html_tail
        # print(html)
        # html_file = open("file.html", "w", encoding='utf-8')
        # html_file.write(html)
        # html_file.close()

        return html

if __name__ == "__main__":

    app = QApplication(sys.argv)
    # initial
    myWin = UiMainWindow()
    myWin.show()
    sys.exit(app.exec_())
