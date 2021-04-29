import torch
import numpy as np
from utils import add_hist, label_accuracy_score


def validation(model, data_loader, criterion, device):
    model.eval()
    with torch.no_grad():
        total_loss = 0
        cnt = 0
        hist = np.zeros((12, 12))
        for step, (images, masks) in enumerate(data_loader):
            masks = masks.long()
            images, masks = images.to(device), masks.to(device)
            outputs = model(images)
            loss = criterion(outputs, masks)
            total_loss += loss
            cnt += 1
            outputs = torch.argmax(outputs, dim=1).detach().cpu().numpy()
            hist = add_hist(hist, masks.detach().cpu().numpy(), outputs, n_class=12)
        acc, acc_cls, miou, fwavacc = label_accuracy_score(hist)
        avg_loss = total_loss / cnt
    return avg_loss, miou