from tensorflow import keras
from stable_diffusion_tensorflow.stable_diffusion import StableDiffusion
import argparse
from PIL import Image
from PIL.PngImagePlugin import PngInfo

parser = argparse.ArgumentParser()

parser.add_argument(
    "--prompt",
    type=str,
    nargs="?",
    default="DSLR photograph of a beautiful nature scenery, with waterfall, clear water, and trees",
    help="the prompt to rdner",
)

parser.add_argument(
    "--negative-prompt",
    type=str,
    help="the negative prompt to use (if any)",
)

parser.add_argument(
    "--output", type=str,
    default="output.png",
    nargs="?",
    help="where to save the output image"
)

parser.add_argument(
    "--H",
    type=int,
    default=512,
    help="image height, in pixels",
)

parser.add_argument(
    "--W",
    type=int,
    default=512,
    help="image width, in pixels",
)

parser.add_argument(
    "--scale",
    type=float,
    default=7.5,
    help="unconditional guidance scale: eps = eps(x, empty) + scale * (eps(x, cond) - eps(x, empty))",
)

parser.add_argument(
    "--steps", type=int, default=50, help="number of ddim sampling steps"
)

parser.add_argument(
    "--seed",
    type=int,
    help="optionally specify a seed integer for reproducible results",
)

parser.add_argument(
    "--mp",
    default=False,
    action="store_true",
    help="Enable mixed precision (fp16 computation)",
)

args = parser.parse_args()

if args.mp:
    print("using mixed precision")
    keras.mixed_precision.set_global_policy("mixed_float16")

generator = StableDiffusion(img_height=args.H, img_width=args.W, jit_compile=False)
img = generator.generate(
    args.prompt,
    negative_prompt=args.negative_prompt,
    num_steps=args.steps,
    unconditional_guidance_scale=args.scale,
    temperature=1,
    batch_size=1,
    seed=args.seed,
)

pnginfo = PngInfo()
pnginfo.add_text("prompt", args.prompt)
Image.fromarray(img[0].save(args.output, pnginfo=pnginfo))
print(f"saved at {args.output}")
