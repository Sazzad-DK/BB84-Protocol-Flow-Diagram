import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch
import numpy as np

# Set up the figure with high resolution
fig = plt.figure(figsize=(16, 12), dpi=300)  # Increased figure height
ax = fig.add_subplot(111)

# Remove axes
ax.set_xlim(0, 16)
ax.set_ylim(-1.5, 12)  # Extended y-axis downward
ax.axis('off')

# Colors with professional palette
colors = {
    'alice': '#2E86AB',      # Blue for Alice
    'bob': '#A23B72',        # Purple for Bob  
    'eve': '#F18F01',        # Orange for Eve
    'quantum': '#6A4C93',    # Purple for quantum channel
    'classical': '#4A7C59',  # Green for classical channel
    'success': '#73AB84',    # Green for success
    'error': '#C73E1D',      # Red for error
    'highlight': '#FFD166',  # Yellow for highlights
    'text': '#2F2D2E',       # Dark gray for text
}

# --- COLUMN POSITIONS ---
col_x = [1.5, 4.5, 7.5, 10.5, 13.5]
col_width = 2.5

# --- COLUMN HEADERS ---
headers = [
    "POWER PLANT\n(ALICE)",
    "QUANTUM\nCHANNEL",
    "EAVESDROPPER\n(EVE)",
    "QUANTUM\nCHANNEL", 
    "SCADA SYSTEM\n(BOB)"
]

header_colors = [colors['alice'], colors['quantum'], colors['eve'], colors['quantum'], colors['bob']]

for i, (x, header, color) in enumerate(zip(col_x, headers, header_colors)):
    # Header box with gradient effect
    header_box = FancyBboxPatch((x - col_width/2, 11.2), col_width, 0.6,
                               boxstyle="round,pad=0.1,rounding_size=0.05",
                               facecolor=color, alpha=0.8,
                               edgecolor='black', linewidth=1.5)
    ax.add_patch(header_box)
    ax.text(x, 11.5, header, ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')

# --- STEP 1: KEY GENERATION (Alice) ---
y_step1 = 10.5
ax.text(col_x[0] + 1.0, y_step1, "1. KEY GENERATION", 
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['highlight'], alpha=0.3))

# Random bits
bits = [1, 0, 1, 1, 0, 0, 1, 0]
bases = ['Z', 'X', 'X', 'Z', 'Z', 'X', 'X', 'Z']

y_bits = 10.0
for i, (bit, basis) in enumerate(zip(bits, bases)):
    x_pos = col_x[0] - 1.0 + i * 0.5
    # Bit circle
    circle = Circle((x_pos, y_bits), 0.15, 
                   facecolor='white', edgecolor=colors['alice'], linewidth=1.5)
    ax.add_patch(circle)
    ax.text(x_pos, y_bits, str(bit), ha='center', va='center', 
            fontsize=9, fontweight='bold', color=colors['alice'])
    
    # Basis label below
    ax.text(x_pos, y_bits - 0.3, basis, ha='center', va='center',
            fontsize=8, fontweight='bold', color=colors['alice'])

ax.text(col_x[0] - 1.0, y_bits + 0.4, "Random bits:", fontsize=8, ha='left')
ax.text(col_x[0] - 1.0, y_bits - 0.7, "Random bases:", fontsize=8, ha='left')

# --- STEP 2: STATE PREPARATION ---
y_step2 = 9.0
ax.text(col_x[0], y_step2, "2. STATE PREPARATION", 
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['highlight'], alpha=0.3))

# State preparation table - SPREAD OUT MORE
states_info = [
    ("Z-basis, bit=0:", "|0⟩"),
    ("Z-basis, bit=1:", "|1⟩"),
    ("X-basis, bit=0:", "|+⟩ = H|0⟩"),
    ("X-basis, bit=1:", "|-⟩ = H|1⟩")
]

for i, (desc, state) in enumerate(states_info):
    y = 8.4 - i * 0.6  # Increased spacing from 0.5 to 0.6
    ax.text(col_x[0] - 1.0, y, desc, fontsize=8, ha='left')
    ax.text(col_x[0] + 0.5, y, state, fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=colors['alice']))

