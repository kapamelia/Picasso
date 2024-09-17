import asyncio
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from .graphics_endpoints import (
    FluxDev,
    FluxMerged,
    FluxSchnell,
    WanXiang,
    VolcEngineV14,
    VolcEngineV20,
)
from .tools import create_image_grid_with_text_bytes, download_images

picasso = on_command("picasso", priority=5)

drawers = [
    FluxSchnell(),
    FluxDev(),
    FluxMerged(),
    WanXiang(),
    VolcEngineV14(),
    VolcEngineV20(),
]

cache = {}


@picasso.handle()
async def handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    prompt = args.extract_plain_text().strip()
    group_id = event.group_id
    if prompt.isdigit() and group_id in cache:
        index = int(prompt)
        if 0 <= index < len(drawers):
            await picasso.finish(
                [
                    MessageSegment.reply(event.message_id),
                    MessageSegment.image(cache[group_id][index]),
                ]
            )

    if prompt:
        try:
            await picasso.send("正在生成图片，请稍等哦~")
            tasks = []
            for drawer in drawers:
                tasks.append(drawer.draw(prompt))
            results = await asyncio.gather(*tasks)
            descriptions = [drawer.name for drawer in drawers]
            cache[group_id] = results
            results_downloaded = await download_images(results)
            result_bytes = create_image_grid_with_text_bytes(
                results_downloaded, descriptions
            )
            await picasso.send(
                [
                    MessageSegment.reply(event.message_id),
                    MessageSegment.image(result_bytes),
                ]
            )
        except Exception as e:
            await picasso.finish(f"生成图片时发生错误：{e}")
