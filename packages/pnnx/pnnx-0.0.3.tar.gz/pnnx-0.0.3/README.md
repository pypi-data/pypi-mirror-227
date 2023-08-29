# pnnx_package
pnnx python wrapper



## How to use

```shell
pip install pnnx
```



currently support the model with only 1 input

**example**

```python
import pnnx
import torch
import torchvision

def test_pnnx_export():
    resnet_test_model = torchvision.models.resnet18()
    x = torch.rand(1, 3, 224, 224)
    pnnx.export(resnet_test_model, x)

if __name__ == "__main__":
    test_pnnx_export()
```