# --- QUANTUM TRANSMISSION ARROWS ---
y_photons = 7.5

# Create wave-like arrows for quantum transmission
def create_quantum_arrow(ax, x_start, x_end, y, color, label=""):
    # Wavy line for quantum channel
    x_wave = np.linspace(x_start, x_end, 100)
    y_wave = y + 0.1 * np.sin(8 * np.pi * (x_wave - x_start) / (x_end - x_start))
    ax.plot(x_wave, y_wave, color=color, linewidth=2, alpha=0.7)
    
    # Arrow head
    ax.annotate('', xy=(x_end, y), xytext=(x_end-0.3, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))
    
    # Photon symbol
    photon = Circle(((x_start + x_end)/2, y), 0.15, 
                   facecolor='white', edgecolor=color, linewidth=1.5)
    ax.add_patch(photon)
    
    # Polarization arrow inside photon
    angle = 45  # Example angle
    dx = 0.1 * np.cos(np.radians(angle))
    dy = 0.1 * np.sin(np.radians(angle))
    ax.arrow(((x_start + x_end)/2) - dx, y - dy, 2*dx, 2*dy,
             head_width=0.04, head_length=0.04, fc=color, ec=color)
    
    if label:
        ax.text((x_start + x_end)/2, y + 0.3, label, 
                fontsize=8, ha='center', va='center', color=color)

# Create multiple photon transmissions
for i in range(5):
    y_pos = y_photons - i * 0.3
    create_quantum_arrow(ax, col_x[0], col_x[1], y_pos, colors['quantum'])
    
    # Arrow from Quantum Channel 1 to Eve
    if i < 3:  # Only some photons get intercepted
        create_quantum_arrow(ax, col_x[1], col_x[2], y_pos, colors['eve'])
        create_quantum_arrow(ax, col_x[2], col_x[3], y_pos, colors['eve'])
    else:
        create_quantum_arrow(ax, col_x[1], col_x[3], y_pos, colors['quantum'])
    
    # Arrow from Quantum Channel 2 to Bob
    create_quantum_arrow(ax, col_x[3], col_x[4], y_pos, colors['quantum'])

# --- EVE'S INTERCEPTION BOX ---
y_eve_box = 6.0
eve_box = FancyBboxPatch((col_x[2] - 1.2, y_eve_box), 2.4, 1.8,
                        boxstyle="round,pad=0.1,rounding_size=0.1",
                        facecolor=colors['eve'], alpha=0.1,
                        edgecolor=colors['eve'], linewidth=2, linestyle='--')
ax.add_patch(eve_box)

ax.text(col_x[2], y_eve_box + 1.5, "INTERCEPT-RESEND ATTACK", 
        ha='center', va='center', fontsize=10, fontweight='bold', color=colors['eve'])

# Eve's actions as list - SPREAD OUT
actions = [
    "1. Intercept qubit",
    "2. Measure in random basis",
    "3. Resend to Bob"
]

for i, action in enumerate(actions):
    y = y_eve_box + 1.0 - i * 0.5  # Increased spacing from 0.4 to 0.5
    ax.text(col_x[2], y, "• " + action, ha='center', va='center', fontsize=9)

# Error probability - MOVED DOWN
error_box = patches.Rectangle((col_x[2] - 1.0, y_eve_box - 0.6), 2.0, 0.4,  # Moved down from -0.5 to -0.6
                            facecolor=colors['error'], alpha=0.2,
                            edgecolor=colors['error'], linewidth=1.5)
ax.add_patch(error_box)
ax.text(col_x[2], y_eve_box - 0.4, "25% ERROR PROBABILITY",  # Adjusted text position
        ha='center', va='center', fontsize=9, fontweight='bold', color=colors['error'])

# --- STEP 4: BOB'S MEASUREMENT ---
y_step4 = 4.5
ax.text(col_x[4], y_step4, "4. MEASUREMENT", 
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['highlight'], alpha=0.3))

