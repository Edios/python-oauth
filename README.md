## Implementation of authentication server backend based on oAuth protocol (simplified)
### API Documentation with examples: [ Postman Documentation ](https://documenter.getpostman.com/view/19890048/2sAY545Hwm)
- [x] Auth Server Backend (MVP)
  - [x] Session management
  - [x] Access / Refresh token generation
  - [x] Token Expiration mechanism 
- [x] Data Server Backend (MVP)
  - [x] Make it use Auth server as identity provider
  - [x] Mock up "user data" and enable to fetch it via auth token
- [x] Flask endpoints
  - *This implementation skips requesting for short-living code* 
  - [x] Fetch tokens /fetch_token
    - example: ```localhost/fetch_token```
    - 
    - response (json): 
     ```
    {
      "access_token": access_token,
      "refresh_token": refresh_token,
      "expires_in": 3600,
      "token_type": "bearer"
    }
    ```
    - Pass credentials in header as basic auth
    - Possible Errors: Invalid Credentials
  - [x] Refresh token /refresh_token
    - example: ```localhost/refresh_token?refresh_token=```
    - response (json): 
     ```
    {
      "access_token": access_token,
      "expires_in": 3600,
      "token_type": "bearer"
    }
    ```
    - Possible Errors: Invalid Credentials
  - [x] Login - Authorization test endpoint (Get user info)
    - localhost/login?auth_token=
    - response (json): 

    - ```
      {
        "authorized_user": ,
        "content": ,
      }
      ```
    - MVP: Access_token should be given in header as bearer token
    - Possible Errors: Invalid Token, Expired token
- [ ] Mongo DB usage implementation
  - [ ] Database for UserData
  - [ ] Session management