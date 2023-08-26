from json import dumps as jsonDumps
from json import dumps
from json import loads as jsonLoads
from typing import Dict
import openai
from ._core import system_msg, user_msg, assistant_msg, Chat


class GCRoles:
    '''
        roles: {
            '李白': {'desc':'中国唐代的著名大诗人'}
        }
    '''
    roles: Dict[str, dict]
    def __init__(self):
        self.roles = {}
    
    def __getitem__(self, role):
        return self.roles.setdefault(role, {})


class GroupChat(Chat):

    MustRolesInfo = {
        '小许3号':{'desc':'一个聪明的程序员'},
        '小许1号':{'desc':'一个帅气的男人'},
        '小许2号':{'desc':'一个漂亮的女人'},
    }
    user_example = dumps({'dialogues':[{'speaker':'李白', 'audiences':['杜甫', '小许'], 'remark':'你们好呀'}, {'speaker':'杜甫', 'audiences':['李白'], 'remark':'你好, 你今天写诗了吗?'}, {'speaker':'小许', 'audiences':['李白'], 'remark':'你好, 你吃了吗?'}], 'dialogues to be generated':[{'speaker':'李白', 'audiences':['小许']}, {'speaker':'李白', 'audiences':['杜甫']}, {'speaker':'李白', 'audiences':['杜甫', '小许']}]}, ensure_ascii=False)
    assistant_example = dumps(['我今天写诗了', '我吃饭了','你们有什么有趣的事情分享吗?'], ensure_ascii=False)

    def __init__(self, *vs, **kvs):
        Chat.__init__(self, *vs, **kvs)
        self.roles = GCRoles()
    
    @property
    def pinned_message(self):
        system_text = f'''以下JSON格式的文档描述了一些人物信息:
【{dumps(self.MustRolesInfo | self.roles.roles, ensure_ascii=False)}】
assistant需要了解这些人物的信息. user将会收集这些人物的对话记录并整理成固定格式, 然后以JSON格式发送给assistant,在发送给assistant的JSON文档中, 还会注明需要assistant模拟生成哪些人对哪些人的对话, 例如:
【{self.user_example}】
在上面的例子中, 'dialogues to be generated' 字段有3个元素, 则assistant的回答也需要有3个元素,然后放在一个列表中,以JSON格式返回, 例如:
【{self.assistant_example}】
assistant每次只返回JSON文档即可,勿包含任何其它信息,否则会干扰user的解析.
assistant在回答时可以编造,比如在回答年龄时,可以随意编一个年龄.'''
        return [
            system_msg(system_text),
            user_msg(dumps({'dialogues':[{'speaker':'小许1号', 'audiences':['小许2号'], 'remark':'你是谁?'}, {'speaker':'小许2号', 'audiences':['小许1号'], 'remark':'我叫小许2号,今年13岁'}, {'speaker':'小许3号', 'audiences':['小许1号', '小许2号'], 'remark':'你们是哪里人?'}], 'dialogues to be generated':[{'speaker':'小许1号', 'audiences':['小许2号']}, {'speaker':'小许1号', 'audiences':['小许3号']}, {'speaker':'小许2号', 'audiences':['小许3号']}]}, ensure_ascii=False)),
            assistant_msg(dumps(['哦哦, 我比你大1岁', '我是河南人', '不告诉你'], ensure_ascii=False)),
            user_msg(dumps({'dialogues':[{'speaker':'小许3号', 'audiences':['小许2号'], 'remark':'呵呵,这么神秘呀?'}, {'speaker':'小许3号', 'audiences':['小许1号'], 'remark':'你知道小许2号是哪里人吗?'}], 'dialogues to be generated':[{'speaker':'小许1号', 'audiences':['小许3号']}, {'speaker':'小许2号', 'audiences':['小许3号']}]}, ensure_ascii=False)),
            assistant_msg(dumps(['哈哈, 我也不知道哦', '哈哈, 也没啥神秘的,我是湖北人'], ensure_ascii=False))
        ]
    
    def request(self, user:dict):
        text = jsonDumps(user, ensure_ascii=False)
        self.recently_used_apikey = self._akpool.fetch_key()
        completion = openai.ChatCompletion.create(**{
            'api_key': self.recently_used_apikey,
            'model': self.model,
            'messages': [dict(x) for x in self.pinned_message] + list(self._messages) + [{"role": "user", "content": text}],
            **self.kwargs
        })
        answer:str = completion.choices[0].message['content']
        self._messages.add_many(
            {"role": "user", "content": text},
            {"role": "assistant", "content": answer}
        )
        return answer