Tinkering with FPGAs, embedded systems, Linux, audio DSP, 3D printing.<br>
Tools, experiments, learning projects. Side projects<sub>(of side projects<sub>(of side projects<sub>(...)</sub>)</sub>)</sub>

## Project index

| Explore | Projects & focus |
| :--- | :--- |
| **[FPGA & digital design](#fpga--digital-design)** | **[learning_fpga](#learning_fpga--from-digital-logic-to-a-risc-v-cpu)** — paired VHDL/Verilog, RISC-V CPUs and SoC, peripherals, testbenches and CI diagrams. |
| [HDL tooling](#hdltools--hdl-toolchain--waveform-rendering) | [hdltools / waveview](#hdltools--hdl-toolchain--waveform-rendering) — simulation, synthesis and waveform rendering. |
| [Embedded Linux](#embedded-linux) | **RISC-V & Arm:** [esp32s31-alpine](#alpine-linux-on-esp32-s31) · [alpine-riscv32](#alpine-linux-for-32-bit-risc-v) · [luckfox_rockchip_testing](#luckfox_rockchip_testing) · [openbouffalo_dev_container / BL808](#openbouffalo_dev_container) |
| [Microcontrollers & firmware](#microcontrollers--firmware) | **ESP32 / ESP32-S3 / ESP32-C3:** [signal-generator experiments](https://github.com/naelolaiz/esp32_wifiAP_httpServer_signalGenerator) · [timers & DAC](https://github.com/naelolaiz/test_esp32_timers) · [PoC_PoV](https://github.com/naelolaiz/PoC_PoV) · [DMX512](https://github.com/naelolaiz/osc_to_dmx512) |
| [Board support & build automation](#board-support--build-automation) | [PlatformIO ESP32-S31 support](#esp32-s31-support-for-platformio) · [Sipeed M1s / BL808 SDK](#m1s_bl808_linux_sdk) |
| [Drivers & peripheral interfaces](#drivers--peripheral-interfaces) | **[PyMOPanel](#pymopanel)** · Linux GPIO/PWM · MPU6050 · FPGA UART/I²C · UDA1380 · AD9833 experiments. |
| [3D printing & mechanical design](#3d-printing--mechanical-design) | [3d_models](#3d_models) — OpenSCAD enclosures, motor supports and mirror mounts. |
| [Linux packaging & infrastructure](#linux-packaging--infrastructure) | **[gentoo-binhost](#gentoo-binhost)** — signed binary packages & build automation · [gitea-rootless-podman-kit](#gitea-rootless-podman-kit) |
| [C++ & compiler experiments](#c--compiler-experiments) | **[gcc_updates](#gcc_updates)** — language/library examples, GCC/Clang, sanitizers and CI. |
| [Audio & instrument control](#audio--instrument-control) | [WaveDiff](https://github.com/naelolaiz/vamp_wavediff) · [VoxPad](#voxpad) · [PSG9080 control](https://github.com/naelolaiz/JDY-31_PSG9080) |
| [Games & simulations](#games--simulations) | **[Sprint to Nowhere](#sprint-to-nowhere)** — a satirical sprint-management browser game. |

**Languages:** VHDL, Verilog, C / C++, Python, Shell<br>
**Platforms & tools:** GHDL, Yosys, RISC-V, Linux, ESP32, Qt, Podman / Docker, GitHub Actions

## FPGA & digital design

### [learning_fpga — from digital logic to a RISC-V CPU](https://github.com/naelolaiz/learning_fpga)

A progressive collection of **paired VHDL and Verilog designs**, from clock enables, PWM and FIFOs to UART, I²C, displays and processor architecture.

- **CPU design:** tutorial CPUs implementing an RV32I subset, in single-cycle and five-stage pipelined forms, with forwarding, load-use stalls and branch flushing.
- **Hardware/software integration:** a small SoC with memory-mapped UART, SIMD and FIR accelerators, plus a Python assembler and executable test programs.
- **Verification:** assertion-based testbenches and a shared container build for local development and CI, which publishes netlists and waveforms.

[CPU & SoC walkthrough](https://github.com/naelolaiz/learning_fpga/tree/main/cpu) · [Timing notes](https://github.com/naelolaiz/learning_fpga/blob/main/docs/timing.md) · [Live CI gallery](https://github.com/naelolaiz/learning_fpga/tree/ci-gallery/latest)

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

A containerized VHDL, Verilog and SystemVerilog toolchain combining **GHDL, Yosys with ghdl-yosys-plugin, Icarus Verilog, Verilator and slang**. Includes **netlistsvg** for RTL schematics and the **waveview** renderer, which turns VCD/FST/GHW traces into deterministic SVG/PNG diagrams without a desktop session, with configurable signal groups and time windows. Used by `learning_fpga` for simulation and CI artifacts.

[Container & build targets](https://github.com/naelolaiz/hdltools) · [waveview documentation](https://github.com/naelolaiz/hdltools/tree/main/waveview)

## Embedded systems

### Embedded Linux

Linux bring-up, root filesystems, cross-compilation and peripheral access across **RISC-V and Arm** platforms.

#### [Alpine Linux on ESP32-S31](https://github.com/naelolaiz/esp32s31-alpine)

Bringing Alpine Linux to the **ESP32-S31 Function-CoreBoard-1**, using Espressif's Linux BSP and a custom kernel configuration.

- **Working on hardware:** Linux 6.18 boots an ext4 root filesystem from USB, OpenRC starts a serial login, Ethernet gets an address through DHCP, and `apk` installs signed packages.
- **Behind the boot:** documented BSP versions, kernel configuration fragments, a Buildroot overlay, and a dated journal of the bring-up. Pressing the reset button boots Alpine when the USB stick is present, with a Buildroot fallback when it is absent.

[Source & setup](https://github.com/naelolaiz/esp32s31-alpine) · [Boot journal](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-07-boot-from-stick.md) · [Ethernet & package-install logs](https://github.com/naelolaiz/esp32s31-alpine/blob/main/docs/journal/2026-10-07-network-apk.md)

#### [Alpine Linux for 32-bit RISC-V](https://github.com/naelolaiz/alpine-riscv32)

The distribution work behind the board bring-up: a compact **aports patch series**, cross toolchain and musl-based userspace for `rv32imac` / `ilp32` soft-float, kept independent of board-specific changes.

- **Bootstrap milestone:** cross-built Alpine's bootstrap package set, including `alpine-base`; boots to an OpenRC login in QEMU with working `apk` installs.
- **Beyond cross-compilation:** native riscv32 package builds under qemu-user, including Nano and Dropbear, with SSH logins tested in the VM. GitHub Actions runs the cross and native package builds.

[Patch series](https://github.com/naelolaiz/alpine-riscv32/tree/main/patches) · [Package status](https://github.com/naelolaiz/alpine-riscv32/blob/main/RISCV32.md) · [Build & boot guides](https://github.com/naelolaiz/alpine-riscv32/tree/main/docs/steps)

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

### [gentoo-binhost](https://github.com/naelolaiz/gentoo-binhost)

Signed binary packages for **Gentoo KDE Plasma / OpenRC / `~amd64`**, built through GitHub Actions. Tiered package builds, compiler caching and automatic follow-up runs handle long builds. Packages are published as release assets with an index on the `binhost` branch; clean-container install checks verify package signatures.

[Architecture](https://github.com/naelolaiz/gentoo-binhost/blob/main/docs/ARCHITECTURE.md) · [Build & publication workflow](https://github.com/naelolaiz/gentoo-binhost/blob/main/.github/workflows/build.yml)

### [gitea-rootless-podman-kit](https://github.com/naelolaiz/gitea-rootless-podman-kit)

Scripts for **rootless Gitea deployment, encrypted backups and restoration**, using Podman, age and zstd. Includes scheduled backups, OpenRC/systemd integration and a backup/restore round trip in CI.

[Setup & scripts](https://github.com/naelolaiz/gitea-rootless-podman-kit) · [Restore verification](https://github.com/naelolaiz/gitea-rootless-podman-kit/blob/main/.github/workflows/ci.yml)

## C++ & compiler experiments

### [gcc_updates](https://github.com/naelolaiz/gcc_updates)

An executable **C++11–26 language and standard-library reference**, with compiler-version gates and examples of GCC extensions, changing defaults and diagnostics. CMake/CTest runs a GCC/Clang matrix on **amd64 and arm64**, alongside sanitizer and static-analysis examples. Expected-failure tests check diagnostic output as well as compilation and runtime behavior.

[Feature index](https://github.com/naelolaiz/gcc_updates/blob/main/features/TOPICS.md) · [Reference routes](https://github.com/naelolaiz/gcc_updates/blob/main/docs/reference-paths.md) · [Compiler CI matrix](https://github.com/naelolaiz/gcc_updates/blob/main/.github/workflows/ci.yml)

## Audio & instrument control

| Project | What it does | Stack |
| :--- | :--- | :--- |
| [WaveDiff](https://github.com/naelolaiz/vamp_wavediff) | Audio A/B analysis: RMS, null-test residual and peak difference, through a Vamp plugin for hosts such as Sonic Visualiser, plus a Qt Quick interface. | C++17 · Qt Quick · CMake / CTest |
| [Bluetooth instrument control](https://github.com/naelolaiz/JDY-31_PSG9080) | Python/Qt control of a PSG9080 signal generator, with logic-analyzer captures documenting the protocol. | Python · Qt · Bluetooth |

### [VoxPad](https://github.com/naelolaiz/voxpad)

Audio and WhatsApp voice-message transcription through a **Python CLI, Qt desktop application and browser interface**. Uses Whisper-based speech recognition, with local inference available.

[Documentation](https://github.com/naelolaiz/voxpad/blob/main/README.md) · [Browser application](https://naelolaiz.github.io/voxpad/)

## Games & simulations

### [Sprint to Nowhere](https://github.com/naelolaiz/sprint_to_nowhere)

A satirical **sprint-management browser game** about backlog planning, interruptions, technical debt and burnout. Built with React, Vite and Tailwind CSS, with automated GitHub Pages deployment. The goal is to complete at least ten sprints while keeping technical debt low.

[Play online](https://naelolaiz.github.io/sprint_to_nowhere/) · [Game mechanics](https://github.com/naelolaiz/sprint_to_nowhere/blob/main/src/game/mechanics.js)

[Browse all repositories →](https://github.com/naelolaiz?tab=repositories)
