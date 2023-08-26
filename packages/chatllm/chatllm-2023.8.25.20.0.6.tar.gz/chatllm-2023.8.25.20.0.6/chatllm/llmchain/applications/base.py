#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : base
# @Time         : 2023/8/9 15:04
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

from langchain.chat_models import ChatOpenAI
from langchain.schema.language_model import BaseLanguageModel
from chatllm.llmchain.decorators import llm_stream, llm_astream


class ChatBase(object):

    def __init__(
        self,
        llm: Optional[BaseLanguageModel] = None,
        get_api_key: Optional[Callable[[int], List[str]]] = None,  # 队列
        **kwargs
    ):
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo-16k-0613", temperature=0, streaming=True)

        if get_api_key:
            self.llm.openai_api_key = get_api_key(1)[0]

    def run(self, prompt):
        yield from llm_stream(self.llm.predict)(prompt)

    def arun(self, prompt):
        yield from asyn2sync_generator(llm_astream(self.llm.apredict)(prompt))


if __name__ == '__main__':
    ChatBase().run('1+1') | xprint(end='\n')
    # ChatBase().arun('周杰伦是谁') | xprint(end='\n')
