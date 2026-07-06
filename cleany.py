import pandas as pd


def safe_mode(serie: pd.Series):
    mode_res = serie.mode()
    return mode_res.iloc[0] if not mode_res.empty else None


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df["track_name"] = df["track_name"].str.lower()
    df["artists"] = df["artists"].str.lower()
    df = df.drop(columns=["Unnamed: 0"])
    df = df.dropna()
    return df


def group_songs(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["track_name", "artists"], as_index=False).agg(
        {
            "album_name": "first",
            "popularity": "max",
            "duration_ms": "median",
            "explicit": safe_mode,
            "danceability": "mean",
            "energy": "mean",
            "key": safe_mode,
            "loudness": "median",
            "mode": safe_mode,
            "speechiness": "mean",
            "acousticness": "mean",
            "instrumentalness": "mean",
            "liveness": "min",
            "valence": "mean",
            "tempo": "median",
            "time_signature": safe_mode,
            "track_genre": safe_mode,
        }
    )  # type: ignore


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    return group_songs(normalize_df(df))
