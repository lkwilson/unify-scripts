import os
import requests

# Core handler
def handle_session_started(base_url, session):
  """
  This is the primary handler once the session with the device has been created.
  base_url is the url to the device, and session contains auth cookies used to
  talk to the device.
  """
  get_image = '/snap.jpeg'
  resp = session.get(base_url + get_image)
  if resp.status_code != 200:
    print("Error getting image!")
    return 1

  with open("output.jpeg", 'wb') as fout:
    fout.write(resp.content)

  return 0

def load_env():
  """
  Load environment variables defined in .env
  """
  try:
    with open('./.env') as fin:
      for line in fin:
        content = line.lstrip()[:-1] # cut left white space and trailing \n
        if not content or content.startswith('#'):
          continue

        env_var, env_val = content.split('=', 1)
        os.environ[env_var] = env_val
  except FileNotFoundError:
    print("Info: No .env file")

def check_env():
  """
  Ensure required env vars are set.
  """
  if 'UB_PASSWORD' not in os.environ:
    print("Error: UB_PASSWORD environment variable not set. Set this to the password to the device.")

  if 'UB_HOST' not in os.environ:
    print("Error: UB_HOST environment variable not set. Set this to the ip address of the device.")

def create_session(session_started_cb):
  """
  Create a session and log in. Once logged in, pass session to
  session_started_cb.
  """
  with requests.Session() as session:
    base_url = 'http://' + os.environ['UB_HOST']
    login_api = '/api/1.1/login'
    login_info = {
      "username": "ubnt",
      "password": os.environ['UB_PASSWORD'],
    }

    try:
      resp = session.post(base_url + login_api, json=login_info)
    except BaseException as exc:
      print("Failed to make login requests")
      print(repr(exc))
      return 1

    if resp.status_code != 200:
      print("Login failed!")
      print(f"Status Code: {resp.status_code}")
      #print(resp.request.body)
      return 1

    return session_started_cb(base_url, session)

def run():
  load_env()
  check_env()
  return create_session(handle_session_started)

def main():
  return run()

if __name__ == '__main__':
  exit(main())
