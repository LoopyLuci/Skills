# Layer Implementations — Forward/Backward Math

## Dense Layer

**Forward:**
```
out = x @ W + b
```
- x: (N, in_features)
- W: (in_features, out_features)
- b: (out_features,)
- out: (N, out_features)

**Activation functions:**
- relu: max(0, x)
- sigmoid: 1 / (1 + exp(-x))
- tanh: (exp(x) - exp(-x)) / (exp(x) + exp(-x))
- softmax: exp(x - max(x)) / sum(exp(x - max(x)))

**Backward:**
```
dW = x.T @ grad_output
db = sum(grad_output, axis=0)
dx = grad_output @ W.T
```

## Conv2D Layer

**Forward:**
```
out[n, f, i, j] = sum(patch * W[f]) + b[f]
```
- patch: x[:, :, i*s:i*s+K, j*s:j*s+K]
- K: kernel size
- s: stride

**Backward:**
```
dW[f] += sum(patch * grad_output[:, f, i, j])
dx[:, :, i*s:i*s+K, j*s:j*s+K] += W[f] * grad_output[:, f, i, j]
```

## LSTM Layer

**Forward (per timestep):**
```
f = sigmoid(concat([h, x]) @ Wf + bf)  # forget gate
i = sigmoid(concat([h, x]) @ Wi + bi)  # input gate
c_tilde = tanh(concat([h, x]) @ Wc + bc)  # candidate
c = f * c_prev + i * c_tilde  # cell state
o = sigmoid(concat([h, x]) @ Wo + bo)  # output gate
h = o * tanh(c)  # hidden state
```

**Backward:** Complex — propagates through all gates and cell state.

## BatchNorm Layer

**Forward:**
```
mean = mean(x, axis=0)
var = var(x, axis=0)
x_norm = (x - mean) / sqrt(var + eps)
out = gamma * x_norm + beta
```

**Backward:**
```
dgamma = sum(grad * x_norm, axis=0)
dbeta = sum(grad, axis=0)
dx = (grad * gamma) / sqrt(var + eps)
```

## Dropout Layer

**Forward:**
```
mask = (rand(x.shape) > p) / (1 - p)
out = x * mask  # training
out = x  # inference
```

**Backward:**
```
dx = grad * mask
```
