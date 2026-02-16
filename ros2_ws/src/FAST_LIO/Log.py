# After running your SLAM system
cd ~/ros2_ws/src/FAST_LIO/Log

# Create Python script to analyze alphas
python3 -c "
import numpy as np
import matplotlib.pyplot as plt

# Load alpha values from file (you'll need to save them)
# For now, let's create a simple simulation
alphas = np.random.beta(2, 5, 10000)  # Simulated data

plt.figure(figsize=(10, 6))
plt.hist(alphas, bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(x=0.3, color='red', linestyle='--', label='P2PL Heavy (<0.3)')
plt.axvline(x=0.7, color='green', linestyle='--', label='P2P Heavy (>0.7)')
plt.xlabel('Alpha (0=P2PL heavy, 1=P2P heavy)')
plt.ylabel('Frequency')
plt.title('Adaptive Weight Distribution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('alpha_distribution.png')
print('Saved alpha_distribution.png')
"
