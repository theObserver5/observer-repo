import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ─── DATA ─────────────────────────────────────────────────────────────────────
# 3x3 grid: rows = front-to-back (near element → far end)
# columns = left-to-right across tray
# Positions 1-3 = row 0 (near element), 4-6 = row 1 (middle), 7-9 = row 2 (far end)

fan_off = np.array([
    [46.3, 47.8, 48.6],   # positions 1, 2, 3  (near element)
    [48.7, 48.9, 48.2],   # positions 4, 5, 6  (middle)
    [46.6, 45.9, 46.4],   # positions 7, 8, 9  (far end)
])

fan_on = np.array([
    [50.6, 48.5, 45.1],   # positions 1, 2, 3  (near element/fan)
    [44.3, 41.3, 41.3],   # positions 4, 5, 6  (middle)
    [43.3, 45.0, 44.5],   # positions 7, 8, 9  (far end)
])

positions = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

row_labels = ["Near Element\n(Positions 1–3)",
              "Middle\n(Positions 4–6)",
              "Far End\n(Positions 7–9)"]
col_labels = ["Left", "Centre", "Right"]

# ─── SHARED COLOUR SCALE ──────────────────────────────────────────────────────
vmin = 40
vmax = 52

# ─── FIGURE 1: SIDE-BY-SIDE HEATMAPS ─────────────────────────────────────────
fig1, axes = plt.subplots(1, 2, figsize=(13, 5))
fig1.suptitle("Spatial Temperature Distribution — Tray Dryer (Set-point: 60°C)",
              fontsize=13, fontweight="bold", y=1.01)

datasets = [("Fan OFF — Natural Convection", fan_off),
            ("Fan ON — Forced Convection",   fan_on)]

for ax, (title, data) in zip(axes, datasets):
    im = ax.imshow(data, cmap="RdYlBu_r", vmin=vmin, vmax=vmax, aspect="auto")

    # Annotate each cell with position number and temperature
    for i in range(3):
        for j in range(3):
            ax.text(j, i,
                    f"P{positions[i, j]}\n{data[i, j]:.1f}°C",
                    ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color="white" if data[i, j] < 44 else "black")

    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_xticklabels(col_labels, fontsize=9)
    ax.set_yticklabels(row_labels, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Tray Width", fontsize=9)
    ax.set_ylabel("Tray Depth (relative to heating element)", fontsize=9)

    cbar = fig1.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Temperature (°C)", fontsize=9)

plt.tight_layout()
plt.savefig("heatmaps_side_by_side.png", dpi=200, bbox_inches="tight")
print("Saved: heatmaps_side_by_side.png")
plt.show()


# ─── FIGURE 2: BAR CHART COMPARISON ──────────────────────────────────────────
pos_labels = [f"P{i}" for i in range(1, 10)]
fan_off_flat = fan_off.flatten()
fan_on_flat  = fan_on.flatten()

x = np.arange(9)
width = 0.35

fig2, ax2 = plt.subplots(figsize=(12, 5))

bars1 = ax2.bar(x - width/2, fan_off_flat, width,
                label="Fan OFF (Natural Convection)",
                color="#4472C4", edgecolor="white", linewidth=0.6)
bars2 = ax2.bar(x + width/2, fan_on_flat, width,
                label="Fan ON (Forced Convection)",
                color="#ED7D31", edgecolor="white", linewidth=0.6)

# Set-point reference line
ax2.axhline(60, color="red", linestyle="--", linewidth=1.2, label="Set-point (60°C)")

# Zone shading
for start, end, label in [(0, 3, "Near Element"), (3, 6, "Middle"), (6, 9, "Far End")]:
    ax2.axvspan(start - 0.5, end - 0.5, alpha=0.06, color="grey")
    ax2.text((start + end - 1) / 2, 38.5, label,
             ha="center", va="bottom", fontsize=8, color="grey", style="italic")

# Value labels on bars
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7.5)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7.5)

ax2.set_xticks(x)
ax2.set_xticklabels(pos_labels, fontsize=10)
ax2.set_ylim(38, 63)
ax2.set_xlabel("Tray Position", fontsize=11)
ax2.set_ylabel("Temperature (°C)", fontsize=11)
ax2.set_title("Temperature Comparison by Position — Fan Off vs Fan On\n(Tray Dryer Set-point: 60°C)",
              fontsize=12, fontweight="bold")
ax2.legend(fontsize=10)
ax2.yaxis.set_minor_locator(ticker.MultipleLocator(1))
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("bar_chart_comparison.png", dpi=200, bbox_inches="tight")
print("Saved: bar_chart_comparison.png")
plt.show()
