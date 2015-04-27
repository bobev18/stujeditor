import unittest
from userjourney import UserJourney

class EditorTest(unittest.TestCase):

    def test_load(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual('Update Purchase Order', test_uj.name)


if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass



