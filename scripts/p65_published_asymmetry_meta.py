"""Random-effects summary of per-experiment space-time asymmetry (registered rule, sec. Counting rule).

Included: experiments whose two cross-dimensional effects are reported (or derivable) as slopes of the
judged magnitude on the irrelevant magnitude in a COMMON unit (proportion of stimulus range, or both
predictors rescaled to the same range) with an SE for each direction. Values copied from the coded TSV
(published-asymmetry/p65_published-asymmetry-coded_2026-11-13.tsv, effsize columns).

asymmetry a_i = b(space->time) - b(time->space)   (positive = space intrudes on time more = against Navon)
SE(a_i) = sqrt(SE1^2 + SE2^2)  (within-subject covariance unknown, assumed 0)
Pooling: DerSimonian-Laird random effects. Negative control: within each experiment the two direction
labels are swapped at random (sign of a_i flipped with p = .5), 10,000 permutations, seed 20261113.

Usage: python3 -I p65_published_asymmetry_meta.py
"""
import math, random

# key, b_SonT, se_SonT, b_TonS, se_TonS, source note
DATA = [
    ('Cai2018_E1', 0.056, 0.016, -0.001, 0.008, 'proportion of range, derived from beta per SD'),
    ('Cai2018_E2', 0.005, 0.017, 0.012, 0.008, 'proportion of range'),
    ('Cai2018_E3', 0.025, 0.013, 0.008, 0.005, 'proportion of range'),
    ('Cai2018_E4', 0.053, 0.016, 0.020, 0.004, 'proportion of range'),
    ('StarrBrannon2016', 0.102, 0.009, 0.067, 0.0067, 'raw slopes x range ratio (600 px / 4000 ms)'),
    ('BratzkeUlrich2025_E1', 0.048, 0.0127, 0.022, 0.0075, 'both predictors scaled 0-100; SE from p (S->T SE is an upper bound)'),
    ('BratzkeUlrich2025_E2', 0.019, 0.012, 0.023, 0.0072, 'as above, SE from p'),
    ('BratzkeUlrich2025_E3', -0.008, 0.0099, 0.016, 0.0068, 'as above, SE from p'),
    ('Riemer2024', 0.170, 0.068, -0.056, 0.088, 'PSE shift, comparison values rescaled to -1..+1'),
]


def dl(y, v):
    w = [1 / x for x in v]
    fe = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
    q = sum(wi * (yi - fe) ** 2 for wi, yi in zip(w, y))
    k = len(y)
    c = sum(w) - sum(wi * wi for wi in w) / sum(w)
    tau2 = max(0.0, (q - (k - 1)) / c)
    ws = [1 / (x + tau2) for x in v]
    m = sum(wi * yi for wi, yi in zip(ws, y)) / sum(ws)
    se = math.sqrt(1 / sum(ws))
    return m, se, tau2, q, fe


def norm_p(z):
    return math.erfc(abs(z) / math.sqrt(2))


def main():
    y = [a - c for _, a, sa, c, sc, _ in DATA]
    v = [sa ** 2 + sc ** 2 for _, a, sa, c, sc, _ in DATA]
    print('experiment              asym     SE')
    for (k, *_), yi, vi in zip(DATA, y, v):
        print(f'{k:22s} {yi:+.4f} {math.sqrt(vi):.4f}')
    m, se, tau2, q, fe = dl(y, v)
    z = m / se
    print(f'\nk = {len(y)}; DL random-effects mean asymmetry = {m:+.4f} (95% CI {m-1.96*se:+.4f} to {m+1.96*se:+.4f}), z = {z:.2f}, p = {norm_p(z):.4f}')
    print(f'tau^2 = {tau2:.6f}; Q = {q:.2f} on {len(y)-1} df; fixed-effect mean = {fe:+.4f}')
    # leave-one-out
    for i in range(len(y)):
        mm, ss, *_ = dl(y[:i] + y[i+1:], v[:i] + v[i+1:])
        print(f'  without {DATA[i][0]:22s}: {mm:+.4f} (95% CI {mm-1.96*ss:+.4f} to {mm+1.96*ss:+.4f})')
    # negative control: random label swap within experiment
    rng = random.Random(20261113)
    perm = []
    for _ in range(10000):
        yy = [yi if rng.random() < .5 else -yi for yi in y]
        perm.append(dl(yy, v)[0])
    pm = sum(perm) / len(perm)
    pp = sum(1 for x in perm if abs(x) >= abs(m)) / len(perm)
    print(f'\nNegative control (labels swapped at random within experiment, 10,000 perms): mean of permuted pooled asymmetry = {pm:+.5f}; '
          f'permutation p(|perm| >= |observed|) = {pp:.4f}')


if __name__ == '__main__':
    main()
