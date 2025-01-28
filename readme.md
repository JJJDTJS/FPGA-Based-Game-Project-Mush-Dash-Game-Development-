# **FPGA-Based Game Project**

## **Overview**

This project is a **real-time game implemented on an FPGA (Cyclone V)**, utilizing **C programming and hardware memory-mapped IO** to interact with peripherals such as **VGA display, switches, and LEDs**. The game incorporates **real-time user interaction, graphics rendering, and keyboard input processing**.

The game logic is written in **C** and runs on the FPGA's **ARM processor (HPS - Hard Processor System)**, interacting with the **hardware accelerators** through memory-mapped registers.

------

## **Project Features**

### 🎮 **Game Mechanics**

- **Character movement** controlled via **keyboard input**.
- **Real-time VGA display updates** for smooth animation.
- **Collision detection** for obstacles.
- **Scoring system** displayed on the **VGA screen**.
- **Timer tracking** for gameplay duration.

### 🎨 **Graphics Rendering**

- **Pixel-based rendering on VGA**: Uses **320x240 resolution**.
- Characters and objects are displayed using a **7x7 matrix-based font**.
- Predefined **bitmaps for words and numbers** (`PERFECT`, `GREAT`, `SCORE`, etc.).
- **RGB565 color encoding** for efficient display.

### ⌨️ **User Input**

- **Keyboard input (PS/2 via HPS-FPGA bridge)** for movement.
- **FPGA switches (SW_BASE) and push buttons (KEY_BASE)** for additional controls.

### ⚡ **Performance Considerations**

- **Double-buffering technique** to prevent flickering.
- **Minimal CPU load** by offloading calculations to the hardware.
- Optimized **memory-mapped I/O access** for real-time updates.

------

## **Project Architecture**

### **🔹 FPGA Memory Mapping**

The game interacts with FPGA peripherals using **memory-mapped addresses**:

| **Component**        | **Base Address** |
| -------------------- | ---------------- |
| SDRAM                | `0xC0000000`     |
| FPGA On-Chip Memory  | `0xC8000000`     |
| VGA Character Buffer | `0xC9000000`     |
| LED Registers        | `0xFF200000`     |
| HEX Display          | `0xFF200020`     |
| Switches (SW)        | `0xFF200040`     |
| Push Buttons (KEY)   | `0xFF20005C`     |
| Timer                | `0xFFFEC600`     |
| VGA Pixel Buffer     | `0xFF203020`     |
| VGA Text Buffer      | `0xFF203030`     |
| Keyboard Input       | `0xFF200100`     |

------

## **Implementation Details**

### **🔹 Hardware-Accelerated Graphics**

- The **VGA display** is controlled via **memory-mapped registers**.

- **Characters are stored as bitmaps** in arrays like `PERFECT_matrix`, `SCORE_matrix`, etc.

- The game 

  draws pixels directly to the framebuffer

   using:

  ```c
  void plot_pixel(int x, int y, short int color);
  ```

- **Double-buffering** is used to prevent flickering during rendering.

### **🔹 Input Handling**

- The 

  keyboard input is read from the PS/2 interface

   using:

  ```c
  int *KEYBOARD_input = (int *)KEYBOARD_BASE;
  ```

- **Switch and push-button inputs** control game mechanics.

### **🔹 Collision Detection & Game Logic**

- Uses **2D arrays for object positions**.
- Checks for **overlapping pixels** to detect **collisions**.
- Updates **score and game state** accordingly.

------

## **Code Structure**

### **🔹 Core C Files**

- `project_final_sumit.c` – **Main game loop, rendering, and logic**.
- `vga_display.c` – **Functions for drawing objects on VGA**.
- `keyboard.c` – **Handles keyboard input and movement**.
- `collision.c` – **Implements collision detection logic**.

### **🔹 Key Functions**

#### **1️⃣ VGA Pixel Drawing**

```c
void plot_pixel(int x, int y, short int color) {
    volatile short int *pixel_buffer = (volatile short int *)(PIXEL_BUF_CTRL_BASE);
    pixel_buffer[(y << 9) + x] = color;
}
```

- Writes directly to the **VGA framebuffer**.

#### **2️⃣ Wait for VSYNC (Screen Refresh)**

```c
void wait_for_vsync() {
    volatile int *pixel_ctrl_ptr = (int *)(PIXEL_BUF_CTRL_BASE);
    *pixel_ctrl_ptr = 1; // Request buffer swap
    while ((*pixel_ctrl_ptr) & 1); // Wait for buffer swap
}
```

- Synchronizes drawing to **avoid tearing artifacts**.

#### **3️⃣ Handling Keyboard Input**

```c
void read_keyboard() {
    int key_val = *KEYBOARD_input;
    if (key_val == 0x1D) hero_dx = -1; // Move left
    if (key_val == 0x1C) hero_dx = 1;  // Move right
}
```

- Maps **keyboard scan codes** to movement commands.

------

## ⚖️ Copyright Notice

© 2025 University of Toronto
All rights reserved.  
This project complies with the University of Toronto's academic integrity policies & academic integrity guidelines. Redistribution or reuse without explicit permission is strictly prohibited.

For the university’s academic integrity policy, see https://www.academicintegrity.utoronto.ca/