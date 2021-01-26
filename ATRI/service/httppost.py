from ATRI.config import RUNTIME_CONFIG


URL = (
    f"http://{RUNTIME_CONFIG['http_post']['host']}"
    f"{RUNTIME_CONFIG['http_post']['port']}"
)

class HttpPost:
    @classmethod
    def send_private_msg(cls):
        ...
    
    @classmethod
    def send_group_msg(cls):
        ...
    
    @classmethod
    def send_msg(cls):
        ...
    
    @classmethod
    def delete_msg(cls):
        ...
    
    @classmethod
    def get_msg(cls):
        ...
    
    @classmethod
    def get_forward_msg(cls):
        ...
    
    @classmethod
    def send_like(cls):
        ...
    
    @classmethod
    def set_group_kick(cls):
        ...
    
    @classmethod
    def set_group_ban(cls):
        ...
    
    @classmethod
    def set_group_anonymous_ban(cls):
        ...
    
    @classmethod
    def set_group_whole_ban(cls):
        ...
    
    @classmethod
    def set_group_admin(cls):
        ...
    
    @classmethod
    def set_group_anonymous(cls):
        ...
    
    @classmethod
    def set_group_card(cls):
        ...

    @classmethod
    def set_group_name(cls):
        ...
    
    @classmethod
    def set_group_leave(cls):
        ...
    
    @classmethod
    def set_group_special_title(cls):
        ...
    
    @classmethod
    def set_friend_add_request(cls):
        ...
    
    @classmethod
    def set_group_add_request(cls):
        ...

    @classmethod
    def get_login_info(cls):
        ...
    
    @classmethod
    def get_stranger_info(cls):
        ...
    
    @classmethod
    def get_friend_list(cls):
        ...
    
    @classmethod
    def get_group_info(cls):
        ...
    
    @classmethod
    def get_group_list(cls):
        ...
    
    @classmethod
    def get_group_member_info(cls):
        ...
    
    @classmethod
    def get_group_member_list(cls):
        ...

    @classmethod
    def get_group_honor_info(cls):
        ...
    
    @classmethod
    def get_cookies(cls):
        ...
    
    @classmethod
    def get_csrf_token(cls):
        ...
    
    @classmethod
    def get_credentials(cls):
        ...
    
    @classmethod
    def get_record(cls):
        ...
    
    @classmethod
    def get_image(cls):
        ...
    
    @classmethod
    def can_send_image(cls):
        ...
    
    @classmethod
    def can_send_record(cls):
        ...
    
    @classmethod
    def get_status(cls):
        ...
    
    @classmethod
    def get_version_info(cls):
        ...
    
    @classmethod
    def set_restart(cls):
        ...
    
    @classmethod
    def clean_cache(cls):
        ...
    