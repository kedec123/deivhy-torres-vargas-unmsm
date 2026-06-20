import pathlib
import numpy as np
import pandas as pd


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def main():
    rng = np.random.default_rng(42)
    n = 1200

    region = rng.choice(["coast", "highlands", "amazon"], size=n, p=[0.42, 0.33, 0.25])
    age_months = rng.integers(6, 36, size=n)
    rural = rng.binomial(1, 0.38, size=n)
    sex_male = rng.binomial(1, 0.51, size=n)
    wealth_quintile = rng.integers(1, 6, size=n)
    maternal_education_years = rng.integers(0, 19, size=n)
    recent_iron_supplement = rng.binomial(1, 0.43, size=n)
    recent_diarrhea = rng.binomial(1, 0.18, size=n)
    safe_water = rng.binomial(1, 0.72, size=n)
    block_id = rng.integers(1, 61, size=n)

    altitude = np.where(
        region == "highlands",
        rng.normal(3200, 700, size=n),
        np.where(region == "amazon", rng.normal(250, 120, size=n), rng.normal(300, 180, size=n)),
    )
    altitude = np.clip(altitude, 0, 4500)

    region_amazon = (region == "amazon").astype(int)
    region_highlands = (region == "highlands").astype(int)
    poorest_two_quintiles = (wealth_quintile <= 2).astype(int)

    # Synthetic signal: younger children, rural households, lower wealth, lower maternal
    # education, diarrhea, and lack of supplementation increase anemia risk.
    logit = (
        0.9
        - 0.045 * (age_months - 6)
        + 0.55 * rural
        + 0.60 * poorest_two_quintiles
        - 0.08 * maternal_education_years
        - 0.50 * recent_iron_supplement
        + 0.65 * recent_diarrhea
        - 0.35 * safe_water
        + 0.45 * region_amazon
        + 0.20 * region_highlands
        + 0.12 * sex_male
        + rng.normal(0, 0.55, size=n)
    )

    anemia = rng.binomial(1, sigmoid(logit))

    df = pd.DataFrame(
        {
            "age_months": age_months,
            "sex_male": sex_male,
            "rural": rural,
            "wealth_quintile": wealth_quintile,
            "maternal_education_years": maternal_education_years,
            "recent_iron_supplement": recent_iron_supplement,
            "recent_diarrhea": recent_diarrhea,
            "safe_water": safe_water,
            "region": region,
            "altitude_m": np.round(altitude, 0).astype(int),
            "block_id": block_id,
            "target_anemia": anemia,
        }
    )

    out_path = pathlib.Path(__file__).resolve().parent / "anemia_peru_synthetic.csv"
    df.to_csv(out_path, index=False)
    print(f"Dataset created at: {out_path}")
    print(f"Rows: {len(df)} | Anemia prevalence: {df['target_anemia'].mean():.3f}")


if __name__ == "__main__":
    main()
