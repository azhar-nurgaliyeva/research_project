from scipy.optimize import minimize
from scipy.optimize import Bounds

from scipy import sparse as sp
import numpy as np


def log_evidence(alpha, gamma, beta, T, s, V, X, M):
    N, D = T.shape
    sigma = 1 / alpha + 1 / gamma * (s ** 2)
    pi = beta / np.sum(beta)
    Hp = M @ pi
    logp = -N * D / 2 * np.log(2 * np.pi) \
           - N / 2 * np.sum(np.log(sigma)) \
           - 1 / 2 * ((T - Hp @ X) @ V @ sp.diags(1 / sigma) @ V.T @ (T - Hp @ X).T).diagonal().sum()
    assert ~np.isnan(logp)
    return logp


def negative_log_evidence(x, T, s, V, X, M):
    alpha, gamma, beta = x[0], x[1], x[2:]
    return -log_evidence(alpha, gamma, beta, T, s, V, X, M)


def get_optimal_x(x0, *args, bounds, method='L-BFGS-B', options={'maxiter': 500, 'tol': 1e-8, 'disp': False}):
    res = minimize(negative_log_evidence, x0=x0, args=args,
                   method=method,
                   bounds=bounds, options={'maxiter': options['maxiter'], 'disp': options['disp']},
                   tol=options['tol'],
                   )
    return res


def get_optimal_H(X, T, M):
    params = dict()
    eps = 1e-7
    N = X.shape[0]
    bounds = Bounds((M.shape[2] + 2) * [eps], (M.shape[2] + 2) * [np.inf])
    x0 = np.ones((M.shape[2] + 2))
    _, s, Vh = np.linalg.svd(X, full_matrices=False)
    V = Vh.T

    res = get_optimal_x(x0, T, s, V, X, M, bounds=bounds)  # first try

    if not res.success: res = get_optimal_x(np.random.rand(M.shape[2] + 2), T, s, V, X, M,
                                            bounds=bounds)  # second try
    if not res.success: res = get_optimal_x(x0, T, s, V, X, M, bounds=bounds, method='TNC')  # second try

    alpha, gamma, beta = res.x[0], res.x[1], res.x[2:]
    pi = beta / np.sum(beta)
    success = res.success
    params['alpha'], params['pi'], params['gamma'] = alpha, pi, gamma
    p_data, p_prior = np.linalg.norm(alpha * s / (alpha * s + gamma)), np.linalg.norm(
        gamma / (alpha * s + gamma))
    params['p_data'] = p_data
    params['p_prior'] = p_prior
    Hp = M @ pi
    H = (alpha * T @ X.T + gamma * Hp) @ np.linalg.pinv(alpha * X @ X.T + gamma * np.eye(N))
    return H, success, params
