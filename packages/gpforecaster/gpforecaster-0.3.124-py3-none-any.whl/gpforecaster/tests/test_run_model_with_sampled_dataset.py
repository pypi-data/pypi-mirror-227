import unittest

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets(
            "prison", sample_perc=0.9, freq='Q'
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.dataset_name = "prison"
        self.gpf = GPF("prison", self.data, gp_type="exact90")

    def test_calculate_metrics_dict(self):
        model, like = self.gpf.train(epochs=10)
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_original=self.gpf.train_x.numpy(),
            x_test=self.gpf.test_x.numpy(),
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res['mase']['bottom'], 20)
