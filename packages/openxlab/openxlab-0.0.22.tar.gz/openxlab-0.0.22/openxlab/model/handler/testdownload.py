from openxlab.model.handler.download_file import download, download_from_url
from openxlab.model import init
from openxlab.model import wget


# inference("mmocr/SVTR", ['./demo_text_ocr.jpg'])
# download("dongxiaozhuang/digo_01", "model_1", overwrite=False)
# download("alvin123/digo_01", "model_1", overwrite=False)
# download("thomas-yanxin/MindChat-InternLM-7B", "config.json", overwrite=False)
# download("dongxiaozhuang/digo_01", "mm", overwrite=True)
# download("dongxiaozhuang/yy_001", "model_1", overwrite=True)
# wget("https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_offset_example-lora_1.0.safetensors", overwrite=True)
# wget("https://static.openxlab.org.cn/puyu/staging/9205894-7602aeab-8264-4b3a-a40c-70b2d0fd5bbe.mp4", overwrite=True)
# download_from_url("https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/model_index.json", overwrite=True)
# init(path=r'C:\\Users\\meijiawen\\automationTest\python')

download(model_repo='RenRuiZhang/sam_vit_h_4b8939',
model_name='sam_vit_h_4b8939', overwrite=True)
