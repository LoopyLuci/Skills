---
name: generative-models
description: "Use when building GANs, VAEs, or diffusion models."
category: mlops
tags: [generative, gans, vaes, diffusion, image-generation]
---
# Generative Models

Building and training GANs, VAEs, and diffusion models.

## Variational Autoencoders (VAEs)

```python
import torch
import torch.nn as nn

class VAE(nn.Module):
    def __init__(self, input_dim=784, latent_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
        )
        self.mu = nn.Linear(128, latent_dim)
        self.logvar = nn.Linear(128, latent_dim)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, input_dim), nn.Sigmoid(),
        )

    def encode(self, x):
        h = self.encoder(x)
        return self.mu(h), self.logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar

# Loss: reconstruction + KL divergence
def vae_loss(recon_x, x, mu, logvar):
    recon = nn.functional.binary_cross_entropy(recon_x, x, reduction='sum')
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon + kl
```

## Diffusion Models (Simplified)

```python
# Forward: add noise step by step
# Reverse: denoise step by step (learned)

class DiffusionModel:
    def __init__(self, model, timesteps=1000):
        self.model = model
        self.T = timesteps
        self.beta = torch.linspace(1e-4, 0.02, timesteps)
        self.alpha = 1 - self.beta
        self.alpha_bar = torch.cumprod(self.alpha, dim=0)

    def forward_diffusion(self, x0, t):
        # q(x_t | x_0) = N(x_t; sqrt(ᾱ_t)x_0, (1-ᾱ_t)I)
        noise = torch.randn_like(x0)
        xt = torch.sqrt(self.alpha_bar[t]) * x0 + \
             torch.sqrt(1 - self.alpha_bar[t]) * noise
        return xt, noise

    def training_loss(self, x0):
        t = torch.randint(0, self.T, (x0.shape[0],))
        xt, noise = self.forward_diffusion(x0, t)
        predicted_noise = self.model(xt, t)
        return nn.functional.mse_loss(predicted_noise, noise)

    @torch.no_grad()
    def sample(self, shape):
        x = torch.randn(shape)
        for t in reversed(range(self.T)):
            z = torch.randn_like(x) if t > 0 else 0
            predicted_noise = self.model(x, t)
            x = (1 / torch.sqrt(self.alpha[t])) * \
                (x - (1 - self.alpha[t]) / torch.sqrt(1 - self.alpha_bar[t]) * predicted_noise) + \
                torch.sqrt(self.beta[t]) * z
        return x
```

## GANs (Generative Adversarial Networks)

```python
class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_dim=784):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 256), nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Linear(256, 512), nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Linear(512, img_dim), nn.Tanh(),
        )

class Discriminator(nn.Module):
    def __init__(self, img_dim=784):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(img_dim, 256), nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(256, 128), nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(128, 1), nn.Sigmoid(),
        )

# Training loop alternates
# 1. Train discriminator on real + fake
# 2. Train generator to fool discriminator
```

## Pitfalls

- VAEs produce blurry images — use β-VAE or VQ-VAE for sharper output
- Diffusion models are slow to sample (1000 steps) — use DDIM or LCM for speed
- GAN training is unstable — use WGAN-GP or StyleGAN architecture
- Mode collapse in GANs: generator produces limited variety
- Diffusion models need careful noise schedule tuning
