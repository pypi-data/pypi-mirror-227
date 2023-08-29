import requests
import pandas as pd
from datetime import date


class APIError(Exception):
    pass


class APIKeyError(Exception):
    pass

class API(object):
    def __init__(self, token):
        """
        Initialise the eia object:
        :param token: string
        :return: eia object
        """
        self.token = token

    def get_routes(self):
        '''
        Get available routes for the API
        :return: Returns available routes for EIA APIs in dictionary form
        '''
        eia_api_url = 'https://api.eia.gov/v2/?api_key={}'

        values_dict = {}
        response = requests.get(eia_api_url.format(self.token))
        if response.json().get('error'):
            error_msg = response.json().get('error').get('message')
            raise APIKeyError(error_msg)
        else:
            data = response.json().get('response').get('routes')

            lst_ids = [x.get('id')
                       for x in data]
            lst_descriptions = [x.get('description')
                                for x in data]
            return dict(zip(lst_ids, lst_descriptions))

    def get_topics(self, route):
        '''
        Get available topics for the given route
        :param route: string
        :return: Returns available topics for EIA series in dictionary form
        '''
        eia_api_url = 'https://api.eia.gov/v2/{}/?api_key={}'

        response = requests.get(eia_api_url.format(route, self.token))
        if response.json().get('error'):
            error_msg = response.json().get('error').get('message')
            raise APIKeyError(error_msg)
        else:
            data = response.json().get('response').get('routes')

        if data is not None:
            lst_ids = [str(x.get('id'))
                       for x in data]
            lst_descriptions = [str(x.get('name'))
                                for x in data]
            return dict(zip(lst_ids, lst_descriptions))
        else:
            return {}

    def get_sub_topics(self, route, topic):
        '''
        Get available sub-topics for the given route and topic
        :param route: string
        :param topic: string
        :return: Returns available sub-topics for EIA series in dictionary form
        '''
        eia_api_url = 'https://api.eia.gov/v2/{}/{}/?api_key={}'

        values_dict = {}
        response = requests.get(eia_api_url.format(route, topic, self.token))
        if response.json().get('error'):
            error_msg = response.json().get('error').get('message')
            raise APIKeyError(error_msg)
        if response.json().get('response').get('data'):
            return values_dict
        else:
            data = response.json().get('response').get('routes')

            lst_ids = [str(x.get('id'))
                       for x in data]
            lst_descriptions = [str(x.get('name'))
                                for x in data]
            return dict(zip(lst_ids, lst_descriptions))

    def get_data(self, start_date: date, end_date: date, route: str, topic: str, sub_topic='', frequency='annual'):
        '''
        Get available subroutes for the given route
        :param start_date: date
        :param end_date: date
        :param route: string
        :param topic: string
        :param optional sub-topic: string
        :param default(annual) frequency: string
        :return: Returns available sub-routes for EIA series in dataFrame
        '''
        eia_topic_url = 'https://api.eia.gov/v2/{}/{}/data?api_key={}&start={}&end={}&frequency={}&offset={}&length={}'
        eia_sub_topic_url = 'https://api.eia.gov/v2/{}/{}/{}/data?api_key={}&start={}&end={}&frequency={}&offset={}&length={}'

        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        stop_fetch = False
        data_df = pd.DataFrame()
        offset = 0
        max_length = 5_000
        while(not stop_fetch):
            # Don't want infinite loop
            stop_fetch = True
            if sub_topic:
                response = requests.get(eia_sub_topic_url.format(
                    route, topic, sub_topic, self.token, start_date_str, end_date_str, frequency, offset, max_length))
            else:
                response = requests.get(eia_topic_url.format(
                    route, topic, self.token, start_date_str, end_date_str, frequency, offset, max_length))

            if response.json().get('error'):
                error_msg = response.json().get('error').get('message')
                raise APIKeyError(error_msg)
            else:
                if response.json().get('response').get('data'):
                    data = response.json().get('response').get('data')
                    values_dict = {}
                    for count, item in enumerate(data):
                        values_dict[count] = {}
                        for k in item:
                            values_dict[count][k] = item[k]

                if max_length == len(data):
                    stop_fetch = False
                    offset += max_length
                else:
                    stop_fetch = True
            result = pd.concat(
                [data_df, pd.DataFrame.from_dict(values_dict, orient='index')])
            data_df = result
        return data_df
