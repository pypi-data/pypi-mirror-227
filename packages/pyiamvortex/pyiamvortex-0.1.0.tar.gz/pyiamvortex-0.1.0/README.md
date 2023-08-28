# pyiamvortex
A python utility library used for getting all available AWS IAM actions and performing different operations on them.

## Install

```bash
pip install pyiamvortex
```

## Usage

```python
from pyiamvortex import Vortex

vortex = Vortex() # initializes a vortex object with the default AWS actions map from AWS Policy Generator
print(vortex.get_aws_services()) # prints all available AWS services (i.e. ec2, s3, iam, etc.)
print(vortex.get_aws_actions()) # prints all available AWS actions (i.e. ec2:DescribeInstances, s3:GetObject, etc.)
```