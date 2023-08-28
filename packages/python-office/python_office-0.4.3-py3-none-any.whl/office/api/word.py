#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: word.py
# 公众号/B站/小红书/抖音: 程序员晚枫
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关word的自动化操作
#############################################
# from office.lib.utils.except_utils import except_dec
# from office.core.WordType import MainWord

# 创建对象
# mainWord = MainWord()
import poword

# 1、文件的批量转换
# 自己指定路径，
# 为了适配wps不能转换doc的问题，这里限定：只能转换docx
# @except_dec()
from office.lib.decorator_utils.instruction_url import instruction


@instruction
def docx2pdf(path: str, output_path: str = None):
    if output_path == None:
        output_path = path
    poword.docx2pdf(path, output_path)


@instruction
def merge4docx(input_path: str, output_path: str, new_word_name: str = 'merge4docx'):
    poword.merge4docx(input_path, output_path, new_word_name)


@instruction
def doc2docx(input_path: str, output_path: str = r'./'):
    poword.doc2docx(input_path, output_path)


@instruction
def docx2doc(input_path: str, output_path: str = r'./'):
    poword.docx2doc(input_path, output_path)
