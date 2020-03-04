# create_order.py
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from faker import Faker
import random
import time


def create_woo_order(headless=False):

    # create instance of faker
    fake = Faker()

    # get the store up in selenium
    url = "http://woocommerce.sales.ns8demos.com"
    opts = Options()
    opts.headless = headless
    browser = Firefox(options=opts)
    browser.get(url)

    # Choose Products
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/main/section[2]/div/ul/li[1]/a[1]/img').click()

    # Adjust number of items to add to cart
    qty = browser.find_elements_by_class_name("input-text.qty.text")[0]
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(str(random.choice(range(1, 11))))

    # Add product to cart
    browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[2]/main/div[2]/div[2]/form/button').click()

    # Go to the cart
    browser.find_element_by_xpath(
        '/html/body/div[1]/header/div[2]/div/ul/li[1]/a').click()

    # Procede to checkout
    browser.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div/div[2]/main/article/div/div/div[2]/div/div/a').click()

    # Fill in the checkout form
    first_name = browser.find_element_by_xpath('//*[@id="billing_first_name"]')
    first_name.send_keys(fake.first_name())

    last_name = browser.find_element_by_xpath('//*[@id="billing_last_name"]')
    last_name.send_keys(fake.last_name())

    st_ad = browser.find_element_by_xpath('//*[@id="billing_address_1"]')
    st_ad.send_keys(fake.street_address())

    city = browser.find_element_by_xpath('//*[@id="billing_city"]')
    city.send_keys(fake.city())

    zip = browser.find_element_by_xpath('//*[@id="billing_postcode"]')
    zip.send_keys(fake.postalcode_in_state(state_abbr='NV'))

    email = browser.find_element_by_xpath('//*[@id="billing_email"]')
    email.send_keys(fake.ascii_free_email())

    phone = browser.find_element_by_xpath('//*[@id="billing_phone"]')
    phone.send_keys(fake.phone_number().split('x')[0])

    card = browser.find_element_by_xpath('//*[@id="authnet-card-number"]')
    card.send_keys('4111111111111111')

    expires = browser.find_element_by_xpath('//*[@id="authnet-card-expiry"]')
    expires.send_keys(fake.credit_card_expire(
        start='now', end='+3y', date_format='%m/%y'))

    code = browser.find_element_by_xpath('//*[@id="authnet-card-cvc"]')
    code.send_keys(fake.credit_card_security_code())

    print(first_name.get_attribute('value') +
          ' ' + last_name.get_attribute('value'))
    print(st_ad.get_attribute('value'))
    print(city.get_attribute('value') + ', ' + zip.get_attribute('value'))
    print(email.get_attribute('value'))
    print(phone.get_attribute('value'))
    print(card.get_attribute('value'))
    print(expires.get_attribute('value'))
    print(code.get_attribute('value'))

    # Wait a few moments
    time.sleep(10)

    # Place the order
    browser.find_element_by_xpath('//*[@id="place_order"]').click()


