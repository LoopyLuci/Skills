---
name: modern-cpp-patterns
description: "Use when writing modern C++17/20/23: concepts, ranges, coros."
category: software-development
tags: [cpp, modern, cpp20, concepts, ranges, coroutines]
---
# Modern C++ Patterns

C++17/20/23 patterns: concepts, ranges, coroutines, smart pointers, move semantics.

## Concepts (C++20)

```cpp
#include <concepts>

template<typename T>
concept Trainable = requires(T model, std::vector<float> data) {
    { model.forward(data) } -> std::same_as<std::vector<float>>;
    { model.backward(data) } -> std::convertible_to<float>;
    requires std::copyable<T>;
};

template<Trainable T>
float train_step(T& model, const std::vector<float>& batch) {
    auto pred = model.forward(batch);
    return model.backward(pred);
}
```

## Ranges (C++20)

```cpp
#include <ranges>
#include <vector>
#include <iostream>

namespace rv = std::views;

std::vector<int> data = {1, 2, 3, 4, 5, 6, 7, 8};

auto result = data
    | rv::filter([](int n) { return n % 2 == 0; })   // 2,4,6,8
    | rv::transform([](int n) { return n * n; })      // 4,16,36,64
    | rv::take(3);                                     // 4,16,36

for (int v : result) std::cout << v << " ";
```

## Smart Pointers

```cpp
#include <memory>

class Model {
    std::unique_ptr<Layer[]> layers;
    size_t num_layers;
public:
    Model(size_t n) : layers(std::make_unique<Layer[]>(n)), num_layers(n) {}
    virtual ~Model() = default;
    Model(const Model&) = delete;           // no copy
    Model(Model&&) = default;               // move ok
};

auto model = std::make_shared<Model>(12);
auto weak = std::weak_ptr<Model>(model);    // non-owning reference

// For shared state
struct TrainingConfig {
    float lr = 0.001;
    int batch_size = 32;
};
auto config = std::make_shared<TrainingConfig>();
```

## Move Semantics

```cpp
class Tensor {
    float* data_;
    size_t size_;
public:
    // Move constructor
    Tensor(Tensor&& other) noexcept
        : data_(std::exchange(other.data_, nullptr))
        , size_(std::exchange(other.size_, 0)) {}

    // Move assignment
    Tensor& operator=(Tensor&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = std::exchange(other.data_, nullptr);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
};
```

## Pitfalls

- Concepts don't fully SFINAE — use `requires` clauses for constraints
- Ranges views are lazy — materialize with `std::ranges::to<std::vector>()`
- `std::move` doesn't move — it casts to rvalue; move happens in constructor/assignment
- Coroutines are viral — any function calling `co_await` becomes a coroutine
- `std::shared_ptr` has overhead (control block, atomic refcount) — prefer `unique_ptr`
