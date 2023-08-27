import yaml
from SoyDNGP import *


def remodel(path, num_classes, show_structure=True):
    # 读取yaml
    with open(path, 'r') as f:
        dic = yaml.load(f, Loader=yaml.FullLoader)
    layer_dic = dic['model']
    layer_list = []
    # 根据yaml字典实例化net
    for key, value in layer_dic.items():
        layer_list.append(eval(key.split('.')[0] + f'{value}'))
    net = nn.Sequential(*layer_list)
    # 根据实例化的net生成对应decoder 注意仅对卷积和全连接层有效
    layer_list = []
    for layer in net.modules():
        if isinstance(layer, torch.nn.Conv2d):
            layer_list.append(nn.ConvTranspose2d(in_channels=layer.out_channels,
                                                 out_channels=layer.in_channels,
                                                 kernel_size=layer.kernel_size,
                                                 padding=layer.padding,
                                                 stride=layer.stride))
        elif isinstance(layer, torch.nn.Linear):
            out_channel = layer_list[-1].in_channels
            out_length = layer.in_features
            layer_list.append(
                Reshape(out_channel, int((out_length / out_channel) ** 0.5), int((out_length / out_channel) ** 0.5)))
            layer_list.append(nn.Linear(in_features=layer.out_features, out_features=layer.in_features))
    if show_structure:
        print(f"Your model structure is: \n{net}")
    layer_list = layer_list[::-1]
    decoder = nn.Sequential(*layer_list)
    return net, decoder
