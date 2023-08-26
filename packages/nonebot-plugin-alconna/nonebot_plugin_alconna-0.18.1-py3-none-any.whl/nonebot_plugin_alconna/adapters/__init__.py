"""通用标注, 无法用于创建 MS对象"""
import re
from dataclasses import field, dataclass
from typing import Any, Union, Literal, Optional

from nepattern import create_local_patterns
from nonebot.internal.adapter import Message, MessageSegment

from nonebot_plugin_alconna.typings import gen_unit

Text = str


@dataclass
class Segment:
    """基类标注"""

    origin: MessageSegment


@dataclass
class At(Segment):
    """At对象, 表示一类提醒某用户的元素"""

    type: Literal["user", "role", "channel"]
    target: str


@dataclass
class AtAll(Segment):
    """AtAll对象, 表示一类提醒所有人的元素"""


@dataclass
class Emoji(Segment):
    """Emoji对象, 表示一类表情元素"""

    id: str
    name: Optional[str] = field(default=None)


@dataclass
class Media(Segment):
    url: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)


@dataclass
class Image(Media):
    """Image对象, 表示一类图片元素"""


@dataclass
class Audio(Media):
    """Audio对象, 表示一类音频元素"""


@dataclass
class Voice(Media):
    """Voice对象, 表示一类语音元素"""


@dataclass
class Video(Media):
    """Video对象, 表示一类视频元素"""


@dataclass
class File(Segment):
    """File对象, 表示一类文件元素"""

    id: str
    name: Optional[str] = field(default=None)


@dataclass
class Reply(Segment):
    """Reply对象，表示一类回复消息"""

    origin: Any
    id: str
    msg: Optional[Union[Message, str]] = field(default=None)


_Segment = gen_unit(
    Segment,
    {
        "*": lambda seg: Segment(seg),
    },
)


def _handle_kmarkdown_met(seg: MessageSegment):
    content = seg.data["content"]
    if not content.startswith("(met)"):
        return None
    if (end := content.find("(met)", 5)) == -1:
        return None
    return content[5:end] not in ("here", "all") and At(seg, "user", content[5:end])


def _handle_at(seg: MessageSegment):
    if "qq" in seg.data and seg.data["qq"] != "all":
        return At(seg, "user", str(seg.data["qq"]))
    if "user_id" in seg.data:
        return At(seg, "user", str(seg.data["user_id"]))


_At = gen_unit(
    At,
    {
        "at": _handle_at,
        "mention": lambda seg: At(
            seg, "user", seg.data.get("user_id", seg.data.get("text"))
        ),
        "mention_user": lambda seg: At(
            seg, "user", str(seg.data.get("user_id", seg.data["mention_user"].user_id))
        ),
        "mention_channel": lambda seg: At(seg, "channel", str(seg.data["channel_id"])),
        "mention_role": lambda seg: At(seg, "role", str(seg.data["role_id"])),
        "mention_robot": lambda seg: At(
            seg, "user", str(seg.data["mention_robot"].bot_id)
        ),
        "At": lambda seg: At(seg, "user", str(seg, seg.data["target"])),
        "kmarkdown": _handle_kmarkdown_met,
        "room_link": lambda seg: At(
            seg,
            "channel",
            f'{seg.data["room_link"].villa_id}:{seg.data["room_link"].room_id}',
        ),
    },
)
"""
at: ob11, feishu
mention: ob12, tg
mention_user: qqguild, discord, villa
mention_channel: discord, qqguild
mention_role: discord
mention_robot: villa
At: mirai
kmarkdown: kook
room_link: villa
"""


def _handle_kmarkdown_atall(seg: MessageSegment):
    content = seg.data["content"]
    if not content.startswith("(met)"):
        return None
    if (end := content.find("(met)", 5)) == -1:
        return None
    return content[5:end] in ("here", "all") and AtAll(seg)


_AtAll = gen_unit(
    AtAll,
    {
        "at": lambda seg: AtAll(seg) if seg.data["qq"] == "all" else None,
        "AtAll": lambda seg: AtAll(seg),
        "mention_everyone": lambda seg: AtAll(seg),
        "mention_all": lambda seg: AtAll(seg),
        "kmarkdown": _handle_kmarkdown_atall,
    },
)
"""
at: ob11
AtAll: mirai
mention_everyone: discord, qqguild
mention_all: villa, ob12
kmarkdown: kook
"""


def _handle_kmarkdown_emj(seg: MessageSegment):
    content = seg.data["content"]
    if content.startswith("(emj)"):
        mat = re.search(
            r"\(emj\)(?P<name>[^()\[\]]+)\(emj\)\[(?P<id>[^\[\]]+)\]", content
        )
        return mat and Emoji(seg, mat["id"], mat["name"])
    if content.startswith(":"):
        mat = re.search(r":(?P<name>[^:]+):", content)
        return mat and Emoji(seg, mat["name"], mat["name"])


def _handle_custom_emoji(seg: MessageSegment):
    if "custom_emoji_id" in seg.data:  # telegram
        return Emoji(seg, seg.data["custom_emoji_id"], seg.data["text"])
    if "id" in seg.data:  # discord
        return Emoji(seg, seg.data["id"], seg.data["name"])


