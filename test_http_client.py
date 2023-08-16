# Standard library imports...
import unittest
from unittest.mock import MagicMock, patch

import http_client
from constants import BASE_URL
from http_client import get_content

HEADERS = {'Content-Type': 'text/csv',
           'X-Frame-Options': 'ALLOW-FROM https://docs.google.com',
           'X-Robots-Tag': 'noindex, nofollow, nosnippet',
           'Expires': 'Fri, 11 Aug 2023 19:23:28 GMT',
           'Date': 'Fri, 11 Aug 2023 19:23:28 GMT', 'Cache-Control': 'private, max-age=300',
           'Content-Disposition': 'attachment; filename="-Sheet3.csv"; filename*=UTF-8\'\'%D0%9C%D0%B5%D0%BD%D1%8E%20-%20Sheet3.csv',
           'Content-Encoding': 'gzip', 'Access-Control-Allow-Origin': '*',
           'Access-Control-Expose-Headers': 'Cache-Control,Content-Disposition,Content-Encoding,Content-Length,Content-Type,Date,Expires,Server,Transfer-Encoding',
           'Content-Security-Policy': "require-trusted-types-for 'script';report-uri https://csp.withgoogle.com/csp/docs-tt, frame-ancestors 'self' https://docs.google.com, base-uri 'self';object-src 'self';report-uri https://doc-0g-0s-sheets.googleusercontent.com/spreadsheets/cspreport;script-src 'nonce-JLvp3fGTHLE7jTuTUK-0DA' 'unsafe-inline' 'strict-dynamic' https: http: 'unsafe-eval';worker-src 'self' blob:",
           'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block',
           'Server': 'GSE', 'Alt-Svc': 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000',
           'Transfer-Encoding': 'chunked'}
