#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatocr
# @Time         : 2023/8/25 16:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://aistudio.baidu.com/modelsdetail?modelId=332

from meutils.pipe import *
from chatllm.llmchain.applications.base import ChatBase
from chatllm.llmchain.prompts.prompt_templates import ocr_prompt_template


class ChatOCR(ChatBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        pass

    def arun(self):
        pass

from rapidocr_onnxruntime import RapidOCR

rapid_ocr = RapidOCR()

p = "/Users/betterme/PycharmProjects/AI/MeUtils/meutils/ai_cv/invoice.jpg"
ocr_result, _ = rapid_ocr(p)
