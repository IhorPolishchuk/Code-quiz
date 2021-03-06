import config from './../../config';
import axios from 'axios';
import cookie from 'react-cookies';

const {
    global: {
        api: {
            url: apiUrl,
            ttl: tokenTtl
        }
    }
} = config;

const TOKEN_NAME = 'token';

export const saveToken = token => cookie.save(TOKEN_NAME, token, {
    path: '/',
    expires: tokenTtl,
    maxAge: tokenTtl,
    secure: true,
    httpOnly: true
});

export const removeToken = () => cookie.remove(TOKEN_NAME, { path: '/' });

export const withAuth = (method, url, data) => axios({ 
    method,
    url: `${apiUrl}${url}`,
    data,
    headers: { Authorization: `Bearer ${cookie.load(TOKEN_NAME) || ''}` }
});
