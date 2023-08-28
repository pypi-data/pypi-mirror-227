from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import CommandArg
from nonebot import require
from nonebot.plugin import PluginMetadata
from .acountant import writeIn, readBook

require("nonebot_plugin_localstore")

__plugin_meta__ = PluginMetadata(
    name="群账本",
    description="记录群友的共同花销，统一清算",
    usage="1. 记录花销：/记账 [开销名] [人数] [金额]    2. 清算： /清算 [clear](可选，用于清空账本)",
    type="application",
    homepage="https://github.com/shilapi/nonebot-plugin-groupAccountant",
    extra={
        "unique_name": "groupAccountant",
        "example": "/记账 海底捞 5 600",
        "author": "shilapi <shilapi@outlook.com>",
        "version": "0.0.1",
    },
)

groupAccountant = on_command('accountant', aliases={'记账', '记'}, priority=13, block=True)

@groupAccountant.handle()
async def _(event: MessageEvent, msg: Message = CommandArg()):
    if text := msg.extract_plain_text():
        resp = await writeIn(text, event.get_user_id())
        #await account.finish('好了'+'(debug:'+str(resp)+str(event.get_user_id())+')')
        await groupAccountant.finish('好了')
    else:
        await groupAccountant.finish('使用方式为：@bot /记账 *开销名称* *人数* *金额*')
    
    
clearance = on_command('reader', aliases={'结账', '清算', '结算'}, priority=13, block=True)

@clearance.handle()
async def handle_function(event: MessageEvent, msg: Message = CommandArg()):
    print('start')
    if text := msg.extract_plain_text():
        if text == 'final' or 'clear':
            resp = await readBook(True)
            await clearance.finish(resp)
        elif text == 'help':
            await clearance.finish('使用方式为：@bot /结算 (可选的)clear')
    else:
        resp = await readBook(False)
        await clearance.finish(resp)