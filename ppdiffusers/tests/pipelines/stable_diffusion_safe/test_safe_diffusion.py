# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
# Copyright 2023 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gc
import random
import tempfile
import unittest

import numpy as np
import paddle
from paddlenlp.transformers import CLIPTextConfig, CLIPTextModel, CLIPTokenizer

from ppdiffusers import (
    AutoencoderKL,
    DDIMScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
    UNet2DConditionModel,
)
from ppdiffusers.pipelines.stable_diffusion_safe import (
    StableDiffusionPipelineSafe as StableDiffusionPipeline,
)
from ppdiffusers.utils import floats_tensor, nightly
from ppdiffusers.utils.testing_utils import require_paddle_gpu


class SafeDiffusionPipelineFastTests(unittest.TestCase):
    def tearDown(self):
        super().tearDown()
        gc.collect()
        paddle.device.cuda.empty_cache()

    @property
    def dummy_image(self):
        batch_size = 1
        num_channels = 3
        sizes = 32, 32
        image = floats_tensor((batch_size, num_channels) + sizes, rng=random.Random(0))
        return image

    @property
    def dummy_cond_unet(self):
        paddle.seed(0)
        model = UNet2DConditionModel(
            block_out_channels=(32, 64),
            layers_per_block=2,
            sample_size=32,
            in_channels=4,
            out_channels=4,
            down_block_types=("DownBlock2D", "CrossAttnDownBlock2D"),
            up_block_types=("CrossAttnUpBlock2D", "UpBlock2D"),
            cross_attention_dim=32,
        )
        return model

    @property
    def dummy_vae(self):
        paddle.seed(0)
        model = AutoencoderKL(
            block_out_channels=[32, 64],
            in_channels=3,
            out_channels=3,
            down_block_types=["DownEncoderBlock2D", "DownEncoderBlock2D"],
            up_block_types=["UpDecoderBlock2D", "UpDecoderBlock2D"],
            latent_channels=4,
        )
        return model

    @property
    def dummy_text_encoder(self):
        paddle.seed(0)
        config = CLIPTextConfig(
            bos_token_id=0,
            eos_token_id=2,
            hidden_size=32,
            intermediate_size=37,
            layer_norm_eps=1e-05,
            num_attention_heads=4,
            num_hidden_layers=5,
            pad_token_id=1,
            vocab_size=1000,
        )
        return CLIPTextModel(config).eval()

    @property
    def dummy_extractor(self):
        def extract(*args, **kwargs):
            class Out:
                def __init__(self):
                    self.pixel_values = paddle.ones(shape=[0])

                def to(self, device):
                    self.pixel_values
                    return self

            return Out()

        return extract

    def test_safe_diffusion_ddim(self):
        unet = self.dummy_cond_unet
        scheduler = DDIMScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
        )
        vae = self.dummy_vae
        bert = self.dummy_text_encoder
        tokenizer = CLIPTokenizer.from_pretrained("hf-internal-testing/tiny-random-clip")
        sd_pipe = StableDiffusionPipeline(
            unet=unet,
            scheduler=scheduler,
            vae=vae,
            text_encoder=bert,
            tokenizer=tokenizer,
            safety_checker=None,
            feature_extractor=self.dummy_extractor,
        )
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "A painting of a squirrel eating a burger"
        generator = paddle.Generator().manual_seed(0)
        output = sd_pipe([prompt], generator=generator, guidance_scale=6.0, num_inference_steps=2, output_type="np")
        image = output.images
        generator = paddle.Generator().manual_seed(0)
        image_from_tuple = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=6.0,
            num_inference_steps=2,
            output_type="np",
            return_dict=False,
        )[0]
        image_slice = image[0, -3:, -3:, -1]
        image_from_tuple_slice = image_from_tuple[0, -3:, -3:, -1]
        assert image.shape == (1, 64, 64, 3)
        expected_slice = np.array(
            [0.28519452, 0.23807159, 0.38150585, 0.21930319, 0.26092738, 0.517212, 0.2563907, 0.2503956, 0.47978917]
        )
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01
        assert np.abs(image_from_tuple_slice.flatten() - expected_slice).max() < 0.01

    def test_stable_diffusion_pndm(self):
        unet = self.dummy_cond_unet
        scheduler = PNDMScheduler(skip_prk_steps=True)
        vae = self.dummy_vae
        bert = self.dummy_text_encoder
        tokenizer = CLIPTokenizer.from_pretrained("hf-internal-testing/tiny-random-clip")
        sd_pipe = StableDiffusionPipeline(
            unet=unet,
            scheduler=scheduler,
            vae=vae,
            text_encoder=bert,
            tokenizer=tokenizer,
            safety_checker=None,
            feature_extractor=self.dummy_extractor,
        )
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "A painting of a squirrel eating a burger"
        generator = paddle.Generator().manual_seed(0)
        output = sd_pipe([prompt], generator=generator, guidance_scale=6.0, num_inference_steps=2, output_type="np")
        image = output.images
        generator = paddle.Generator().manual_seed(0)
        image_from_tuple = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=6.0,
            num_inference_steps=2,
            output_type="np",
            return_dict=False,
        )[0]
        image_slice = image[0, -3:, -3:, -1]
        image_from_tuple_slice = image_from_tuple[0, -3:, -3:, -1]
        assert image.shape == (1, 64, 64, 3)
        expected_slice = np.array(
            [0.18763152, 0.24242553, 0.36067978, 0.21772456, 0.27213728, 0.5194623, 0.2227565, 0.2217454, 0.4453961]
        )
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01
        assert np.abs(image_from_tuple_slice.flatten() - expected_slice).max() < 0.01

    def test_stable_diffusion_no_safety_checker(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            "hf-internal-testing/tiny-stable-diffusion-lms-pipe", safety_checker=None
        )
        assert isinstance(pipe, StableDiffusionPipeline)
        assert isinstance(pipe.scheduler, LMSDiscreteScheduler)
        assert pipe.safety_checker is None
        image = pipe("example prompt", num_inference_steps=2).images[0]
        assert image is not None
        with tempfile.TemporaryDirectory() as tmpdirname:
            pipe.save_pretrained(tmpdirname)
            pipe = StableDiffusionPipeline.from_pretrained(tmpdirname, from_diffusers=False)
        assert pipe.safety_checker is None
        image = pipe("example prompt", num_inference_steps=2).images[0]
        assert image is not None

    def test_stable_diffusion_fp16(self):
        """Test that stable diffusion works with fp16"""
        unet = self.dummy_cond_unet
        scheduler = PNDMScheduler(skip_prk_steps=True)
        vae = self.dummy_vae
        bert = self.dummy_text_encoder
        tokenizer = CLIPTokenizer.from_pretrained("hf-internal-testing/tiny-random-clip")
        unet = unet.to(dtype=paddle.float16)
        vae = vae.to(dtype=paddle.float16)
        bert = bert.to(dtype=paddle.float16)
        sd_pipe = StableDiffusionPipeline(
            unet=unet,
            scheduler=scheduler,
            vae=vae,
            text_encoder=bert,
            tokenizer=tokenizer,
            safety_checker=None,
            feature_extractor=self.dummy_extractor,
        )
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "A painting of a squirrel eating a burger"
        image = sd_pipe([prompt], num_inference_steps=2, output_type="np").images
        assert image.shape == (1, 64, 64, 3)


