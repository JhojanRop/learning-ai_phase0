import pandas as pd

from src.analysis import Queries
from src.cleaning import clean_df
from src.graphs import distribution_per_mood, most_danceable_genres, most_popular_albums


def main():
    df = pd.read_csv("data/dataset.csv")
    df_grouped = clean_df(df)

    queries_grouped = Queries(df_grouped)
    queries_albums = Queries(df)

    mean_danceability, most_danceability_genres = (
        queries_grouped.most_danceable_genres()
    )

    most_danceable_genres(
        mean_danceability,
        most_danceability_genres,
        savePath="outputs/most_danceable_genres.png",
        show=False,
    )

    distribution_per_mood(
        queries_grouped.distribution_per_moods(),
        savePath="outputs/ditribution_per_mood.png",
        show=False,
    )

    most_popular_albums(
        queries_albums.most_popular_albums().head(10),
        show=False,
        savePath="outputs/most_popular_albums.png",
    )


if __name__ == "__main__":
    main()
