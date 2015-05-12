import unittest
from userjourney import UserJourney, DDINameException
from step import StepNameException

DDI_LIST = ["Build Date", "csrftoken", "Cycle Success", "Friendly Name", "Homepage", "loginstamp", "pageseqnum", "Password", "PO Code", "PO Description", "PO Number", "uisessionid", "Update Purchase Order ID 1", "Update Purchase Order ID 10", "Update Purchase Order ID 11", "Update Purchase Order ID 12", "Update Purchase Order ID 13", "Update Purchase Order ID 14", "Update Purchase Order ID 15", "Update Purchase Order ID 16", "Update Purchase Order ID 17", "Update Purchase Order ID 18", "Update Purchase Order ID 2", "Update Purchase Order ID 20", "Update Purchase Order ID 21", "Update Purchase Order ID 22", "Update Purchase Order ID 23", "Update Purchase Order ID 24", "Update Purchase Order ID 25", "Update Purchase Order ID 26", "Update Purchase Order ID 3", "Update Purchase Order ID 4", "Update Purchase Order ID 5", "Update Purchase Order ID 6", "Update Purchase Order ID 7", "Update Purchase Order ID 8", "Update Purchase Order ID 9", "Update Purchase Order ID 9b", "Username", "xhrseqnum"]
STEP_LIST = ['Home Page', 'Login', 'portletrenderer.jsp', 'portletrenderer.jsp (2)', 'portletrenderer.jsp (3)', 'portletrenderer.jsp (4)', 'Go To', 'blank.gif', 'modimg_asset.gif', 'modimg_consists.gif', 'modimg_financial.gif', 'modimg_int.gif', 'modimg_contract.gif', 'modimg_inventor.gif', 'modimg_plustmp.gif', 'modimg_pm.gif', 'modimg_plans.gif', 'modimg_purchase.gif', 'modimg_sd.gif', 'modimg_sla.gif', 'modimg_util.gif', 'modimg_plustwarr.gif', 'modimg_wo.gif', 'menuback.png', 'item_over.gif', 'Purchase Orders', 'vcobappspr43/maximo/ui/', 'Search WAPPR', 'Next Page', 'More Pages', 'Choose PO', 'PO Lines', 'New Row', 'maximo.jsp', 'Line Type', 'maximo.jsp (2)', 'Item Description', 'Order Unit', 'Unit Cost', 'Work Order', 'SWP', 'Change Status', 'IE_dropdown.gif', 'Open Drop Down', 'maximo.jsp (3)', 'Approved', 'Status OK',]
STEPGROUP_LIST = ['More Pages', 'Purchase Orders', 'Home Page', 'Work Order', 'Next Page', 'Choose PO', 'Status OK', 'SWP', 'Login', 'Go To', 'PO Lines', 'Order Unit', 'Open Drop Down', 'Item Description', 'Unit Cost', 'Search WAPPR', 'Change Status', 'New Row', 'Approved', 'Line Type']

