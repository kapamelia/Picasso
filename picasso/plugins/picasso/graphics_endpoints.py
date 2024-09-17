import os

from nonebot import get_driver

os.environ["DASHSCOPE_API_KEY"] = get_driver().config.dash_scope_api_key
os.environ["VOLC_ACCESSKEY"] = get_driver().config.volc_accesskey
os.environ["VOLC_SECRETKEY"] = get_driver().config.volc_secretkey

from abc import abstractmethod, ABC
import asyncio
from dashscope import ImageSynthesis
from volcengine.visual.VisualService import VisualService


class GraphicsBase(ABC):
    @abstractmethod
    async def draw(self, *args, **kwargs):
        raise NotImplementedError("Method draw is not implemented")


class FluxDev(GraphicsBase):
    name = "flux-dev"

    async def draw(self, prompt, *args, **kwargs):
        response = await asyncio.to_thread(
            ImageSynthesis.call,
            model="flux-dev",
            prompt=prompt,
            size="1024*1024",
            steps=30,
        )
        return response.output.results[0]["url"]


class FluxSchnell(GraphicsBase):
    name = "flux-schnell"

    async def draw(self, prompt, *args, **kwargs):
        response = await asyncio.to_thread(
            ImageSynthesis.call,
            model="flux-schnell",
            prompt=prompt,
            size="1024*1024",
            steps=30,
        )
        return response.output.results[0]["url"]


class FluxMerged(GraphicsBase):
    name = "flux-merged"

    async def draw(self, prompt, *args, **kwargs):
        response = await asyncio.to_thread(
            ImageSynthesis.call,
            model="flux-merged",
            prompt=prompt,
            size="1024*1024",
            steps=30,
        )
        return response.output.results[0]["url"]


class WanXiang(GraphicsBase):
    name = "wanxiang"

    async def draw(self, prompt, *args, **kwargs):
        response = await asyncio.to_thread(
            ImageSynthesis.call,
            model=ImageSynthesis.Models.wanx_v1,
            prompt=prompt,
            size="1024*1024",
        )
        return response.output.results[0]["url"]


class VolcEngineV14(GraphicsBase):
    name = "volcengine_v14"

    def __init__(self) -> None:
        super().__init__()
        self.visual_service = VisualService()
        

    async def draw(self, prompt, *args, **kwargs):
        form = {
            "req_key": "high_aes_general_v14",
            "prompt": prompt,
            "model_version": "general_v1.4",
            "seed": -1,
            "scale": 3.0,
            "ddim_steps": 25,
            "width": 512,
            "height": 512,
            "use_rephraser": True,
            "return_url": True,
            "use_predict_tags": True,
            "logo_info": {
                "add_logo": False,
                "position": 0,
                "language": 0,
                "opacity": 0.3,
            },
        }

        resp = await asyncio.to_thread(self.visual_service.high_aes_smart_drawing, form)
        return resp["data"]["image_urls"][0]


class VolcEngineV20(GraphicsBase):
    name = "volcengine_v20"

    def __init__(self) -> None:
        super().__init__()
        self.visual_service = VisualService()
        

    async def draw(self, prompt, *args, **kwargs):
        form = {
            "req_key": "high_aes_general_v20",
            "prompt": prompt,
            "model_version": "general_v2.0",
            "seed": -1,
            "scale": 3.0,
            "ddim_steps": 25,
            "width": 512,
            "height": 512,
            "use_rephraser": True,
            "return_url": True,
            "use_predict_tags": True,
            "logo_info": {
                "add_logo": False,
                "position": 0,
                "language": 0,
                "opacity": 0.3,
            },
        }

        resp = await asyncio.to_thread(self.visual_service.high_aes_smart_drawing, form)
        return resp["data"]["image_urls"][0]


