import os
import numpy as np
import matplotlib.pyplot as plt

# 기본 설정
sampling_rate = 20e9  # 20GHz 샘플링 주파수
num_points = int(5e5)  # 데이터 포인트 개수
num_waveforms = 10  # 생성할 파형 개수
output_dir = "/Volumes/Ohbin_SSD/UROP/virtual_trace"  # 저장 디렉토리

# 저장 디렉토리 생성
os.makedirs(output_dir, exist_ok=True)

# 시간 축 생성
t = np.linspace(0, num_points / sampling_rate, num_points, endpoint=False)

# 기준 파형 생성
np.random.seed(42)  # 재현 가능성을 위한 랜덤 시드
num_frequencies = 10  # 기준 파형의 주파수 성분 개수
frequencies = np.random.uniform(0, sampling_rate / 2, num_frequencies)  # 0~20GHz
amplitudes = np.random.uniform(0.1, 1, num_frequencies)  # 진폭
phases = np.random.uniform(0, 2 * np.pi, num_frequencies)  # 위상

reference_waveform = np.zeros_like(t)
for f, a, p in zip(frequencies, amplitudes, phases):
    reference_waveform += a * np.sin(2 * np.pi * f * t + p)

# 기준 파형 저장
np.save(os.path.join(output_dir, "reference_waveform.npy"), reference_waveform)

# 기준 파형 플롯
plt.figure(figsize=(12, 6))
plt.plot(t[:100], reference_waveform[:100], label="Reference Waveform", linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Reference Waveform")
plt.legend()
plt.grid()
plt.show()

# jitter 적용한 파형 생성 및 저장
plt.figure(figsize=(12, 6))
for i in range(num_waveforms):
    # x축 jitter: 샘플 위치 흔들림
    shifts = np.random.randint(-5, 5, size=num_points)  # -5 ~ 5 샘플 범위에서 이동
    jittered_waveform = np.zeros_like(reference_waveform)
    for j, shift in enumerate(shifts):
        shifted_index = j + shift
        if 0 <= shifted_index < num_points:
            jittered_waveform[shifted_index] = reference_waveform[j]

    # y축 jitter: 진폭에 잡음 추가
    noise = 0.05 * np.random.randn(num_points)  # 가우시안 잡음
    jittered_waveform += noise

    # 파일 저장
    filename = os.path.join(output_dir, f"trace_{i}.npy")
    np.save(filename, jittered_waveform)
    plt.plot(t[:100], jittered_waveform[:100], label=f"Waveform {i+1}", alpha=0.7)  # 일부 샘플 시각화
    print(f"Saved jittered waveform {i+1}/{num_waveforms} to {filename}")

plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Jittered Waveforms")
plt.legend()
plt.grid()
plt.show()