from pydub import AudioSegment
from pydub.generators import Sine

# 创建一个循环背景音乐，简单三和弦叠加
duration_ms = 10000  # 10秒循环音乐

# 三个音调叠加
tone1 = Sine(261.63).to_audio_segment(duration=duration_ms)  # C4
tone2 = Sine(329.63).to_audio_segment(duration=duration_ms)  # E4
tone3 = Sine(392.00).to_audio_segment(duration=duration_ms)  # G4

# 叠加三和弦
background_music = tone1.overlay(tone2).overlay(tone3)

# 导出为mp3
background_music.export("background.mp3", format="mp3")
print("background.mp3生成完成！")
