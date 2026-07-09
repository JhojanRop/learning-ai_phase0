import matplotlib.pyplot as plt
import pandas as pd


def _plot_hbars(
    y_data,
    x_data,
    title: str,
    color: str,
    xlabel: str | None = None,
    ylabel: str | None = None,
    xticks: list | None = None,
    savePath: str | None = None,
    show: bool = True,
):
    _, ax = plt.subplots(figsize=(8, 5))
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    bars = ax.barh(y_data, x_data, color=color)
    ax.bar_label(bars, fmt="%.1f%%", padding=5, fontsize=10)
    ax.invert_yaxis()

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, labelpad=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11)
    if xticks:
        ax.set_xticks(xticks)

    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.tick_params(axis="x", labelsize=9)
    for spine in ["top", "right", "bottom"]:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()

    if savePath is not None:
        plt.savefig(savePath)

    if show:
        plt.show()

    plt.close()


def most_danceable_genres(
    mean_danceability: float,
    genres: pd.Series,
    savePath: str | None = None,
    show: bool = True,
):
    pomean = ((genres - mean_danceability) / mean_danceability) * 100
    top5 = pomean.head(5)

    _plot_hbars(
        y_data=top5.index,
        x_data=top5.values,
        title="Géneros más bailables",
        color="skyblue",
        xlabel="% más bailable que el promedio general",
        ylabel="Géneros",
        xticks=[0, 10, 20, 30, 40],
        savePath=savePath,
        show=show,
    )


def distribution_per_mood(
    distribution: pd.DataFrame, savePath: str | None = None, show: bool = True
):
    distribution["percentage"] = (
        distribution["count"] / distribution["count"].sum()
    ) * 100

    _plot_hbars(
        y_data=distribution["mood"],
        x_data=distribution["percentage"],
        title="Distribución de canciones por mood",
        color="red",
        savePath=savePath,
        show=show,
    )


def most_popular_albums(
    albums: pd.DataFrame, savePath: str | None = None, show: bool = True
):
    _, ax = plt.subplots(figsize=(12, 5))
    ax.set_title("", fontsize=14, fontweight="bold", pad=15)
    ax.barh(albums["album_name"], albums["popularity"], color="orange")
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.tick_params(axis="x", labelsize=9)
    for spine in ["top", "right", "bottom"]:
        ax.spines[spine].set_visible(False)
    plt.tight_layout()

    if savePath is not None:
        plt.savefig(savePath)

    if show:
        plt.show()

    plt.close()
