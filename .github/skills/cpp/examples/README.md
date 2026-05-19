# C++ Skill — Examples
## 1. RAII Pattern
```cpp
#include <memory>
std::unique_ptr<int> ptr = std::make_unique<int>(42);
```
## 2. Lint with clang-tidy
```text
clang-tidy myfile.cpp --
```
## 3. Static Analysis with cppcheck
```sh
cppcheck myfile.cpp
```
