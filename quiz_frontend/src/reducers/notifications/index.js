import {
  combineReducers
} from 'redux';

import * as notificationsTypes from './../../constants/notifications';

const types = {
  ...notificationsTypes
};

const initialState = {
  isSuccessMessage: false,
  isErrorMessage: false,
  isInfoMessage: false,
  message: '',
  notificationTtl: 20 //20s
};

const isSuccessMessage = (state = initialState.isSuccessMessage, action) => {
  switch (action.type) {
    case types.NOTIFICATION_SHOW_SUCCESS_MESSAGE:
      return true;
    case types.NOTIFICATION_SHOW_ERROR_MESSAGE:
    case types.NOTIFICATION_SHOW_INFO_MESSAGE:
    case types.NOTIFICATION_CLOSE_MESSAGE:
      return false;
    default:
      return state;
  }
};

const isErrorMessage = (state = initialState.isErrorMessage, action) => {
  switch (action.type) {
    case types.NOTIFICATION_SHOW_ERROR_MESSAGE:
      return true;
    case types.NOTIFICATION_SHOW_INFO_MESSAGE:
    case types.NOTIFICATION_SHOW_SUCCESS_MESSAGE:
    case types.NOTIFICATION_CLOSE_MESSAGE:
      return false;
    default:
      return state;
  }
};

const isInfoMessage = (state = initialState.isInfoMessage, action) => {
  switch (action.type) {
    case types.NOTIFICATION_SHOW_INFO_MESSAGE:
      return true;
    case types.NOTIFICATION_SHOW_ERROR_MESSAGE:
    case types.NOTIFICATION_SHOW_SUCCESS_MESSAGE:
    case types.NOTIFICATION_CLOSE_MESSAGE:
      return false;
    default:
      return state;
  }
};

const message = (state = initialState.message, action) => {
  switch (action.type) {
    case types.NOTIFICATION_SHOW_ERROR_MESSAGE:
    case types.NOTIFICATION_SHOW_SUCCESS_MESSAGE:
    case types.NOTIFICATION_SHOW_INFO_MESSAGE:
      if (action.message && typeof action.message === 'string') {
        return action.message;
      }
      return state;
    case types.NOTIFICATION_CLOSE_MESSAGE:
      return '';
    default:
      return state;
  }
};

export default combineReducers({
  isSuccessMessage,
  isErrorMessage,
  isInfoMessage,
  message
});
