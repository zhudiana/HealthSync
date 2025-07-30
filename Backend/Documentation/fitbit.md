# Fitbit API

## Authorization with OAuth 2.0

### There are 3 main steps to OAuth 2.0:

1. Request authorization from a user to access their data.
2. Query the user's data using the provided access token.
3. Refresh expired access tokens with the corresponding <i>refresh token </i>

### Accessing user data requires an Access Token. The following are the steps of asking a user to authorize our app and retrieve the token.

### Steps for getting an access token:

1. Generate PKCE and State Values
   - PKCE Code Verifier
   - PKCE Code Challenge (a <b>SHA-256</b> hash of the code verifier)
   - State
2. Display Authorization Page

   - The URL for this should include:

     - The PKCE Code Challenge
     - State
     - The requested Permission Scopes

   - The required query parameters are:

     - client_id
     - scope
     - code_challenge
     - code_challenge_method: S256
     - response_type: code

3. Retrieving the Authorization Code
   - The URL generated from step 2 should have two queries:
     - Code
     - State (should be similar with the one generated in step 2)
   - Our App should implement endpoints to recieve these two query parameters
4. Get Tokens

   - Our app must exchange the authorization code for a pair of access and refresh Tokens.
   - Authorization header with their Basic Token(Client ID and Client Secret) must be passed.

   ```python
   "Basic" + base64encode(client_id + ":" + client_secret)
   ```

5. Check Scopes
   - The app should check which of the requested scopes the user actually granted.

### Accessing user data

- Now we already have the access token from the above steps.
  - We will use the API endpoints with the access token we have.

### Refresh Tokens

- The access token expires after some time. When this happens, our app should use the <b>Refresh Token</b> to get a new pair of tokens.
