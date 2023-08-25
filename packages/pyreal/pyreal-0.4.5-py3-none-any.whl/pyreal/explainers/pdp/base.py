from abc import ABC, abstractmethod

from pyreal.explainers import ExplainerBase


class PartialDependenceExplainerBase(ExplainerBase, ABC):
    """
    Base class for PartialDependence explainer objects. Abstract class

    A PartialDependenceExplainer object explains a machine learning prediction by showing the
    marginal effect each feature has on the model prediction.

    Args:
        model (string filepath or model object):
           Filepath to the pickled model to explain, or model object with .predict() function
        x_train_orig (dataframe of shape (n_instances, x_orig_feature_count)):
           The training set for the explainer
        interpretable_features (Boolean):
            If True, return explanations using the interpretable feature descriptions instead of
            default names
        **kwargs: see base Explainer args
    """

    def __init__(self, model, x_train_orig=None, interpretable_features=True, **kwargs):
        self.interpretable_features = interpretable_features
        self.pdp_explanation = None
        super(PartialDependenceExplainerBase, self).__init__(model, x_train_orig, **kwargs)

    @abstractmethod
    def fit(self, x_train_orig=None, y_train=None):
        """
        Fit this explainer object

        Args:
            x_train_orig (DataFrame of shape (n_instances, n_features):
                Training set to fit on, required if not provided on initialization
            y_train:
                Targets of training set, required if not provided on initialization
        """

    def produce(self, x_orig=None):
        """
        Produce the partial dependence explanation

        Returns:
            DataFrame of shape (n_instances, n_features)
                Contribution of each feature for each instance
            DataFrame of shape (n_instances, x_orig_feature_count)
                `x_orig` transformed to the state of the final explanation
        """
        if self.pdp_explanation is None:
            explanation = self.get_pdp()
            explanation = self.transform_explanation(explanation)
            if self.interpretable_features:
                explanation.update_feature_names(self.feature_descriptions)
            self.pdp_explanation = explanation

        return self.pdp_explanation

    @abstractmethod
    def get_pdp(self):
        """
        Gets the raw explanation

        Returns:
            PDP explanation object.
        """
        raise NotImplementedError("Partial dependence not implemented for this explainer.")

    def evaluate_variation(self, with_fit=False, explanations=None, n_iterations=20, n_rows=10):
        """
        Evaluate the variation of the explanations generated by this Explainer.
        Not currently implemented for partial dependence explainers

        Args:
            with_fit (Boolean):
                If True, evaluate the variation in explanations including the fit (fit each time
                before running). If False, evaluate the variation in explanations of a pre-fit
                Explainer.
            explanations (None or List of DataFrames of shape (n_instances, n_features)):
                If provided, run the variation check on the precomputed list of explanations
                instead of generating
            n_iterations (int):
                Number of explanations to generate to evaluation variation
            n_rows (int):
                Number of rows of dataset to generate explanations on

        Returns:
            None

        Raises:
            NotImplementedError
        """
        raise NotImplementedError
