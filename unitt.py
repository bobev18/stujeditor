import unittest, sys
from userjourney import UserJourney, DDINameException
from step import StepNameException

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from uj_editor_gui import Window

DDI_LIST = ["Build Date", "csrftoken", "Cycle Success", "Friendly Name", "Homepage", "loginstamp", "pageseqnum", "Password", "PO Code", "PO Description", "PO Number", "uisessionid", "Update Purchase Order ID 1", "Update Purchase Order ID 10", "Update Purchase Order ID 11", "Update Purchase Order ID 12", "Update Purchase Order ID 13", "Update Purchase Order ID 14", "Update Purchase Order ID 15", "Update Purchase Order ID 16", "Update Purchase Order ID 17", "Update Purchase Order ID 18", "Update Purchase Order ID 2", "Update Purchase Order ID 20", "Update Purchase Order ID 21", "Update Purchase Order ID 22", "Update Purchase Order ID 23", "Update Purchase Order ID 24", "Update Purchase Order ID 25", "Update Purchase Order ID 26", "Update Purchase Order ID 3", "Update Purchase Order ID 4", "Update Purchase Order ID 5", "Update Purchase Order ID 6", "Update Purchase Order ID 7", "Update Purchase Order ID 8", "Update Purchase Order ID 9", "Update Purchase Order ID 9b", "Username", "xhrseqnum"]
STEP_LIST = ['Home Page', 'Login', 'portletrenderer.jsp', 'portletrenderer.jsp (2)', 'portletrenderer.jsp (3)', 'portletrenderer.jsp (4)', 'Go To', 'blank.gif', 'modimg_asset.gif', 'modimg_consists.gif', 'modimg_financial.gif', 'modimg_int.gif', 'modimg_contract.gif', 'modimg_inventor.gif', 'modimg_plustmp.gif', 'modimg_pm.gif', 'modimg_plans.gif', 'modimg_purchase.gif', 'modimg_sd.gif', 'modimg_sla.gif', 'modimg_util.gif', 'modimg_plustwarr.gif', 'modimg_wo.gif', 'menuback.png', 'item_over.gif', 'Purchase Orders', 'vcobappspr43/maximo/ui/', 'Search WAPPR', 'Next Page', 'More Pages', 'Choose PO', 'PO Lines', 'New Row', 'maximo.jsp', 'Line Type', 'maximo.jsp (2)', 'Item Description', 'Order Unit', 'Unit Cost', 'Work Order', 'SWP', 'Change Status', 'IE_dropdown.gif', 'Open Drop Down', 'maximo.jsp (3)', 'Approved', 'Status OK',]
STEPGROUP_LIST = ['More Pages', 'Purchase Orders', 'Home Page', 'Work Order', 'Next Page', 'Choose PO', 'Status OK', 'SWP', 'Login', 'Go To', 'PO Lines', 'Order Unit', 'Open Drop Down', 'Item Description', 'Unit Cost', 'Search WAPPR', 'Change Status', 'New Row', 'Approved', 'Line Type']

class EditorTest(unittest.TestCase):
    def setUp(self):
        self.test_uj = UserJourney('')
        self.test_uj.import_uj('Update Purchase Order User Journey.xml')

    def test_load(self):
        #  self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual('Update Purchase Order', self.test_uj.name)

    def test_list_ddi(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(DDI_LIST, self.test_uj.list_ddi_names())

    def test_find_ddi_by_attribute(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(2, len(self.test_uj.find_ddi_by_name('Update Purchase Order ID 21').siphons))

    def test_uj_textdump(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertGreaterEqual(self.test_uj.xml().count('Update Purchase Order ID 13'), 1)

    def test_rename_ddi(self):
        # just change the name of DDI object
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        id13 = self.test_uj.find_ddi_by_name('Update Purchase Order ID 13')
        self.assertRaises(DDINameException, self.test_uj.rename_ddi, 'Update Purchase Order ID 13', 'Update Purchase Order ID 14')
        id13.rename('MXID Item')
        self.assertEqual('MXID Item', id13.name)
        id13_anew = self.test_uj.find_ddi_by_name('MXID Item')
        self.assertEqual(id13_anew, id13)
        self.assertRaises(DDINameException, self.test_uj.rename_ddi, 'Update Purchase Order ID 14', 'MXID Item')

    def test_list_steps(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(set(STEP_LIST), set(self.test_uj.list_step_names()))

    def test_find_step_by_attribute(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        # item_desc_step = self.test_uj.find_steps_by_attribute('name', 'Item Description')
        self.assertEqual('Freight', self.test_uj.find_step_by_name('Item Description').success)

    def test_find_step_by_ddi(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        steps_with_id16 = self.test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        item_desc_step = self.test_uj.find_step_by_name('Item Description')
        self.assertIn(item_desc_step, steps_with_id16)

    def test_replace_ddi_referece_in_all_steps(self):
        # replace refereces of ddi name in all steps
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')

        # confirm it works in multiple steps
        step_names_with_csrf = set([str(z) for z in self.test_uj.find_steps_by_ddi_reference('csrftoken')])
        self.test_uj.replace_ddi_references('csrftoken', 'n0_su4_token')
        step_names_with_n0_su4 = set([str(z) for z in self.test_uj.find_steps_by_ddi_reference('n0_su4_token')])
        self.assertEqual(step_names_with_csrf, step_names_with_n0_su4)

        # confirm it works in multiple POST rows
        # {{Update Purchase Order ID 5}}
        steps_with_id5 = self.test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 5')
        self.assertEqual(1, len(steps_with_id5))
        step_with_id5 = steps_with_id5[0]

        self.test_uj.replace_ddi_references('Update Purchase Order ID 5', 'MXID PO App')
        steps_with_po_app = self.test_uj.find_steps_by_ddi_reference('MXID PO App')
        self.assertEqual(1, len(steps_with_po_app))
        step_with_po_app = steps_with_po_app[0]
        self.assertEqual(set(['currentfocus', 'events']), set([  z['name'] for z in step_with_po_app.post_items if z['name'].count('MXID PO App') or z['value'].count('MXID PO App')  ]))

        # confirm it works in multiple step istems - URL, Post, Validation, Headers, [Scripts]
        number_of_steps_with_homepage = len([str(z) for z in self.test_uj.find_steps_by_ddi_reference('Homepage')])
        po_step = self.test_uj.find_step_by_name('Purchase Orders')
        self.assertEqual(1, po_step.request.count('{{Homepage}}'))
        self.assertIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Homepage}}') or z['value'].count('{{Homepage}}') ])
        self.test_uj.replace_ddi_references('Homepage', 'Domain')
        self.assertEqual(0, po_step.request.count('{{Homepage}}'))
        self.assertEqual(1, po_step.request.count('{{Domain}}'))
        self.assertNotIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Homepage}}') or z['value'].count('{{Homepage}}') ])
        self.assertIn('Referer', [ z['name'] for z in po_step.headers if z['name'].count('{{Domain}}') or z['value'].count('{{Domain}}') ])
        number_of_steps_with_domain = len([str(z) for z in self.test_uj.find_steps_by_ddi_reference('Domain')])
        self.assertEqual(number_of_steps_with_homepage, number_of_steps_with_domain)

    def test_rename_and_replace_ddi(self):
        # change the DDI name and relevant occurences in steps
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        id13 = self.test_uj.find_ddi_by_name('Update Purchase Order ID 13')
        self.assertEqual(0, len(self.test_uj.find_steps_by_ddi_reference('MXID Item')))
        self.assertEqual(1, len(self.test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 13')))
        self.assertRaises(DDINameException, self.test_uj.rename_ddi, 'Update Purchase Order ID 13', 'Update Purchase Order ID 14')
        self.test_uj.rename_ddi('Update Purchase Order ID 13', 'MXID Item')
        self.assertEqual('MXID Item', id13.name)
        ddi_by_new_name = self.test_uj.find_ddi_by_name('MXID Item')
        self.assertEqual(id13, ddi_by_new_name)
        self.assertEqual(0, self.test_uj.xml().count('Update Purchase Order ID 13'))
        self.assertEqual(1, len(self.test_uj.find_steps_by_ddi_reference('MXID Item')))

    def test_rename_step(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        steps_with_id16 = self.test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        id16_step = steps_with_id16[0]
        self.assertEqual('Item Description', id16_step.name)
        self.assertRaises(StepNameException, self.test_uj.rename_step, 'Item Description', 'Purchase Orders')
        self.test_uj.rename_step('Item Description', 'Description of Item')
        step_desc_item = self.test_uj.find_step_by_name('Description of Item')
        anew_steps_with_id16 = self.test_uj.find_steps_by_ddi_reference('Update Purchase Order ID 16')
        self.assertIn(step_desc_item, anew_steps_with_id16)

    def test_list_stepgroup_names(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(set(STEPGROUP_LIST), set(self.test_uj.list_stepgroup_names()))

    def test_step_tree_output(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        stepgroup_names = set(self.test_uj.list_stepgroup_names())
        step_names = set(self.test_uj.list_step_names())
        tree_output = self.test_uj.tree_output()

        stepgroup_counts = map(tree_output.count, stepgroup_names)
        map(lambda x: self.assertEqual(1, x), stepgroup_counts)

        step_counts = map(tree_output.count, step_names)
        map(lambda x: self.assertEqual(1, x), step_counts)

    def test_promote_step_to_lead(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(self.test_uj.find_step_by_id(16).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/img_longdescription_off_over.gif')
        self.assertEqual(1, len(self.test_uj.find_steps_by_attribute('id', 16)))
        self.test_uj.promote_step_to_lead(17)
        self.assertEqual(1, len(self.test_uj.find_steps_by_attribute('id', 16)))
        self.assertEqual(self.test_uj.find_step_by_id(16).request, '{{Homepage}}/ui/maximo.jsp')
        self.assertEqual(self.test_uj.find_step_by_id(25).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/IE_dropdown_over.gif')
        self.test_uj.promote_step_to_lead(26)
        self.assertEqual(self.test_uj.find_step_by_id(25).request, '{{Homepage}}/ui/maximo.jsp')

    def test_write_to_file(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(self.test_uj.find_step_by_id(16).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/img_longdescription_off_over.gif')
        self.assertEqual(self.test_uj.find_step_by_id(25).request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/IE_dropdown_over.gif')
        self.assertEqual(1, len(self.test_uj.find_steps_by_attribute('id', 16)))
        self.test_uj.promote_step_to_lead(17)

        self.test_uj.promote_step_to_lead(26)
        self.test_uj.change_uj_name('Update Purchase Order Altered')
        self.test_uj.export_uj('Update Purchase Order Altered User Journey.xml')
        self.test_uj = UserJourney('')
        self.test_uj.import_uj('Update Purchase Order Altered User Journey.xml')
        self.assertEqual(self.test_uj.find_step_by_id(16).request, '{{Homepage}}/ui/maximo.jsp')
        self.assertEqual(1, len(self.test_uj.find_steps_by_attribute('id', 16)))
        self.assertEqual(self.test_uj.find_step_by_id(25).request, '{{Homepage}}/ui/maximo.jsp')
        self.assertEqual(1, self.test_uj.tree_output().split('\n')[0].count('Home Page')) # this ensures the list of steps starts with Home
        self.assertEqual(set(STEPGROUP_LIST), set(self.test_uj.list_stepgroup_names()))
        new_step_names_list = STEP_LIST.copy()
        new_step_names_list[STEP_LIST.index('maximo.jsp (2)')] = 'img_longdescription_off_over.gif'
        new_step_names_list[STEP_LIST.index('maximo.jsp (3)')] = 'IE_dropdown_over.gif'
        self.assertNotEqual(set(STEP_LIST), set(self.test_uj.list_step_names()))
        self.assertEqual(set(new_step_names_list), set(self.test_uj.list_step_names()))

    def test_lone_step_deletion(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(self.test_uj.find_stepgroup_by_id(12).lead_step, self.test_uj.find_step_by_id(12))
        self.assertEqual('{{Homepage}}/ui/maximo.jsp', self.test_uj.find_stepgroup_by_id(12).lead_step.request)
        self.test_uj.delete_step_by_id(12)
        self.assertIsNone(self.test_uj.find_step_by_id(12))
        self.assertIsNone(self.test_uj.find_stepgroup_by_step_id(12))
        self.assertIsNone(self.test_uj.find_stepgroup_by_id(12))
        self.assertEqual(set(STEPGROUP_LIST) - {'Choose PO'}, set(self.test_uj.list_stepgroup_names()))

    def test_non_lead_step_deletion(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertIsNotNone(self.test_uj.find_step_by_id(17))
        self.assertEqual('{{Homepage}}/ui/maximo.jsp', self.test_uj.find_step_by_id(17).request)
        self.assertEqual(16, self.test_uj.find_stepgroup_by_id(self.test_uj.find_step_by_id(17).stepgroup_id).lead_step.id)
        self.test_uj.delete_step_by_id(17)
        self.assertIsNone(self.test_uj.find_step_by_id(17))
        self.assertIsNotNone(self.test_uj.find_stepgroup_by_id(16))

    def test_lead_step_deletion(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(self.test_uj.find_stepgroup_by_id(16).lead_step, self.test_uj.find_step_by_id(16))
        self.assertEqual(self.test_uj.find_stepgroup_by_id(16).lead_step.request, '{{Homepage}}/webclient/{{Build Date}}/tivoli09/images/img_longdescription_off_over.gif')
        self.test_uj.delete_step_by_id(16)
        self.assertEqual(16, self.test_uj.find_stepgroup_by_id(16).lead_step.id)
        self.assertEqual(self.test_uj.find_step_by_id(self.test_uj.find_stepgroup_by_id(16).lead_step.id).request, '{{Homepage}}/ui/maximo.jsp')

    def test_delete_ddi(self):
        # self.test_uj = UserJourney('Update Purchase Order User Journey.xml')
        self.assertEqual(2, len(self.test_uj.find_ddi_by_name('Update Purchase Order ID 21').siphons))
        self.test_uj.delete_ddi('Update Purchase Order ID 21')
        self.assertIsNone(self.test_uj.find_ddi_by_name('Update Purchase Order ID 21'))
        ddi_list_copy = DDI_LIST.copy()
        ddi_list_copy.remove('Update Purchase Order ID 21')
        self.assertEqual(ddi_list_copy, self.test_uj.list_ddi_names())
        self.assertEqual(0, self.test_uj.xml().count('NAME="Update Purchase Order ID 21"'))

    def test_export_matching(self):
        with open('Update Purchase Order User Journey.xml', 'rt') as f:
            original = f.readlines()

        # self.test_uj.name = 'processed'
        # self.test_uj.app_name = 'test'
        # with open('page.xml', 'wt') as f:
        #     f.write(self.test_uj.xml())

        # """
        # text_diff does the following:
        #  - joins lines that do not start with tag for both texts
        #  - compares line to line and pushes lines with difference to tuple
        #  - ignores lines of original has arbitrary '<SUCCESS/>' tag
        #     = adjusts line index for rest of the comparison
        # """
        differences = text_diff(original, self.test_uj.xml().splitlines())
        #  clean the siphon <STARTTEXT> because these differ by the encoded double quotes
        differences = [ z for z in differences if z[0].count('<STARTTEXT') == 0 and z[0].count('<ENDTEXT') == 0 ]
        self.assertEqual([], differences)
        # print(differences)


import re

def text_diff(text1, text2):

    def join_untagged_lines(text):
        result = []
        for i in range(len(text)):
            match = re.search(r'^\s*?<', text[i])
            if match:
                result.append(text[i])
            else:
                # print(i)
                # print(text3[-1].strip())
                result[-1] = result[-1].rstrip() + ' '
                result[-1] += text[i].strip()

        # print(text3[-1].strip())
        return result

    text1 = join_untagged_lines(text1)
    text2 = join_untagged_lines(text2)

    # print(len(text1), len(text2))
    mutator = 0
    differences = []
    for i in range(len(text1)):
        # print(i)
        try:
            if text1[i + mutator].strip() != text2[i].strip():
                # print('t1',i + mutator, text1[i + mutator].strip())
                # print('t2',i, text2[i].strip())
                if text1[i + mutator].strip()=='<SUCCESS/>':
                    mutator += 1
                else:
                    differences.append((text1[i + mutator].strip(), text2[i].strip()))
        except IndexError:
            pass

    return differences




# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

class CustomAssertions:
    def assertIsVisibleToParent(self, widget):
        if not widget.isVisibleTo(widget.parent()):
            widget_ = str(widget)
            try:
                widget_ = widget.text()
            except AttributeError:
                widget_ = str(widget)
            raise AssertionError('widget ' + widget_ +' is not visible')

    def assertIsNotVisibleToParent(self, widget):
        if widget.isVisibleTo(widget.parent()):
            widget_ = str(widget)
            try:
                widget_ = widget.text()
            except AttributeError:
                widget_ = str(widget)
            raise AssertionError('widget ' + widget_ +' is visible')

class UITest(unittest.TestCase, CustomAssertions):
    def setUp(self):
        '''Create the GUI'''
        self.app = QApplication(sys.argv)
        self.window = Window()
        self.window.import_uj(['ddi_exmples UJ.xml'])
        self.select('const') #clears visibility on all special fields apart from Value

    def select(self, name):
        ddi = self.window.ddi_tree.findItems(name, Qt.MatchExactly)[0]
        self.window.ddi_tree.setCurrentItem(ddi)

    def test_import_function(self):
        ddi_tree_root = self.window.ddi_tree.invisibleRootItem()
        child_count = ddi_tree_root.childCount()
        self.assertEqual(child_count, 59)
        step_tree_root = self.window.step_tree.invisibleRootItem()
        self.assertEqual(step_tree_root.childCount(), 2)

    def test_constant_ddi_selection(self):
        # select some DDI type that doesn't show 'value' field
        self.select('Homepage')
        self.select('list')
        self.assertNotEqual(self.window.ddi_value_widget.line_edit.text(), '0')
        self.assertIsNotVisibleToParent(self.window.ddi_value_widget.line_edit)
        # now select contant type DDI
        self.select('const')
        self.assertEqual(self.window.ddi_value_widget.line_edit.text(), '0')
        self.assertIsVisibleToParent(self.window.ddi_value_widget.line_edit)
        # self.assertTrue(self.window.ddi_value_widget.line_edit.isVisibleTo(self.window.ddi_value_widget.line_edit.parent()))

    def test_common_fields(self):
        # self.select('const')    # now covered in SetUp
        self.assertEqual(self.window.ddi_name.line_edit.text(), 'const')
        self.assertIsVisibleToParent(self.window.ddi_name.line_edit)
        self.assertEqual(self.window.ddi_description.line_edit.text(), '')
        self.assertIsVisibleToParent(self.window.ddi_description.line_edit)
        self.assertEqual(self.window.ddi_type.text(), 'Constant')
        self.assertIsVisibleToParent(self.window.ddi_type.combo_box)
        self.assertEqual(self.window.ddi_sharing.text(), '&Single User')
        self.assertIsVisibleToParent(self.window.ddi_sharing.checked())
        self.assertEqual(self.window.ddi_refresh.text(), 'Once per Run')
        self.assertIsVisibleToParent(self.window.ddi_refresh.checked())

    def test_date_ddi_no_offset_now_selection(self):
        self.select('date')
        self.assertEqual(self.window.ddi_date.starting_point.text(), 'now')
        self.assertIsVisibleToParent(self.window.ddi_date.starting_point.checked())
        self.assertEqual(self.window.ddi_date.fixed_value_edit.line_edit.text(), '')
        self.assertIsNotVisibleToParent(self.window.ddi_date.fixed_value_edit.line_edit)
        # self.assertEqual(self.window.ddi_date.related_ddi_box.text(), '')
        self.assertIsNotVisibleToParent(self.window.ddi_date.related_ddi_box.combo_box)
        self.assertEqual(self.window.ddi_date.offset_type.text(), 'none')
        self.assertIsVisibleToParent(self.window.ddi_date.offset_type.checked())
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset1.sign)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset1.amount)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset1.unit)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.sign)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.amount)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.unit)
        self.assertEqual(self.window.ddi_date.format.line_edit.text(), 'dd/MM/yyyy HH:mm')
        self.assertIsVisibleToParent(self.window.ddi_date.format.line_edit)

    def test_date_ddi_fixed_offset_another_date_selection(self):
        self.select('date 3')
        self.assertEqual(self.window.ddi_date.starting_point.text(), 'another date')
        self.assertIsVisibleToParent(self.window.ddi_date.starting_point.checked())
        # self.assertEqual(self.window.ddi_date.fixed_value_edit.line_edit.text(), '')
        self.assertIsNotVisibleToParent(self.window.ddi_date.fixed_value_edit.line_edit)
        self.assertEqual(self.window.ddi_date.related_ddi_box.text(), 'date')
        self.assertIsVisibleToParent(self.window.ddi_date.related_ddi_box.combo_box)
        self.assertEqual(self.window.ddi_date.offset_type.text(), 'fixed')
        self.assertIsVisibleToParent(self.window.ddi_date.offset_type.checked())
        self.assertEqual(self.window.ddi_date.offset1.sign.currentText(), '+')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.sign)
        self.assertEqual(self.window.ddi_date.offset1.amount.text(), '33')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.amount)
        self.assertEqual(self.window.ddi_date.offset1.unit.currentText(), 'sec')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.unit)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.sign)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.amount)
        self.assertIsNotVisibleToParent(self.window.ddi_date.offset2.unit)
        self.assertEqual(self.window.ddi_date.format.line_edit.text(), 'dd/MM/yyyy HH:mm mm:HH')
        self.assertIsVisibleToParent(self.window.ddi_date.format.line_edit)

    def test_date_ddi_random_offset_fixed_date_selection(self):
        self.select('date2')
        self.assertEqual(self.window.ddi_date.starting_point.text(), 'fixed value')
        self.assertIsVisibleToParent(self.window.ddi_date.starting_point.checked())
        self.assertEqual(self.window.ddi_date.fixed_value_edit.line_edit.text(), '21/05/2015 12:00')
        self.assertIsVisibleToParent(self.window.ddi_date.fixed_value_edit.line_edit)
        # self.assertEqual(self.window.ddi_date.related_ddi_box.text(), '')
        self.assertIsNotVisibleToParent(self.window.ddi_date.related_ddi_box.combo_box)
        self.assertEqual(self.window.ddi_date.offset_type.text(), 'random')
        self.assertIsVisibleToParent(self.window.ddi_date.offset_type.checked())
        self.assertEqual(self.window.ddi_date.offset1.sign.currentText(), '-')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.sign)
        self.assertEqual(self.window.ddi_date.offset1.amount.text(), '3')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.amount)
        self.assertEqual(self.window.ddi_date.offset1.unit.currentText(), 'sec')
        self.assertIsVisibleToParent(self.window.ddi_date.offset1.unit)
        self.assertEqual(self.window.ddi_date.offset2.sign.currentText(), '+')
        self.assertIsVisibleToParent(self.window.ddi_date.offset2.sign)
        self.assertEqual(self.window.ddi_date.offset2.amount.text(), '4')
        self.assertIsVisibleToParent(self.window.ddi_date.offset2.amount)
        self.assertEqual(self.window.ddi_date.offset2.unit.currentText(), 'sec')
        self.assertIsVisibleToParent(self.window.ddi_date.offset2.unit)
        self.assertEqual(self.window.ddi_date.format.line_edit.text(), 'dd/MM/yyyy HH:mm')
        self.assertIsVisibleToParent(self.window.ddi_date.format.line_edit)

    def test_delimited_ddi_selection(self):
        self.assertIsNotVisibleToParent(self.window.ddi_delimiter_character_widget.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_delimited_filename_widget.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_delimited_file_picker_button)
        self.assertIsNotVisibleToParent(self.window.ddi_column_index_widget.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_selector_widget.combo_box)
        self.select('delimited')
        self.assertEqual(self.window.ddi_delimiter_character_widget.line_edit.text(), ',')
        self.assertIsVisibleToParent(self.window.ddi_delimiter_character_widget.line_edit)
        self.assertEqual(self.window.ddi_delimited_filename_widget.line_edit.text(), 'a.txt')
        self.assertIsVisibleToParent(self.window.ddi_delimited_filename_widget.line_edit)
        self.assertIsVisibleToParent(self.window.ddi_delimited_file_picker_button)
        self.assertEqual(self.window.ddi_column_index_widget.line_edit.text(), '1')
        self.assertIsVisibleToParent(self.window.ddi_column_index_widget.line_edit)
        self.assertEqual(self.window.ddi_selector_widget.text(), 'Sequential Unique')
        self.assertIsVisibleToParent(self.window.ddi_selector_widget.combo_box)

    def test_list_ddi_selection(self):
        # self.ddi_selector_widget: 'selection_type', self.ddi_column_index_widget: 'column', self.ddi_list_table: ['table']
        self.assertIsNotVisibleToParent(self.window.ddi_selector_widget.combo_box)
        self.assertIsNotVisibleToParent(self.window.ddi_column_index_widget.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_list_table.table)
        self.select('list')
        self.assertEqual(self.window.ddi_selector_widget.text(), 'First')
        self.assertIsVisibleToParent(self.window.ddi_selector_widget.combo_box)
        self.assertEqual(self.window.ddi_column_index_widget.line_edit.text(), '1')
        self.assertIsVisibleToParent(self.window.ddi_column_index_widget.line_edit)
        self.assertEqual(self.window.ddi_list_table.get_values(), [['2', 'a'], ['5', '55']])
        self.assertIsVisibleToParent(self.window.ddi_list_table.table)

    def test_variable_ddi_selection(self):
        self.select('list')
        self.assertIsNotVisibleToParent(self.window.ddi_value_widget.line_edit)
        self.select('variable')
        self.assertEqual(self.window.ddi_value_widget.line_edit.text(), '99')
        self.assertIsVisibleToParent(self.window.ddi_value_widget.line_edit)

    def test_related_ddi_selection(self):
        self.assertIsNotVisibleToParent(self.window.ddi_related_ddi.combo_box)
        self.assertIsNotVisibleToParent(self.window.ddi_column_index_widget.line_edit)
        self.select('related')
        self.assertEqual(self.window.ddi_related_ddi.text(), 'list')
        self.assertIsVisibleToParent(self.window.ddi_related_ddi.combo_box)
        self.assertEqual(self.window.ddi_column_index_widget.line_edit.text(), '33')
        self.assertIsVisibleToParent(self.window.ddi_column_index_widget.line_edit)

    def test_response_ddi(self):
        self.assertIsNotVisibleToParent(self.window.ddi_selector_widget.combo_box)
        self.assertIsNotVisibleToParent(self.window.ddi_response_source_step.combo_box)
        self.assertIsNotVisibleToParent(self.window.ddi_siphon_table.table)
        self.select('response multiline')
        self.assertEqual(self.window.ddi_response_source_step.text(), 'bbb')
        self.assertIsVisibleToParent(self.window.ddi_response_source_step.combo_box)
        self.assertEqual(self.window.ddi_selector_widget.text(), 'Random Unique')
        self.assertIsVisibleToParent(self.window.ddi_selector_widget.combo_box)
        self.assertEqual(self.window.ddi_siphon_table.get_values(), [['Text Substring', 'tuka', 'taka', '2'],
                                                                     ['Regular Expression', 'the(.+?)test', '', '1'],
                                                                     ['Delimiter', '', '', 'All']])
        self.assertIsVisibleToParent(self.window.ddi_siphon_table.table)

    def test_auto_correlated_ddi_selection(self):
        boxes = list(self.window.ddi_auto_correlate_appears_in.boxes.values())
        self.assertIsNotVisibleToParent(self.window.ddi_auto_correlate_type.combo_box)
        self.assertIsNotVisibleToParent(self.window.ddi_auto_correlate_name.combo_box)
        self.assertIsNotVisibleToParent(boxes[0])
        self.select('auto_correlated_repeated')
        self.assertEqual(self.window.ddi_auto_correlate_type.text(), 'Repeated Fields')
        self.assertIsVisibleToParent(self.window.ddi_auto_correlate_type.combo_box)
        self.assertEqual(self.window.ddi_auto_correlate_name.text(), 'Host')
        self.assertIsVisibleToParent(self.window.ddi_auto_correlate_name.combo_box)
        self.assertEqual(self.window.ddi_auto_correlate_appears_in.text(), {'URL': True, 'Post': False, 'Headers': False})
        for box in boxes:
            self.assertIsVisibleToParent(box)

    def test_auto_increment_ddi_selection(self):
        self.assertIsNotVisibleToParent(self.window.ddi_auto_increment_starting_value.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_auto_increment_increment.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_auto_increment_prefix.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_auto_increment_suffix.line_edit)
        self.assertIsNotVisibleToParent(self.window.ddi_auto_increment_min_lenght.line_edit)
        self.select('auto_increment')
        self.assertEqual(self.window.ddi_auto_increment_starting_value.text(), '55')
        self.assertIsVisibleToParent(self.window.ddi_auto_increment_starting_value.line_edit)
        self.assertEqual(self.window.ddi_auto_increment_increment.text(), '43')
        self.assertIsVisibleToParent(self.window.ddi_auto_increment_increment.line_edit)
        self.assertEqual(self.window.ddi_auto_increment_prefix.text(), 'asda')
        self.assertIsVisibleToParent(self.window.ddi_auto_increment_prefix.line_edit)
        self.assertEqual(self.window.ddi_auto_increment_suffix.text(), '342sdf')
        self.assertIsVisibleToParent(self.window.ddi_auto_increment_suffix.line_edit)
        self.assertEqual(self.window.ddi_auto_increment_min_lenght.text(), '2')
        self.assertIsVisibleToParent(self.window.ddi_auto_increment_min_lenght.line_edit)























if __name__ == "__main__":
    try: unittest.main()
    except SystemExit: pass



