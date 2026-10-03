import torch
import torchvision
from torchvision.models import ResNet50_Weights

model = torchvision.models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
model.fc = torch.nn.Identity()
model.eval()

print(dir(model))
print(dir(model.eval()))
