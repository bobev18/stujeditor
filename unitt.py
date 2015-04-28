import unittest
from userjourney import UserJourney

DDI_LIST = ["Build Date", "csrftoken", "Cycle Success", "Friendly Name", "Homepage", "loginstamp", "pageseqnum", "Password", "PO Code", "PO Description", "PO Number", "uisessionid", "Update Purchase Order ID 1", "Update Purchase Order ID 10", "Update Purchase Order ID 11", "Update Purchase Order ID 12", "Update Purchase Order ID 13", "Update Purchase Order ID 14", "Update Purchase Order ID 15", "Update Purchase Order ID 16", "Update Purchase Order ID 17", "Update Purchase Order ID 18", "Update Purchase Order ID 2", "Update Purchase Order ID 20", "Update Purchase Order ID 21", "Update Purchase Order ID 22", "Update Purchase Order ID 23", "Update Purchase Order ID 24", "Update Purchase Order ID 25", "Update Purchase Order ID 26", "Update Purchase Order ID 3", "Update Purchase Order ID 4", "Update Purchase Order ID 5", "Update Purchase Order ID 6", "Update Purchase Order ID 7", "Update Purchase Order ID 8", "Update Purchase Order ID 9", "Update Purchase Order ID 9b", "Username", "xhrseqnum"]
STEP_LIST = ['Home Page', 'Login', 'portletrenderer.jsp', 'portletrenderer.jsp (2)', 'portletrenderer.jsp (3)', 'portletrenderer.jsp (4)', 'Go To', 'blank.gif', 'modimg_asset.gif', 'modimg_consists.gif', 'modimg_financial.gif', 'modimg_int.gif', 'modimg_contract.gif', 'modimg_inventor.gif', 'modimg_plustmp.gif', 'modimg_pm.gif', 'modimg_plans.gif', 'modimg_purchase.gif', 'modimg_sd.gif', 'modimg_sla.gif', 'modimg_util.gif', 'modimg_plustwarr.gif', 'modimg_wo.gif', 'menuback.png', 'item_over.gif', 'Purchase Orders', 'vcobappspr43/maximo/ui/', 'Search WAPPR', 'Next Page', 'More Pages', 'Choose PO', 'PO Lines', 'New Row', 'maximo.jsp', 'Line Type', 'maximo.jsp (2)', 'Item Description', 'Order Unit', 'Unit Cost', 'Work Order', 'SWP', 'Change Status', 'IE_dropdown.gif', 'Open Drop Down', 'maximo.jsp (3)', 'Approved', 'Status OK',]

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

    def test_uj_textdump(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertGreaterEqual(str(test_uj).count('Update Purchase Order ID 13'), 1)

    def test_ddi_name_change(self):
        # just change the name of DDI object
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        id13 = test_uj.pull_ddi_by('name', 'Update Purchase Order ID 13')
        id13.rename('MXID Item')
        self.assertEqual('MXID Item', id13.name)
        id13_anew = test_uj.pull_ddi_by('name', 'MXID Item')
        self.assertEqual(id13_anew, id13)



    def test_list_steps(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(STEP_LIST, test_uj.list_step_names())

    def test_find_step_by_attribute(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        item_desc_step = test_uj.pull_step_by('name', 'Item Description')
        self.assertEqual('Freight', test_uj.pull_step_by('name', 'Item Description').success)

    def test_find_step_by_ddi(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        steps_with_id16 = test_uj.pull_steps_by_ddi('Update Purchase Order ID 16')
        item_desc_step = test_uj.pull_step_by('name', 'Item Description')
        self.assertIn(item_desc_step, steps_with_id16)

        # id13 = test_uj.pull_step_by_ddi('Update Purchase Order ID 13')
        # id13.rename('MXID Item')
        # self.assertEqual('MXID Item', id13.name)
        # id13_anew = test_uj.pull_ddi_by('name', 'MXID Item')
        # self.assertEqual(id13_anew, id13)



    # def test_rename_ddi(self):
    #     # change the DDI name and relevant occurences in steps
    #     test_uj = UserJourney('Update Purchase Order User Journey.xml')
    #     id13 = test_uj.pull_ddi_by('name', 'Update Purchase Order ID 13')
    #     self.assertEqual(0, str(test_uj).count('MXID Item'))
    #     # greater than 1 is due to = one in DDI definition, may have more in refference to the DDI among the steps
    #     self.assertGreaterEqual(str(test_uj).count('Update Purchase Order ID 13'), 1)
    #     old_count = str(test_uj).count('Update Purchase Order ID 13')
    #     id13.rename('MXID Item')
    #     self.assertEqual('MXID Item', id13.name)
    #     id13_anew = test_uj.pull_ddi_by('name', 'MXID Item')
    #     self.assertEqual(id13_anew, id13)
    #     self.assertEqual(0, str(test_uj).count('Update Purchase Order ID 13'))
    #     self.assertEqual(old_count, str(test_uj).count('MXID Item'))








if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass



