import requests


class SMMS(object):
    root: str = "https://sm.ms/api/v2/"

    def __init__(self, token: str):
        self.header = {"Authorization": token}

    def upload_image(self, path) -> str:
        err: str = ''
        try:
            with open(path, 'rb') as file:
                files = {'smfile': file}
                res = requests.post(self.root + 'upload', files=files, headers=self.header)
                err = res.text
                res = res.json()
                if res['success']:
                    return res['data']['url']
                elif res['code'] == 'image_repeated':
                    return res['images']
                else:
                    raise ImageUploadError(res['message'])
        except requests.exceptions.JSONDecodeError:
            raise Exception(err)


class ImageUploadError(Exception):
    pass
