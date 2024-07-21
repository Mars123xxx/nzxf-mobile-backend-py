from const.code import NOT_ACCESS_TOKEN_ERROR, ALL_TOKEN_EXPIRED, USER_EXISTS_ERROR

msg_map = {
    NOT_ACCESS_TOKEN_ERROR: "access token is blank",
    ALL_TOKEN_EXPIRED: "token is expired",

    USER_EXISTS_ERROR:"not the user"
}


def get_msg(_: int) -> str:
    return msg_map.get(_, '')
