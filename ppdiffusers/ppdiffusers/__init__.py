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
# flake8: noqa

from . import patches
from .configuration_utils import ConfigMixin
from .utils import (
    OptionalDependencyNotAvailable,
    is_einops_available,
    is_fastdeploy_available,
    is_inflect_available,
    is_invisible_watermark_available,
    is_k_diffusion_available,
    is_k_diffusion_version,
    is_librosa_available,
    is_note_seq_available,
    is_paddle_available,
    is_paddle_version,
    is_paddlenlp_available,
    is_paddlenlp_version,
    is_paddlesde_available,
    is_ppxformers_available,
    is_safetensors_available,
    is_scipy_available,
    is_torch_available,
    is_unidecode_available,
    is_visualdl_available,
    logging,
)
from .version import VERSION as __version__

try:
    if not is_fastdeploy_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_fastdeploy_objects import *  # noqa F403
else:
    from .pipelines import FastDeployRuntimeModel

try:
    if not is_paddle_available():
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_objects import *  # noqa F403
else:
    from .models import (
        AsymmetricAutoencoderKL,
        AutoencoderKL,
        ControlNetModel,
        LitEma,
        LVDMAutoencoderKL,
        LVDMUNet3DModel,
        ModelMixin,
        MultiAdapter,
        PriorTransformer,
        T2IAdapter,
        T5FilmDecoder,
        Transformer2DModel,
        UNet1DModel,
        UNet2DConditionModel,
        UNet2DModel,
        UNet3DConditionModel,
        VQModel,
    )
    from .optimization import (
        get_constant_schedule,
        get_constant_schedule_with_warmup,
        get_cosine_schedule_with_warmup,
        get_cosine_with_hard_restarts_schedule_with_warmup,
        get_linear_schedule_with_warmup,
        get_polynomial_decay_schedule_with_warmup,
        get_scheduler,
    )
    from .pipelines import (
        AudioPipelineOutput,
        AutoPipelineForImage2Image,
        AutoPipelineForInpainting,
        AutoPipelineForText2Image,
        ConsistencyModelPipeline,
        DanceDiffusionPipeline,
        DDIMPipeline,
        DDPMPipeline,
        DiffusionPipeline,
        DiTPipeline,
        ImagePipelineOutput,
        KarrasVePipeline,
        LDMPipeline,
        LDMSuperResolutionPipeline,
        PNDMPipeline,
        RePaintPipeline,
        ScoreSdeVePipeline,
        TextPipelineOutput,
    )
    from .schedulers import (
        CMStochasticIterativeScheduler,
        DDIMInverseScheduler,
        DDIMParallelScheduler,
        DDIMScheduler,
        DDPMParallelScheduler,
        DDPMScheduler,
        DEISMultistepScheduler,
        DPMSolverMultistepInverseScheduler,
        DPMSolverMultistepScheduler,
        DPMSolverSinglestepScheduler,
        DPMSolverUniDiffuserScheduler,
        EulerAncestralDiscreteScheduler,
        EulerDiscreteScheduler,
        HeunDiscreteScheduler,
        IPNDMScheduler,
        KarrasVeScheduler,
        KDPM2AncestralDiscreteScheduler,
        KDPM2DiscreteScheduler,
        PNDMScheduler,
        RePaintScheduler,
        SchedulerMixin,
        ScoreSdeVeScheduler,
        UnCLIPScheduler,
        UniPCMultistepScheduler,
        VQDiffusionScheduler,
    )
    from .schedulers.preconfig import (
        PreconfigEulerAncestralDiscreteScheduler,
        PreconfigLMSDiscreteScheduler,
    )
    from .training_utils import EMAModel

