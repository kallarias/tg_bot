from unittest import TestCase
from unittest.mock import patch

from bot import bot


class Test1(TestCase):
    MESSAGE_START ={'content_type': 'text', 'id': 1847, 'message_id': 1847,
                    'from_user': {'id': 505034770, 'is_bot': False, 'first_name': 'Андрей',
                                  'username': 'Jskoo', 'last_name': 'Шепелев', 'language_code': 'ru',
                                  'can_join_groups': None, 'can_read_all_group_messages': None,
                                  'supports_inline_queries': None, 'is_premium': None,
                                  'added_to_attachment_menu': None},
                    'date': 1671572168,
                    'chat': {'id': 505034770, 'type': 'private', 'title': None, 'username': 'Jskoo',
                             'first_name': 'Андрей', 'last_name': 'Шепелев', 'photo': None, 'bio': None,
                             'join_to_send_messages': None, 'join_by_request': None,
                             'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None,
                             'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None,
                             'slow_mode_delay': None, 'message_auto_delete_time': None, 'has_protected_content': None,
                             'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None,
                             'location': None},
                    'sender_chat': None, 'forward_from': None, 'forward_from_chat': None,
                    'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None,
                    'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None,
                    'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': None,
                    'text': '/start', 'entities': '[<telebot.types.MessageEntity object at 0x0000020A19FD8C50>]',
                    'caption_entities': None, 'audio': None, 'document': None, 'photo': None,
                    'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None,
                    'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None,
                    'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None,
                    'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None,
                    'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None,
                    'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None,
                    'successful_payment': None, 'connected_website': None, 'reply_markup': None,
                    'json': {'message_id': 1847,
                             'from': {'id': 505034770, 'is_bot': False, 'first_name': 'Андрей',
                                      'last_name': 'Шепелев', 'username': 'Jskoo', 'language_code': 'ru'},
                             'chat': {'id': 505034770, 'first_name': 'Андрей', 'last_name': 'Шепелев',
                                      'username': 'Jskoo', 'type': 'private'}, 'date': 1671572168, 'text': '/start',
                             'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}
    def test_ok(self):
        # bot.message_handler().
        pass