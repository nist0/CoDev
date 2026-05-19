---
name: pic
description: PIC firmware — MCU identification, ISR safety, peripheral configuration, memory constraints, and debugging.
argument-hint: "[PIC model] [peripheral or subsystem]"
user-invocable: true

disable-model-invocation: false
---

# PIC Firmware (Elite)

## When to use

- You write/debug PIC firmware (Microchip).

- You need to handle low-level constraints, interrupts, and peripherals.

## Configuration Bits Reference

| Bit | Common setting | Notes |
|-----|---------------|-------|
| `FOSC` | `HS` / `INTOSC` | Clock source; match crystal or internal osc |
| `WDTE` | `OFF` | Disable watchdog for dev; enable for production |
| `PWRTE` | `ON` | Power-up timer (voltage stabilization) |
| `MCLRE` | `ON` / `OFF` | Master clear enable |
| `LVP` | `OFF` | Low-voltage programming (disable in production) |

## Workflow

### 1. Identify target

- PIC model, toolchain (MPLAB XC8/XC16/XC32), clock frequency, configuration bits.

- Programmer type (PICkit, ICD, SNAP).

### 2. Interrupt strategy

- Keep ISRs minimal: set flag, return.

- Protect shared data with `GIE` disable/re-enable or atomic operations.

### 3. Peripheral setup

- Timers, UART, ADC, PWM as needed.

- Calculate prescaler and reload values for target frequency/baud.

### 4. Memory and performance constraints

- Keep loops tight; avoid heavy runtime features (dynamic alloc).

- Bank switching awareness (PIC16/18): use `BANKSEL` or MCC-managed banks.

### 5. Debug and verify

- Serial logging (UART `printf`), MPLAB simulator, ICD/JTAG if available.

- Minimal test harness with known inputs and observable outputs.

## Self-check

- [ ] Configuration bits explicitly set (no defaults assumed).

- [ ] ISRs minimal (set flag only, no blocking calls).

- [ ] Shared data between ISR and main loop protected.

- [ ] Timer/baud calculations verified against actual clock frequency.

- [ ] Watchdog timer configured intentionally (not accidentally left on/off).

## Outputs

- Firmware setup checklist.

- ISR and peripheral safety checklist.

- Debugging and verification plan.
