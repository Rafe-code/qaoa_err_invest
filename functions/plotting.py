import matplotlib.pyplot as plt
import numpy as np


def single_plot(rotation_angles, means, stds, save_loc):
    """single plot graph, got smoe rx assumptions (axis labels)"""

    # do plot
    fig, ax = plt.subplots()
    plt.figure(figsize=(8, 5))
    # normalise angle by pi
    ax.errorbar(
        np.array(rotation_angles) / np.pi,
        means,
        yerr=stds,
        marker="o",
        linestyle="-",
        color="r",
    )
    # rx label assumptions
    ax.set_xlabel(r"Rotation Angle / π (rad/π)")
    ax.set_ylabel("E_rel")
    ax.set_title("Error Rate by rotation angle of Rx Gate on IBM Noise Model")
    ax.grid()
    fig.savefig(save_loc, bbox_inches="tight")


def multi_subplot(df_all_results, fname):
    """Designed for rzz
    Plots subplots for each result_type from the DataFrame df_all_results.
    Each subplot has gamma on the x-axis and the average value on the y-axis,
    with error bars representing the standard deviation over repeats.
    """
    # Reset the index to work with grouped data
    df_reset = df_all_results.reset_index()

    # Group by result_type and gamma, and calculate mean and standard deviation
    grouped = (
        df_reset.groupby(["result_type", "rotation_angle"])
        .agg(mean_value=("error_rate", "mean"), std_value=("error_rate", "std"))
        .reset_index()
    )

    # Get unique result_types for subplots
    result_types = grouped["result_type"].unique()

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    clrs = ["b", "r", "g", "m"]

    # Plot for each result_type
    for i, (ax, result_type) in enumerate(zip(axes.flatten(), result_types)):
        # Filter data for the current result_type
        data = grouped[grouped["result_type"] == result_type]

        # Plot with error bars
        # normalise angle by pi
        ax.errorbar(
            data["rotation_angle"] / np.pi,
            data["mean_value"],
            yerr=data["std_value"] / 2,
            fmt="o-",
            capsize=5,
            label=result_type,
            color=clrs[i],
        )

        # Set labels and title
        if len(str(result_type)) == 1:
            result_type = "0" + str(result_type)
        ax.set_title(f"Output: {result_type}")
        ax.grid("on")
        ax.set_xlabel(r"Rotation Angle / π (rad/π)")
        ax.set_ylabel("E_rel")
        ax.set_ylim([-0.08, 0.08])

        ax.plot(
            [min(ax.get_xlim()), max(ax.get_xlim())], [0, 0], color="k", linewidth=1.5
        )
        ax.set_xlim([-0.025, 2.05])

    # Adjust layout
    plt.savefig(fname, bbox_inches="tight")