@nightly
@require_paddle_gpu
class SafeDiffusionPipelineIntegrationTests(unittest.TestCase):
    def tearDown(self):
        super().tearDown()
        gc.collect()
        paddle.device.cuda.empty_cache()

    def test_harm_safe_stable_diffusion(self):
        sd_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
        sd_pipe.scheduler = LMSDiscreteScheduler.from_config(sd_pipe.scheduler.config)
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "portrait of girl with smokey eyes makeup in abandoned hotel, grange clothes, redshift, wide high angle coloured polaroid photograph with flash, kodak film, hyper real, stunning moody cinematography, with anamorphic lenses, by maripol, fallen angels by wong kar - wai, style of suspiria and neon demon and children from bahnhof zoo, detailed "
        seed = 4003660346
        guidance_scale = 7
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=0,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = [0.2278, 0.2231, 0.2249, 0.2333, 0.2303, 0.1885, 0.2273, 0.2144, 0.2176]
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=2000,
            sld_warmup_steps=7,
            sld_threshold=0.025,
            sld_momentum_scale=0.5,
            sld_mom_beta=0.7,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = [0.2383, 0.2276, 0.236, 0.2192, 0.2186, 0.2053, 0.1971, 0.1901, 0.1719]
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01

    def test_nudity_safe_stable_diffusion(self):
        sd_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", safety_checker=None)
        sd_pipe.scheduler = LMSDiscreteScheduler.from_config(sd_pipe.scheduler.config)
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "padme amidala taking a bath artwork, safe for work, no nudity"
        seed = 2734971755
        guidance_scale = 7
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=0,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = [0.3502, 0.3622, 0.3396, 0.3642, 0.3478, 0.3318, 0.35, 0.3348, 0.3297]
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=2000,
            sld_warmup_steps=7,
            sld_threshold=0.025,
            sld_momentum_scale=0.5,
            sld_mom_beta=0.7,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = [0.5531, 0.5206, 0.4895, 0.5156, 0.5182, 0.4751, 0.4802, 0.4803, 0.4443]
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01

    def test_nudity_safetychecker_safe_stable_diffusion(self):
        sd_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        sd_pipe.set_progress_bar_config(disable=None)
        prompt = "the four horsewomen of the apocalypse, painting by tom of finland, gaston bussiere, craig mullins, j. c. leyendecker"
        seed = 1044355234
        guidance_scale = 12
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=0,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 1e-07
        generator = paddle.Generator().manual_seed(seed=seed)
        output = sd_pipe(
            [prompt],
            generator=generator,
            guidance_scale=guidance_scale,
            num_inference_steps=50,
            output_type="np",
            width=512,
            height=512,
            sld_guidance_scale=2000,
            sld_warmup_steps=7,
            sld_threshold=0.025,
            sld_momentum_scale=0.5,
            sld_mom_beta=0.7,
        )
        image = output.images
        image_slice = image[0, -3:, -3:, -1]
        expected_slice = np.array([0.5818, 0.6285, 0.6835, 0.6019, 0.625, 0.6754, 0.6096, 0.6334, 0.6561])
        assert image.shape == (1, 512, 512, 3)
        assert np.abs(image_slice.flatten() - expected_slice).max() < 0.01
