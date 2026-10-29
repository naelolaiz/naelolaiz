# Projects & experiments

A collection of open-source tools, simulations and hardware experiments, from digital logic and embedded Linux to real-time scheduling, acoustics and music software.

**Areas:** FPGA & digital design · Embedded systems & RISC-V · Linux scheduling & real-time systems · Room & outdoor acoustics · Music production · Linux infrastructure · 3D design

**Technologies:** VHDL · Verilog · C/C++ (C++11–26) · Python · Rust · JavaScript · Shell · Linux · Qt · CMake/CTest · GHDL · Yosys · Podman · OpenSCAD · GitHub Actions

[Explore the project index](#project-index) · [View project statistics](#project-statistics) · [Browse all repositories](https://github.com/naelolaiz?tab=repositories)

## Featured work

| Project | Highlights |
| :--- | :--- |
| [learning_fpga](#learning_fpga--from-digital-logic-to-a-risc-v-cpu) | Paired VHDL/Verilog designs, single-cycle and pipelined RV32I CPUs, a memory-mapped SoC with SIMD/FIR accelerators, and a CI-generated schematic/waveform gallery. |
| [Alpine Linux on ESP32-S31](#alpine-linux-on-esp32-s31) | 32-bit RISC-V Linux bring-up on hardware and in QEMU, with a 19-patch `aports` series, signed `apk` repository on GitHub Pages, Ethernet, native Wi-Fi and SSH. |
| [linux-scheduling-lab](#linux-scheduling-lab) | Measured Linux scheduling experiments in C++20 and Python: synthesized audio/video workloads, `SCHED_FIFO`/`RR`/`DEADLINE`, priority inheritance, `mlock`, cgroup v2 and offline HTML reports. |
| [acoustic-spaces](#acoustic-spaces) | Indoor and outdoor acoustics simulator on PyPI, with a Qt editor, ray tracing, edge diffraction, wave and parabolic-equation solvers on CPU/GPU, four binaural demos and published validation. |
| [Ferrous Lineup](#ferrous-lineup) | Five-crate Rust music studio with an automatic backing band, 300+ demo songs, 171 styles, audio-to-chord transcription, MP4/PDF/WAV/MIDI export, and a bilingual companion book. |

## Project index

| Explore | Projects & focus |
| :--- | :--- |
| **[FPGA & digital design](#fpga--digital-design)** | **[learning_fpga](#learning_fpga--from-digital-logic-to-a-risc-v-cpu)** — paired VHDL/Verilog, RV32I CPUs and SoC, VGA/audio/serial peripherals, testbenches and CI diagrams. |
| [HDL tooling](#hdltools--hdl-toolchain--waveform-rendering) | [hdltools / waveview](#hdltools--hdl-toolchain--waveform-rendering) — containerized simulation, synthesis and headless waveform rendering. |
| [Embedded Linux](#embedded-linux) | **RISC-V & Arm:** [esp32s31-alpine](#alpine-linux-on-esp32-s31) · [alpine-riscv32](#alpine-linux-for-32-bit-risc-v) · [ESP32-S31 kernel work](#linux--esp32-s31-kernel-work) · [luckfox_rockchip_testing](#luckfox_rockchip_testing) · [openbouffalo_dev_container / BL808](#openbouffalo_dev_container) |
| [Microcontrollers & firmware](#microcontrollers--firmware) | **ESP32 / ESP32-S3 / ESP32-C3:** [signal-generator experiments](https://github.com/naelolaiz/esp32_wifiAP_httpServer_signalGenerator) · [timers & DAC](https://github.com/naelolaiz/test_esp32_timers) · [PoC_PoV](https://github.com/naelolaiz/PoC_PoV) · [DMX512](https://github.com/naelolaiz/osc_to_dmx512) |
| [Board support & build automation](#board-support--build-automation) | [PlatformIO ESP32-S31 support](#esp32-s31-support-for-platformio) · [Sipeed M1s / BL808 SDK](#m1s_bl808_linux_sdk) |
| [Drivers & peripheral interfaces](#drivers--peripheral-interfaces) | **[PyMOPanel](#pymopanel)** · [Linux GPIO/PWM · MPU6050 · FPGA UART/I²C · UDA1380 · AD9833 experiments](#other-peripheral-interfaces) |
| [3D printing & mechanical design](#3d-printing--mechanical-design) | [3d_models](#3d_models) — OpenSCAD enclosures, motor supports and galvanometer mirror mounts with CI-rendered STL/PNG previews. |
| [Linux scheduling, packaging & infrastructure](#linux-packaging--infrastructure) | **[linux-scheduling-lab](#linux-scheduling-lab)** — measured scheduling, RT & cgroup v2 experiments · **[gentoo-binhost](#gentoo-binhost)** — signed `x86-64-v3` binary packages · [gitea-rootless-podman-kit](#gitea-rootless-podman-kit) |
| [C++ & compiler experiments](#c--compiler-experiments) | **[gcc_updates](#gcc_updates)** — C++11–26 & GCC 13–16 executable reference, Clang 23 cross-check, sanitizers and `-fanalyzer` CI. |
| [Room & outdoor acoustics](#room-acoustics--audio-dsp) | **[acoustic-spaces](#acoustic-spaces)** — indoor/outdoor acoustics simulator on PyPI: CAD/BIM & map scenes, ray tracing, wave/WAPE GPU solvers, binaural demos, portable scene packs and validation. |
| [Music production](#music-production) | **[Ferrous Lineup](#ferrous-lineup)** — Rust music studio with a backing band, sequencer, harmony tools, audio-to-chord analysis and an English/Spanish book. |
| [Audio & instrument control](#audio--instrument-control) | [WaveDiff](https://github.com/naelolaiz/vamp_wavediff) · [VoxPad](#voxpad) · [PSG9080 control](https://github.com/naelolaiz/JDY-31_PSG9080) |
| [Games & simulations](#games--simulations) | **[Sprint to Nowhere](#sprint-to-nowhere)** — satirical sprint-management roguelike in React. |
| [Project statistics](#project-statistics) | Language mix, source-repository activity, workflow presence and project counts. |

## FPGA & digital design

### [learning_fpga — from digital logic to a RISC-V CPU](https://github.com/naelolaiz/learning_fpga)

A progressive collection of **paired VHDL and Verilog designs**, from logic styles, clock enables, PWM, synchronous RAM/ROM and FIFOs to 7-segment and 640×480 VGA displays, serial buses, audio playback and processor architecture.

- **CPU design:** tutorial CPUs implementing an RV32I subset in both single-cycle and five-stage pipelined forms, with data forwarding, load-use hazard stalls and branch flushing.
- **Hardware/software integration:** a runnable RV32I SoC pairing the CPU with memory-mapped UART TX/RX, a four-lane SIMD ALU and a 4-tap FIR filter accelerator, backed by a zero-dependency Python assembler (`rv32_asm`) and executable test programs.
- **Verification:** self-checking assertion testbenches and a shared container build (`hdltools`) for local development and CI, which automatically synthesizes RTL schematics and renders waveform diagrams.

[CPU & SoC walkthrough](https://github.com/naelolaiz/learning_fpga/tree/main/cpu) · [RV32I assembler](https://github.com/naelolaiz/learning_fpga/tree/main/tools/rv32_asm) · [Timing notes](https://github.com/naelolaiz/learning_fpga/blob/main/docs/timing.md) · [Live CI gallery](https://github.com/naelolaiz/learning_fpga/tree/ci-gallery/latest)

| `blink_led` · VHDL schematic | `blink_led` · Verilog schematic |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/basics-blink_led/blink_led.svg" alt="Blink LED RTL schematic synthesized from VHDL" width="340">](https://github.com/naelolaiz/learning_fpga/tree/main/basics/blink_led) | [<img src="https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/basics-blink_led/blink_led_v.svg" alt="Blink LED RTL schematic synthesized from Verilog" width="340">](https://github.com/naelolaiz/learning_fpga/tree/main/basics/blink_led) |

[![Blink LED testbench waveform](https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/basics-blink_led/tb_blink_led.png)](https://github.com/naelolaiz/learning_fpga/tree/main/basics/blink_led)

| 7-segment clock · RTL schematic | Clock dot-blink waveform |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/display-7segments-clock/top_level_7segments_clock.svg" alt="Top-level RTL schematic of the 7-segment clock" width="340">](https://github.com/naelolaiz/learning_fpga/tree/main/display/7segments/clock) | [<img src="https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/display-7segments-clock/tb_clock_dot_blink.png" alt="Clock dot-blink testbench comparing MMSS and HHMM blink timing" width="340">](https://github.com/naelolaiz/learning_fpga/tree/main/display/7segments/clock) |

*Schematics and testbench waveforms update through CI; the clock waveform checks dot-blink timing.*

[![UART receiver simulation showing serial input, decoded bytes and receive-valid pulses](https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/comm-uart_rx/tb_uart_rx.png)](https://github.com/naelolaiz/learning_fpga/tree/main/comm/uart_rx)

*UART receiver testbench output; regenerated by CI as the design changes.*

### [hdltools — HDL toolchain & waveform rendering](https://github.com/naelolaiz/hdltools)

A containerized VHDL, Verilog and SystemVerilog toolchain combining **GHDL, Yosys with ghdl-yosys-plugin, Icarus Verilog, Verilator and slang**. Includes **netlistsvg** for RTL schematics and the **waveview** renderer, which turns VCD/FST/GHW traces into deterministic SVG/PNG diagrams without a desktop session, with sidecar YAML control over signal groups, formatting and time windows. Used by `learning_fpga` for simulation and CI artifacts.

[Container & build targets](https://github.com/naelolaiz/hdltools) · [waveview documentation](https://github.com/naelolaiz/hdltools/tree/main/waveview)

## Embedded systems

### Embedded Linux

Linux bring-up, root filesystems, cross-compilation and peripheral access across **RISC-V and Arm** platforms.

#### [Alpine Linux on ESP32-S31](https://github.com/naelolaiz/esp32s31-alpine)

Bringing Alpine Linux (`riscv32`, musl, OpenRC, `apk`) to the **ESP32-S31 Function-CoreBoard-1**, using Espressif's Linux 6.18 BSP, custom kernel fragments and a dual-hart SMP/Wi-Fi stack.

- **Working on hardware:** Linux 6.18 boots an ext4 root filesystem from USB automatically on reset (falling back to Buildroot when unplugged), OpenRC starts a serial console and Dropbear SSH, Ethernet and native WPA2 Wi-Fi (including channels 12 and 13) connect at boot, the on-chip temperature sensor (`esp32s31_tsens`) is enabled via a runtime device-tree overlay, and `apk` installs signed packages over the network.
- **Step-by-step engineering record:** a 24-step bring-up plan across six phases with reproducible guides, pinned BSP commits, kernel patches/fragments, Buildroot overlays and a dated hardware journal.

[Source & setup](https://github.com/naelolaiz/esp32s31-alpine) · [Steps & guides](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/steps/README.md) · [Boot from USB](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-07-boot-from-stick.md) · [Ethernet & apk](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-07-network-apk.md) · [Native Wi-Fi & SSH](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-11-alpine-wifi.md) · [Temperature sensor](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-11-temperature-sensor.md)

#### [linux — ESP32-S31 kernel work](https://github.com/naelolaiz/linux/tree/review/esp32s31-smp-wifi)

**Kernel fork:** targeted ESP32-S31 fixes and experimental SMP/Wi-Fi integration with Espressif's boot stack. Includes RV32 F-only floating-point support, non-coherent DMA setup and XIP RAM-resource accounting fixes, plus adaptations of an existing SMP/radio port for per-hart interrupts, timers and cache handling.

CI builds the XIP kernel and bootloader artifacts, plus matched radio artifacts on the SMP/Wi-Fi branch.

[Focused fixes](https://github.com/naelolaiz/linux/tree/review/esp32s31-fixes) · [SMP/Wi-Fi integration](https://github.com/naelolaiz/linux/tree/review/esp32s31-smp-wifi) · [Patch comparison](https://github.com/naelolaiz/linux/compare/dc0e3821e39bd7c169cefd274691e1998a844028...review/esp32s31-smp-wifi) · [CI runs](https://github.com/naelolaiz/linux/actions/workflows/esp32s31.yml?query=branch%3Areview%2Fesp32s31-smp-wifi)

#### [Alpine Linux for 32-bit RISC-V](https://github.com/naelolaiz/alpine-riscv32)

The board-independent distribution work behind the bring-up: a 19-patch **`aports` series**, cross toolchain and musl-based userspace for `rv32imac_zicsr_zifencei` / `ilp32` soft-float, suitable for QEMU, LiteX or any RV32 Linux target.

- **Bootstrap & native packages:** cross-builds Alpine's bootstrap set (`alpine-base`, OpenRC, `apk`) and builds 450+ `riscv32` packages natively under `qemu-user`—including `python3` (3.14), `openssl`, `openssh`, `wpa_supplicant`, `iw`, `htop`, `vim`, `tmux`, `btop` and `lm-sensors`.
- **Automated `apk` repository:** GitHub Actions builds incremental changes and publishes a signed `apk` repository on [GitHub Pages](https://naelolaiz.github.io/alpine-riscv32/) alongside versioned GitHub release archives for offline USB installation.

[Patch series](https://github.com/naelolaiz/alpine-riscv32/tree/main/patches) · [Package status](https://github.com/naelolaiz/alpine-riscv32/blob/main/RISCV32.md) · [Build & boot guides](https://github.com/naelolaiz/alpine-riscv32/tree/main/docs/steps) · [Package CI & Pages repo](https://github.com/naelolaiz/alpine-riscv32/blob/main/docs/steps/23-package-ci.md)

#### [luckfox_rockchip_testing](https://github.com/naelolaiz/luckfox_rockchip_testing)

Cross-compiled C++ GPIO/PWM applications and bench measurements of PWM and UART on **Arm-based Rockchip RV1103/RV1106** boards. [Two servos and a laser draw Lissajous curves](https://raw.githubusercontent.com/naelolaiz/luckfox_rockchip_testing/main/test_programs/pwm_two_servos/doc/lissajous.gif).

| Lissajous laser projection | UART transmission capture |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/luckfox_rockchip_testing/main/test_programs/pwm_two_servos/doc/lissajous.gif" alt="Animated laser projection of Lissajous curves controlled by two servos" width="340">](https://github.com/naelolaiz/luckfox_rockchip_testing/tree/main/test_programs/pwm_two_servos) | [<img src="https://raw.githubusercontent.com/naelolaiz/luckfox_rockchip_testing/main/doc/testing_uart_tx.png" alt="UART transmission from Linux on a Luckfox board, captured with a logic analyzer" width="340">](https://github.com/naelolaiz/luckfox_rockchip_testing#uart) |

#### [openbouffalo_dev_container](https://github.com/naelolaiz/openbouffalo_dev_container)

Ubuntu-based development container for **Bouffalo BL808 / Pine64 Ox64**. Builds OpenBouffalo's Linux image and Buildroot SDK, with ncurses support for kernel `menuconfig`.

[Container definition](https://github.com/naelolaiz/openbouffalo_dev_container/blob/main/Dockerfile)

### Microcontrollers & firmware

ESP32-family firmware experiments covering Wi-Fi, HTTP, timers, DAC output, motion sensors, LEDs and DMX512.

| Platform | Project | Contents |
| :--- | :--- | :--- |
| ESP32 / LOLIN32 · ESP-IDF | [esp32_wifiAP_httpServer_signalGenerator](https://github.com/naelolaiz/esp32_wifiAP_httpServer_signalGenerator) | Wi-Fi access-point and HTTP-interface proof of concept, with AD9833 experiments, browser forms and oscilloscope captures. |
| ESP32 / TTGO T1 · ESP-IDF | [test_esp32_timers](https://github.com/naelolaiz/test_esp32_timers) | General-purpose and high-resolution timers, GPIO callback/task comparisons and timer-driven DAC sawtooth generation. |
| ESP32-S3-DevKitC-1 / ESP-WROVER-KIT · Arduino | [PoC_PoV](https://github.com/naelolaiz/PoC_PoV) | LED persistence-of-vision prototype with MPU6050 motion measurements, bitmap-column playback and WebSocket sensor telemetry. |
| ESP32-C3 / LOLIN C3 Mini · Arduino | [osc_to_dmx512](https://github.com/naelolaiz/osc_to_dmx512) | Wi-Fi browser controls for DMX512 output, with pattern selection, zoom and movement settings. |

### Board support & build automation

#### [ESP32-S31 support for PlatformIO](https://github.com/naelolaiz/platform-espressif32/tree/esp32s31-support)

**Contribution branch:** board definition, RISC-V build integration and the correct bootloader flash offset for ESP32-S31. ESP-IDF **build, upload and boot have been tested on hardware**. Upstream integration is tracked separately.

[Implementation](https://github.com/naelolaiz/platform-espressif32/commit/87beab60446b1dffdcfec12d90676c715c5ca97f) · [Upstream discussion](https://github.com/platformio/platform-espressif32/issues/1777)

#### [M1s_BL808_Linux_SDK](https://github.com/naelolaiz/M1s_BL808_Linux_SDK)

**SDK fork:** build automation and dependency documentation around Sipeed's BL808 Linux SDK. The added workflow installs the upstream toolchains, builds firmware and uploads artifacts.

[SDK build-automation changes](https://github.com/naelolaiz/M1s_BL808_Linux_SDK/compare/baee2020e4dc418363205ac94a2d80deb9477cc2...main)

## Drivers & peripheral interfaces

### [PyMOPanel](https://github.com/naelolaiz/PyMOPanel)

Python driver for **Matrix Orbital GLK19264-7T-1U LCD/keypad panels**, with serial and direct USB transport, text and graphics, keypad input and GPO control. Includes monitoring demos and bitmap/GIF frame playback. Work in progress.

[Panel interface](https://github.com/naelolaiz/PyMOPanel/blob/main/PyMOPanel/PyMOPanel.py) · [USB transport](https://github.com/naelolaiz/PyMOPanel/blob/main/PyMOPanel/usb_transport.py)

### Other peripheral interfaces

| Interface | Implementation |
| :--- | :--- |
| [Linux GPIO](https://github.com/naelolaiz/luckfox_rockchip_testing/blob/main/test_programs/peripherals_interface/GPIO.h) / [PWM](https://github.com/naelolaiz/luckfox_rockchip_testing/blob/main/test_programs/peripherals_interface/PWM.h) | C++ userspace interfaces through Linux sysfs, used by GPIO blink and PWM/servo experiments. |
| [MPU6050](https://github.com/naelolaiz/PoC_PoV/blob/main/src/MPU6050.h) | I²C register access for accelerometer, gyroscope and temperature measurements, used by the persistence-of-vision prototype. |
| [FPGA UART TX](https://github.com/naelolaiz/learning_fpga/tree/main/comm/uart_tx) / [RX](https://github.com/naelolaiz/learning_fpga/tree/main/comm/uart_rx) | Paired VHDL/Verilog serial controllers with simulation testbenches. |
| [FPGA I²C master](https://github.com/naelolaiz/learning_fpga/tree/main/comm/i2c_master) | Byte engine with START/STOP, repeated START, ACK/NACK and clock-stretching support. |
| [UDA1380 audio codec](https://github.com/naelolaiz/learning_fpga/tree/main/comm/uda1380) | Codec initialization over I²C and I²S playback logic, verified in simulation. |
| [AD9833 wrapper](https://github.com/naelolaiz/esp32_wifiAP_httpServer_signalGenerator/blob/master/lib/AD9833_function_generator/AD9833Driver.cpp) | Prototype driver experiments around the MD_AD9833 library. |

## 3D printing & mechanical design

### [3d_models](https://github.com/naelolaiz/3d_models)

**OpenSCAD** models for ADAU1701 DSP enclosures, stackable boxes, motor supports and galvanometer mirror mounts. GitHub Actions generates STL files and PNG previews from the model sources.

| Mirror support render | ADAU1701 DSP case | Assembled galvanometer |
| :---: | :---: | :---: |
| [<img src="https://naelolaiz.github.io/3d_models/45_degree_angle_mirror_support.png" alt="Rendered OpenSCAD mirror support for a stepper motor" width="250">](https://github.com/naelolaiz/3d_models/tree/main/stepper_motors_galvo_support/v1/45_degree_angle_mirror_support) | [<img src="https://raw.githubusercontent.com/naelolaiz/3d_models/main/DSP_ADAU1701_case/pictures/bottom_case_v2.jpg" alt="Printed ADAU1701 DSP enclosure with its circuit boards fitted" width="250">](https://github.com/naelolaiz/3d_models/tree/main/DSP_ADAU1701_case) | [<img src="https://raw.githubusercontent.com/naelolaiz/3d_models/main/stepper_motors_galvo_support/doc/IMG20231224195128.png" alt="Assembled stepper-motor mirror mounts made from the OpenSCAD models" width="250">](https://github.com/naelolaiz/3d_models/tree/main/stepper_motors_galvo_support) |

## Linux packaging & infrastructure

### [linux-scheduling-lab](https://github.com/naelolaiz/linux-scheduling-lab)

Hands-on, measured **Linux scheduling experiments** for real-time and offline workloads. A **C++20** native engine executes real work—48 kHz mono PCM audio synthesis/filtering and 160×90 grayscale PGM frame generation/blurring—while a zero-dependency **Python standard-library** harness (`schedlab`) orchestrates runs and renders self-contained offline HTML reports (`report.html`).

- **Policies, locks & resource controls:** compares `SCHED_OTHER` / nice levels, `SCHED_BATCH`, `SCHED_IDLE`, `SCHED_FIFO` / `SCHED_RR`, and `SCHED_DEADLINE` (`sched_setattr` admission and runtime/deadline/period budgets); measures priority inversion against `PTHREAD_PRIO_INHERIT` mutexes, page faults with prefaulting and `mlock`, CPU affinity, and delegated cgroup v2 CPU weight and quota.
- **Threading & cross-system analysis:** includes a runnable C++20 `std::jthread` and bounded-queue audio pipeline with its publication and shutdown protocol, plus `doctor`, `replay` and `compare` commands to evaluate results across kernel preemption modes (`PREEMPT_DYNAMIC`, `PREEMPT_RT`), boots and machines.
- **Portable & safe by default:** invokes Linux per-thread scheduler syscalls directly so both glibc and musl behave identically; runs unprivileged by default with Gentoo/OpenRC as a first-class setup, explicit `--allow-rt` opt-in, and independent native and Python watchdogs. CI validates GCC and Clang on x86-64 and arm64, static Alpine musl builds, and arm64/riscv64 cross-compilation.

[Tutorial](https://github.com/naelolaiz/linux-scheduling-lab/blob/main/docs/TUTORIAL.md) · [Threading & C++20 pipeline](https://github.com/naelolaiz/linux-scheduling-lab/blob/main/docs/THREADING_AND_CODE.md) · [Kernels & hardware](https://github.com/naelolaiz/linux-scheduling-lab/blob/main/docs/KERNELS_AND_HARDWARE.md) · [Advanced experiments](https://github.com/naelolaiz/linux-scheduling-lab/blob/main/docs/ADVANCED.md) · [CI matrix](https://github.com/naelolaiz/linux-scheduling-lab/blob/main/.github/workflows/ci.yml)

### [gentoo-binhost](https://github.com/naelolaiz/gentoo-binhost)

Signed `.gpkg.tar` binary packages for **Gentoo `default/linux/amd64/23.0/desktop/plasma` (OpenRC, `~amd64`, `-march=x86-64-v3`)**, built inside fresh stage3 containers on GitHub Actions and layered above the official Gentoo `x86-64-v3` binhost via `binrepos.conf`.

- **Tiered build pipeline:** builds `00-smoke`, `10-heavy` (LLVM, Clang, QtWebEngine, WebKitGTK, VTK), `20-desktop` (Plasma, Qt, KDE apps, audio production, CAD), `21-desktop-more`, `25-steam-runtime` (32-bit `abi_x86_32` libraries for Steam) and `30-kmod` (kernel and VirtualBox modules), with compiler caching and automatic follow-up runs when a job reaches its time window.
- **Verified publication & maintenance:** a standard-library Python publisher uploads category release assets before updating the `Packages` index on the `binhost` branch, a clean-container consumer check verifies GPG signatures and binary installs, and a weekly workflow (`check-workarounds.yml`) tests whether profile workarounds can be retired.

[Architecture](https://github.com/naelolaiz/gentoo-binhost/blob/main/docs/ARCHITECTURE.md) · [Usage guide](https://github.com/naelolaiz/gentoo-binhost/blob/main/docs/USING.md) · [Steam 32-bit runtime](https://github.com/naelolaiz/gentoo-binhost/blob/main/docs/STEAM.md) · [Build & publication workflow](https://github.com/naelolaiz/gentoo-binhost/blob/main/.github/workflows/build.yml) · [Workaround checks](https://github.com/naelolaiz/gentoo-binhost/blob/main/.github/workflows/check-workarounds.yml)

### [gitea-rootless-podman-kit](https://github.com/naelolaiz/gitea-rootless-podman-kit)

Scripts for **rootless Gitea deployment, encrypted backups and restoration**, using Podman, age and zstd. Includes scheduled backups, OpenRC/systemd integration and a backup/restore round trip in CI.

[Setup & scripts](https://github.com/naelolaiz/gitea-rootless-podman-kit) · [Restore verification](https://github.com/naelolaiz/gitea-rootless-podman-kit/blob/main/.github/workflows/ci.yml)

## C++ & compiler experiments

### [gcc_updates](https://github.com/naelolaiz/gcc_updates)

An executable **C++11–26 language and standard-library reference**, with compiler-version gates, GCC extensions (`gccext_*`), measured toolchain default changes (`gccdef_*`) and curated per-release highlights for **GCC 13, 14, 15 and 16**.

- **Multi-compiler & multi-arch CI:** CMake/CTest runs the suite across **GCC 13–16 on both amd64 and arm64** (covering C++20 modules on GCC 15+ and C++26 contracts, reflection and library features on GCC 16), plus a **Clang 23 cross-check on amd64 and arm64** compiled against the same upstream libstdc++ 16.
- **Sanitizers & static analysis:** repeats the test suite under **UBSan+ASan+LSan and TSan on both GCC 15 and Clang 23**, alongside deliberate-trip sanitizer demos and compile-time **`-fanalyzer` path-analysis tests on GCC 16** that assert exact diagnostic output.

[Feature index](https://github.com/naelolaiz/gcc_updates/blob/main/features/TOPICS.md) · [Reference routes](https://github.com/naelolaiz/gcc_updates/blob/main/docs/reference-paths.md) · [GCC 13–16 release notes](https://github.com/naelolaiz/gcc_updates/blob/main/docs/gcc-changelogs.md) · [Sanitizers](https://github.com/naelolaiz/gcc_updates/blob/main/docs/sanitizers.md) · [Compiler CI matrix](https://github.com/naelolaiz/gcc_updates/blob/main/.github/workflows/ci.yml)

## Room acoustics & audio DSP

### [acoustic-spaces](https://github.com/naelolaiz/acoustic-spaces)

Open-source indoor and outdoor acoustics simulator and auralisation toolkit in the spirit of CATT-Acoustic and ODEON, with a **Qt editor, command line, Python API and C++ core**. Load a 3D model, draw a floor plan or build an outdoor terrain scene, place sources and listeners, compute impulse responses and listen to the result. Published on PyPI, with wheels for Linux, macOS and Windows on CPython 3.10–3.14:

```sh
pip install "acoustic-spaces[viz,gui]"
```

- **Indoor & outdoor scenes:** OBJ, DXF, glTF, STL, IFC, Collada and SketchUp imports or floor-plan drawing, CATT-Acoustic and ODEON material libraries, doors between rooms, audience areas, directional/line/surface and coherent element-by-element array sources, and a leak finder for open models—plus outdoor scenes with buildings, barriers, map terrain, finite and extended-reacting ground impedance, wind/temperature gradients, turbulence, vegetation and moving sources with Doppler shift.
- **Simulation & remote GPU packs:** ray-traced early reflections with edge diffraction, pressure-based low-frequency summation, a stochastic late tail, a low-frequency wave solver, and an outdoor wide-angle parabolic equation (WAPE) solver on CPU or GPU (`wgpu`). Computes ISO 3382-1/3382-2 parameters, STI, echo criteria and multi-level audience coverage maps; `acoustic-spaces pack` bundles any scene into a self-contained `.zip` for headless Vulkan GPU containers on remote servers or cloud jobs.
- **Spatial audio & binaural demos:** mono, binaural (with downloadable HRTF sets), Ambisonics (AmbiX) and loudspeaker impulse responses, offline and real-time convolution, head tracking and keyframed multi-mover video walkthroughs. Includes four scripted binaural headphone demos—Beethoven's 8th symphony from 61 anechoic tracks in the concert hall, choir and organ in the church, a band with its PA system in the stadium, and a lakeside concert in wind vs. still air—with a [YouTube playlist](https://www.youtube.com/playlist?list=PLWz5JDREfod8).
- **Measurements & verification:** sine-sweep measurement of real rooms, ISO 3382-1 JND comparison and material absorption fitting. A published validation report compares indoor and outdoor results against modal/UTD/FFP theory, `pyroomacoustics`, the BRAS benchmark and Hannover outdoor propagation measurements.

[PyPI](https://pypi.org/project/acoustic-spaces/) · [Getting started](https://github.com/naelolaiz/acoustic-spaces/blob/main/docs/getting-started.md) · [Outdoor scenes](https://github.com/naelolaiz/acoustic-spaces/blob/main/docs/outdoor.md) · [Demos](https://github.com/naelolaiz/acoustic-spaces/blob/main/docs/demos.md) · [Remote GPU runs](https://github.com/naelolaiz/acoustic-spaces/blob/main/docs/remote.md) · [Validation & known issues](https://github.com/naelolaiz/acoustic-spaces/blob/main/docs/validation.md) · [Releases](https://github.com/naelolaiz/acoustic-spaces/releases) · [Changelog](https://github.com/naelolaiz/acoustic-spaces/blob/main/CHANGELOG.md)

[![Beethoven's 8th in the virtual concert hall: the orchestra on stage and a seat in the middle of the stalls, with the first reflections from a violin](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/orchestra_video.png)](https://www.youtube.com/watch?v=c0-5F-iNhIE)

*Beethoven's 8th symphony in the concert-hall example: 61 anechoic tracks, one per instrument, heard binaurally from the stalls. Select the image to watch the video, or browse the [full demo playlist](https://www.youtube.com/playlist?list=PLWz5JDREfod8).*

<details>
<summary>Acoustic simulation gallery — editor, visualisations and measurements</summary>

*Select an image to open its full-size view.*

| Qt editor & concert-hall results | Floor-plan editing |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/editor.png" alt="Qt editor showing a concert-hall model, source properties, reflection paths and simulation results" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/editor.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/plan.png" alt="Floor-plan editor showing draggable corners, wall lengths, sources and listeners" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/plan.png) |

| Church model & reflection paths | Animated sound particles |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/church_paths.png" alt="Church model with direct sound and reflection paths through third order" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/church_paths.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/particles.gif" alt="Animated sound particles propagating through the concert hall, colored by level at 1 kHz" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/particles.gif) |

| Speech-intelligibility overlay in the editor | Audience coverage map |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/editor_map.png" alt="Speech transmission index overlaid on the lecture-hall model in the Qt editor" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/editor_map.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/coverage.png" alt="Top-down speech transmission index map across 176 audience positions" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/coverage.png) |

| Echogram & octave-band reverberation | Arrival directions |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/response.png" alt="Simulated concert-hall echogram and reverberation decay curves by octave band" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/response.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/directions.png" alt="Early arrival directions and late directional energy at a listener position" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/directions.png) |

| Source-directivity patterns | Diffraction around a corner |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/directivity.png" alt="Horizontal and vertical source-directivity polar patterns across octave bands" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/directivity.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/diffraction.png" alt="Sound levels around a gallery corner, with and without edge diffraction" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/diffraction.png) |

| Low-frequency wave-model comparison | Measured-room response analysis |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/wave.png" alt="Low-frequency transfer functions comparing modal theory, the wave solver and geometric rays" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/wave.png) | [<img src="https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/measured.png" alt="Measured BRAS CR2 seminar-room impulse response with noise-floor estimates and corrected octave-band decay curves" width="370">](https://raw.githubusercontent.com/naelolaiz/acoustic-spaces/main/docs/images/measured.png) |

*Measured-response example: BRAS CR2, LS1→MP1, from the [BRAS benchmark](https://doi.org/10.14279/depositonce-6726.3), CC BY-SA 4.0.*

</details>

## Music production

### [Ferrous Lineup](https://github.com/naelolaiz/ferrous-lineup)

An open-source **music studio and automatic backing band written in Rust** across five workspace crates (`lineup-core`, `lineup-audio`, `lineup-listen`, `lineup-video` and `lineup-app`). Enter a song's chords on the chord sheet, choose a style and play it in any key and tempo, or write and arrange parts by hand. Runs on Linux, macOS and Windows.

- **Backing band & practice:** chord sheets, **171+ harmony styles**, **107+ drum rhythms** and **300+ demo songs** drive piano, bass, drums, guitar, strings and organ—with intros, choruses, endings, A/B variations, swing, shots/pushes, an optional soloist, count-in, metronome, bar looping and part muting for live practice.
- **Writing & harmony:** a multi-track playlist, step sequencer, piano roll, style editor and mixer, with Roman-numeral chord naming and voice-leading suggestions, ear training, pitch-class sets by Forte number, twelve-tone rows (P/R/I/RI) and Kröpfl micromodes.
- **Audio, MIDI & export:** real-time synthesis and SoundFont playback (`rustysynth`), live MIDI In/Out (`midir`), audio-to-chord beat and key analysis of imported recordings (`lineup-listen`), headless CLI note tracing (`--trace`), PDF lead sheets, and WAV, MIDI and H.264/MP3 MP4 video export.
- **Bilingual companion book & Rust course:** *Ferrous Lineup: Building a Music Studio in Rust* (and its Spanish edition, *Construyendo un estudio de música en Rust*), available online and as downloadable PDFs, documenting both the studio workflow and the step-by-step Rust architecture.

[Book (EN)](https://naelolaiz.github.io/ferrous-lineup/) · [PDF (EN)](https://naelolaiz.github.io/ferrous-lineup/ferrous-lineup-book.pdf) · [Libro (ES)](https://naelolaiz.github.io/ferrous-lineup/es/) · [PDF (ES)](https://naelolaiz.github.io/ferrous-lineup/es/ferrous-lineup-book-es.pdf) · [App tour](https://naelolaiz.github.io/ferrous-lineup/tour.html) · [Build & run](https://github.com/naelolaiz/ferrous-lineup#build-and-run) · [Releases](https://github.com/naelolaiz/ferrous-lineup/releases) · [Project layout](https://github.com/naelolaiz/ferrous-lineup#project-layout)

| Studio & harmony keys | Chord sheet |
| :---: | :---: |
| [<img src="https://raw.githubusercontent.com/naelolaiz/ferrous-lineup/main/screenshots/main-window.png" alt="Ferrous Lineup playing a song, with the playlist, channel rack and harmony keys" width="370">](https://github.com/naelolaiz/ferrous-lineup) | [<img src="https://raw.githubusercontent.com/naelolaiz/ferrous-lineup/main/screenshots/chord-sheet.png" alt="Ferrous Lineup chord sheet showing a song's chords and Roman numerals" width="370">](https://github.com/naelolaiz/ferrous-lineup) |

## Audio & instrument control

| Project | What it does | Stack |
| :--- | :--- | :--- |
| [WaveDiff](https://github.com/naelolaiz/vamp_wavediff) | Audio A/B analysis: RMS, null-test residual and peak difference, through a Vamp plugin for hosts such as Sonic Visualiser, plus a Qt Quick interface and stdlib signal generator. | C++17 · Qt Quick · CMake / CTest |
| [Bluetooth instrument control](https://github.com/naelolaiz/JDY-31_PSG9080) | Python/Qt control of a PSG9080 signal generator over Bluetooth serial, with logic-analyzer captures documenting the protocol. | Python · Qt · Bluetooth |

### [VoxPad](https://github.com/naelolaiz/voxpad)

Local audio and WhatsApp voice-message transcription powered by Whisper (`faster-whisper`) through a **Python CLI, Qt desktop application and zero-install browser interface**. Accepts individual recordings (`.opus`, `.m4a`, `.ogg`, `.mp3`, `.wav`, `.flac`) or exported WhatsApp chat ZIPs/folders, matching voice notes to sender names and timestamps with optional word-level timestamps, keyword boosting and opt-in Hugging Face remote transcription.

[Documentation](https://github.com/naelolaiz/voxpad/blob/main/README.md) · [Browser application](https://naelolaiz.github.io/voxpad/)

## Games & simulations

### [Sprint to Nowhere](https://github.com/naelolaiz/sprint_to_nowhere)

A satirical **sprint-management roguelike** about backlog planning, interruptions, technical debt and burnout. Built with React 19, Vite and Tailwind CSS, deployed to GitHub Pages, and playable in English and Spanish. The goal is to survive ten sprints while keeping technical debt and burnout under control.

[Play online](https://naelolaiz.github.io/sprint_to_nowhere/) · [Game mechanics](https://github.com/naelolaiz/sprint_to_nowhere/blob/main/src/game/mechanics.js)

## Project statistics

Statistics for the featured projects, with support forks counted separately from source repositories.

[![Project overview: featured repositories, source repositories, support forks, detected languages and workflow presence](https://raw.githubusercontent.com/naelolaiz/naelolaiz/project-statistics/overview.svg)](stats/README.md)

[![Language mix across source repositories, measured by GitHub-detected code bytes](https://raw.githubusercontent.com/naelolaiz/naelolaiz/project-statistics/languages.svg)](stats/README.md)

[![Monthly non-merge commit activity across source repositories' default branches; current month is partial](https://raw.githubusercontent.com/naelolaiz/naelolaiz/project-statistics/activity.svg)](stats/README.md)

[Snapshot data](https://github.com/naelolaiz/naelolaiz/blob/project-statistics/data.json) · [Metrics & refresh details](stats/README.md)

[Browse all repositories →](https://github.com/naelolaiz?tab=repositories)
