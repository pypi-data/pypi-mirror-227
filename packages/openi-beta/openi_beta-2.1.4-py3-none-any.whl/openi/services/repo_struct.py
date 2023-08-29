from dataclasses import dataclass

from ..apis import OpeniAPI
from ..utils import logger

log = logger.setup_logger()


@dataclass
class OpeniRepo:
    repo_id: str

    # api = OpeniAPI()

    def __post_init__(self):
        self.api = OpeniAPI()
        self.get_repo_by_name()
        self.get_repo_access()

    def get_repo_by_name(self):
        try:
            response = self.api.repo_info(self.repo_id).json()
            self.repo_id = response["full_name"]
            self.repo_uuid = response["id"]
            self.full_display_name = response["full_display_name"]
        except:
            msg = (
                f"`{self.repo_id}` 无法获取仓库信息，"
                "请检查仓库是否存在或者repo_id是否正确，"
                "repo_id为仓库链接中的 `拥有者(组织)/仓库名`"
            )
            log.error(msg)
            raise ValueError(msg)

    def get_repo_access(self):
        try:
            response = self.api.repo_access(self.repo_id).json()["right"]
            self.access = response
        except:
            msg = (
                f"`{self.repo_id}` 无法获取仓库权限，"
                "请检查仓库是否存在或者repo_id是否正确，"
                "repo_id为仓库链接中的 `拥有者(组织)/仓库名`"
            )
            log.error(msg)
            raise ValueError(msg)
