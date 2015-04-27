import unittest
from userjourney import UserJourney

DDI_LIST = ["Build Date", "csrftoken", "Cycle Success", "Friendly Name", "Homepage", "loginstamp", "pageseqnum", "Password", "PO Code", "PO Description", "PO Number", "uisessionid", "Update Purchase Order ID 1", "Update Purchase Order ID 10", "Update Purchase Order ID 11", "Update Purchase Order ID 12", "Update Purchase Order ID 13", "Update Purchase Order ID 14", "Update Purchase Order ID 15", "Update Purchase Order ID 16", "Update Purchase Order ID 17", "Update Purchase Order ID 18", "Update Purchase Order ID 2", "Update Purchase Order ID 20", "Update Purchase Order ID 21", "Update Purchase Order ID 22", "Update Purchase Order ID 23", "Update Purchase Order ID 24", "Update Purchase Order ID 25", "Update Purchase Order ID 26", "Update Purchase Order ID 3", "Update Purchase Order ID 4", "Update Purchase Order ID 5", "Update Purchase Order ID 6", "Update Purchase Order ID 7", "Update Purchase Order ID 8", "Update Purchase Order ID 9", "Update Purchase Order ID 9b", "Username", "xhrseqnum"]

class EditorTest(unittest.TestCase):

    def test_load(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual('Update Purchase Order', test_uj.name)

    def test_list_ddi(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(DDI_LIST, test_uj.list_ddi_names())

    def test_find_ddi_by_attribute(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(2, len(test_uj.pull_ddi_by('name', 'Update Purchase Order ID 21').siphons))


if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass



