"""Exercise the actual app navigation, form validation and saved conditions."""
import unittest
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_main_flow(self):
        app=AppTest.from_file('app.py',default_timeout=30).run()
        self.assertFalse(app.exception)
        app.button(key='menu_rules').click().run()
        self.assertFalse(app.exception)
        app.button(key='run_rules').click().run()
        self.assertFalse(app.exception)
        app.button[1].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.page,'results')
        self.assertEqual(len(app.metric),8)
        app.button(key='back_conditions').click().run()
        self.assertEqual(app.selectbox[0].value,'원문 재현 가정')
        app.date_input[1].set_value(app.date_input[0].value)
        app.button[1].click().run()
        self.assertEqual(len(app.error),1)
        app.button(key='back_home').click().run()
        app.button(key='menu_audit').click().run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('월별').run()
        self.assertFalse(app.exception)

if __name__=='__main__': unittest.main()
