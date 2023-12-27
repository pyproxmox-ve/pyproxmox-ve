# Access Resources

|  Endpoint | Method | Method Name | Purpose |
| --------- | ------ | ----------- | ------- |
| /access/users | GET | get_users | Get all API Users |
| /access/users | POST | create_user | Create a new API User |
| /access/users/{userid} | GET | get_user | Get a specific API User |
| /access/users/{userid} | PUT | update_user | Update a specific API User |
| /access/users/{userid} | DELETE | delete_user | Delete a specific API User |
| /access/users/{userid}/tfa | GET | get_user_tfa_types | Get 2FA details for a specific API User |
| /access/users/{userid}/unlock-tfa | PUT | unlock_user_tfa | Unlock 2FA for a specific API User |
| /access/users/{userid}/token | GET | get_user_tokens | Get a specific API User's Tokens |
| /access/users/{userid}/token/{tokenid} | GET | get_user_token | Get a specific API User's Token |
| /access/users/{userid}/token/{tokenid} | POST | create_user_token | Create a new API token for an existing API User |
| /access/users/{userid}/token/{tokenid} | PUT | update_user_token | Update a specific API User's Token |
| /access/users/{userid}/token/{tokenid} | DELETE | delete_user_token | Delete a specific API User's Token |

# Pools Resources

|  Endpoint | Method | Method Name | Purpose |
| --------- | ------ | ----------- | ------- |
| /pools | GET | get_pools | List pools or get pool configuration |
| /pools | POST | create_pool | Create a new pool |
| /pools | PUT | update_pool | Update an existing pool |
| /pools | DELETE | delete_pool | Delete an existing pool |
