import pytest
import allure
from hamcrest import *
from shared.data_generators import Generators


@allure.issue("SAN-71", "Drafts")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestConfigSync:
    """ Tests for synchronization, setting and getting configs
    """

    @allure.title("Test for drafts")
    @allure.testcase("XTE-11", "Test for drafts")
    def test_drafts(self, d_user, update1):
        """
        Test for drafts
        """
        with allure.step("User1 send draft"):
            updates = update1
            msg = Generators.random_text_message()
            d_user.send_draft(d_user.u1, d_user.outpeer1, draft_type='drafts_PRIVATE_', msg=msg)
            params = d_user.get_parameters(d_user.u1)
            print(params)
        with allure.step("User1 gets draft, check draft body and chat id"):
            for update in updates:
                print(update)
                if update.unboxed_update.HasField('updateParameterChanged'):
                    key = list(update.unboxed_update.updateParameterChanged.key.split('\n'))
                    id = key[1].split(' ')[1]
                    assert_that(int(id), equal_to(d_user.u2.user_info.user.id))
                    assert_that(update.unboxed_update.updateParameterChanged.value.value, equal_to(msg))
                    break
        with allure.step("User1 delete draft"):
            d_user.send_draft(d_user.u1, d_user.outpeer1, draft_type='drafts_PRIVATE_', msg=None)
        with allure.step("User1 gets update with deletion of draft"):
            for update in updates:
                if update.unboxed_update.HasField('updateParameterChanged'):
                    assert_that(update.unboxed_update.updateParameterChanged.value.value is '')
                    break
        with allure.step("Draft of User1 should be empty"):
            params = d_user.get_parameters(d_user.u1)
            assert_that(getattr(params.parameters[0], 'key'), is_not(''))
            assert_that(getattr(params.parameters[0], 'value'), equal_to(''))