_Emoji = gen_unit(
    Emoji,
    {
        "emoji": lambda seg: Emoji(seg, str(seg.data.get("id", seg.data.get("name")))),
        "Face": lambda seg: Emoji(seg, str(seg.data["faceId"]), seg.data["name"]),
        "face": lambda seg: str(Emoji(seg, seg.data["id"])),
        "custom_emoji": _handle_custom_emoji,
        "kmarkdown": _handle_kmarkdown_emj,
        "sticker": lambda seg: Emoji(seg, seg.data["id"]) if "id" in seg.data else None,
    },
)


def _handle_image(seg: MessageSegment):
    if "file_id" in seg.data:  # ob12
        return Image(seg, id=seg.data["file_id"])
    if "image" in seg.data:  # villa
        return Image(seg, url=seg.data["image"].url)
    if "image_key" in seg.data:  # feishu
        return Image(seg, url=seg.data["image_key"])
    if "file_key" in seg.data:  # kook
        return Image(seg, url=seg.data["file_key"])
    if "url" in seg.data:  # ob11
        return Image(seg, url=seg.data["url"], id=seg.data["file"])
    if "msgData" in seg.data:  # minecraft
        return Image(seg, url=seg.data["msgData"])
    if "file_path" in seg.data:  # ntchat
        return Image(seg, id=seg.data["file_path"])
    if "picURL" in seg.data:  # ding
        return Image(seg, url=seg.data["picURL"])


def _handle_attachment(seg: MessageSegment):
    if "url" in seg.data:  # qqguild:
        return Image(seg, url=seg.data["url"])
    if "attachment" in seg.data:  # discord
        return Image(seg, id=seg.data["attachment"].filename)


_Image = gen_unit(
    Image,
    {
        "image": _handle_image,
        "photo": lambda seg: Image(seg, id=seg.data["file"]),
        "attachment": _handle_attachment,
        "Image": lambda seg: Image(seg, seg.data["url"], seg.data["imageId"]),
    },
)


def _handle_video(seg: MessageSegment):
    if "file_id" in seg.data:  # ob12, telegram
        return Video(seg, id=seg.data["file_id"])
    if "file" in seg.data:  # ob11
        return Video(seg, url=seg.data["file"])
    if "file_key" in seg.data:  # kook
        return Video(seg, url=seg.data["file_key"])
    if "msgData" in seg.data:  # minecraft
        return Video(seg, url=seg.data["msgData"])
    if "file_path" in seg.data:  # ntchat
        return Video(seg, id=seg.data["file_path"])


_Video = gen_unit(
    Video,
    {
        "video": lambda seg: Video(seg, seg.data["url"], seg.data["videoId"]),
        "animation": lambda seg: Video(seg, id=seg.data["file_id"]),
    },
)


def _handle_voice(seg: MessageSegment):
    if "file_id" in seg.data:  # ob12, telegram
        return Voice(seg, id=seg.data["file_id"])
    if "file_key" in seg.data:  # kook
        return Voice(seg, url=seg.data["file_key"])
    if "file_path" in seg.data:  # ntchat
        return Voice(seg, id=seg.data["file_path"])


_Voice = gen_unit(
    Voice,
    {
        "voice": _handle_voice,
        "record": lambda seg: Voice(seg, seg.data["url"]),
        "Voice": lambda seg: Voice(seg, seg.data["url"], seg.data["voiceId"]),
    },
)


def _handle_audio(seg: MessageSegment):
    if "file_id" in seg.data:  # ob12, telegram
        return Audio(seg, id=seg.data["file_id"])
    if "file_key" in seg.data:  # kook, feishu
        return Audio(seg, url=seg.data["file_key"])
    if "file_path" in seg.data:  # ntchat
        return Audio(seg, id=seg.data["file_path"])


_Audio = gen_unit(
    Audio,
    {
        "audio": _handle_audio,
    },
)


def _handle_file(seg: MessageSegment):
    if "file_id" in seg.data:  # ob12
        return File(seg, id=seg.data["file_id"])
    if "file_key" in seg.data:  # feishu, kook
        return File(
            seg,
            id=seg.data["file_key"],
            name=seg.data.get("file_name", seg.data.get("title")),
        )
    if "file_path" in seg.data:  # ntchat
        return File(seg, id=seg.data["file_path"])


_File = gen_unit(
    File,
    {
        "file": _handle_file,
        "document": lambda seg: File(seg, seg.data["file_id"], seg.data["file_name"]),
        "File": lambda seg: File(seg, seg.data["id"], seg.data["name"]),
    },
)


def _handle_quote(seg: MessageSegment):
    if "msg_id" in seg.data:  # kook:
        return Reply(seg, seg.data["msg_id"], seg.data.get("content"))
    if "quoted_message_id" in seg.data:  # villa
        return Reply(seg, seg.data["quoted_message_id"])


_Reply = gen_unit(
    Reply,
    {
        "reference": lambda seg: Reply(
            seg, seg.data.get("message_id", seg.data["reference"].message_id)
        ),
        "reply": lambda seg: Reply(seg, seg.data.get("id", seg.data["message_id"])),
        "quote": _handle_quote,
        "Quote": lambda seg: Reply(seg, str(seg.data["id"]), str(seg.data["origin"])),
    },
)

env = create_local_patterns("nonebot")
env.sets([_At, _AtAll, _Image, _Video, _Voice, _Audio, _File, _Reply, _Segment])
