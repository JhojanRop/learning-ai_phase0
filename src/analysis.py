import numpy as np
import pandas as pd


class Queries:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    @staticmethod
    def _format_duration(milliseconds: float) -> str:
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return (
            f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
        )

    def duration_mean_per_genre(
        self, genres: list[str] | None = None, format: bool = False
    ) -> pd.Series:
        mean_ms = self.df.groupby("track_genre")["duration_ms"].mean()

        if genres is not None:
            mean_ms = mean_ms[mean_ms.index.isin(genres)]

        return mean_ms.apply(self._format_duration) if format else mean_ms

    def most_danceable_genres(self):
        mean_danceability_group = self.df.groupby("track_genre")["danceability"].mean()
        mean_danceability = self.df["danceability"].mean()
        return (
            mean_danceability,
            mean_danceability_group.sort_values(ascending=False),
        )

    def most_popular_albums(self):
        return (
            self.df.sort_values("popularity", ascending=False)
            .drop_duplicates(subset="album_name")[["album_name", "popularity"]]
            .reset_index(drop=True)
        ).head(10)

    def longest_albums(self, format: bool = False, values: int = 10) -> pd.DataFrame:
        sum_ms = (
            self.df.groupby("album_name", as_index=False)
            .agg({"duration_ms": "sum"})
            .sort_values("duration_ms", ascending=False)
        )
        if format:
            sum_ms["duration_ms"] = sum_ms["duration_ms"].apply(self._format_duration)
        return sum_ms.head(values)

    def distribution_per_moods(self):
        dfc = self.df.copy()

        conditions = [
            (dfc["valence"] >= 0.5)
            & (dfc["energy"] >= 0.6)
            & (dfc["danceability"] >= 0.65),
            (dfc["valence"] >= 0.5)
            & (dfc["energy"] >= 0.6)
            & (dfc["danceability"] < 0.65),
            (dfc["valence"] >= 0.5)
            & (dfc["energy"] < 0.6)
            & (dfc["acousticness"] >= 0.5),
            (dfc["valence"] >= 0.5)
            & (dfc["energy"] < 0.6)
            & (dfc["acousticness"] < 0.5),
            (dfc["valence"] < 0.5)
            & (dfc["energy"] < 0.6)
            & (dfc["mode"] == 0)
            & (dfc["tempo"] < 100),
            (dfc["valence"] < 0.5) & (dfc["energy"] < 0.6),
            (dfc["valence"] < 0.5)
            & (dfc["energy"] >= 0.6)
            & (dfc["danceability"] < 0.5),
            (dfc["valence"] < 0.5)
            & (dfc["energy"] >= 0.6)
            & (dfc["danceability"] >= 0.5),
        ]

        choices = [
            "Eufórica / Fiesta",
            "Feliz / Enérgica",
            "Acústica / Relajada",
            "Chill / Pop Suave",
            "Depresiva / Desoladora",
            "Triste / Melancólica",
            "Agresiva / Tensa",
            "Oscura / Intensa",
        ]

        dfc["mood"] = np.select(conditions, choices, default="Neutral")

        return dfc["mood"].value_counts().reset_index()
