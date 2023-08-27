import numpy as np
import torch
from torch.nn.parameter import Parameter


def weight_decoder(net, decoder, snp_list, percentage):
    snp = snp_list
    net_weight_list = []
    # 权重赋值
    for layer in net.modules():
        if isinstance(layer, torch.nn.Conv2d):
            net_weight_list.append(layer.weight)
        elif isinstance(layer, torch.nn.Linear):
            net_weight_list.append(Parameter(layer.weight.T))
    net_weight_list = net_weight_list[::-1]
    num_class = 1 if np.array(net_weight_list[0].shape).min() == np.array(net_weight_list[0].shape).max() else np.array(
        net_weight_list[0].shape).min()
    decoder.to('cuda')
    decoder.eval()

    # 特征解码
    with torch.no_grad():
        i = 0
        for layer in decoder.modules():
            if isinstance(layer, torch.nn.ConvTranspose2d) or isinstance(layer, torch.nn.Linear):
                layer.weight = net_weight_list[i]
                i += 1
        x = (torch.zeros((1, num_class)) + 1).to('cuda')
        y = decoder(x)
        y = torch.sum(y, dim=1).to('cpu').numpy()
        data = y.reshape((206 * 206))[:len(snp) + 1]
        # 获取位点
        snp_pos = np.array(np.where(data >= np.percentile(data, 1 - percentage)))
        snp_pos = [snp[pos] for pos in snp_pos[0]]
        return snp_pos
