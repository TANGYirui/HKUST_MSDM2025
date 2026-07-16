import torch
import numpy as np
import bz2
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.optim as optim
import os

dfile = bz2.BZ2File('./xyData.bz2')
data = torch.from_numpy(np.load(dfile)).to(torch.float32)
dfile.close()
batch_size = 100


class XYDataset(Dataset):
    def __init__(self, xydata, transformation=None):
        self.xydata = xydata
        self.transformation = transformation

    def __len__(self):
        return self.xydata.shape[0]

    def __getitem__(self, idx):
        ret = self.xydata[idx, :, :, :]
        if self.transformation:
            ret = self.transformation(ret)
        return ret


trainset = XYDataset(data[:-10000, :, :, :])
train_loader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                           shuffle=True)
testset = XYDataset(data[10000:, :, :, :])
test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False)



class NeuralNetwork(nn.Module):

    class ResidualBlock(nn.Module):
        """
        Residual block with two conv layers and a skip connection.
        GroupNorm is used instead of BatchNorm for stability at small batch sizes
        and consistent behaviour between train and eval modes.
        """
        def __init__(self, channels):
            super(NeuralNetwork.ResidualBlock, self).__init__()
            self.block = nn.Sequential(
                nn.Conv2d(channels, channels, kernel_size=3, padding=1),
                nn.GroupNorm(8, channels),
                nn.SiLU(),
                nn.Conv2d(channels, channels, kernel_size=3, padding=1),
                nn.GroupNorm(8, channels),
            )
            self.act = nn.SiLU()

        def forward(self, x):
            return self.act(x + self.block(x))
        
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.latent_dim = 256

        # Encoder: angles are embedded as (cos theta, sin theta)
        # Input shape: [B, 2, 16, 16]
        # Output shape: [B, 2048]
        self.encoder = nn.Sequential(
            nn.Conv2d(2, 64, kernel_size=3, stride=1, padding=1),
            nn.SiLU(),
            self.ResidualBlock(64),
            self.ResidualBlock(64),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.SiLU(),
            self.ResidualBlock(128),
            self.ResidualBlock(128),
            nn.Conv2d(128, 256, kernel_size=3, stride=2, padding=1),
            nn.SiLU(),
            self.ResidualBlock(256),
            self.ResidualBlock(256),
            nn.Conv2d(256, 512, kernel_size=3, stride=2, padding=1),
            nn.SiLU(),
            self.ResidualBlock(512),
            nn.Flatten(),
        )
        self.fc_mu     = nn.Linear(512 * 2 * 2, self.latent_dim)
        self.fc_logvar = nn.Linear(512 * 2 * 2, self.latent_dim)

        # Decoder: latent vector -> 2-channel output -> angles via atan2
        self.fc_dec = nn.Linear(self.latent_dim, 512 * 2 * 2)
        self.decoder = nn.Sequential(
            nn.Unflatten(1, (512, 2, 2)),
            self.ResidualBlock(512),
            nn.ConvTranspose2d(512, 256, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.SiLU(),
            self.ResidualBlock(256),
            self.ResidualBlock(256),
            nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.SiLU(),
            self.ResidualBlock(128),
            self.ResidualBlock(128),
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.SiLU(),
            self.ResidualBlock(64),
            self.ResidualBlock(64),
            nn.Conv2d(64, 2, kernel_size=3, stride=1, padding=1),
        )

    def sample(self, batchSize):
        """
        Generate samples with the correct output shape [batchSize, 1, 16, 16]
        """
        device = next(self.parameters()).device
        with torch.no_grad():
            z = torch.randn(batchSize, self.latent_dim, device=device)
            cs = self.decoder(self.fc_dec(z))
            
            # Normalize to unit circle
            norm = torch.sqrt((cs ** 2).sum(dim=1, keepdim=True) + 1e-8)
            cs = cs / norm
            
            # Convert from (cos, sin) to angles: atan2(sin, cos) = angle
            samples = torch.atan2(cs[:, 1:2, :, :], cs[:, 0:1, :, :])
            
        return samples.cpu()

    def implement_your_method_if_needed(self):
        pass

    def reparameterize(self, mu, logvar):
        """Reparameterisation trick: z = mu + eps * std, eps ~ N(0, I)."""
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(std)

    def forward(self, x):
        # x shape: [B, 1, 16, 16]
        # Convert to (cos, sin) representation
        cs_in = torch.cat([torch.cos(x), torch.sin(x)], dim=1)  # [B, 2, 16, 16]
        
        h = self.encoder(cs_in)  # [B, 2048]
        mu     = self.fc_mu(h)   # [B, 256]
        logvar = torch.clamp(self.fc_logvar(h), min=-20, max=20)  # [B, 256]
        
        z = self.reparameterize(mu, logvar)  # [B, 256]
        cs_out = self.decoder(self.fc_dec(z))  # [B, 2, 16, 16]
        
        # Normalize to unit circle
        norm = torch.sqrt((cs_out ** 2).sum(dim=1, keepdim=True) + 1e-8)  # [B, 1, 16, 16]
        cs_out = cs_out / norm  # [B, 2, 16, 16]
        
        # ✅ CRITICAL FIX: Keep spatial dimensions in output
        recon = torch.atan2(cs_out[:, 1:2, :, :], cs_out[:, 0:1, :, :])  # [B, 1, 16, 16]
        
        return recon, mu, logvar


def train(net):
    '''
    Train your model on GPU with proper device management
    '''
    device = torch.device("cuda" if torch.cuda.is_available() else
                          ("mps" if torch.backends.mps.is_available() else "cpu"))
    print(f"Training on device: {device}")
    net.to(device)

    optimizer = optim.AdamW(net.parameters(), lr=1e-3, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=400, eta_min=1e-5)

    epochs   = 400
    patience = 15
    best_val_loss    = float('inf')
    patience_counter = 0
    ckpt_path        = 'temp_best_model.pth'

    for epoch in range(epochs):
        # KL annealing: ramp beta from 0 to 1 over the first 150 epochs
        beta = min(1.0, epoch / 150.0)

        # ── Training pass ─────────────────────────────────────────────────────
        net.train()
        total_train = 0.0
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()

            recon, mu, logvar = net(batch)

            # Reconstruction loss: angular distance
            recon_loss = torch.mean(1.0 - torch.cos(recon - batch)) * 256

            # KL divergence
            kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / batch.size(0)

            loss = recon_loss + beta * kl_loss
            loss.backward()
            nn.utils.clip_grad_norm_(net.parameters(), max_norm=1.0)
            optimizer.step()
            total_train += loss.item()

        scheduler.step()

        # ── Validation pass ───────────────────────────────────────────────────
        net.eval()
        total_val = 0.0
        with torch.no_grad():
            for batch in test_loader:
                batch = batch.to(device)
                recon, mu, logvar = net(batch)
                recon_loss = torch.mean(1.0 - torch.cos(recon - batch)) * 256
                kl_loss    = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp()) / batch.size(0)
                total_val += (recon_loss + beta * kl_loss).item()

        avg_train = total_train / len(train_loader)
        avg_val   = total_val   / len(test_loader)
        lr_now    = optimizer.param_groups[0]['lr']
        print(f"Epoch [{epoch+1:03d}/{epochs}] | LR: {lr_now:.6f} | Beta: {beta:.4f} | "
              f"Train: {avg_train:.4f} | Val: {avg_val:.4f}")

        # ── Early stopping ────────────────────────────────────────────────────
        if avg_val < best_val_loss:
            best_val_loss    = avg_val
            patience_counter = 0
            net.to('cpu')
            torch.save(net.state_dict(), ckpt_path)
            net.to(device)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping triggered at epoch {epoch + 1}.")
                break

    # Restore the best checkpoint before saving the final model
    if os.path.exists(ckpt_path):
        net.load_state_dict(torch.load(ckpt_path, map_location='cpu', weights_only=True))
        os.remove(ckpt_path)
    net.to('cpu')


if __name__ == "__main__":
    net = NeuralNetwork()
    print(net)
    train(net)
    torch.save(net, 'generative.pth')