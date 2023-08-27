from kdb import report
from kdb.webdriver import kdb_driver
from scripts.vb.mobile.page_object.auth.active_page import ActivePage
from scripts.vb.mobile.page_object.auth.login_page import LoginPage
from scripts.vb.mobile.page_object.auth.prelogin_page import PreLoginPage
from scripts.vb.mobile.page_object.home.home_page import HomePage
from scripts.vb.mobile.page_object.home.popup_active_softotp_page import PopupActiveSoftOtpPage
from scripts.vb.mobile.page_object.home.popup_lucky_money_page import PopupLuckyMoneyPage
from scripts.vb.mobile.page_object.softotp.popup_set_pin_soft_success_page import PopupSetPinSoftSuccessPage
from scripts.vb.mobile.page_object.softotp.set_pin_page import SetPinPage
from scripts.vb.mobile.page_object.transfer import TransferConfirmPage, TransferSuccessPage
from scripts.vb.mobile.page_object.transfer.transfer_in.transfer_to_same_holder_page import TransferInToSameHolderPage


def login_test(profile, data_test, params):
    report.add_comment("Open a app")
    # start browser
    kdb_driver.open_app('vb-dev.apk', 'android', False)
    kdb_driver.screen_shot()
    prelogin = PreLoginPage()
    prelogin.wait_page_loaded()
    kdb_driver.screen_shot()
    prelogin.is_language_vi()
    # prelogin.click_language()
    # prelogin.is_language_en()
    prelogin.click_login()

    kdb_driver.screen_shot(extra_time=3)
    login = LoginPage()
    login.login('0963204943', 'Abc123')
    kdb_driver.verify_text_on_page(
        'Quý khách lần đầu đăng nhập trên thiết bị này hoặc đã kích hoạt thành công trên thiết bị khác. Để đảm bảo an toàn giao dịch, mã kích hoạt đã được gửi đến số ĐTDĐ đăng ký. Quý khách vui lòng nhập mã số để kích hoạt sử dụng.')
    kdb_driver.verify_text_on_page('để nhập mã kích hoạt')
    kdb_driver.screen_shot()
    active_page = ActivePage()
    active_page.active('8888888')

    popup_softotp = PopupActiveSoftOtpPage()
    popup_softotp.click_continue()

    set_pin_page = SetPinPage()
    set_pin_page.active('080894')

    popup_set_pin_success = PopupSetPinSoftSuccessPage()
    popup_set_pin_success.click_close()

    popup_lucky_money = PopupLuckyMoneyPage()
    popup_lucky_money.close_popup()

    home_page = HomePage()
    home_page.click_transfer()

    transfer_in_to_same_holder = TransferInToSameHolderPage()
    transfer_in_to_same_holder.click_to_same_holder()
    # kdb_driver.mobile_gestures.swipe(direction=kdb_driver.mobile_gestures.direction.DOWN)
    transfer_in_to_same_holder.transfer('000000190445', '000000307339', '2234', 'noi dung ck')
    transfer_confirm_page = TransferConfirmPage()
    transfer_confirm_page.click_continue()

    transfer_success_page = TransferSuccessPage()
    transfer_success_page.wait_page_loaded()
    kdb_driver.screen_shot()
    transfer_success_page.click_home()

    home_page.wait_page_loaded()
    kdb_driver.screen_shot()