CONTENT = b'breakfast,lunch,dinner,snacks\r\n"\xd0\x9e\xd0\xb2\xd1\x81\xd1\x8f\xd0\xbd\xd0\xba\xd0\xb0 + \xd1\x8f\xd0\xb3\xd0\xbe\xd0\xb4\xd1\x8b \xd1\x82\xd0\xbe\xd1\x81\xd1\x82 \xd1\x81 \xd1\x81\xd1\x8b\xd1\x80\xd0\xbe\xd0\xbc \xd0\xb8\xd0\xbb\xd0\xb8 \xd1\x81 \xd0\xbc\xd1\x8f\xd1\x81\xd0\xbe\xd0\xbc\n![\xd0\x9e\xd0\xb2\xd1\x81\xd1\x8f\xd0\xbd\xd0\xba\xd0\xb0 - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/d/d8/Oatmeal_porridge_1-minute_with_additional_ingredients.jpg)\n\n**ingredients:**\n\n- oatmeal: 1cup\n- milk: 1cup\n- berries: 0.5cup","\xd0\x91\xd0\xbe\xd1\x80\xd1\x89 ![\xd0\x91\xd0\xbe\xd1\x80\xd1\x89 - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Borscht_served.jpg/2880px-Borscht_served.jpg)\n\n**ingredients:**\n\n- beef\n- pork\n- salo (lard)\n- beetroots\n- cabbage\n- carrots\n- celeriac\n- onions\n- potatoes\n- tomato paste\n- parsley\n- chives\n- dill\n- bay leaves\n- allspice and black pepper",kumpir,\xd0\xba\xd0\xb5\xd1\x84\xd0\xb8\xd1\x80\r\n"\xd0\xaf\xd0\xb8\xd1\x87\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbe\xd0\xbc\xd0\xbb\xd0\xb5\xd1\x82 \xd0\xb9\xd0\xbe\xd0\xb3\xd1\x83\xd1\x80\xd1\x82 \xd1\x81 \xd1\x8f\xd0\xb3\xd0\xbe\xd0\xb4\xd0\xb0\xd0\xbc\xd0\xb8 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbc\xd1\x8e\xd1\x81\xd0\xbb\xd0\xb8, bacon ![\xd0\xaf\xd0\xb8\xd1\x87\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbe\xd0\xbc\xd0\xbb\xd0\xb5\xd1\x82 - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/7/7e/Omelet_With_Fixings.jpg) \n\n**ingredients:**\n\n- eggs: 6\n- milk: 1cup\n- shreded cheese: 0.5cup","\xd0\x93\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9 \xd1\x81\xd1\x83\xd0\xbf ![\xd0\x93\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9 \xd1\x81\xd1\x83\xd0\xbf - Wikipedia](https://upload.wikimedia.org/wikipedia/commons/b/be/Goroh_014.jpg)\n\n**ingredients:**",pizza with salad,\xd0\xb1\xd0\xb0\xd0\xbd\xd0\xb0\xd0\xbd\xd1\x8b\r\n"\xd0\xa2\xd0\xbe\xd1\x81\xd1\x82 \xd1\x81 \xd0\xb0\xd0\xb2\xd0\xbe\xd0\xba\xd0\xb0\xd0\xb4\xd0\xbe \xd0\xb8 \xd1\x8f\xd0\xb8\xd1\x87\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5\xd0\xb9 \xd0\xb1\xd0\xb0\xd0\xbd\xd0\xb0\xd0\xbd/\xd0\xb0\xd0\xbf\xd0\xb5\xd0\xbb\xd1\x8c\xd1\x81\xd0\xb8\xd0\xbd/\xd1\x8f\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xba\xd0\xbe ![\xd0\xa2\xd0\xbe\xd1\x81\xd1\x82 \xd1\x81 \xd0\xb0\xd0\xb2\xd0\xbe\xd0\xba\xd0\xb0\xd0\xb4\xd0\xbe \xd0\xb8 \xd1\x8f\xd0\xb8\xd1\x87\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5\xd0\xb9 \xd0\xb1\xd0\xb0\xd0\xbd\xd0\xb0\xd0\xbd/\xd0\xb0\xd0\xbf\xd0\xb5\xd0\xbb\xd1\x8c\xd1\x81\xd0\xb8\xd0\xbd/\xd1\x8f\xd0\xb1\xd0\xbb\xd0\xbe\xd0\xba\xd0\xbe](https://images.pexels.com/photos/11975658/pexels-photo-11975658.jpeg)\n\n**ingredients:**\n\n- eggs: 1-2\n- bread\n- avocado",\xd0\x9a\xd1\x83\xd1\x80\xd0\xb8\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbb\xd0\xb0\xd0\xbf\xd1\x88\xd0\xb0,salad with shrimps,\xd1\x81\xd0\xbb\xd0\xb0\xd0\xb9\xd1\x81\xd1\x8b \xd1\x80\xd0\xb8\xd1\x81\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb5\r\n"\xd0\xa0\xd1\x8b\xd0\xb1\xd0\xbd\xd1\x8b\xd0\xb5 \xd0\xbf\xd0\xb0\xd0\xbb\xd0\xbe\xd1\x87\xd0\xba\xd0\xb8 \xd0\xb9\xd0\xbe\xd0\xb3\xd1\x83\xd1\x80\xd1\x82 \xd0\xb8\xd0\xbb\xd0\xb8 \xd1\x81\xd0\xbc\xd0\xb5\xd1\x82\xd0\xb0\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xb8 \xd1\x82\xd0\xb2\xd0\xbe\xd1\x80\xd0\xbe\xd0\xb3 \xd0\xbc\xd1\x8e\xd1\x81\xd0\xbb\xd0\xb8 \xd1\x8f\xd0\xb3\xd0\xbe\xd0\xb4\xd1\x8b ![\xd0\xb9\xd0\xbe\xd0\xb3\xd1\x83\xd1\x80\xd1\x82 \xd0\xb8\xd0\xbb\xd0\xb8 \xd1\x81\xd0\xbc\xd0\xb5\xd1\x82\xd0\xb0\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xb8 \xd1\x82\xd0\xb2\xd0\xbe\xd1\x80\xd0\xbe\xd0\xb3 \xd0\xbc\xd1\x8e\xd1\x81\xd0\xbb\xd0\xb8 \xd1\x8f\xd0\xb3\xd0\xbe\xd0\xb4\xd1\x8b](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.weightwatchers.com%2Fimages%2F1033%2Fdynamic%2Fmeals%2F2013%2F08%2F35_GreekYogurtBerries_008_xl.jpg&f=1&nofb=1&ipt=9130552f066d199db6cadf5a8419af886590fc5345b33bc4be0af6d5ee168c6a&ipo=images)\n\n**ingredients:**\n\n- yougurt\n- berries\n- fish sticks\n- musley",\xd0\x9c\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xbe\xd0\xbd\xd0\xbd\xd0\xb8,salad with grilled meat,\xd1\x81\xd1\x8b\xd1\x80\r\n"\xd0\x9b\xd0\xb0\xd0\xb2\xd0\xb0\xd1\x88 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xbb\xd0\xb5\xd0\xbf\xd0\xb5\xd1\x88\xd0\xba\xd0\xb0 \xd1\x81 \xd1\x81\xd1\x8b\xd1\x80\xd0\xbe\xd0\xbc \xd1\x8f\xd0\xb9\xd1\x86\xd0\xbe\xd0\xbc/\xd0\xba\xd0\xbe\xd0\xbb\xd0\xb1\xd0\xb0\xd1\x81\xd0\xbe\xd0\xb9/\xd0\xb7\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xbd\xd1\x8c/\xd0\xb3\xd1\x80\xd0\xb8\xd0\xb1\xd1\x8b ![](https://media.gettyimages.com/id/599256404/photo/scrambled-egg-and-cheese-breakfast-wrap.webp?s=2048x2048&w=gi&k=20&c=ivVE-mBnfNEY0G30QVloiNXfve_30wjRqme1rfsNEzA=)\n\n**ingredients:**\n\n- eggs: 1-2\n- flat bread\n- avocado",\xd0\xa1\xd1\x83\xd0\xbf \xd1\x81 \xd1\x84\xd1\x80\xd0\xb8\xd0\xba\xd0\xb0\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xba\xd0\xb0\xd0\xbc\xd0\xb8,mexican food with salad,\xd0\xba\xd0\xbe\xd0\xbb\xd0\xb1\xd0\xb0\xd1\x81\xd0\xb0\r\n"\xd0\x91\xd0\xbb\xd0\xb8\xd0\xbd\xd1\x8b \xd1\x81\xd0\xbc\xd0\xb5\xd1\x82\xd0\xb0\xd0\xbd\xd0\xb0/\xd0\xb9\xd0\xbe\xd0\xb3\xd1\x83\xd1\x80\xd1\x82 \xd1\x8f\xd0\xb3\xd0\xbe\xd0\xb4\xd1\x8b ![](https://images.pexels.com/photos/8601528/pexels-photo-8601528.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2)\n\n**ingredients:**\n\n- Eggs\n- Milk, whole or 2%\xc2\xa0\n- Cane sugar, or honey\n- Kosher salt\n- Baking soda\n- Light olive oil, or refined coconut oil",\xd0\xa3\xd1\x85\xd0\xb0,roast beef with salad,\xd0\xbc\xd0\xb5\xd0\xb4\r\n"\xd0\xa8\xd0\xb0\xd0\xba\xd1\x88\xd1\x83\xd0\xba\xd0\xb0 ![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Shakshuka_by_Calliopejen1.jpg/2560px-Shakshuka_by_Calliopejen1.jpg)\n\n**ingredients:**\n\n- Eggs\n- Milk, whole or 2%\xc2\xa0\n- Tomato\n- Bell pepper\n- Kosher salt\n- Roasted garlic\n- Light olive oil, or refined coconut oil",\xd0\x93\xd1\x83\xd0\xbb\xd1\x8f\xd1\x88 \xd0\xb3\xd1\x80\xd0\xb5\xd1\x87\xd0\xba\xd0\xb0/\xd0\xb3\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x8e\xd1\x80\xd0\xb5/\xd0\xbc\xd0\xb0\xd0\xba\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b/\xd0\xb7\xd0\xb0\xd0\xbf\xd1\x87 \xd0\xba\xd0\xbe\xd1\x80\xd1\x82\xd0\xbe\xd1\x84\xd0\xb5\xd0\xbb\xd1\x8c \xd1\x81 \xd0\xbe\xd0\xb2\xd0\xbe\xd1\x89\xd0\xb0\xd0\xbc\xd0\xb8,boiled eggs with vegetables,\r\n,\xd0\x97\xd0\xb0\xd0\xbf\xd0\xb5\xd1\x87\xd1\x91\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f \xd1\x80\xd1\x8b\xd0\xb1\xd0\xb0 \xd1\x81\xd0\xb0\xd0\xbb\xd0\xb0\xd1\x82 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xb3\xd1\x80\xd0\xb5\xd1\x87\xd0\xba\xd0\xb0/\xd0\xb3\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x8e\xd1\x80\xd0\xb5/\xd0\xbc\xd0\xb0\xd0\xba\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b/\xd0\xb7\xd0\xb0\xd0\xbf\xd1\x87 \xd0\xba\xd0\xbe\xd1\x80\xd1\x82\xd0\xbe\xd1\x84\xd0\xb5\xd0\xbb\xd1\x8c \xd1\x81 \xd0\xbe\xd0\xb2\xd0\xbe\xd1\x89\xd0\xb0\xd0\xbc\xd0\xb8,sandwiches with meat/ham,\r\n,\xd0\x97\xd0\xb0\xd0\xbf\xd0\xb5\xd1\x87\xd1\x91\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xba\xd1\x83\xd1\x80\xd0\xb8\xd1\x86\xd0\xb0 \xd1\x81\xd0\xb0\xd0\xbb\xd0\xb0\xd1\x82/\xd0\xb3\xd1\x80\xd0\xb5\xd1\x87\xd0\xba\xd0\xb0/\xd0\xb3\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x8e\xd1\x80\xd0\xb5/\xd0\xbc\xd0\xb0\xd0\xba\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b/\xd0\xb7\xd0\xb0\xd0\xbf\xd1\x87 \xd0\xba\xd0\xbe\xd1\x80\xd1\x82\xd0\xbe\xd1\x84\xd0\xb5\xd0\xbb\xd1\x8c \xd1\x81 \xd0\xbe\xd0\xb2\xd0\xbe\xd1\x89\xd0\xb0\xd0\xbc\xd0\xb8,buckwheat with something,\r\n,\xd0\xa7\xd0\xb8\xd0\xbb\xd0\xb8,caesar salad,\r\n,Chicken with vegetables in tomato sauce,sushi,\r\n,shepard\'s pie,,\r\n,kotlety with \xd1\x81\xd0\xb0\xd0\xbb\xd0\xb0\xd1\x82 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xb3\xd1\x80\xd0\xb5\xd1\x87\xd0\xba\xd0\xb0/\xd0\xb3\xd0\xbe\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x8e\xd1\x80\xd0\xb5/\xd0\xbc\xd0\xb0\xd0\xba\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b/\xd0\xb7\xd0\xb0\xd0\xbf\xd1\x87 \xd0\xba\xd0\xbe\xd1\x80\xd1\x82\xd0\xbe\xd1\x84\xd0\xb5\xd0\xbb\xd1\x8c \xd1\x81 \xd0\xbe\xd0\xb2\xd0\xbe\xd1\x89\xd0\xb0\xd0\xbc\xd0\xb8,,\r\n,lentil soap,,\r\n,pirozhki,,\r\n,pirog s myasom,,\r\n,\xd0\x9c\xd1\x8f\xd1\x81\xd0\xbe \xd0\xba\xd1\x83\xd1\x81\xd0\xbe\xd1\x87\xd0\xba\xd0\xb0\xd0\xbc\xd0\xb8 \xd1\x81 \xd0\xba\xd0\xb0\xd1\x80\xd1\x82\xd0\xbe\xd1\x84\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbf\xd1\x8e\xd1\x80\xd1\x83 \xd0\xb8\xd0\xbb\xd0\xb8 \xd1\x82\xd1\x83\xd1\x88\xd0\xb5\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xba\xd0\xb0\xd0\xbf\xd1\x83\xd1\x81\xd1\x82\xd0\xb0,,\r\n,mushroom soap,,\r\n,myso po francuzski,,\r\n,baked salmon with salad,,'
CORRECT_MEAL = '''Тост с авокадо и яичницей банан/апельсин/яблоко ![Тост с авокадо и яичницей банан/апельсин/яблоко](https://images.pexels.com/photos/11975658/pexels-photo-11975658.jpeg)

**ingredients:**

- eggs: 1-2
- bread
- avocado'''
NO_IMAGE_MEAL = '''Тост с авокадо и яичницей банан/апельсин/яблоко 

**ingredients:**

- eggs: 1-2
- bread
- avocado'''
NO_IMAGE_URL = 'https://placehold.co/600x400?text=No+Image'

