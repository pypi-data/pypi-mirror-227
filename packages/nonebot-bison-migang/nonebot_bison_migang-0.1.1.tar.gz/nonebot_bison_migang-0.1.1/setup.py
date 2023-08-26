# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_bison',
 'nonebot_bison.admin_page',
 'nonebot_bison.config',
 'nonebot_bison.config.migrations',
 'nonebot_bison.config.subs_io',
 'nonebot_bison.config.subs_io.nbesf_model',
 'nonebot_bison.platform',
 'nonebot_bison.post',
 'nonebot_bison.scheduler',
 'nonebot_bison.script',
 'nonebot_bison.sub_manager',
 'nonebot_bison.utils']

package_data = \
{'': ['*'],
 'nonebot_bison.admin_page': ['dist/*',
                              'dist/static/css/*',
                              'dist/static/js/*'],
 'nonebot_bison.post': ['templates/*', 'templates/ark_announce/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'expiringdict>=1.2.1,<2.0.0',
 'feedparser>=6.0.2,<7.0.0',
 'httpx>=0.16.1',
 'lxml>=4.9.3,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0,<3.0.0',
 'nonebot-plugin-apscheduler>=0.2,<0.4',
 'nonebot-plugin-datastore>=0.6.2,<2.0.0',
 'nonebot-plugin-htmlrender>=0.2.0',
 'nonebot-plugin-send-anything-anywhere>=0.2.7',
 'nonebot2[fastapi]>=2.0.0,<3.0.0',
 'pillow>=8.1,<11.0',
 'pyjwt>=2.1.0,<3.0.0',
 'python-socketio>=5.4.0,<6.0.0',
 'tinydb>=4.3.0,<5.0.0']

entry_points = \
{'nb_scripts': ['bison = nonebot_bison.script.cli:main']}

setup_kwargs = {
    'name': 'nonebot-bison-migang',
    'version': '0.1.1',
    'description': 'Subscribe message from social medias',
    'long_description': '<div align="center">\n<h1>Bison </br>通用订阅推送插件</h1>\n\n[![pypi](https://badgen.net/pypi/v/nonebot-bison)](https://pypi.org/project/nonebot-bison/)\n[![license](https://img.shields.io/github/license/felinae98/nonebot-bison)](https://github.com/felinae98/nonebot-bison/blob/main/LICENSE)\n[![action](https://img.shields.io/github/actions/workflow/status/felinae98/nonebot-bison/main.yml?branch=main)](https://github.com/felinae98/nonebot-bison/actions/workflows/main.yml)\n[![docker](https://img.shields.io/docker/image-size/felinae98/nonebot-bison)](https://hub.docker.com/r/felinae98/nonebot-bison)\n[![codecov](https://codecov.io/gh/felinae98/nonebot-bison/branch/main/graph/badge.svg?token=QCFIODJOOA)](https://codecov.io/gh/felinae98/nonebot-bison)\n[![qq group](https://img.shields.io/badge/QQ%E7%BE%A4-868610060-orange)](https://qm.qq.com/cgi-bin/qm/qr?k=pXYMGB_e8b6so3QTqgeV6lkKDtEeYE4f&jump_from=webapi)\n\n[文档](https://nonebot-bison.netlify.app)|[开发文档](https://nonebot-bison.netlify.app/dev)\n\n</div>\n\n## 简介\n\n一款自动爬取各种站点，社交平台更新动态，并将信息推送到 QQ 的机器人。\n基于 [`NoneBot2`](https://github.com/nonebot/nonebot2) 开发（诞生于明日方舟的蹲饼活动）\n\n<details>\n<summary>本项目原名原名nonebot-hk-reporter</summary>\n\n寓意本 Bot 要做全世界跑的最快的搬运机器人，后因名字过于暴力改名\n\n</details>\n本项目名称来源于明日方舟角色拜松——一名龙门的信使，曾经骑自行车追上骑摩托车的德克萨斯\n\n支持的平台：\n\n- 微博\n- Bilibili\n- Bilibili 直播\n- RSS\n- 明日方舟\n- 网易云音乐\n- FF14\n- mcbbs 幻翼块讯\n\n## 功能\n\n- [x] 定时爬取指定网站\n- [x] 通过图片发送文本，防止风控\n- [x] 使用队列限制发送频率\n- [x] 使用网页后台管理 Bot 订阅\n- [ ] 使用可以设置权重的调度器按时间调节不同账号的权重\n\n## 使用方法\n\n**!!注意，如果要使用后台管理功能请使用 pypi 版本或者 docker 版本，如果直接 clone 源代码\n需要按下面方式进行 build**\n\n```bash\ncd ./admin-frontend\npnpm && pnpm run build\n```\n\n可以使用 Docker，docker-compose，作为插件安装在 nonebot 中，或者直接运行\n\n在群里 at Bot 或者直接私聊 Bot “添加订阅”，按照提示输入需要订阅的账号，就可以愉快接收消息了。\n\n参考[文档](https://nonebot-bison.vercel.app/usage/#%E4%BD%BF%E7%94%A8)\n\n## FAQ\n\n1. 报错`TypeError: \'type\' object is not subscriptable`  \n   本项目使用了 Python 3.10 的语法，请将 Python 版本升级到 3.10 及以上，推荐使用 docker 部署\n2. bot 不理我  \n   请确认自己是群主或者管理员，并且检查`COMMAND_START`环境变量是否设为`[""]`\n   或者按照`COMMAND_START`中的设置添加命令前缀，例：\n   `COMMAND_START=["/"]`则应发送`/添加订阅`\n3. 微博漏订阅了\n   微博更新了新的风控措施，某些含有某些关键词的微博会获取不到。\n4. 无法使用后台管理页面\n   1. 确认自己正确配置了 nonebot 的端口，如果在远程或容器外访问网页请确保`HOST=0.0.0.0`\n   2. 确认自己的云服务器的防火墙配置正确\n   3. 确认自己使用了正确的方法安装插件\n\n## 参与开发\n\n欢迎各种 PR，参与开发本插件很简单，只需要对相应平台完成几个接口的编写就行。你只需要一点简单的爬虫知识就行。\n\n如果对整体框架有任何意见或者建议，欢迎 issue。\n\n## 鸣谢\n\n- [`go-cqhttp`](https://github.com/Mrs4s/go-cqhttp)：简单又完善的 cqhttp 实现\n- [`NoneBot2`](https://github.com/nonebot/nonebot2)：超好用的开发框架\n- [`HarukaBot`](https://github.com/SK-415/HarukaBot/): 借鉴了大体的实现思路\n- [`rsshub`](https://github.com/DIYgod/RSSHub)：提供了大量的 api\n\n## License\n\nMIT\n',
    'author': 'mobai',
    'author_email': 'mobai@mobai.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LambdaYH/nonebot-bison-migang',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0.0',
}


setup(**setup_kwargs)
