from datetime import datetime
from enum import IntEnum
from typing import Type
from tortoise import fields
from tortoise.signals import post_save
from tortoise_api_model import Model
from tortoise_api_model.fields import DatetimeSecField


class UserInChatRole(IntEnum):
    banned = 0
    member = 1
    administrator = 2


class AgentStatus(IntEnum):
    banned = 0
    stopped = 1
    runned = 2


class Proxy(Model):
    host: int = fields.CharField(15)
    port: int = fields.IntField()
    login: str = fields.CharField(63)
    password: str = fields.CharField(63)

    agents: fields.BackwardFKRelation["Agent"]

    _icon = 'net'

    def repr(self):
        return f'{self.host}:{self.port}'

    class Meta:
        table_description = "SOCKS5 Proxies"
        unique_together = (("login", "host", "port"),)


class User(Model):
    id: int = fields.BigIntField(pk=True)
    active: int = fields.BooleanField(default=1)
    username: str = fields.CharField(63, null=True)
    name: str = fields.CharField(63)
    bio: str = fields.CharField(255)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)
    phone: int = fields.BigIntField(null=True)

    client: fields.BackwardOneToOneRelation["Client"]
    agent: fields.BackwardOneToOneRelation["Agent"]
    chats: fields.ManyToManyRelation["Chat"] = fields.ManyToManyField("models.Chat", 'userinchat')

    _icon = 'user'

    class Meta:
        table_description = "Telegram users"


class Agent(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="agent")
    user_id: int
    status: AgentStatus = fields.IntEnumField(AgentStatus, default=AgentStatus.stopped)
    sess: str = fields.CharField(511, null=True)
    proxy: fields.ForeignKeyRelation[Proxy] = fields.ForeignKeyField("models.Proxy", related_name="agents")
    proxy_id: int
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    businesses: fields.BackwardFKRelation["Business"]

    _icon = 'agent'

    class Meta:
        table_description = "Agents"


class Client(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="client")
    user_id: int
    business: fields.ForeignKeyRelation["Business"] = fields.OneToOneField("models.Business", related_name="client")
    business_id: int

    _icon = 'client'

    class Meta:
        table_description = "Clients"


class Chat(Model):
    id: int = fields.BigIntField(pk=True)
    is_private: int = fields.BooleanField(default=0)
    is_channel: int = fields.BooleanField(default=0)
    username: str = fields.CharField(63, null=True)
    name: str = fields.CharField(63)
    description: str = fields.CharField(255)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    users: fields.ManyToManyRelation[User] # = fields.ManyToManyField("models.User", 'userinchat')
    businesses: fields.ManyToManyRelation["Business"] # = fields.ManyToManyField("models.Chat", 'chatinbusiness')

    _icon = 'chat'

    class Meta:
        table_description = "Chats/Channels"


class UserInChat(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User")
    chat: fields.OneToOneRelation[Chat] = fields.OneToOneField("models.Chat")
    role: UserInChatRole = fields.IntEnumField(UserInChatRole, default=UserInChatRole.member)
    created_at: datetime = DatetimeSecField(auto_now_add=True)

    _icon = 'chat'

    class Meta:
        table_description = "User in Chats"


class Region(Model):
    name: str = fields.CharField(127)
    parent: fields.ForeignKeyRelation["Region"] = fields.ForeignKeyField("models.Region", related_name="cities", null=False)

    businesses: fields.BackwardFKRelation["Business"]
    phrases: fields.BackwardFKRelation["Phrase"]
    cities: fields.BackwardFKRelation["Region"]

    _icon = 'location'

    class Meta:
        table_description = "Countries/Cities"


class Topic(Model):
    name: str = fields.CharField(127)

    businesses: fields.BackwardFKRelation["Business"]
    phrases: fields.BackwardFKRelation["Phrase"]

    _icon = 'topic'

    class Meta:
        table_description = "Business types"


class Business(Model):
    topic: fields.ForeignKeyRelation[Topic] = fields.ForeignKeyField("models.Topic", related_name="businesses")
    topic_id: int
    region: fields.ForeignKeyRelation[Region] = fields.ForeignKeyField("models.Region", related_name="businesses", null=False)
    region_id: int
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", related_name="businesses")
    agent_id: int

    chats: fields.ManyToManyRelation["Chat"] = fields.ManyToManyField("models.Chat", 'chatinbusiness')
    clients: fields.BackwardFKRelation[Client]
    phrases: fields.BackwardFKRelation["Phrase"]

    _icon = 'business'

    async def repr(self):
        return f'{(await self.topic).name}:{(await self.region).name}'

    class Meta:
        table_description = "Businesses - Topic in Regions"


class ChatInBusiness(Model):
    business: fields.OneToOneRelation[Business] = fields.OneToOneField("models.Business")
    chat: fields.OneToOneRelation[Chat] = fields.OneToOneField("models.Chat")
    created_at: datetime = DatetimeSecField(auto_now_add=True)

    _icon = 'chat'

    class Meta:
        table_description = "Chats in business"


class Phrase(Model):
    txt: str = fields.CharField(4095, unique=True)
    business: fields.ForeignKeyRelation[Business] = fields.ForeignKeyField("models.Business", related_name="phrases", null=False)
    business_id: int
    topic: fields.ForeignKeyRelation[Topic] = fields.ForeignKeyField("models.Topic", related_name="phrases", null=False)
    topic_id: int
    region: fields.ForeignKeyRelation[Region] = fields.ForeignKeyField("models.Region", related_name="phrases", null=False)
    region_id: int
    is_excl: bool = fields.BooleanField(default=0)
    created_at: datetime = DatetimeSecField(auto_now_add=True)
    updated_at: datetime = DatetimeSecField(auto_now=True)

    _icon = 'symbol'

    def repr(self):
        return f'{self.is_excl and "! "}{self.txt}'

    class Meta:
        table_description = "Businesses - Topic in Regions"


@post_save(Phrase)
async def phrase_consist(
    sender: Type[Phrase], instance: Phrase, created: bool, using_db, update_fields
) -> None:
    if {'business_id', 'topic_id', 'region_id'} & update_fields:
        if instance.business_id:
            if instance.topic_id:
                print('No need to set topic if you set business!')
                instance.topic_id = None
            if instance.region_id:
                print('No need to set region if you set business!')
                instance.region_id = None
        if instance.topic_id and instance.region_id:
            print('No need to set topic and region. Then just set only business!')
            instance.business = await Business.get(topic=instance.topic, region=instance.region)
        await instance.save()
