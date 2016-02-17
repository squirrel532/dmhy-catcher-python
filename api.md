### GET /task
List all tasks.  
The server returns an array of objects with name `tasklist`.

* tid -- <int> task id
* alias -- <string> name of the task
* keywords -- <string> keywords for searching
* status -- <bool> pause/running
* last_update -- <string>

### GET /resource
List all resource.  
The server returns an array of objects with name `resource`.

* title
* last_update

### HEAD /run

### GET /record
paging parameter `page`

* no -- <int>
* content -- <string>
* date -- <string>

### GET /search

* parameter `q` for keywords.
* Sample requests: `GET /search?q=<keywords>`
* Response like `/resource`

### POST /auth

receieve `username`, `password`
return `status`, `token` (if authenticated).
