# InterviewQuestionBank
自定义出题器：附带了算法岗题库，题库内容可自定义

为了记录面试中的知识点，整理了一个机器学习、深度学习、推荐系统、CV相关的题库。

但问题量越来越大复习起来不方便，
所以做了一个简易出题器，
可以随机出题、按关键字搜索题目。

题库使用Excel记录，默认读取问题库`questions.xlsx`，不同问题分类使用不同sheet记录。
可以自行增改题库或者建立自己的题库。

Excel文件第一列是问题，第二列是对应答案解析，支持`文本`和`markdown`格式的答案。

## 环境依赖
```python
pip install PyQt5==5.15.0
pip install PyQtWebEngine==5.15.0
pip install xlrd==1.2.0
pip install Markdown==3.2.2
pip install python-markdown-math==0.7
```

## 使用
一键运行

```python
python main.py
```
显示效果：

<img src="https://tva1.sinaimg.cn/large/007S8ZIlgy1gh7vb7opxzj30tw0q2gp6.jpg" alt="ac6f7a5d.png" width="521" height="458" align="bottom" />

<img src="https://tva1.sinaimg.cn/large/007S8ZIlgy1gh7vhyjrc5j30tm0oen37.jpg" alt="ac6f7a5d.png" width="521" height="458" align="bottom" />