JUST_TITLE_MEAL = 'Тост с авокадо и яичницей банан/апельсин/яблоко'


# def test_request_response():
#     # Send a request to the API server and store the response.
#     response = requests.get(BASE_URL)
#
#     # Confirm that the request-response cycle completed successfully.
#     assert response.ok

@patch('requests.get')
def test_get_content(mock_get: MagicMock):
    mock_get.return_value.ok = True
    mock_get.return_value.content = CONTENT
    mock_get.return_value.headers = HEADERS

    resp = get_content(BASE_URL)
    assert resp is not None
    assert resp.ok is True
    assert resp.headers.get('Content-Type') == 'text/csv'
    assert len(resp.content) > 0


class DataAPITestCase(unittest.TestCase):
    @patch('requests.get')
    def test_get_csv_should_return_csv(self, mock_get: unittest.mock.MagicMock):
        mock_get.return_value.ok = True
        mock_get.return_value.content = CONTENT
        mock_get.return_value.headers = HEADERS

        uto = http_client.DataAPI()

        got = uto.get_csv()
        self.maxDiff = None
        self.assertEquals(str(CONTENT, encoding='utf-8'), got)

    @patch('requests.get')
    def test_get_csv_should_raise_exception(self, mock_get: unittest.mock.MagicMock):
        mock_get.return_value.ok = False
        mock_get.return_value.content = ''
        mock_get.return_value.headers = HEADERS

        uto = http_client.DataAPI()
        self.assertRaises(Exception, uto.get_csv)

        mock_get.return_value.ok = True
        mock_get.return_value.content = ''
        mock_get.return_value.headers = HEADERS

        self.assertRaises(Exception, uto.get_csv)

    @patch('requests.get')
    def test_get_data(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.content = CONTENT
        mock_get.return_value.headers = HEADERS

        uto = http_client.DataAPI()
        data = uto.get_data()

        self.assertIsNotNone(data)
        self.assertNotEquals(0, len(data))

    @patch('requests.get')
    def test_get_data_raise_exception(self, mock_get):
        mock_get.return_value.ok = False
        mock_get.return_value.content = b'\n\n\n'
        mock_get.return_value.headers = HEADERS

        uto = http_client.DataAPI()
        self.assertRaisesRegex(Exception, "Cannot read csv$", uto.get_data)

    def test_get_meal_image(self):
        data = [
            {
                'name': 'correct meal with desc',
                'txt': CORRECT_MEAL,
                'want': 'https://images.pexels.com/photos/11975658/pexels-photo-11975658.jpeg'
            },
            {
                'name': 'meal with no image',
                'txt': NO_IMAGE_MEAL,
                'want': NO_IMAGE_URL
            },
            {
                'name': 'short meal desc(no ingredients)',
                'txt': JUST_TITLE_MEAL,
                'want': NO_IMAGE_URL
            },
        ]

        for d in data:
            print('test_get_meal_image: ', d['name'])
            uto = http_client.DataAPI()
            got = uto.get_meal_image(d['txt'])
            self.assertEqual(d['want'], got)

    def test_get_meal_title(self):
        data = [
            {
                'name': 'correct meal with desc',
                'txt': CORRECT_MEAL,
                'want': 'Тост с авокадо и яичницей банан/апельсин/яблоко'
            },
            {
                'name': 'meal with no image',
                'txt': NO_IMAGE_MEAL,
                'want': 'Тост с авокадо и яичницей банан/апельсин/яблоко'
            },
            {
                'name': 'short meal desc(no ingredients)',
                'txt': JUST_TITLE_MEAL,
                'want': 'Тост с авокадо и яичницей банан/апельсин/яблоко'
            },
        ]

        for d in data:
            print('test_get_meal_title: ', d['name'])
            uto = http_client.DataAPI()
            got = uto.get_meal_title(d['txt'])
            self.assertEqual(d['want'], got, d['name'])

    def test_get_meal_ingredients(self):
        data = [
            {
                'name': 'correct meal with desc',
                'txt': CORRECT_MEAL,
                'want': '**ingredients:**\n\n- eggs: 1-2\n- bread\n- avocado'
            },
            {
                'name': 'meal with no image',
                'txt': NO_IMAGE_MEAL,
                'want': '**ingredients:**\n\n- eggs: 1-2\n- bread\n- avocado'
            },
            {
                'name': 'short meal desc(no ingredients)',
                'txt': JUST_TITLE_MEAL,
                'want': ''
            },
        ]

        for d in data:
            print('test_get_meal_description: ', d['name'])
            uto = http_client.DataAPI()
            got = uto.get_meal_ingredients(d['txt'])
            self.assertEqual(d['want'], got, d['name'])

    def test_parse_meal(self):
        data = [
            {
                'name': 'correct meal with desc',
                'txt': CORRECT_MEAL,
                'want': http_client.Meal(title='Тост с авокадо и яичницей банан/апельсин/яблоко', img_url='https://images.pexels.com/photos/11975658/pexels-photo-11975658.jpeg', ingredients= '**ingredients:**\n\n- eggs: 1-2\n- bread\n- avocado')
            },
            {
                'name': 'meal with no image',
                'txt': NO_IMAGE_MEAL,
                'want': http_client.Meal(title='Тост с авокадо и яичницей банан/апельсин/яблоко', img_url=NO_IMAGE_URL, ingredients= '**ingredients:**\n\n- eggs: 1-2\n- bread\n- avocado')
            },
            {
                'name': 'short meal desc(no ingredients)',
                'txt': JUST_TITLE_MEAL,
                'want': http_client.Meal(title='Тост с авокадо и яичницей банан/апельсин/яблоко', img_url=NO_IMAGE_URL )
            },
        ]

        for d in data:
            print('test_get_meal_description: ', d['name'])
            uto = http_client.DataAPI()
            got = uto.parse_meal(d['txt'])
            self.assertEqual(d['want'], got, d['name'])