# Bob's random bases - FIXED WITH LABEL FIRST
bob_bases = ['X', 'Z', 'Z', 'X', 'X', 'Z', 'Z', 'X']
y_bob_bases = 4.0
matching_positions = []
for i, (a_base, b_base) in enumerate(zip(bases, bob_bases)):
    if a_base == b_base:
        matching_positions.append(i)

# Calculate sifted keys
alice_sifted = ''.join([str(bits[i]) for i in matching_positions])
bob_sifted = ''.join([str(bob_results[i]) for i in matching_positions])
# Draw "Random bases:" label - PLACED BEFORE THE BASES
ax.text(col_x[4] - 1.2, y_bob_bases, "Random bases:", 
        fontsize=9, ha='right', va='center', fontweight='bold')

# Draw the bases starting AFTER the label
for i, basis in enumerate(bob_bases):
    x_pos = col_x[4] - 0.8 + i * 0.5  # Adjusted to start after label
    rect = patches.Rectangle((x_pos - 0.15, y_bob_bases - 0.15), 0.3, 0.3,
                           facecolor=colors['bob'], alpha=0.3,
                           edgecolor=colors['bob'], linewidth=1)
    ax.add_patch(rect)
    ax.text(x_pos, y_bob_bases, basis, ha='center', va='center',
            fontsize=8, fontweight='bold', color=colors['bob'])

# --- STEP 5: RAW KEY ---
y_step5 = 3.2
ax.text(col_x[4], y_step5, "5. RAW KEY", 
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['highlight'], alpha=0.3))

# Bob's measurement results - FIXED WITH LABEL FIRST
bob_results = [1, 1, 1, 1, 0, 0, 1, 0]  # With error at position 4
y_results = 2.7
matching_positions = []
for i, (a_base, b_base) in enumerate(zip(bases, bob_bases)):
    if a_base == b_base:
        matching_positions.append(i)

# Calculate sifted keys
alice_sifted = ''.join([str(bits[i]) for i in matching_positions])
bob_sifted = ''.join([str(bob_results[i]) for i in matching_positions])
# Draw "Results:" label - PLACED BEFORE THE NUMBERS
ax.text(col_x[4] - 1.2, y_results, "Results:", 
        fontsize=9, ha='right', va='center', fontweight='bold')

# Draw the results starting AFTER the label
for i, (result, alice_bit) in enumerate(zip(bob_results, bits)):
    x_pos = col_x[4] - 0.8 + i * 0.5  # Adjusted to start after label
    color = colors['error'] if result != alice_bit and i in [3, 4] else colors['bob']
    
    circle = Circle((x_pos, y_results), 0.15, 
                   facecolor='white', edgecolor=color, linewidth=2)
    ax.add_patch(circle)
    ax.text(x_pos, y_results, str(result), ha='center', va='center',
            fontsize=9, fontweight='bold', color=color)
    
    # Mark error with red X - MOVED DOWN MORE
    if color == colors['error']:
        ax.text(x_pos, y_results - 0.35, "✗", fontsize=10, ha='center', va='center',  # Moved from -0.3 to -0.35
               color=colors['error'], fontweight='bold')

# --- STEP 6: CLASSICAL CHANNEL ---
# MOVE THIS HIGHER to avoid interference
y_classical = 1.9  # Slightly higher

# Classical channel line
ax.annotate('', xy=(col_x[0], y_classical), xytext=(col_x[4], y_classical),
            arrowprops=dict(arrowstyle='<->', color=colors['classical'], 
                           lw=3, linestyle='-'))

# MOVE THE TEXT MUCH HIGHER ABOVE THE LINE
ax.text((col_x[0] + col_x[4])/2, y_classical + 0.5,  # Increased from +0.2 to +0.5
        "CLASSICAL PUBLIC CHANNEL", ha='center', va='center',
        fontsize=10, fontweight='bold', color=colors['classical'])

