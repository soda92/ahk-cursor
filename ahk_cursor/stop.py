import requests


def stop():
    try:
        r = requests.get("http://localhost:12345/shutdown_server")
    except requests.Timeout:
        print("timeout")
    else:
        print(r.content)


if __name__ == "__main__":
    stop()
