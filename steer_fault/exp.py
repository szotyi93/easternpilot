import pickle

# cp.vl["EPS_STATUS"]['LKA_STATE'] status meanings
# 1: steer req is 0, torque is not being commanded or applied. generally ok and fault-free
# 5: engaged and applying torque, no faults

# 9: steer fault ocurred, not applying torque for duration. 200 - 4 frames of 9 after fault

# 21: unknown, but status has been 21 rarely
# 25: on rising edge of a steering fault, occurs for 4 frames

with open('data', 'rb') as f:
  data = pickle.load(f)

lka_states = [line['can']['lka_state'] for sec in data for line in sec]
