# **🆘 Troubleshooting**

For port management and common setup issues,

## **🛠️ Freeing Up Ports (Optional Troubleshooting)**

If the default port (e.g., **7860** or **8000**) is already in use, follow the steps below to identify and stop the process occupying the port.

### **🔧 On Windows**

1. Open **Command Prompt** as Administrator.

2. Find which process is using the port (replace 8000 with your port if different):

    ```
    netstat -ano | findstr :8000
    ```

3. Note the **PID** (Process ID) from the output.

4. Identify the application using that PID:

    ```
    tasklist /fi "pid eq <PID>"
    ```

5. To forcefully terminate the process:
    ```
    taskkill /PID <PID> /F
    ```

### **🐧 On macOS / Linux**:


1. Open **Terminal**.

2. Run the following command to find out which process is using port 8000:
    ```
    sudo lsof -i :8000
    ```

3. Look for the **PID** in the output, which is usually in the second column.

4. To stop the process, you can use the kill command:
    ```
    sudo kill -9 <PID>
    ```

**Note**: Replace `8000` with your specific port (e.g., `7860` for Gradio by default).