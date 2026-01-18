from pydub import AudioSegment
import numpy as np

# 参数
duration_ms = 300  # 音效时长 300ms
freq = 600         # 音调频率

# 采样参数
sample_rate = 44100
t = np.linspace(0, duration_ms/1000, int(sample_rate*duration_ms/1000), False)

# 生成简单的正弦波
tone = np.sin(freq * 2 * np.pi * t)

# 生成快速衰减
tone *= np.exp(-5 * t)

# 转换为16位PCM
audio = (tone * 32767).astype(np.int16)

# 创建AudioSegment对象
hit_sound = AudioSegment(
    audio.tobytes(),
    frame_rate=sample_rate,
    sample_width=2,
    channels=1
)

# 导出音效
hit_sound.export("hit.wav", format="wav")
print("hit.wav生成完成！")