class EditorTest(unittest.TestCase):

    def test_load(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual('Update Purchase Order', test_uj.name)

    def test_list_ddi(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(DDI_LIST, test_uj.list_ddi_names())

    def test_find_ddi_by_attribute(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(2, len(test_uj.find_ddi_by_name('Update Purchase Order ID 21').siphons))

    def test_uj_textdump(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertGreaterEqual(str(test_uj).count('Update Purchase Order ID 13'), 1)

    def test_rename_ddi(self):
        # just change the name of DDI object
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        id13 = test_uj.find_ddi_by_name('Update Purchase Order ID 13')
        self.assertRaises(DDINameException, test_uj.rename_ddi, 'Update Purchase Order ID 13', 'Update Purchase Order ID 14')
        id13.rename('MXID Item')
        self.assertEqual('MXID Item', id13.name)
        id13_anew = test_uj.find_ddi_by_name('MXID Item')
        self.assertEqual(id13_anew, id13)
        self.assertRaises(DDINameException, test_uj.rename_ddi, 'Update Purchase Order ID 14', 'MXID Item')



    def test_list_steps(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(set(STEP_LIST), set(test_uj.list_step_names()))

    def test_find_step_by_attribute(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        # item_desc_step = test_uj.find_steps_by_attribute('name', 'Item Description')
        self.assertEqual('Freight', test_uj.find_step_by_name('Item Description').success)

    def test_find_step_by_ddi(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        steps_with_id16 = test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        item_desc_step = test_uj.find_step_by_name('Item Description')
        self.assertIn(item_desc_step, steps_with_id16)

    def test_replace_ddi_referece_in_all_steps(self):
        # replace refereces of ddi name in all steps
        test_uj = UserJourney('Update Purchase Order User Journey.xml')

        # confirm it works in multiple steps
        step_names_with_csrf = set([str(z) for z in test_uj.find_steps_by_ddi_reference('csrftoken')])
        test_uj.replace_ddi_references('csrftoken', 'n0_su4_token')
        step_names_with_n0_su4 = set([str(z) for z in test_uj.find_steps_by_ddi_reference('n0_su4_token')])
        self.assertEqual(step_names_with_csrf, step_names_with_n0_su4)

        # confirm it works in multiple POST rows
        # {{Update Purchase Order ID 5}}
        steps_with_id5 = test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 5')
        self.assertEqual(1, len(steps_with_id5))
        step_with_id5 = steps_with_id5[0]

        test_uj.replace_ddi_references('Update Purchase Order ID 5', 'MXID PO App')
        steps_with_po_app = test_uj.find_steps_by_ddi_reference('MXID PO App')
        self.assertEqual(1, len(steps_with_po_app))
        step_with_po_app = steps_with_po_app[0]
        self.assertEqual(set(['currentfocus', 'events']), set([  z['name'] for z in step_with_po_app.post_items if z['name'].count('MXID PO App') or z['value'].count('MXID PO App')  ]))

        # confirm it works in multiple step istems - URL, Post, Validation, Headers, [Scripts]
        number_of_steps_with_homepage = len([str(z) for z in test_uj.find_steps_by_ddi_reference('Homepage')])
        po_step = test_uj.find_step_by_name('Purchase Orders')
        self.assertEqual(1, po_step.request.count('{{Homepage}}'))
        self.assertIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Homepage}}') or z['value'].count('{{Homepage}}') ])
        test_uj.replace_ddi_references('Homepage', 'Domain')
        self.assertEqual(0, po_step.request.count('{{Homepage}}'))
        self.assertEqual(1, po_step.request.count('{{Domain}}'))
        self.assertNotIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Homepage}}') or z['value'].count('{{Homepage}}') ])
        self.assertIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Domain}}') or z['value'].count('{{Domain}}') ])
        number_of_steps_with_domain = len([str(z) for z in test_uj.find_steps_by_ddi_reference('Domain')])
        self.assertEqual(number_of_steps_with_homepage, number_of_steps_with_domain)

    def test_rename_and_replace_ddi(self):
        # change the DDI name and relevant occurences in steps
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        id13 = test_uj.find_ddi_by_name('Update Purchase Order ID 13')
        self.assertEqual(0, len(test_uj.find_steps_by_ddi_reference('MXID Item')))
        self.assertEqual(1, len(test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 13')))
        self.assertRaises(DDINameException, test_uj.rename_ddi, 'Update Purchase Order ID 13', 'Update Purchase Order ID 14')
        test_uj.rename_ddi('Update Purchase Order ID 13', 'MXID Item')
        self.assertEqual('MXID Item', id13.name)
        ddi_by_new_name = test_uj.find_ddi_by_name('MXID Item')
        self.assertEqual(id13, ddi_by_new_name)
        self.assertEqual(0, str(test_uj).count('Update Purchase Order ID 13'))
        self.assertEqual(1, len(test_uj.find_steps_by_ddi_reference('MXID Item')))

    def test_rename_step(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        steps_with_id16 = test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        id16_step = steps_with_id16[0]
        self.assertEqual('Item Description', id16_step.name)
        self.assertRaises(StepNameException, test_uj.rename_step, 'Item Description', 'Purchase Orders')
        test_uj.rename_step('Item Description', 'Description of Item')
        step_desc_item = test_uj.find_step_by_name('Description of Item')
        anew_steps_with_id16 = test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        self.assertIn(step_desc_item, anew_steps_with_id16)

    def test_list_stepgroup_names(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(set(STEPGROUP_LIST), set(test_uj.list_stepgroup_names()))

    def test_step_tree_output(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        stepgroup_names = set(test_uj.list_stepgroup_names())
        step_names = set(test_uj.list_step_names())
        tree_output = test_uj.tree_output()

        stepgroup_counts = map(tree_output.count, stepgroup_names)
        map(lambda x: self.assertEqual(1, x), stepgroup_counts)

        step_counts = map(tree_output.count, step_names)
        map(lambda x: self.assertEqual(1, x), step_counts)

    def test_promote_step_to_lead(self):
        test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(test_uj.find_step_by_id(16).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/img_longdescription_off_over.gif')
        test_uj.promote_step_to_lead(17)
        self.assertEqual(test_uj.find_step_by_id(16).request, '{{Homepage}}/ui/maximo.jsp')
        self.assertEqual(test_uj.find_step_by_id(25).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/IE_dropdown_over.gif')
        test_uj.promote_step_to_lead(26)
        self.assertEqual(test_uj.find_step_by_id(25).request, '{{Homepage}}/ui/maximo.jsp')

    # def test_write_to_file(self):
    #     test_uj = UserJourney('Update Purchase Order User Journey.xml')
    #     self.assertEqual(test_uj.find_step_by_id(16).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/img_longdescription_off_over.gif')
    #     self.assertEqual(test_uj.find_step_by_id(25).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/IE_dropdown_over.gif')
    #     test_uj.promote_step_to_lead(17)
    #     test_uj.promote_step_to_lead(26)
    #     test_uj.change_uj_name('Update Purchase Order Altered')
    #     test_uj.write_to_file('Update Purchase Order Altered User Journey.xml')
    #     test_uj = UserJourney('Update Purchase Order Altered User Journey.xml')
    #     self.assertEqual(test_uj.find_step_by_id(16).request, '{{Homepage}}/ui/maximo.jsp')
    #     self.assertEqual(test_uj.find_step_by_id(25).request, '{{Homepage}}/ui/maximo.jsp')















if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass



