# coding=utf-8

'''
Author:franztao
Email:taoheng@stonewise.cn;franztaoheng@gmail.com
github:https://github.com/hengfanz
'''
import torch.optim
import transformers
from torch import nn


def dwpw_conv(ic, oc, kernel_size=3, stride=2, padding=1):
    return nn.Sequential(
        nn.Conv2d(ic, ic, kernel_size=kernel_size, stride=stride, padding=padding, groups=ic),  # depthwise convolution
        nn.BatchNorm2d(ic),
        nn.LeakyReLU(0.01, inplace=True),
        nn.Conv2d(ic, oc, 1),
        nn.BatchNorm2d(oc),
        nn.LeakyReLU(0.01, inplace=True)
    )


class StudentNet(nn.Module):
    def __init__(self):
        self.conv1 = nn.Conv2d(3, 64, kerinel_size=7, stide=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = dwpw_conv(64, 64, stride=1)
        self.layer2 = dwpw_conv(64, 128)
        self.layer3 = dwpw_conv(128, 256)
        self.layer4 = dwpw_conv(256, 140)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(140, 11)

    def forword(self, x):
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.maxpool(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.avgpool(out)
        out = out.flatten(1)
        out = self.fc(out)
        return out


if __name__ == '__main__':
    pass
    optimizer=torch.optim.Adam(filter(lambda p:p.requires_grad, student_model.parameters()), lr=cfg['lr'], weight_decay=cfg['weight_decay'])
    schedule=torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=6, T_mult=2, eta_min=1e-5)

    from torchvision import datasets, transforms

    import torch.nn.functional as F
    F.nll_loss()
    F.pad()
