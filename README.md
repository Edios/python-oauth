## Implementation of authentication server backend based on oAuth protocol (simplified)
- [ ] Flask endpoints
  - *This implementation skips requesting for short-living code* 
  - [ ] Fetch tokens /fetch_token
    - example: ```localhost/fetch_token&user=admin&password=admin (returns: token, refresh token)```
    - response (json): 
     ```
    {
      "access_token": access_token,
      "refresh_token": refresh_token,
      "expires_in": 3600,
      "token_type": "bearer"
    }
    ```
    - MVP: Pass credentials in &user and &password, but it should be POST and given in header as basic auth
    - Possible Errors: Invalid Credentials
  - [ ] Refresh token /refresh_token
    - example: ```localhost/refresh_token&refresh_token=```
    - response (json): 
     ```
    {
      "access_token": access_token,
      "expires_in": 3600,
      "token_type": "bearer"
    }
    ```
    - Possible Errors: Invalid Credentials
  - [ ] Get user info - Authorization test endpoint
    - localhost/login&auth_token=
    - response (json): 

    - ```
      {
        "authorized_user": ,
        "content": ,
      }
      ```
    - MVP: Pass token in &access_token, but it should be POST and given in header as bearer
    - Possible Errors: Invalid Token, Expired token
- [ ] Mongo DB implemented in backend