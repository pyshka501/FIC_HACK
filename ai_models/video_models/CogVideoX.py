import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video

pipe = CogVideoXPipeline.from_pretrained(
        "THUDM/CogVideoX-5b",
        torch_dtype=torch.bfloat16
    )

pipe.enable_model_cpu_offload()
pipe.vae.enable_tiling()

def generate_video(prompt: str, output_path: str = "output.mp4") -> str:
    global pipe

    video = pipe(
        prompt=prompt,
        num_videos_per_prompt=1,
        num_inference_steps=50,
        num_frames=49,
        guidance_scale=6,
        generator=torch.Generator(device="cuda").manual_seed(42),
    ).frames[0]

    export_to_video(video, output_path, fps=8)

    return output_path
if __name__ == "__main__":
    # Пример использования функции:
    prompt = "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest..."
    file_path = generate_video(prompt)
    print(f"Video saved at: {file_path}")


# prompt = "A panda, dressed in a small, red jacket and a tiny hat, sits on a wooden stool in a serene bamboo forest. The panda's fluffy paws strum a miniature acoustic guitar, producing soft, melodic tunes. Nearby, a few other pandas gather, watching curiously and some clapping in rhythm. Sunlight filters through the tall bamboo, casting a gentle glow on the scene. The panda's face is expressive, showing concentration and joy as it plays. The background includes a small, flowing stream and vibrant green foliage, enhancing the peaceful and magical atmosphere of this unique musical performance."
#
# pipe = CogVideoXPipeline.from_pretrained(
#     "THUDM/CogVideoX-5b",
#     torch_dtype=torch.bfloat16
# )
#
# pipe.enable_model_cpu_offload()
# pipe.vae.enable_tiling()
#
# video = pipe(
#     prompt=prompt,
#     num_videos_per_prompt=1,
#     num_inference_steps=50,
#     num_frames=49,
#     guidance_scale=6,
#     generator=torch.Generator(device="cuda").manual_seed(42),
# ).frames[0]
#
# export_to_video(video, "output.mp4", fps=8)
