from enum import Enum

class ActionName(Enum):
    GRAPHQL = "graphql"
    GENDER_DETECTION = "process"
    # TODO: We need to change it
    EVENT = "event"
    ADD_LOG = "add"
    GET_ALL_GROUPS = "getAllGroups"
    GET_GROUP_BY_NAME = "getGroupByName"
    GET_GROUP_BY_ID = "getGroupById"
    CREATE_USER = "createUser"
    UPDATE_USER = "updateUser"
    LOGIN = "login"
    TIMELINE = "timeline"
    VALIDATE_JWT = "validate-jwt"
    EMPTY = ""