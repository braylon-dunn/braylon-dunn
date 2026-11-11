import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from storykeeper import offline_preview,validate,markdown

SOURCE='In 1984 she moved. “A small miracle” was how she described it.'

class StorykeeperTests(unittest.TestCase):
    def test_quote_and_timeline(self):
        result=offline_preview(SOURCE)
        self.assertEqual(result['quotes'],['A small miracle'])
        self.assertEqual(result['timeline'][0]['date'],'1984')
        self.assertIn('## Timeline',markdown(result))
    def test_invented_quote_rejected(self):
        result=offline_preview(SOURCE)
        result['quotes']=['Invented sentence']
        with self.assertRaises(ValueError):
            validate(result,SOURCE)
    def test_missing_key_rejected(self):
        result=offline_preview(SOURCE)
        del result['title']
        with self.assertRaises(ValueError):
            validate(result,SOURCE)

if __name__=='__main__':
    unittest.main()
