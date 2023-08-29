import pandas as pd

class PMLStream(object):
    piwebapi = None
    path = None
    web_id = None

    def __init__(self, piwebapi, web_id, path):
        self.piwebapi = piwebapi
        self.web_id = web_id
        self.path = path

    def convert_summary_to_df(self, items, selected_fields):

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
        addSubstituted = False
        value = []
        timestamp = []
        unitsAbbreviation = []
        good = []
        questionable = []
        substituted = []
        summaryType = []

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
                addSubstituted = True
        else:
            addValues = True
            addTimeStamp = True
            addUnitAbbr = True
            addGood = True
            addQuestionable = True
            addSubstituted = True

        for item in items:
            summaryType.append(item.type)
            if (addValues == True):
                value.append(item.value.value)
            if (addTimeStamp == True):
                timestamp.append(item.value.timestamp)
            if (addUnitAbbr == True):
                unitsAbbreviation.append(item.value.units_abbreviation)
            if (addGood == True):
                good.append(item.value.good)
            if (addQuestionable == True):
                questionable.append(item.value.questionable)
            if addSubstituted == True:
                substituted.append(item.value.substituted)

        data = {}
        data['SummaryType'] = summaryType
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
        if (addSubstituted == True):
            data['Substituted'] = substituted;
        df = pd.DataFrame(data)
        return df


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

    def get_recorded_values(self, boundary_type=None, desired_units=None, end_time="*", filter_expression=None,
                            include_filtered_values=None, max_count=None, selected_fields=None, start_time="*-1h",
                            time_zone=None):

        res = self.piwebapi.stream.get_recorded(self.web_id, boundary_type=boundary_type, desired_units=desired_units,
                                          end_time=end_time, filter_expression=filter_expression,
                                          include_filtered_values=include_filtered_values, max_count=max_count,
                                          selected_fields=selected_fields, start_time=start_time, time_zone=time_zone)
        df = self.convert_to_df(res.items, selected_fields)
        return df

    def get_interpolated_values(self, desired_units=None, end_time="*", filter_expression=None,
                                include_filtered_values=None, interval="1h", selected_fields=None, start_time=None,
                                sync_time=None, sync_time_boundary_type=None, time_zone=None):
        
        res = self.piwebapi.stream.get_interpolated(self.web_id, desired_units=desired_units, end_time=end_time,
                                              filter_expression=filter_expression,
                                              include_filtered_values=include_filtered_values, interval=interval,
                                              selected_fields=selected_fields, start_time=start_time,
                                              sync_time=sync_time, sync_time_boundary_type=sync_time_boundary_type,
                                              time_zone=time_zone)
        df = self.convert_to_df(res.items, selected_fields)
        return df

    def get_plot_values(self, desired_units=None, end_time="*", intervals=10, selected_fields=None,
                        start_time="*-1d", time_zone=None):
        res = self.piwebapi.stream.get_plot(self.web_id, desired_units=desired_units, end_time=end_time, intervals=intervals,
                                      selected_fields=selected_fields, start_time=start_time, time_zone=time_zone)
        df = self.convert_to_df(res.items, selected_fields)
        return df

    def get_summary_values(self, calculation_basis='TimeWeighted', end_time="*", filter_expression=None,
                           sample_interval=None, sample_type='ExpressionRecordedValues', selected_fields=None,
                           start_time="*-1d", summary_duration=None, summary_type=['Total'], time_type='Auto',
                           time_zone=None):
        res = self.piwebapi.stream.get_summary(self.web_id, calculation_basis, end_time, filter_expression,
                                         sample_interval, sample_type, selected_fields, start_time, summary_duration,
                                         summary_type, time_type, time_zone)
        df = self.convert_summary_to_df(res.items, selected_fields)
        return df






