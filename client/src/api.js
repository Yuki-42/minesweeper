export default class Api {
    constructor() {
        this.url = "http://192.168.0.32:8000"
    }

    async _get(path) {
        /*
        Gets data from specific api path.

        Args:
            path (str): Path to get data from.

        Returns:
            dict: Response from api.
        */
        const response = await fetch(this.url + path)
        return await response.json()
    }

    async _post(
        path,
        data
    ) {
        /*
        Posts data to specific api path.

        Args:
            path (str): Path to post data to.
            data (dict): Data to post.

        Returns:
            dict: Response from api.
        */
        const response = await fetch(this.url + path, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        return await response.json()
    }

    async _options(
        path
    ) {
        /*
        Gets options for specific api path.

        Args:
            path (str): Path to get options from.

        Returns:
            dict: Response from api.
        */
        const response = await fetch(this.url + path, {
            method: 'OPTIONS'
        })
        return await response.json()
    }

    async login(
        username,
        password
    ) {
        /*
        Logs in user.

        Args:
            username (str): Username of user.
            password (str): Password of user.

        Returns:
            dict: Access token and token type.
        */
        return await this._post('/login', {
            "username": username,
            "password": password
            }
        )
    }
}

