import pytest
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome(executable_path='C:\\drivers\\chromedriver.exe')


@pytest.fixture(autouse=True)
def testing():
    # Неявное ожидание всех элементов
    driver.implicitly_wait(20)

    # Переходим на страницу авторизации
    driver.get('http://petfriends1.herokuapp.com/login')
    yield
    driver.close()
    driver.quit()


def test_show_my_pets():
    # Вводим email и пароль
    driver.find_element_by_id('email').send_keys('mailmail@mail.ru')
    driver.find_element_by_id('pass').send_keys('passpass')
    time.sleep(2)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    time.sleep(3)

    # Явные ожидания текста в заголовке страницы и центрального элемента страницы по XPath;
    WebDriverWait(driver, 10).until(EC.title_contains("My Pets"))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='text-center']")))

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element_by_tag_name('h1').text == "PetFriends"

    images = driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0
