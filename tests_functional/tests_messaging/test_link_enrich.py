import allure
import pytest
from hamcrest import assert_that, is_


@allure.issue("SAN-12", "Link enrich")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestEnrichLink:
    """ Tests for enriching links"""

    @allure.title("Test for enrich link without picture")
    @allure.testcase("XTE-35", "Test for enrich link without picture")
    def test_enrich_link_in_message(self, d_user, update2, update1):
        """
        Test for enrich external link
        """
        updates = update2
        updates_send = update1
        with allure.step('User1 send link to User2'):
            d_user.send(d_user.u1, d_user.outpeer1, message='https://yandex.com/')
        with allure.step('User2 gets update for link enrich'):
            for update in updates:
                media = update.unboxed_update.updateMessageContentChanged.message.textMessage.media
                if len(media) is not 0:
                    assert media[-1].webpage.HasField('url')
                    assert media[-1].webpage.HasField('title')
                    assert media[-1].webpage.HasField('description')
                    break

        with allure.step('User1 gets update for enriching link'):
            for update in updates_send:
                media = update.unboxed_update.updateMessageContentChanged.message.textMessage.media
                if len(media) is not 0:
                    assert media[-1].webpage.HasField('url')
                    assert media[-1].webpage.HasField('title')
                    assert media[-1].webpage.HasField('description')
                    break
