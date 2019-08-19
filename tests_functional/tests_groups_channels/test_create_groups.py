import allure
from hamcrest import *
import pytest
from dialog_api.search_pb2 import *
from dialog_api.peers_pb2 import *
from dialog_api.groups_pb2 import *
from dialog_api import groups_pb2
import grpc


@allure.issue("SAN-41", "Create Group")
@pytest.mark.parametrize('d_user', ["2 users"], indirect=True)
class TestCreateGroup:
    """ Ctreating public and private groups specific cases for each types """

    @allure.title("Test create group and invite user")
    @allure.testcase("XTE-20", "Test create group and invite user")
    def test_create_group(self, d_user, update2):
        """  Creating private group and inviting new member"""
        updates = update2
        with allure.step('User1 creates new group'):
            new_group = d_user.create_group(d_user.u1)
            print(new_group)
        with allure.step('User1 invites User2 to group'):
            d_user.add_group_members(d_user.u1, d_user.outpeer1, new_group.group)
        with allure.step('User2 gets update for inviting to group'):
            for update in updates:
                if update.unboxed_update.HasField('updateGroupInviteObsolete'):
                    assert_that(update.unboxed_update.updateGroupInviteObsolete.group_id == new_group.group.id)
                    break

    @allure.title("Test group permissions for creator of private chat")
    @allure.testcase("XTE-42", "Test group permissions for creator of private chat")
    def test_group_admin_permissions(self, d_user):
        """ Group permissions for creator of private chat """
        with allure.step('User1 creates private group chat'):
            new_group = d_user.create_group(d_user.u1)
        with allure.step('Single member of group is their creator'):
            assert new_group.group.HasField("is_admin")
            assert new_group.group.creator_uid == new_group.group.members[0].uid
        with allure.step('Checking default permission set for group admin'):
            permissions_list = []
            for permission in new_group.group.members[0].permissions:
                print(permission)
                permissions_list.append(permission)
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_SETPERMISSIONS') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_PINMESSAGE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_EDITSHORTNAME') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_EDITMESSAGE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_SENDMESSAGE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_INVITE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_DELETEMESSAGE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_KICK') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_VIEWMEMBERS') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_GETINTEGRATIONTOKEN') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_UPDATEINFO') in permissions_list

    @allure.title("Test for group member permissions")
    @allure.testcase("XTE-42", "Test for group member permissions")
    def test_group_member_permissions(self, d_user):
        with allure.step('User1 create private group chat'):
            new_group = d_user.create_group(d_user.u1, user_outpeers=[d_user.outpeer1])
        with allure.step('User1 invite User2'):
            invite = d_user.add_group_members(d_user.u1, d_user.outpeer1, new_group.group)
            group_id = new_group.group.id
            print(new_group.group)
        with allure.step('Get permissions of members'):
            response = d_user.u1.groups.GetGroupMemberPermissions(
                RequestGetGroupMemberPermissions(group_id=new_group.group.id, user_ids=[d_user.outpeer1.id]))
            print(response)
        with allure.step('Check default permission set for private group'):
            permissions_list = []
            for permission in response.permissions[0].permissions:
                print(permission)
                permissions_list.append(permission)

            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_VIEWMEMBERS') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_INVITE') in permissions_list
            assert groups_pb2.GroupAdminPermission.Value('GROUPADMINPERMISSION_SENDMESSAGE') in permissions_list

    @allure.title("Test invite invalid user")
    @allure.testcase("XTE-42", "Test invite invalid user")
    ## TO DO : Узнать как правильно строить поисковой запрос
    @pytest.mark.skip(reason="TO DO")
    def test_create_group_public(self, d_user):
        """ Invite unexisting user """
        with allure.step('User1 creates public group with shortname'):
            new_group = d_user.create_group(d_user.u1, with_shortname=True)
            print(new_group)
        with allure.step('User2 search group'):
            search_query = GroupOutPeer(
                group_id=new_group.group.id,
                access_hash=new_group.group.access_hash)
            response = d_user.u2.search.PeerSearch(
                RequestPeerSearch(query=[SearchCondition(searchPeerTypeCondition=SearchPeerTypeCondition(peer_type=1)),
                                         SearchCondition(searchPeerCondition=SearchPeerCondition(peer=OutPeer(
                                             type=2,
                                             id=new_group.group.id,
                                             access_hash=new_group.group.access_hash)))]))
            print(response)

    @allure.title("Test invite invalid user")
    @allure.testcase(" ", " ")
    def test_create_group_invalid_user(self, d_user):
        """  Creating private group and inviting new member with invalid outpeer"""
        invalid_outpeer = OutPeer(id=95394851, access_hash=935347587234, type=PEERTYPE_PRIVATE)
        with allure.step('User1 creates new group with unexisting user'):
            try:
                d_user.create_group(d_user.u1, user_outpeers=[d_user.outpeer1, invalid_outpeer])
            except grpc.RpcError as e:
                print(e.details())
                status_code = e.code()
                assert_that(e)
                assert_that(status_code.value[0], equal_to(5))
                assert_that(status_code.name, equal_to('NOT_FOUND'))
