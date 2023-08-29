# coding: utf-8

import unittest
from piwebapiml.pml_web_api_client import PMLWebApiClient


class TestData(unittest.TestCase):
    def getPIWebApiClient(self):
        piwebapi = PMLWebApiClient("https://marc-pi2018.marc.net/piwebapi", False)
        piwebapi.set_basic_auth("marc.adm", "1")
        return piwebapi


    def test_get_pi_point(self):
        client = self.getPIWebApiClient()
        pi_point = client.get_pi_point("\\\\MARC-PI2018\\sinusoid")
        print(pi_point.web_id)
        pass

    def test_get_pi_points(self):
        client = self.getPIWebApiClient()
        paths = []
        paths.append("\\\\MARC-PI2018\\sinusoid")
        paths.append("\\\\MARC-PI2018\\sinusoidu")
        paths.append("\\\\MARC-PI2018\\cdt158")
        pi_points = client.get_pi_points(paths)
        print(pi_points)
        pass

    def test_data_recorded(self):
        client = self.getPIWebApiClient()
        pi_point = client.get_pi_point("\\\\MARC-PI2018\\sinusoid")
        pi_point2 = client.get_pi_point("\\\\MARC-PI2018\\sinusoidu")
        pi_point3 = client.get_pi_point("\\\\MARC-PI2018\\cdt158")        
        attr = client.get_af_attribute('\\\\MARC-PI2018\\Weather\\Cities\\Chicago|Pressure')
        
        df1 = pi_point.get_recorded_values(start_time="*-1d", end_time="*")
        df2 = pi_point.get_recorded_values(start_time="*-1d", end_time="*",
                                          selected_fields="items.value;items.timestamp")
        df3 = pi_point.get_recorded_values(start_time="*-1d", end_time="*",
                                          selected_fields="items.good;items.questionable;items.substituted")
        df4 = pi_point2.get_recorded_values(start_time="*-10d", end_time="*")
        df5 = pi_point3.get_recorded_values(start_time="*-10d", end_time="*-9d")
        df6 = pi_point.get_interpolated_values(start_time="*-1d", end_time="*", interval="1h")
        df7 = pi_point.get_interpolated_values(start_time="*-1d", end_time="*", interval="1h", selected_fields="items.value;items.timestamp")
        df8 = pi_point2.get_interpolated_values(start_time="*-1d", end_time="*", interval="2h")
        df9 = pi_point3.get_interpolated_values(None, "*", None, None, "3h", None, "*-1d", None, None, None)
        df10 = attr.get_interpolated_values(None, "*", None, None, "3h", None, "*-20d", None, None, None)

        df11 = pi_point.get_plot_values(end_time="*", intervals=15, start_time= "*-1d")
        df12 = pi_point.get_plot_values(None, "*", 15, "items.value;items.timestamp",
                                      "*-1d", None)
        df13 = pi_point2.get_plot_values(None, "*", 10, None, "*-3d", None)
        df14 = pi_point3.get_plot_values(None, "*", 20, None, "*-2d", None)
        df15 = attr.get_plot_values(None, "*", 20, None, "*-40d", None)
        pass

    def test_data_summary(self):
        client = self.getPIWebApiClient()
        pi_point = client.get_pi_point("\\\\MARC-PI2018\\sinusoid")
        df1 = pi_point.get_summary_values(start_time="*-1d", end_time="*", summary_type=['Average'], summary_duration='1h')
        df2 = pi_point.get_summary_values(start_time="*-1d", end_time="*", summary_type=['Average', 'Total'], summary_duration='1h')
        pass


    def test_data_multiple_recorded(self):
        client = self.getPIWebApiClient()
        paths = ["\\\\MARC-PI2018\\sinusoid", "\\\\MARC-PI2018\\sinusoidu", "\\\\MARC-PI2018\\cdt158"]
        pi_points = client.get_pi_points(paths)
        df1 = pi_points.get_recorded_values_in_bulk(start_time="*-1d", end_time= "*")
        pass


if __name__ == '__main__':
    unittest.main()
