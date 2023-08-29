#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : notice
# @Time         : 2023/8/29 10:20
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.notice import feishu as _feishu
from meutils.notice.wecom import Wecom

cli = typer.Typer(name="MeUtils CLI")


@cli.command()
def email(title, text='', hook_url=None):
    """sh管道传参 echo args | xargs -I {} mecli notice {}"""
    Wecom(hook_url).send_markdown(title, text)
    return 'ok'


@cli.command()
def wechat(path, type='file', hook_url=None):
    """mecli notice file_path"""
    Wecom(hook_url).send_file(path, type)
    return 'ok'


@cli.command()
def feishu(
        title='',
        content='',
        url: Optional[str] = None
):
    """
    echo args | xargs -I {} notice {}

    python notice.py feishu --title t --content c
    """
    _feishu.send_message(title=title, content=content, url=url)


@cli.command()
def feishu4openai(trace: Optional[bool] = False, openai_api_base='https://api.openai-proxy.com/v1'):
    @_feishu.catch(task_name='CheckOpenaiKey', trace=trace)
    def fn():
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(openai_api_base=openai_api_base)
        return llm.predict('1+1')

    fn()


if __name__ == '__main__':
    cli()
