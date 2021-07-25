# unify-scripts

A repo containing scripts that interact with the unify api

# How to Run

Create a file in this directory called `.env`.

Set `UB_HOST` and `UB_PASSWORD` in it:
```
UB_HOST=192.168.1.xxx
UB_PASSWORD=device_password
```

`UB_HOST` is the ip address of the device
`UB_PASSWORD` is the password to the device

Run the `get_image.py` script with python3. It should produce an output.jpeg if
successful. Otherwise, it should output an error.

# Status 401 Error

This means the provided password didn't work. Navigate to the web portal of
your device. Something like: http://192.168.1.44/. Try to log in there with
username `ubnt` and your password. Once successful, add that password to
`.env`.
