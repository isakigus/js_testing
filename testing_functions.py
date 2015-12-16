import datetime
import common as cmn


def get_browser_params(driver):
    url = driver.current_url
    window_name = cmn.get_window_name(driver)
    topbar = cmn.check_topbar(driver)
    print cmn.get_datetime(driver)
    # for c in driver.get_cookies():
    #     print c
    return url, window_name, topbar


class Functions:

    CTX_URL = 'http://www.vuelosbaratos.es'
    RON_URL = 'http://www.google.com'

    @staticmethod
    def test_cookies(self, driver, data, mode):
        if mode == 'ctx':
            url, cookie_name = Functions.CTX_URL, 'domain_ctx_cookie'
        elif mode == 'ron':
            url, cookie_name = Functions.RON_URL, 'domain_ron_cookie'

        browser, dt = None, datetime.datetime.now()

        try:
            browser = cmn.get_driver(driver)

            print
            print '-' * 100
            print browser

            pid = data.get('pid')

            aff_id = cmn.get_aff_id(pid)

            ctx_injection = cmn.injection_script(pid, aff_id)
            load_time_script = cmn.time_script_init(dt)
            time_up = cmn.increase_time(data.get(cookie_name), dt)

            # print time_up

            browser.get(url)
            browser.execute_script(ctx_injection)
            browser.execute_script(load_time_script)

            url_base, window_name, topbar = get_browser_params(browser)
            print 'web loaded'
            print url_base, window_name, topbar

            # First click No cookie
            cmn.body_click(browser)
            url1, window_name, topbar = get_browser_params(browser)
            print 'after first click'
            print url1, window_name, topbar

            # Second click with cookie
            browser.get(url)
            browser.execute_script(load_time_script)
            browser.execute_script(time_up)
            cmn.body_click(browser)

            url2, window_name, topbar = get_browser_params(browser)
            print 'after second click'
            print url2, window_name, topbar

            self.assertEqual(url_base, url2)
            self.assertNotEqual(url_base, url1)

        finally:
            if browser:
                cmn.close_driver(browser)

    @staticmethod
    def test_ctx_cookie_times(self, driver, data):

        browser, dt = None, datetime.datetime.now()
        try:
            browser = cmn.get_driver(driver)

            print
            print '-' * 100
            print browser

            pid = data.get('pid')

            aff_id = cmn.get_aff_id(pid)

            ctx_injection = cmn.injection_script(pid, aff_id)
            load_time_script = cmn.time_script_init(dt)
            time_up = cmn.increase_time(data.get('domain_ctx_cookie'), dt)

            # print time_up

            url = Functions.CTX_URL

            browser.get(url)
            browser.execute_script(ctx_injection)
            browser.execute_script(load_time_script)

            url_base, window_name, topbar = get_browser_params(browser)
            print 'web loaded'
            print url_base, window_name, topbar

            # First click No cookie
            cmn.body_click(browser)
            url1, window_name, topbar = get_browser_params(browser)
            print 'after first click'
            print url1, window_name, topbar

            # Second click with cookie
            browser.get(url)
            browser.execute_script(load_time_script)
            browser.execute_script(time_up)
            cmn.body_click(browser)

            url2, window_name, topbar = get_browser_params(browser)
            print 'after second click'
            print url2, window_name, topbar

            self.assertEqual(url_base, url2)
            self.assertNotEqual(url_base, url1)

        finally:
            if browser:
                cmn.close_driver(browser)