try:
    if not (is_paddle_available() and is_scipy_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_scipy_objects import *  # noqa F403
else:
    from .schedulers import LMSDiscreteScheduler

try:
    if not (is_paddle_available() and is_paddlesde_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlesde_objects import *  # noqa F403
else:
    from .schedulers import DPMSolverSDEScheduler


try:
    if not (is_paddle_available() and is_paddlenlp_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlenlp_objects import *  # noqa F403
else:
    from .pipelines import (  # ImageTextPipelineOutput,
        AltDiffusionImg2ImgPipeline,
        AltDiffusionPipeline,
        AudioLDMPipeline,
        CycleDiffusionPipeline,
        IFImg2ImgPipeline,
        IFImg2ImgSuperResolutionPipeline,
        IFInpaintingPipeline,
        IFInpaintingSuperResolutionPipeline,
        IFPipeline,
        IFSuperResolutionPipeline,
        KandinskyCombinedPipeline,
        KandinskyImg2ImgCombinedPipeline,
        KandinskyImg2ImgPipeline,
        KandinskyInpaintCombinedPipeline,
        KandinskyInpaintPipeline,
        KandinskyPipeline,
        KandinskyPriorPipeline,
        KandinskyV22CombinedPipeline,
        KandinskyV22ControlnetImg2ImgPipeline,
        KandinskyV22ControlnetPipeline,
        KandinskyV22Img2ImgCombinedPipeline,
        KandinskyV22Img2ImgPipeline,
        KandinskyV22InpaintCombinedPipeline,
        KandinskyV22InpaintPipeline,
        KandinskyV22Pipeline,
        KandinskyV22PriorEmb2EmbPipeline,
        KandinskyV22PriorPipeline,
        LDMTextToImagePipeline,
        LVDMTextToVideoPipeline,
        LVDMUncondPipeline,
        PaintByExamplePipeline,
        SemanticStableDiffusionPipeline,
        ShapEImg2ImgPipeline,
        ShapEPipeline,
        StableDiffusionAdapterPipeline,
        StableDiffusionAttendAndExcitePipeline,
        StableDiffusionControlNetImg2ImgPipeline,
        StableDiffusionControlNetInpaintPipeline,
        StableDiffusionControlNetPipeline,
        StableDiffusionDepth2ImgPipeline,
        StableDiffusionDiffEditPipeline,
        StableDiffusionImageVariationPipeline,
        StableDiffusionImg2ImgPipeline,
        StableDiffusionInpaintPipeline,
        StableDiffusionInpaintPipelineLegacy,
        StableDiffusionInstructPix2PixPipeline,
        StableDiffusionLatentUpscalePipeline,
        StableDiffusionLDM3DPipeline,
        StableDiffusionMegaPipeline,
        StableDiffusionModelEditingPipeline,
        StableDiffusionPanoramaPipeline,
        StableDiffusionParadigmsPipeline,
        StableDiffusionPipeline,
        StableDiffusionPipelineAllinOne,
        StableDiffusionPipelineSafe,
        StableDiffusionPix2PixZeroPipeline,
        StableDiffusionSAGPipeline,
        StableDiffusionUpscalePipeline,
        StableDiffusionXLControlNetPipeline,
        StableDiffusionXLImg2ImgPipeline,
        StableDiffusionXLInpaintPipeline,
        StableDiffusionXLInstructPix2PixPipeline,
        StableDiffusionXLPipeline,
        StableUnCLIPImg2ImgPipeline,
        StableUnCLIPPipeline,
        TextToVideoSDPipeline,
        TextToVideoZeroPipeline,
        UnCLIPImageVariationPipeline,
        UnCLIPPipeline,
        UniDiffuserPipeline,
        VersatileDiffusionDualGuidedPipeline,
        VersatileDiffusionImageVariationPipeline,
        VersatileDiffusionPipeline,
        VersatileDiffusionTextToImagePipeline,
        VideoToVideoSDPipeline,
        VQDiffusionPipeline,
    )
    from .pipelines.latent_diffusion.pipeline_latent_diffusion import LDMBertModel

try:
    if not (is_paddle_available() and is_paddlenlp_available() and is_k_diffusion_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlenlp_and_k_diffusion_objects import *  # noqa F403
else:
    from .pipelines import StableDiffusionKDiffusionPipeline

try:
    if not (is_paddle_available() and is_paddlenlp_available() and is_fastdeploy_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlenlp_and_fastdeploy_objects import *  # noqa F403
else:
    from .pipelines import (
        FastDeployCycleDiffusionPipeline,
        FastDeployStableDiffusionControlNetPipeline,
        FastDeployStableDiffusionImageVariationPipeline,
        FastDeployStableDiffusionImg2ImgPipeline,
        FastDeployStableDiffusionInpaintPipeline,
        FastDeployStableDiffusionInpaintPipelineLegacy,
        FastDeployStableDiffusionMegaPipeline,
        FastDeployStableDiffusionPipeline,
        FastDeployStableDiffusionUpscalePipeline,
    )

try:
    if not (is_paddle_available() and is_librosa_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_librosa_objects import *  # noqa F403
else:
    from .pipelines import AudioDiffusionPipeline, Mel

try:
    if not (is_paddle_available() and is_paddlenlp_available() and is_note_seq_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlenlp_and_note_seq_objects import *  # noqa F403
else:
    from .pipelines import SpectrogramDiffusionPipeline

try:
    if not (is_paddle_available() and is_paddlenlp_available() and is_einops_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_paddlenlp_and_einops_objects import *  # noqa F403
else:
    from .pipelines import UniDiffuserPipeline

try:
    if not (is_paddle_available() and is_einops_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_paddle_and_einops_objects import *  # noqa F403
else:
    from .pipelines.unidiffuser import (
        UniDiffuserModel,
        UniDiffuserPipeline,
        UniDiffuserTextDecoder,
    )

try:
    if not (is_note_seq_available()):
        raise OptionalDependencyNotAvailable()
except OptionalDependencyNotAvailable:
    from .utils.dummy_note_seq_objects import *  # noqa F403
else:
    from .pipelines import MidiProcessor
