import pandas as pd
from piwebapiml.pml_stream import PMLStream

class PMLStreamSet(object):
    piwebapi = None
    streams = None
    web_ids = []
    paths = []

    def __init__(self, piwebapi, streams: list):
        self.piwebapi = piwebapi
        self.streams = streams
        for stream in streams:
            self.web_ids.append(stream.web_id)
            self.paths.append(stream.path)
        
    def convert_to_df(self, items, selected_fields):

        if (items is None):
            raise Exception('The returned data is Null or None')

        streamsLength = len(items)
        if (streamsLength == 0):
            raise Exception('The returned data is Null or None')

        addValues = False
        addTimeStamp = False
        addUnitAbbr = False
        addGood = False
        addQuestionable = False
        addSubstituded = False
        value = []
        timestamp = []
        unitsAbbreviation = []
        good = []
        questionable = []
        substituted = []

        if (selected_fields != None and selected_fields != ""):
            if ("timestamp" in selected_fields):
                addTimeStamp = True
            if ("value" in selected_fields):
                addValues = True

            if ("questionable" in selected_fields):
                addQuestionable = True

            if ("unitabbr" in selected_fields):
                addUnitAbbr = True

            if ("good" in selected_fields):
                addGood = True

            if ("substituted" in selected_fields):
                addSubstituded = True
        else:
            addValues = True
            addTimeStamp = True
            addUnitAbbr = True
            addGood = True
            addQuestionable = True
            addSubstituded = True

        for item in items:
            if (addValues == True):
                value.append(item.value)
            if (addTimeStamp == True):
                timestamp.append(item.timestamp)
            if (addUnitAbbr == True):
                unitsAbbreviation.append(item.units_abbreviation)
            if (addGood == True):
                good.append(item.good)
            if (addQuestionable == True):
                questionable.append(item.questionable)
            if (addSubstituded == True):
                substituted.append(item.substituted)

        data = {}
        if (addValues == True):
            data['Value'] = value;
        if (addTimeStamp == True):
            data['Timestamp'] = timestamp;
        if (addUnitAbbr == True):
            data['UnitsAbbreviation'] = unitsAbbreviation;
        if (addGood == True):
            data['Good'] = good;
        if (addQuestionable == True):
            data['Questionable'] = questionable;
        if (addSubstituded == True):
            data['Substituted'] = substituted;
        df = pd.DataFrame(data)
        return df
        
    def rename_df(self, df, i):
        df.rename(columns={'Value': 'Value' + str(i + 1)}, inplace=True)
        df.rename(columns={'Timestamp': 'Timestamp' + str(i + 1)}, inplace=True)
        df.rename(columns={'UnitsAbbreviation': 'UnitsAbbreviation' + str(i + 1)}, inplace=True)
        df.rename(columns={'Good': 'Good' + str(i + 1)}, inplace=True)
        df.rename(columns={'Questionable': 'Questionable' + str(i + 1)}, inplace=True)
        df.rename(columns={'Substituted': 'Substituted' + str(i + 1)}, inplace=True)
        return df

    def calculate_index(self, web_id, items):
        for i in range(0, len(items)):
            if (items[i].web_id == web_id):
                return i
        return -1

    def convert_streams_to_data_frame(self, items, merge_in_single_df, web_ids, selected_fields, paths):
        if (items is None):
            raise Exception('The returned data is Null or None')

        streams_length = len(items)
        if (streams_length == 0):
            raise Exception('The returned data is Null or None')

        for i in range(0, streams_length):
            if ((items[i] == None) or (items[i].items == None)):
                raise Exception('Some items are Null or None.')

        if (merge_in_single_df == True):
            main_df = df_ = pd.DataFrame()
            for i in range(0, streams_length):
                j = self.calculate_index(web_ids[i], items);
                df = self.convert_to_df(items[j].items, selected_fields)
                df = self.rename_df(df, i)
                main_df = pd.concat([main_df, df], axis=1)
            return main_df
        else:
            dfs = {}
            for i in range(0, streams_length):
                key = paths[i]
                j = self.calculate_index(web_ids[i], items)
                df = self.convert_to_df(items[j].items, selected_fields)
                dfs[key] = df
            return dfs

    def get_interpolated_values_in_bulk(self, end_time="*", filter_expression=None,
                                         include_filtered_values=None, interval="1h", selected_fields=None,
                                         sort_field=None, sort_order=None, start_time="*-1d", sync_time=None,
                                         sync_time_boundary_type=None, time_zone=None, web_id_type=None):

        res = self.piwebapi.streamSet.get_interpolated_ad_hoc(self.web_ids, end_time=end_time, filter_expression=filter_expression,
                                                        include_filtered_values=include_filtered_values,
                                                        interval=interval, selected_fields=selected_fields,
                                                        sort_field=sort_field, sort_order=sort_order,
                                                        start_time=start_time, sync_time=sync_time,
                                                        sync_time_boundary_type=sync_time_boundary_type,
                                                        time_zone=time_zone, web_id_type=web_id_type)
        df = self.convert_streams_to_data_frame(res.items, True, self.web_ids, selected_fields, None)
        return df

    def get_plot_values_in_bulk(self, end_time="*", intervals="1h", selected_fields=None, sort_field=None,
                                 sort_order=None, start_time="*-1d", time_zone=None, web_id_type=None):
       
        res = self.piwebapi.streamSet.get_plot_ad_hoc(self.web_ids, end_time=end_time, intervals=intervals,
                                                selected_fields=selected_fields, sort_field=sort_field,
                                                sort_order=sort_order, start_time=start_time, time_zone=time_zone,
                                                web_id_type=web_id_type)
        df = self.convert_streams_to_data_frame(res.items, True, self.web_ids, selected_fields, None)
        return df

    def get_recorded_values_in_bulk(self, boundary_type=None, end_time="*", filter_expression=None,
                                     include_filtered_values=None, max_count=None, selected_fields=None,
                                     sort_field=None, sort_order=None, start_time=None, time_zone=None,
                                     web_id_type=None):

        res = self.piwebapi.streamSet.get_recorded_ad_hoc(self.web_ids, boundary_type=boundary_type, end_time=end_time,
                                                    filter_expression=filter_expression,
                                                    include_filtered_values=include_filtered_values,
                                                    max_count=max_count, selected_fields=selected_fields,
                                                    sort_field=sort_field, sort_order=sort_order, start_time=start_time,
                                                    time_zone=time_zone, web_id_type=web_id_type)
        df = self.convert_streams_to_data_frame(res.items, False, self.web_ids, selected_fields, self.paths)
        return df






