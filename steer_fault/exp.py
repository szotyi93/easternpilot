import pickle
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# cp.vl["EPS_STATUS"]['LKA_STATE'] status meanings
# 0: stopped? in park? it's 0 when vehicle first starts

# 1: steer req is 0, torque is not being commanded or applied. generally ok and fault-free
# 5: engaged and applying torque, no faults

# 9: steer fault ocurred, not applying torque for duration. 200 - 4 frames of 9 after fault

# 21: unknown, but status has been 21 rarely
# 25: on rising edge of a steering fault, occurs for 4 frames

ok_states = [0, 1, 5]
after_fault = 9

with open('data', 'rb') as f:
  data = pickle.load(f)

data = [l for s in data for l in s]  # flatten

# for idx, line in enumerate(data):
#   line['angle_steers'] = line['can']['angle_steers']
#   if idx > 0:
#     line['prev_angle_steers'] = data[idx - 1]['angle_steers']

# del data[0]

faults = []
non_faults = []
look_ahead = 0.25  # in seconds

for i, line in enumerate(data):
  line['angle_steers'] = line['can']['angle_steers']
  if i + look_ahead * 100 >= len(data):
    continue
  if line['can']['lka_state'] == 5 and data[i + 1]['can']['lka_state'] == 25:  # catch faults only at frame before rising edge
    faults.append(line)
  elif line['can']['lka_state'] == 5 and 25 not in [data[i + la + 1]['can']['lka_state'] for la in range(int(look_ahead * 100))]:  # gather samples where fault does not occur in x seconds
    non_faults.append(line)


print('{} faults, {} non-faults'.format(len(faults), len(non_faults)))


def fault_check(sample):
  # return abs(sample['angle_rate']) > 100
  # return (sample['angle_steers'] < 0 < sample['angle_rate'] or sample['angle_steers'] > 0 > sample['angle_rate']) and abs(sample['angle_rate']) > 100
  # return abs(sample['angle_steers']) < 100 and abs(sample['angle_rate']) > 100
  # return (((sample['angle_steers'] < 0 < sample['angle_steers'] + sample['angle_rate'] * 0.1) or
  #             (sample['angle_steers'] > 0 > sample['angle_steers'] + sample['angle_rate'] * 0.1)) and abs(sample['can']['torque_cmd']) > 400) or \
  #           (abs(sample['angle_steers']) > 20 and abs(sample['can']['torque_cmd']) > 400 and sample['can']['torque_cmd'] * sample['angle_steers'] < 0)
  return abs(sample['can']['torque_cmd']) > 400 and abs(sample['angle_rate']) > 400

fault_results = list(map(fault_check, faults))
non_fault_results = list(map(fault_check, non_faults))

print('This check correctly caught {} of {} faults ({}%)'.format(fault_results.count(True), len(faults), round(fault_results.count(True) / len(faults) * 100, 2)))
print('This check incorrectly caught {} of {} non faults ({}%)'.format(non_fault_results.count(True), len(non_faults), round(non_fault_results.count(True) / len(non_faults) * 100, 2)))

# lka_states = [line['can']['lka_state'] for sec in data for line in sec]

fig, ax = plt.subplots()
x = [abs(f['angle_steers']) for f in faults]
y = [abs(f['angle_rate']) for f in faults]


scale = [min([f['can']['torque_cmd'] for f in faults]), max([f['can']['torque_cmd'] for f in faults])]
z = [f['can']['torque_cmd'] for f in faults]

for i, txt in enumerate(z):
  print(txt)
  ax.annotate(txt, (x[i] + 2, y[i]), size=9)

x = np.abs(x)
y = np.abs(y)

ax.scatter(x, y, c=np.interp(z, scale, [0, 1]), cmap='gray')

x = [abs(f['angle_steers']) for f in non_faults]
y = [abs(f['angle_rate']) for f in non_faults]
ax.scatter(x, y, c='red', s=1)


# ax.scatter(np.abs(z), np.abs(y))
plt.xlabel('angle')
plt.ylabel('rate')
# plt.ylim(0, 600)

# sns.distplot([f['angle_rate'] for f in faults], bins=27)
# sns.distplot([f['angle_steers'] for f in faults], bins=27)
