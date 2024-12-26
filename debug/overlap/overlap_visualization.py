import matplotlib.pyplot as plt

def main():
    # Data for visualization
    r1_start = 100
    r1_end = 200  # r1send
    r2_start = 150
    r2_end = 250

    # Calculate overlap range based on the logic
    overlap_range = max(0, min(r1_end, r2_end) - max(r1_start, r2_start))

    # Create a figure and axis for visualization
    fig, ax = plt.subplots(figsize=(8, 2))

    # Draw r1 and r2 as horizontal lines
    ax.plot([r1_start, r1_end], [1, 1], label="r1 (100-200)", color="blue", linewidth=6, alpha=0.6)
    ax.plot([r2_start, r2_end], [1.5, 1.5], label="r2 (150-250)", color="green", linewidth=6, alpha=0.6)

    # Highlight the overlap region
    if overlap_range > 0:
        ax.plot([max(r1_start, r2_start), min(r1_end, r2_end)], [1.25, 1.25], label="Overlap (50)", color="red", linewidth=8)

    # Configure the plot
    ax.set_xlim(80, 270)
    ax.set_ylim(0.5, 2)
    ax.set_xticks(range(80, 271, 20))
    ax.set_yticks([])
    ax.axhline(y=1.25, color="black", linestyle="--", linewidth=0.5)
    ax.set_xlabel("Sequence Position")
    ax.set_title("Visualization of Overlap Range")
    ax.legend(loc="upper left")
    ax.grid(axis="x", linestyle="--", alpha=0.6)

    # Show the plot
    plt.tight_layout()
    # plt.show()
    plt.savefig("overlap_range.png")

if __name__ == "__main__":
    main()
