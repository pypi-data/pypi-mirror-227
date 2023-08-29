# flurry

## introduce

基于Cython，uvloop，httptools的一个高性能web框架，目前只支持linux系统

## install

```shell
pip3 install flurry-ce
```

## run

```python
from flurry.app import Application
from flurry.handler import RequestHandler


class RootHandler(RequestHandler):

    async def get(self):
        self.write({
            "hello": "world"
        })

handler_classes = [
    (r"/", RootHandler),
]

Application(
    handler_clses=handler_classes,
    debug=False,
).run()
```

