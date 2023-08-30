from dwai.bailian.model_api.completions import Completions
from dwai.pangu.model_api.completions import PanGuCompletions
from dwai.tione.v20211111.tione_client import TioneClient
from dwai.zhipuai.model_api.api import ModelAPI


def dwai_bailian_qa(**kwargs):
    chat = Completions()
    return chat.call(app_id=kwargs.get('app_id'), prompt=kwargs.get('prompt'))


def zhipuai_chatglm_std(**kwargs):
    model = ModelAPI()
    return model.invoke(model="chatglm_std", prompt=kwargs.get('prompt'),
                        top_p=kwargs.get('top_p'), temperature=kwargs.get('temperature'))


def pangu_completions(**kwargs):
    chat = PanGuCompletions()
    return chat.call(prompt=kwargs.get('prompt'), max_tokens=kwargs.get('max_tokens'),
                     messages=kwargs.get('messages'), temperature=kwargs.get('temperature'))


def tione_chat_completion(**kwargs):
    chat = TioneClient()
    return chat.ChatCompletion(content=kwargs.get('content'))


class UnifiedSDK:
    def __init__(self):
        self.route_map = {
            'alibaba.qwen-plus-v1': dwai_bailian_qa,
            'kingsoft.default': zhipuai_chatglm_std,
            'huawei.default': pangu_completions,
            'tencent.default': tione_chat_completion
        }

    def call(self, model_key, **kwargs):
        func = self.route_map.get(model_key)
        if func:
            return func(**kwargs)
        else:
            raise ValueError(f"Unknown model_key: {model_key}")


import dwai

dwai.api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
dwai.api_base = "https://dwai.shizhuang-inc.com"

if __name__ == '__main__':
    sdk = UnifiedSDK()

    # 测试dwai
    resp = sdk.call('alibaba.qwen-plus-v1', app_id="app_id_here", prompt="你好")
    print(resp)

    # 测试zhipuai
    resp = sdk.call('kingsoft.default', prompt=[{"role": "user", "content": "人工智能"}],
                    top_p=0.7, temperature=0.9)
    print(resp)

    # 测试pangu
    resp = sdk.call('huawei.default', prompt="", max_tokens=600,
                    messages=[{"role": "system",
                               "content": "请用幼儿园老师的口吻回答问题，注意语气温和亲切，通过提问、引导、赞美等方式，激发学生的思维和想象力。"},
                              {"role": "user", "content": "写一首诗"}],
                    temperature=0.9)
    print(resp)

    # 测试tione
    resp = sdk.call('tencent.default', content="2+2=?")
    print(resp)
