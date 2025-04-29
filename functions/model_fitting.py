import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

"""
Script contains some form fitting functions which are not currently used.

They explore fitting fourier series approximations to the data to get statistical tests
into whether relationships exist between error rate and rotation angle, and characterising them if so
"""

ANGLE_RANGE = np.pi
angle_fine = np.linspace(0, ANGLE_RANGE, 500)
np.random.seed(42)  # for reproducibility


def get_model_predictions(model):
    # predict over fine angle grid
    sin_fine = np.sin(angle_fine)
    cos_fine = np.cos(angle_fine)

    # make x and y predictions for plotting
    X_pred = np.column_stack((np.ones_like(angle_fine), sin_fine, cos_fine))
    y_pred = X_pred @ model.params.values  # predicted mean

    return X_pred, y_pred


def do_bootstrap_conf_int(data_df, X_pred):
    # do some bootstrapping to give confidence intervals to
    # model predictions
    n_bootstrap = 1000
    y_bootstrap = np.zeros((n_bootstrap, len(angle_fine)))

    for i in range(n_bootstrap):
        sample = data_df.sample(frac=1, replace=True)
        X_sample = sm.add_constant(sample[["sin_angle", "cos_angle"]])
        y_sample = sample["error_rate"]
        model_sample = sm.OLS(y_sample, X_sample).fit()
        params_sample = model_sample.params
        y_bootstrap[i] = X_pred @ params_sample.values

    lower_bound = np.percentile(y_bootstrap, 5, axis=0)
    upper_bound = np.percentile(y_bootstrap, 95, axis=0)

    return lower_bound, upper_bound


def fit_model(data_df):
    # 2. Build predictors
    data_df["sin_angle"] = np.sin(data_df["angle"])
    data_df["cos_angle"] = np.cos(data_df["angle"])

    X = data_df[["sin_angle", "cos_angle"]]
    X = sm.add_constant(X)
    y = data_df["error_rate"]

    # 3. Fit the regression model
    model = sm.OLS(y, X).fit()

    return model


def fit_and_single_plot(data_df, y_pred, model, lower_bound, upper_bound):
    """Does a single term fourier series fit and then plots this with bootstaps
    not currently used"""
    # single plot for Rx
    # can I generalise this for Rzz? is it even worth it?
    # maybe I just make sure they share the same options

    beta_0 = model.params["const"]
    beta_1 = model.params["sin_angle"]
    beta_2 = model.params["cos_angle"]

    fig, ax = plt.subplots()
    ax.figure(figsize=(12, 7))

    # Raw data points
    ax.scatter(
        data_df["angle"], data_df["error_rate"], color="blue", alpha=0.5, label="Data"
    )

    # Fitted curve
    ax.plot(
        angle_fine,
        y_pred,
        color="red",
        lw=2,
        # label=f"Fit: B₁={beta_1:.2f} (p={p_beta_1:.3g}), B₂={beta_2:.2f} (p={p_beta_2:.3g})")
        label=f"Fit: B₁={beta_1:.2f}, B₂={beta_2:.2f}",
    )

    # Confidence bands
    ax.fill_between(
        angle_fine,
        lower_bound,
        upper_bound,
        color="red",
        alpha=0.2,
        label="95% CI (bootstrap)",
    )

    ax.xlabel("Angle θ (radians)", fontsize=14)
    ax.ylabel("Error Rate", fontsize=14)
    # ax.title(f"Error Rate vs Angle\nOverall Model F={f_stat:.2f}, p={f_pvalue:.3g}", fontsize=16)
    ax.xticks(
        np.linspace(0, 2 * np.pi, 9),
        ["0", "π/4", "π/2", "3π/4", "π", "5π/4", "3π/2", "7π/4", "2π"],
        fontsize=12,
    )
    ax.yticks(fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.legend(fontsize=12)
    ax.tight_layout()
    ax.show()
