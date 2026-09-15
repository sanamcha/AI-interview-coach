"""Common data-science interview prompts expanded into a 100-question library."""

from web_questions import build_library


DATA_SCIENCE_TOPICS = [
    ('the data-science lifecycle', 'It typically includes problem framing, data collection, cleaning, exploration, modeling, evaluation, deployment, and monitoring.', 'Starting with a model before defining the business metric often produces an impressive but unhelpful solution.'),
    ('supervised learning', 'It learns a mapping from labeled input examples to targets for tasks such as classification and regression.', 'Using labels that would not exist at prediction time creates leakage.'),
    ('unsupervised learning', 'It finds structure in unlabeled data, such as clusters, lower-dimensional representations, or anomalies.', 'Treating arbitrary clusters as ground truth without validation leads to false conclusions.'),
    ('classification', 'Classification predicts a discrete class or probability, such as whether a customer will churn.', 'Using accuracy alone on imbalanced data can hide poor minority-class performance.'),
    ('regression', 'Regression predicts a continuous numeric value, such as revenue or delivery time.', 'Ignoring outliers or target distribution can make error metrics misleading.'),
    ('overfitting', 'Overfitting occurs when a model learns training noise and performs poorly on unseen data.', 'Tuning repeatedly on the test set turns it into training data.'),
    ('underfitting', 'Underfitting occurs when a model is too simple to capture important patterns in the data.', 'Adding more training time cannot fix a model with insufficient features or capacity.'),
    ('the bias-variance tradeoff', 'Bias is systematic error from overly simple assumptions; variance is sensitivity to training data.', 'Treating the tradeoff as a reason not to validate models prevents evidence-based choices.'),
    ('train, validation, and test splits', 'Train data fits parameters, validation data guides choices, and test data provides a final unbiased evaluation.', 'Random splits can leak time-dependent information in temporal problems.'),
    ('cross-validation', 'Cross-validation rotates validation folds to estimate generalization more reliably on limited data.', 'Applying preprocessing before splitting leaks information between folds.'),
    ('feature engineering', 'Feature engineering transforms raw data into useful representations based on domain knowledge and valid prediction-time inputs.', 'Creating features with future information causes target leakage.'),
    ('feature scaling', 'Scaling puts numeric features on comparable ranges, which matters for distance-based and gradient-based models.', 'Scaling is usually unnecessary for tree-based models and must be fit only on training data.'),
    ('normalization and standardization', 'Normalization rescales to a range; standardization centers values and scales by standard deviation.', 'Choosing a scaler without considering outliers or model type can distort useful information.'),
    ('missing data', 'Missing values can be dropped, imputed, or modeled, depending on why values are missing and their business meaning.', 'Blindly filling values can hide missingness patterns that are predictive or important.'),
    ('outliers', 'Outliers are unusual observations that may be errors, rare important cases, or valid extremes.', 'Removing all outliers without investigation can erase the population you most need to understand.'),
    ('data leakage', 'Leakage occurs when training uses information unavailable at real prediction time or from validation and test data.', 'Leakage often creates unrealistically high offline metrics and production failure.'),
    ('confusion matrices', 'A confusion matrix counts true and false positives and negatives for a classification threshold.', 'Reading it without considering class prevalence and error cost can lead to the wrong threshold.'),
    ('precision and recall', 'Precision measures correctness of positive predictions; recall measures how many actual positives were found.', 'Optimizing one metric without the business cost of the other can harm users.'),
    ('ROC and precision-recall curves', 'They show metric tradeoffs across thresholds; precision-recall is often more informative for rare positives.', 'Comparing curves without matching the same validation data and target definition is unreliable.'),
    ('linear regression assumptions', 'Common assumptions include linearity, independent errors, stable variance, and appropriately modeled residuals.', 'A high R-squared does not prove causal validity or satisfy all assumptions.'),
    ('logistic regression', 'Logistic regression models the log-odds of a class and outputs probabilities through a logistic function.', 'Interpreting coefficients without considering scaling, interactions, and regularization can be misleading.'),
    ('decision trees and random forests', 'Trees split features into rules; random forests average many randomized trees to reduce variance.', 'Very deep trees can overfit and feature-importance scores can be biased.'),
    ('gradient boosting', 'Gradient boosting builds trees sequentially to correct prior errors and often performs strongly on tabular data.', 'Aggressive depth, learning rate, or iterations can overfit without early stopping and validation.'),
    ('clustering', 'Clustering groups similar observations, commonly with k-means, hierarchical methods, or density-based approaches.', 'Clusters depend on features, scale, distance, and algorithm assumptions; they are not automatically real segments.'),
    ('A/B testing', 'An A/B test randomly assigns variants and compares a pre-defined outcome using sound experiment design.', 'Peeking repeatedly, changing metrics, or unbalanced assignment inflates false positives.'),
]

DATA_SCIENCE_QUESTIONS = build_library(DATA_SCIENCE_TOPICS)
