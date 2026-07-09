def main():
    df = pd.read_csv("data/dataset.csv")
    df_grouped = clean_df(df)

    # queries_grouped = Queries(df_grouped)
    queries_albums = Queries(df)

    danceability_mean, most_danceability_genres = (
        # queries_grouped.most_danceable_genres()
        queries_groupe.most_danceable_genres()
    )

    print(f"Danceability promedio de todas las canciones: {danceability_mean}")
    print(f"Danceability promedio por genero:\n{most_danceability_genres.head(5)}")

    most_danceability_genres["pomean"] = (most_danceability_genres.values - danceability_mean)
    print(f"Danceability promedio por genero:\n{most_danceability_genres.head(5)}")




if __name__ == "__main__":
    main()
