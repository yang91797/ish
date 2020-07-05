from stark.service.stark import site
from wxapi import models
from backstage import models as backstage
from backstage.config.customer import UserInfoConfig
from backstage.config.article import ArticleConfig
from backstage.config.advertise import AdvertiseConfig
from backstage.config.category import CategoryConfig
from backstage.config.comment import CommentConfig
from backstage.config.sign import SignConfig
from backstage.config.studylink import StudyLinkConfig
from backstage.config.trove import TroveConfig
from backstage.config.user import UserConfig
from backstage.config.inform import InformConfig


site.register(models.Customer, UserInfoConfig)
site.register(models.Article, ArticleConfig)
site.register(models.Advertise, AdvertiseConfig)
site.register(models.Category, CategoryConfig)
site.register(models.Comment, CommentConfig)
site.register(models.Sign, SignConfig)
site.register(models.StudyLink, StudyLinkConfig)
site.register(models.Trove, TroveConfig)
site.register(backstage.UserInfo, UserConfig)
site.register(models.Inform, InformConfig)

