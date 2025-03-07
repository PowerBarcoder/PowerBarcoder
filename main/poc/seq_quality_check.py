import matplotlib.pyplot as plt
from collections import Counter


def parse_fastq(file_path, offset=33):
    """Extract Q values from a FASTQ file."""
    q_values = []
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if (i + 1) % 4 == 0:  # Quality score line
                q_values.extend([ord(char) - offset for char in line.strip()])
    return q_values


def analyze_q_values(q_values):
    """Analyze Q values to determine if they are continuous or binned."""
    unique_q = sorted(set(q_values))
    print(f"Unique Q values: {unique_q}")
    print(f"Total unique Q values: {len(unique_q)}")

    # Check intervals
    differences = [unique_q[i + 1] - unique_q[i] for i in range(len(unique_q) - 1)]
    print(f"Intervals between unique Q values: {differences}")

    # Plot the distribution
    counts = Counter(q_values)
    plt.bar(counts.keys(), counts.values())
    plt.xlabel("Q Value")
    plt.ylabel("Frequency")
    plt.title("Distribution of Q Values")
    plt.show()


if __name__ == "__main__":
    # File path to your FASTQ file
    fastq_file = r"C:\Users\kwz50\IdeaProjects\PowerBarcoder\data\result\202402141122\trnLF_result\demultiplexResult\filtered\filtered_trim_trnLF_L5675_br01_F4121_br01_r1.fq"  # Replace with your FASTQ file path
    offset = 33  # Change to 64 if using Phred+64 encoding

    # Extract and analyze Q values
    q_values = parse_fastq(fastq_file, offset=offset)
    analyze_q_values(q_values)

"""
20241212 確認目前的Q應是 continuous Q values
"""