def create_magento_order(headless=False):

    # create instance of faker
    fake = Faker()

    # get the store up in selenium
    url = "https://magento-demo.ns8demos.com" # "https://magento-v2-234.ns8demos.com/index.php/"
    opts = Options()
    opts.headless = headless
    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override", fake.firefox())# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Firefox/73.0')
    browser = Firefox(options=opts, firefox_profile=profile)
    print(browser.execute_script("return navigator.userAgent"))
    browser.get(url)
    time.sleep(2)
    # Go to gear site
    browser.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[2]/nav/ul/li[4]/a/span[2]').click()

    # Select Bags
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[4]/div[2]/div/div/ul/li[1]/a').click()

    # Choose Products
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[3]/div[1]/div[3]/ol/li[1]/div/a/span/span/img').click()

    # Adjust number of items to add to cart
    qty = browser.find_element_by_xpath('//*[@id="qty"]')
    # qty = browser.find_elements_by_class_name("input-text.qty.text")[0]
    qty.send_keys(Keys.BACKSPACE)
    qty.send_keys(str(random.choice(range(1, 11))))

    # Add product to cart
    time.sleep(5)
    browser.find_element_by_xpath(
        '//*[@id="product-addtocart-button"]').click()

    # Go to the cart
    time.sleep(5)
    try:
        browser.find_element_by_xpath(
            '/html/body/div[1]/header/div[2]/div[1]/a').click()

        # Go to checkout
        browser.find_element_by_xpath(
            '//*[@id="top-cart-btn-checkout"]').click()
    except:
        time.sleep(5)
        browser.find_element_by_xpath(
            '/html/body/div[1]/header/div[2]/div[1]/a').click()

        # Go to checkout
        browser.find_element_by_xpath(
            '//*[@id="top-cart-btn-checkout"]').click()

    # Fill in the checkout form
    # Wait for form to load
    time.sleep(10)
    first_name = browser.find_element_by_name('firstname')
    first_name.send_keys(fake.first_name())

    last_name = browser.find_element_by_name('lastname')
    last_name.send_keys(fake.last_name())

    st_ad = browser.find_element_by_name('street[0]')
    st_ad.send_keys(fake.street_address())

    city = browser.find_element_by_name('city')
    city.send_keys(fake.city())

    state_picker = browser.find_element_by_name('region_id')
    # pull this info out of a library somewhere to make dynamic. Must x-ref with state_abbr
    state = 'New York'
    state_picker.send_keys(state)

    zip = browser.find_element_by_name('postcode')
    zip.send_keys(fake.postalcode_in_state(state_abbr='NY'))

    email = browser.find_element_by_xpath('//*[@id="customer-email"]')
    email.send_keys(fake.ascii_free_email())

    phone = browser.find_element_by_name('telephone')
    phone.send_keys(fake.phone_number().split('x')[0])

    # Choose Shipping Method:
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[1]/table/tbody/tr[1]/td[1]/input').click()

    # Print form
    print(first_name.get_attribute('value') +
          ' ' + last_name.get_attribute('value'))
    print(st_ad.get_attribute('value'))
    print(state_picker.get_attribute('value'))
    print(city.get_attribute('value') + ', ' + zip.get_attribute('value'))
    print(email.get_attribute('value'))
    print(phone.get_attribute('value'))

    # Select Next to move to payment:
    browser.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[3]/div/button/span').click()

    # Wait a few moments
    time.sleep(10)

    # Choose payment method
    # browser.find_element_by_xpath('//*[@id="braintree"]').click()
    try:
        browser.find_element_by_xpath('//*[@id="checkmo"]').click()
    # Confirm billing and shipping
    # browser.find_element_by_xpath('//*[@id="billing-address-same-as-shipping-braintree"]').click()
        browser.find_element_by_xpath('//*[@id="billing-address-same-as-shipping-checkmo"]').click()
    # Switch to braintree iframe
    # browser.switch_to_frame('braintree-hosted-field-number')

    # Fill in card info
    # card = browser.find_element_by_id('credit-card-number')
    # card.send_keys('4111111111111111')
    # exp_mo = browser.find_element_by_id('expirationMonth-target-prev')
    # exp_mo.send_keys('03')
    # exp_yr = browser.find_element_by_id('expiration-year')
    # exp_yr.send_keys('22')
    # ccv = browser.find_element_by_id('ccv')
    # ccv.send_keys(fake.credit_card_security_code(card_type='visa'))

    # Place the order
        browser.find_element_by_xpath(
            '/html/body/div[2]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[3]/div[2]/div[4]/div/button/span').click()
    except:
        browser.find_element_by_xpath('//*[@id="billing-address-same-as-shipping-checkmo"]').click()
        browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div[2]/div[4]/ol/li[3]/div/form/fieldset/div[1]/div/div/div[2]/div[2]/div[4]/div/button/span').click()
