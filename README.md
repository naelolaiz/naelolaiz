Tinkering with FPGAs, embedded systems, Linux, audio DSP, 3D printing.<br>
Tools, experiments, learning projects. Side projects<sub>(of side projects<sub>(of side projects<sub>(...)</sub>)</sub>)</sub>

---

### 🔬 [learning_fpga](https://github.com/naelolaiz/learning_fpga) — VHDL & Verilog tutorial

> Progressive FPGA examples with CI-generated netlist diagrams and testbench waveforms.

| Netlist (VHDL) | Simulation waveform |
|:-:|:-:|
| ![blink_led netlist](https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/blink_led/blink_led.svg) | ![blink_led waveform](https://raw.githubusercontent.com/naelolaiz/learning_fpga/ci-gallery/latest/blink_led/tb_blink_led.png) |

*Images auto-update on every `main` push via CI → [`ci-gallery`](https://github.com/naelolaiz/learning_fpga/tree/ci-gallery/latest)*

---

### 🤖 [luckfox_rockchip_testing](https://github.com/naelolaiz/luckfox_rockchip_testing) — RISC-V embedded Linux (RV1103/RV1106)

> Cross-compilation, PWM/UART testing, and two servo motors + a laser pointer drawing Lissajous curves.

| Lissajous laser projection |
|:-:|
| ![Lissajous laser](https://raw.githubusercontent.com/naelolaiz/luckfox_rockchip_testing/main/test_programs/pwm_two_servos/doc/lissajous.gif) |

---

### 📦 [3d_models](https://github.com/naelolaiz/3d_models) — OpenSCAD models with CI rendering

> Parametric cases, galvanometer mirror mounts, stackable boxes. STL + PNG auto-generated from `.scad` sources by CI.

| Stepper galvanometer | DSP case |
|:-:|:-:|
| ![galvo](https://naelolaiz.github.io/3d_models/45_degree_angle_mirror_support.png) | ![DSP case](https://raw.githubusercontent.com/naelolaiz/3d_models/main/DSP_ADAU1701_case/pictures/bottom_case_v2.jpg) |

---

### 🔊 [vamp_wavediff](https://github.com/naelolaiz/vamp_wavediff) — Audio A/B null-test tool

> Vamp plugin + Qt Quick UI for comparing two audio files: RMS, peak divergence, null-test per block. C++17 / Sonic Visualiser.

---

### 🛠️ [hdltools](https://github.com/naelolaiz/hdltools) — HDL toolbox container

> Pinned container (GHDL + Yosys + ghdl-yosys-plugin + iverilog + GTKWave + netlistsvg) used by `learning_fpga` CI. Drop-in for reproducible HDL builds.
