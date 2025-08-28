import pytest
from pages.item_page import ItemPage
from constants.item_constants import MESSAGE_INPUT, SEND_MESSAGE_BUTTON


def test_item_get_info_mock(mocker):
    mock_page = mocker.Mock()
    mock_page.locator().inner_text.return_value = "Mocked Item Info"
    item_page = ItemPage(mock_page, "123")
        
    item_info = item_page.get_info()
    assert item_info == "Mocked Item Info", "The mocked item info should match the expected value"

def test_item_send_message_mock(mocker):
    mock_page = mocker.Mock()
    item_page = ItemPage(mock_page, "123")
    
    item_page.send_message("Test Message")
    mock_page.fill.assert_called_once_with(MESSAGE_INPUT, "Test Message", force=True)
    mock_page.click.assert_called_once_with(SEND_MESSAGE_BUTTON, force=True)

def test_item_e2e(item_page: ItemPage):
    item_info = item_page.get_info()
    assert item_info is not None, "Candidate information should not be None"
    # Not testing send_message.