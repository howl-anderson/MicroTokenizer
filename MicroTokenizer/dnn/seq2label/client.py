from __future__ import print_function

import json
import requests

from tokenizer_tools.tagset.BMES import BMESEncoderDecoder

bmes_decoder = BMESEncoderDecoder()


class HTTPClient(object):
    def __init__(self, host, model_name='seq2label', port=8501, https=False):
        self.server_url = '{protocol}://{host}:{port}/v1/models/{model_name}:predict'.format(
            protocol='https' if https else 'http',
            host=host,
            port=port,
            model_name=model_name
        )

    def segment(self, input_str):
        # Compose a JSON Predict request (send JPEG image in base64).
        request_object = {
            "instances":
                [
                    {
                        "words": [i for i in input_str],
                        "words_len": len(input_str)
                    },
                ]
        }
        predict_request = json.dumps(request_object)

        response = requests.post(self.server_url, data=predict_request)
        response.raise_for_status()
        prediction = response.json()['predictions'][0]

        tags = prediction['tags']

        word_tags_pair = list(zip(input_str, tags))
        word_list = bmes_decoder.decode_char_tag_pair(word_tags_pair)

        return word_list


if __name__ == '__main__':
    http_client = HTTPClient('192.168.8.155')
    word_list = http_client.segment("王小明在北京的清华大学读书。")
    print(word_list)
    # main("中国的首都是北京")
