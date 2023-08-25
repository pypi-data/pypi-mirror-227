from pydantic import BaseModel
from hyko_sdk import SDKFunction, Image, Video, Audio


func = SDKFunction()


class Inputs(BaseModel):
    img: Image
    aud: Audio
    vid: Video
    pass

class Params(BaseModel):
    pass

class Outputs(BaseModel):
    out_img: Image
    out_aud: Audio
    out_vid: Video
    pass

@func.on_execute
async def test_load(inputs: Inputs, params: Params) -> Outputs:
    print(f"{inputs=}")
    return Outputs(
        out_img=Image(bytearray(b'test image'), filename="test.png", mime_type="PNG"),
        out_aud=Audio(bytearray(b'test audio'), filename="test.mp3", mime_type='MPEG'),
        out_vid=Video(bytearray(b'test video'), filename="test.mp4", mime_type="MP4"),
        )

