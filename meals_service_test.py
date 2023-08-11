import unittest
from meals_service import get_meal_image, get_meal_title, get_meal_description, NO_IMAGE_URL

class Test(unittest.TestCase):
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
            print('test_get_meal_image: ' ,d['name'])
            got = get_meal_image(d['txt'])
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
            print('test_get_meal_title: ' ,d['name'])
            got = get_meal_title(d['txt'])         
            self.assertEqual(d['want'], got, d['name'])

    def test_get_meal_description(self):
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
            print('test_get_meal_description: ' ,d['name'])
            got = get_meal_description(d['txt'])         
            self.assertEqual(d['want'], got, d['name'])            

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

JUST_TITLE_MEAL = 'Тост с авокадо и яичницей банан/апельсин/яблоко'

if __name__ == '__main__':
    unittest.main()