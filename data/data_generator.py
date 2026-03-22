import numpy as np
import pandas as pd

def generate_data(n=1000, seed=42):
    np.random.seed(seed)

    # ユーザー属性
    age = np.random.randint(18, 65, n)
    gender = np.random.choice(["male", "female"], n)
    device = np.random.choice(["mobile", "desktop"], n, p=[0.7, 0.3])
    traffic_source = np.random.choice(
        ["organic", "ads", "sns"], n, p=[0.5, 0.3, 0.2]
    )

    # 行動データ
    session_time = np.random.exponential(scale=5, size=n)
    pages_viewed = np.random.poisson(lam=3, size=n)

    # A/Bテスト
    variant = np.random.choice(["A", "B"], n)

    # 購入確率（ロジックを仕込む）
    base_prob = 0.05

    # 行動による影響
    prob = base_prob \
        + 0.01 * (pages_viewed) \
        + 0.02 * (session_time > 5)

    # デバイスの影響
    prob += np.where(device == "mobile", 0.01, 0)

    # A/Bテストの効果（Bの方が少し良い）
    prob += np.where(variant == "B", 0.02, 0)

    # クリップ（確率が1超えないように）
    prob = np.clip(prob, 0, 1)

    # 購入フラグ
    purchased = np.random.binomial(1, prob)

    # 購入金額（購入者のみ）
    purchase_amount = purchased * np.random.normal(5000, 2000, n)

    df = pd.DataFrame({
        "user_id": range(n),
        "age": age,
        "gender": gender,
        "device": device,
        "traffic_source": traffic_source,
        "session_time": session_time,
        "pages_viewed": pages_viewed,
        "variant": variant,
        "purchased": purchased,
        "purchase_amount": purchase_amount
    })

    return df


if __name__ == "__main__":
    df = generate_data(n=1000)
    df.to_csv("sample_data.csv", index=False)
    print("Data generated!")