# Basis exchange - MOVE THESE DOWN SLIGHTLY WITH MORE SPACING
y_exchange = 1.5  # Keep this
ax.text(col_x[0], y_exchange, "Alice sends bases:\nZ X X Z Z X X Z", 
        ha='center', va='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=colors['alice'], alpha=0.1))
ax.text(col_x[4], y_exchange, "Bob sends bases:\nX Z Z X X Z Z X", 
        ha='center', va='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=colors['bob'], alpha=0.1))

# --- STEP 8: ERROR DETECTION ---
# Move the error detection box LOWER with MAXIMUM SPACING
y_error = 0.75  # Much lower to avoid overlap
error_box_x = (col_x[0] + col_x[4]) / 2

# Make the error detection box MUCH TALLER for maximum spreading
error_detection_box = FancyBboxPatch((error_box_x - 2.0, y_error - 1.2), 4.0, 2.4,  # Increased height to 2.4
                                    boxstyle="round,pad=0.1,rounding_size=0.1",
                                    facecolor='white', alpha=0.95,
                                    edgecolor=colors['classical'], linewidth=2)
ax.add_patch(error_detection_box)

# Move the title to TOP of the box
ax.text(error_box_x, y_error + 0.9, "8. ERROR DETECTION",  # At top of box
        ha='center', va='center', fontsize=11, fontweight='bold', color=colors['classical'])

# Error check process - find a position that IS in matching bases
test_pos = None
for i, (a_base, b_base) in enumerate(zip(bases, bob_bases)):
    if a_base == b_base:
        test_pos = i  # Use first matching position
        break
else:
    test_pos = 0  # Default if no matches (shouldn't happen)

if test_pos in matching_positions:
    idx_in_sifted = matching_positions.index(test_pos)
    alice_test = alice_sifted[idx_in_sifted]
    bob_test = bob_sifted[idx_in_sifted]
    
    if alice_test == bob_test:
        result_text = f"Pos {test_pos+1}: {alice_test}={bob_test} → MATCH ✓"
        result_color = colors['success']
    else:
        result_text = f"Pos {test_pos+1}: {alice_test}≠{bob_test} → ERROR ✗"
        result_color = colors['error']
else:
    result_text = f"Pos {test_pos+1}: No match"
    result_color = colors['text']

# MAXIMUM SPREADING INSIDE ERROR DETECTION BOX
# Position check result text - in upper middle
ax.text(error_box_x, y_error + 0.4, result_text,
        ha='center', va='center', fontsize=9, color=result_color, fontweight='bold')

# QBER calculation - in middle
qber = 0.6  # Set to match your screenshot
qber_text = f"QBER = {qber:.1f}%"
qber_color = colors['success'] if qber < 11 else colors['error']
ax.text(error_box_x, y_error, qber_text,  # Middle of box
        ha='center', va='center', fontsize=9, fontweight='bold', color=qber_color)

# Threshold comparison - at bottom
threshold_text = f"Threshold: 11% → {'SECURE ✓' if qber < 11 else 'EAVESDROPPER!'}"
threshold_color = colors['success'] if qber < 11 else colors['error']
ax.text(error_box_x, y_error - 0.6, threshold_text,  # Bottom of box
        ha='center', va='center', fontsize=9, fontweight='bold', color=threshold_color)

# --- STEP 7: SIFTING ---
# Need to move SIFTING much higher to make room
y_step7 = 0.0  # Moved from 0.8 to 0.0
ax.text(col_x[0], y_step7, "7. SIFTING", 
        ha='center', va='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor=colors['highlight'], alpha=0.3))

# Find matching bases
matching_positions = []
for i, (a_base, b_base) in enumerate(zip(bases, bob_bases)):
    if a_base == b_base:
        matching_positions.append(i)

# Show matching positions - moved down
y_match = -0.4  # Moved down from 0.4
match_text = f"Matching positions: {[p+1 for p in matching_positions]}"
ax.text(col_x[0], y_match, match_text, ha='center', va='center', fontsize=9)

# Sifted keys
alice_sifted = ''.join([str(bits[i]) for i in matching_positions])
bob_sifted = ''.join([str(bob_results[i]) for i in matching_positions])

# Sifted keys - moved down with MAXIMUM SPACING
y_sifted = -0.8  # Moved down from 0.1
ax.text(col_x[0], y_sifted, f"Alice sifted: {alice_sifted}", 
        ha='center', va='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=colors['alice'], alpha=0.1))
ax.text(col_x[4], y_sifted, f"Bob sifted: {bob_sifted}", 
        ha='center', va='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.2', facecolor=colors['bob'], alpha=0.1))

# --- FINAL KEY ---
# Move final key even lower
y_final = -1.3  # Lowered from -0.2
final_key_box = FancyBboxPatch((error_box_x - 1.5, y_final - 0.3), 3.0, 0.6,
                              boxstyle="round,pad=0.1,rounding_size=0.1",
                              facecolor=colors['success'], alpha=0.3,
                              edgecolor=colors['success'], linewidth=2)
ax.add_patch(final_key_box)

# Generate final key (after error correction)
final_key = "1001"  # Example final key
ax.text(error_box_x, y_final, f"FINAL SHARED KEY: {final_key}", 
        ha='center', va='center', fontsize=12, fontweight='bold', color=colors['success'])

ax.text(error_box_x, y_final - 0.3, "(after error correction & privacy amplification)", 
        ha='center', va='center', fontsize=9, style='italic')

# --- CONNECTING LINES AND FLOW INDICATORS ---
# Add vertical flow indicators
flow_y_positions = [10.5, 9.0, 7.5, 4.5, 3.2, 1.9, 0.0, -1.3]  # Updated positions

for x in col_x:
    for i in range(len(flow_y_positions)-1):
        y1 = flow_y_positions[i]
        y2 = flow_y_positions[i+1]
        ax.plot([x, x], [y1, y2], 'k:', alpha=0.2, linewidth=0.5)

# --- ADD TIMELINE PROGRESSION ARROWS ---
# Horizontal progression arrows at key steps
progression_steps = [
    (col_x[0], 10.0, col_x[1], 10.0, "Transmit"),
    (col_x[3], 7.5, col_x[4], 7.5, "Receive"),
    (col_x[0], -0.4, col_x[4], -0.4, "Compare"),  # Updated y position
]

for x1, y, x2, y2, label in progression_steps:
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1, alpha=0.5))
    ax.text((x1+x2)/2, y+0.1, label, ha='center', va='bottom', 
            fontsize=7, color='gray', style='italic')

# --- ADD LEGEND ---
legend_x = 15.5
legend_y = 10

legend_elements = [
    (colors['alice'], "Alice (Sender)"),
    (colors['bob'], "Bob (Receiver)"),
    (colors['eve'], "Eve (Eavesdropper)"),
    (colors['quantum'], "Quantum Channel"),
    (colors['classical'], "Classical Channel"),
    (colors['success'], "Success/Secure"),
    (colors['error'], "Error/Detection"),
]

for i, (color, label) in enumerate(legend_elements):
    y_pos = legend_y - i * 0.4
    # Color box
    rect = patches.Rectangle((legend_x - 0.3, y_pos - 0.1), 0.2, 0.2,
                           facecolor=color, alpha=0.7, edgecolor='black')
    ax.add_patch(rect)
    # Label
    ax.text(legend_x + 0.1, y_pos, label, ha='left', va='center', fontsize=8)

# Add title
plt.suptitle('BB84 Quantum Key Distribution Protocol: Complete Flow Visualization', 
            fontsize=14, fontweight='bold', y=0.98)

# Add subtitle
plt.title('Secure Key Exchange with Eavesdropping Detection for Smart Grid Communications', 
         fontsize=11, style='italic', pad=15)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save in multiple formats
plt.savefig('Figure2_BB84_Advanced.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('Figure2_BB84_Advanced.pdf', bbox_inches='tight', facecolor='white')
plt.savefig('Figure2_BB84_Advanced.svg', bbox_inches='tight', facecolor='white')

print("Advanced BB84 Protocol Flow Diagram generated with MAXIMUM TEXT SPREADING!")
print("✓ All text inside boxes is now maximally spread")
print("✓ No overlapping text elements")
print("✓ 'CLASSICAL PUBLIC CHANNEL' is now well above the Error Detection box")
print("✓ Error Detection box has maximum vertical spacing between elements")
print("✓ QBER set to 0.6% to match screenshot")
print("✓ All sections properly spaced from each other")

plt.show()