---
name: avr
description: AVR firmware — MCU identification, ISR safety, peripheral configuration, memory constraints, and debugging.
argument-hint: "[MCU model] [peripheral or subsystem]"
user-invocable: true

disable-model-invocation: false
---

# AVR (Atmel) Firmware (Elite)

## When to use

- You write/debug AVR firmware (Arduino-class MCUs).

- You need low-level constraints: timers, interrupts, IO, memory.

## Memory Constraints Reference

| Resource | Constraint |
|----------|------------|
| Flash | Read-only at runtime; constants in `PROGMEM` |
| SRAM | Stack + heap share; fragmentation risk |
| EEPROM | Limited writes (~100k cycles); use `eeprom_update_*` |
| Registers | 32 general-purpose (r0–r31); r26–r31 as X/Y/Z pointers |

## Workflow

### 1. Identify target

- MCU model (ATmega328P, ATtiny85, etc.), clock frequency, toolchain (avr-gcc/avrdude).

- Fuse bits and programmer type.

### 2. Interrupt strategy

- Keep ISRs minimal: set flag/update variable, return.

- Protect shared data with `ATOMIC_BLOCK(ATOMIC_RESTORESTATE)`.

- Never block or call malloc/free inside ISRs.

### 3. Timing and peripherals

- Calculate timer prescaler for target frequency: $f_{timer} = \frac{f_{cpu}}{prescaler}$.

- Configure UART/SPI/I2C via register settings; validate baud rate error < 2%.

### 4. Memory discipline

- Use `PROGMEM` and `pgm_read_*` for large read-only data.

- Track stack depth; add stack canary in debug builds.

- Avoid dynamic allocation (`malloc`/`free`) in constrained firmware.

### 5. Debug and verify

- Serial logs (UART `printf`), AVR simulator (`simavr`), JTAG if available.

- Minimal test harness with known inputs and observable outputs.

## Self-check

- [ ] ISRs are minimal (set flag only, no blocking calls).

- [ ] Shared data between ISR and main loop protected with `ATOMIC_BLOCK`.

- [ ] Stack depth estimated and verified (no overflow risk).

- [ ] Large constants moved to `PROGMEM`.

- [ ] Timer/baud calculations validated against actual clock frequency.

## Outputs

- Firmware architecture checklist.

- ISR safety checklist.

- Debugging and verification plan.
