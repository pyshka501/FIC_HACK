from diffusers import DiffusionPipeline
import torch

# load both base & refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
# base.to("cuda")
# base.enable_model_cpu_offload()

refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)
# refiner.to("cuda")
# refiner.enable_model_cpu_offload()
# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 40
high_noise_frac = 0.8

prompt = "A majestic lion jumping from a big stone at night"


def sdxl_inference(prompt, num_inference_steps = 40, denoising_end= 0.8):
    image = base(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        denoising_end=denoising_end,
        output_type="latent",
    ).images
    image = refiner(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        denoising_start=denoising_end,
        image=image,
    ).images[0]
    pil_image = Image.fromarray((image * 255).astype('uint8'))
    return pil_image

if __name__ == "__main__":
    sdxl_inference(prompt)
    # run both experts

    import matplotlib.pyplot as plt
    from PIL import Image


    generated_image = sdxl_inference(prompt)
    pil_image = Image.fromarray((generated_image * 255).astype('uint8'))

    # Вывод изображения с использованием matplotlib
    plt.imshow(pil_image)
    plt.axis('off')
    plt.show()



