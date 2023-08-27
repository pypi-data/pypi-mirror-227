from behave import *
from selenium.webdriver.common.by import By
from api.A import A
from volworld_common.test.behave.BehaveUtil import BehaveUtil
from volworld_aws_api_common.test.behave.selenium_utils import get_element_by_dom_id, click_element, \
    w__get_element_by_shown_dom_id


@then('{user} find there are {count} example sentence audio of word {word}')
def then__check_voice_of_word_show_sa(c, user: str, count: str, word: str):
    count_int = BehaveUtil.clear_int(count)
    elm = get_element_by_dom_id(c, [A.Voice, A.List])
    assert elm is not None
    children = elm.find_elements(by=By.XPATH, value=f"./div")
    assert len(children) == count_int, f"{len(children)} != {count_int}"


@when('{user} click on context button of sentence {sentence}')
def when__click_on_context_button_of_sentence(c, user: str, sentence: str):
    sentence = BehaveUtil.clear_string(sentence)
    main = c.browser.find_element(By.XPATH, f"//*[contains(text(),'{sentence}')]")
    context_btn = main.find_element(By.XPATH, f"../../../footer/main/button")
    click_element(c, context_btn)


@then('the sentence {sentence} is in the context')
def then__sentence_is_in_the_context(c, sentence: str):
    sentence = BehaveUtil.clear_string(sentence)
    con = w__get_element_by_shown_dom_id(c, [A.SentenceAudio, A.Context])
    main = con.find_element(By.XPATH, f"//*[contains(text(),'{sentence}')]")
    assert main is not None

