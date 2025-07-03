# Integrations

## OAuth 2

Frappe Framwork uses [`oauthlib`](https://github.com/oauthlib/oauthlib) to manage OAuth2 requirements. A Frappe instance can function as all of these:

1. **Resource Server**: contains resources, for example the data in your DocTypes.
2. **Authorization Server**: server that issues tokens to access some resource.
3. **Client**: app that requires access to some resource on a resource server.

Different DocTypes and features pertain to each of roles:

0. **Common**:
   - **OAuth Settings**: allows configuring certain OAuth features.
1. **Authorization Server**
   - **OAuth Client**: keeps records of _clients_ registered with the frappe instance.
   - **OAuth Bearer Token**: tokens given out to registered _clients_ are maintained here.
   - **OAuth Authorization Code**: keeps track of OAuth codes a client responds with in exchange for a token.
   - **OAuth Provider Settings**: allows skipping authorization
2. **Client**
   - **Connected App**: keeps records of _authorization servers_ against whom this frappe instance is registered as a _client_ so some resource can be accessed. Eg. a users Google Drive account.
   - **Social Key Login**: similar to **Connected App**, but for the purpose of logging into the frappe instance. Eg. a users Google account to enable "Login with Google".
   - **Token Cache**: tokens received by the Frappe instance when accessing a **Connected App**.
3.

## OAuth Settings
