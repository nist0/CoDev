---
name: asm-x86
description: x86 Assembly (Intel) -- calling conventions, stack frames, registers, and low-level debugging procedure.
argument-hint: "[architecture: x86|x64] [context or function name]"
user-invocable: true

disable-model-invocation: false
---

# x86 Assembly (Intel) (Elite)

## When to use

- You need to read/write x86 assembly for performance or low-level debugging.

- You need to understand calling conventions, stack frames, and registers.

## Calling Convention Reference

| Convention | Platform | Args | Return | Caller-saved | Callee-saved |
|------------|----------|------|--------|--------------|--------------|
| `cdecl` | x86 Linux/Windows | Stack (right-to-left) | `eax` | `eax,ecx,edx` | `ebx,esi,edi,ebp` |
| `System V AMD64` | x64 Linux/macOS | `rdi,rsi,rdx,rcx,r8,r9` | `rax` | `r10,r11` | `rbx,r12-r15,rbp` |
| `Microsoft x64` | x64 Windows | `rcx,rdx,r8,r9` | `rax` | `rax,rcx,rdx,r8,r9,r10,r11` | `rbx,rdi,rsi,r12-r15,rbp` |

## Workflow

### 1. Establish context

- Architecture (x86/x64), OS, calling convention, toolchain.

- Identify the function boundary (prologue/epilogue).

### 2. Read control flow

- Trace prologue (stack frame setup) and epilogue (teardown).

- Identify register saving/restoring patterns.

### 3. Trace data flow

- Track values through registers and memory operands.

- Note sign/zero extension issues (`movzx`/`movsx`).

### 4. Debug effectively

- Minimal repro, disassembly (`objdump -d`, `gdb`, `windbg`).

- Set breakpoints at function entry; inspect registers and stack.

### 5. Safety review

- Check alignment (stack 16-byte aligned before `call` on x64).

- Look for buffer overflows, off-by-one stack usage.

- Watch for UB and platform-specific behavior.

## Self-check

- [ ] Calling convention identified and respected.

- [ ] Stack frame alignment verified (x64: 16-byte aligned before call).

- [ ] Caller-saved vs callee-saved registers correctly handled.

- [ ] Data flow traced for all inputs/outputs of the function.

- [ ] Debugger used to confirm hypothesis before declaring fix.

## Outputs

- Calling convention and stack frame summary.

- Debugging checklist (gdb/lldb/windbg commands).

- "What to inspect" list (registers/stack/memory).
