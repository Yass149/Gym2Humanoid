from pathlib import Path
import matplotlib.pyplot as plt
import json

motion_file = Path("data/14_06.amc")

with motion_file.open("r") as f:
    lines = f.readlines()

frames = []

current_frame = None

for line in lines:
    line = line.strip()

    if not line:
        continue

    if line.isdigit():
        if current_frame is not None:
            frames.append(current_frame)

        current_frame = {"frame": int(line)}
        continue

    if current_frame is not None:
        parts = line.split()
        joint_name = parts[0]
        values = [float(value) for value in parts[1:]]
        current_frame[joint_name] = values

if current_frame is not None:
    frames.append(current_frame)

fps = 120

times = []
right_knee = []
left_knee = []

for frame in frames:
    times.append((frame["frame"] - 1) / fps)
    right_knee.append(frame["rtibia"][0])
    left_knee.append(frame["ltibia"][0])

start_frame = 1081
end_frame = 1309

squat_frames = []
with open("outputs/squat_01.json", "w") as f:
    json.dump(squat_frames, f, indent=2)

print("Saved squat to outputs/squat_01.json")

for frame in frames:
    if start_frame <= frame["frame"] <= end_frame:
        squat_frames.append(frame)

print("Squat frames:", len(squat_frames))
print("Start frame:", squat_frames[0]["frame"])
print("End frame:", squat_frames[-1]["frame"])

plt.plot(times, right_knee, label="Right knee")
plt.plot(times, left_knee, label="Left knee")

plt.xlabel("Time (seconds)")
plt.ylabel("Knee flexion")
plt.title("Knee motion - CMU 14_06")
plt.legend()

plt.xlim(8, 14)
plt.savefig("outputs/knee_flexion_squat_zoom.png")
plt.show()